### docker-compose 部署 graylog

```yaml
version: '3'
services:
  mongo:
    image: mongo:4.2
    container_name: mongo
    volumes:
      - mongo_data:/data/db
    restart: always
    ports:
      - 27017:27017
    networks:
      - graylog

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch-oss:7.10.2
    container_name: es
    volumes:
      - es_data:/usr/share/elasticsearch/data
    restart: always
    ports:
      - 9200:9200
      - 9300:9300
    environment:
      - http.host=0.0.0.0
      - transport.host=localhost
      - network.host=0.0.0.0
      - "ES_JAVA_OPTS=-Dlog4j2.formatMsgNoLookups=true -Xms512m -Xmx512m"

    ulimits:
      memlock:
        soft: -1
        hard: -1
    deploy:
      resources:
        limits:
          memory: 1g
    networks:
      - graylog

  graylog:
    image: graylog/graylog:4.2
    container_name: graylog
    volumes:
      - graylog_journal:/usr/share/graylog/data/journal
    environment:
      # 时间
      - GRAYLOG_ROOT_TIMEZONE=Asia/Shanghai
      # 16字符,任意
      - GRAYLOG_PASSWORD_SECRET=tianjigaodaoyuan
      # echo -n "Enter Password: " && head -1 </dev/stdin | tr -d '\n' | sha256sum | cut -d" " -f1
      - GRAYLOG_ROOT_PASSWORD_SHA2=157f69a391ae15eac0d462b50ad789fd61064fcd1b15818ee4e3a02b68d92dab
      # graylog 请求地址
      - GRAYLOG_HTTP_EXTERNAL_URI=http://192.168.1.13:9009/
    entrypoint: /usr/bin/tini -- wait-for-it elasticsearch:9200 --  /docker-entrypoint.sh
    networks:
      - graylog
    restart: always
    depends_on:
      - mongo
      - elasticsearch
    ports:
      # Graylog web interface and REST API
      - 9009:9000
      # Syslog TCP
      - 1514:1514
      # Syslog UDP
      - 1514:1514/udp
      # GELF TCP
      - 12201:12201
      # GELF UDP
      - 12201:12201/udp

networks:
  graylog:
    driver: bridge

volumes:
  
  # 数据卷可以不用 driver_opts ，使用默认地址。
  # 使用挂载路径方便管理，也节省系统盘空间
  mongo_data:
    driver: local
    driver_opts:
      type: 'none'
      device: '/home/mydata/mongo/data'
      o: 'bind'
  es_data:
    driver: local
    driver_opts:
      type: 'none'
      device: '/home/mydata/es/data'
      o: 'bind'
  graylog_journal:
    driver: local
    driver_opts:
      type: 'none'
      device: '/home/mydata/graylog/data'
      o: 'bind'
```

注意点：
graylog 默认账号密码是 `admin/admin`，但是为了安全，使用自定义密码，密码生成命令:
```bash
echo -n "Enter Password: " && head -1 </dev/stdin | tr -d '\n' | sha256sum | cut -d" " -f1
```
复制其中的值，就是环境变量 `GRAYLOG_ROOT_PASSWORD_SHA2` 的值

### graylog 配置

[graylog相关概念](https://blog.csdn.net/WEDUEST/article/details/127811578)

[graylog操作](https://blog.csdn.net/liuyij3430448/article/details/127609313)

### springboot 集成

pom.xml文件中加入

```xml
<dependency>
  <groupId>de.siegmar</groupId>
  <artifactId>logback-gelf</artifactId>
  <version>3.0.0</version>
</dependency>
```

新增配置文件
这里注意端口号，就是 graylog 配置的 input 端口号

```yaml
# graylog 配置
graylog:
    # graylog 地址
  graylogHost: 192.168.1.13
  # graylog upd 端口
  graylogPort: 12201
  # 当前工程项目名
  app_name: user-info
  # 环境变量 pro/test
  app_env: pro
```


修改日志配置 `logback-spring.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>

<configuration debug="false" scan="true" scanPeriod="120 seconds">

    <!--获取配置文件中graylog配置-->
    <springProperty scope="context" name="graylog.graylogHost"
                    source="graylog.graylogHost"/>
    <springProperty scope="context" name="graylog.graylogPort"
                    source="graylog.graylogPort"/>
    <springProperty scope="context" name="graylog.app_name"
                    source="graylog.app_name"/>
    <springProperty scope="context" name="graylog.app_env"
                    source="graylog.app_env"/>


    <!--配置日志输出到统一日志搜集平台Graylog-->
    <appender name="GELF" class="de.siegmar.logbackgelf.GelfUdpAppender">
        <!-- Graylog服务的地址 -->
        <graylogHost>${graylog.graylogHost}</graylogHost>
        <!-- UDP Input端口 -->
        <graylogPort>${graylog.graylogPort}</graylogPort>
        <!-- 最大GELF数据块大小（单位：字节），508为建议最小值，最大值为65467 -->
        <maxChunkSize>508</maxChunkSize>
        <!-- 是否使用压缩 -->
        <useCompression>true</useCompression>
        <encoder class="de.siegmar.logbackgelf.GelfEncoder">
            <!--原始主机名（对应graylog中source字段），如果未指定，将自动检测-->
            <!--<originHost>logback-graylog</originHost>-->
            <!-- 是否发送原生的日志信息 -->
            <includeRawMessage>false</includeRawMessage>
            <includeMarker>true</includeMarker>
            <includeMdcData>true</includeMdcData>
            <includeCallerData>false</includeCallerData>
            <includeRootCauseData>false</includeRootCauseData>
            <!-- 是否发送日志级别的名称，否则默认以数字代表日志级别 -->
            <includeLevelName>true</includeLevelName>
            <!--这个控制message字段，默认值为%m%nopex，表示只输出message，不输出任何堆栈跟踪（nopex）-->
            <shortPatternLayout class="ch.qos.logback.classic.PatternLayout">
                <!--标准日志格式-->
                <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%X{trace_id}] [%thread] %-5p [%file:%line] - %m%n</pattern>
            </shortPatternLayout>
            <!--这个控制full message字段，内容基本上和message一样，所以这里直接配置行分隔符，就会忽略该字段，默认为%m%n-->
            <fullPatternLayout class="ch.qos.logback.classic.PatternLayout">
                <pattern>%n</pattern>
            </fullPatternLayout>

            <!-- 配置应用名称（服务名称），通过staticField标签可以自定义一些固定的日志字段，用于进行日志分类 -->
            <staticField>app_name:${graylog.app_name}</staticField>
            <staticField>app_env:${graylog.app_env}</staticField>
            <!--请求链路-->
            <staticField>trace_id:%X{trace_id}</staticField>
            <staticField>request_ip:%X{request_ip}</staticField>
            <staticField>request_url:%X{request_url}</staticField>
            <staticField>user_agent:%X{user_agent}</staticField>
            <staticField>request_token:%X{request_token}</staticField>
        </encoder>
    </appender>

    <!-- 彩色日志依赖的渲染类 -->
    <conversionRule conversionWord="clr" converterClass="org.springframework.boot.logging.logback.ColorConverter" />
    <conversionRule conversionWord="wex" converterClass="org.springframework.boot.logging.logback.WhitespaceThrowableProxyConverter" />
    <conversionRule conversionWord="wEx" converterClass="org.springframework.boot.logging.logback.ExtendedWhitespaceThrowableProxyConverter" />
    <!-- 彩色日志格式 -->
    <property name="CONSOLE_LOG_PATTERN" value="${CONSOLE_LOG_PATTERN:-%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}) %clr(${LOG_LEVEL_PATTERN:-%5p}) %clr(${PID:- }){magenta} %clr(---){faint} %clr([%15.15t]){faint} %clr(%-40.40logger{39}){cyan} %clr(:){faint} %m%n${LOG_EXCEPTION_CONVERSION_WORD:-%wEx}}"/>
    <!--1. 输出到控制台-->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <!--此日志appender是为开发使用，只配置最底级别，控制台输出的日志级别是大于或等于此级别的日志信息-->
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>debug</level>
        </filter>
        <encoder>
            <Pattern>${CONSOLE_LOG_PATTERN}</Pattern>
            <!-- 设置字符集 -->
            <charset>UTF-8</charset>
        </encoder>
    </appender>


    <!-- 日志文件路径 -->
    <property name="logPath" value="./logs/"></property>
    <!-- 日志文件名称 -->
    <property name="logName" value="ride-web"></property>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!-- 正在记录的日志文档的路径及文档名 -->
        <file>${logPath}${logName}.log</file>
        <!--日志文档输出格式-->
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%X{trace_id}] %-5level -&#45;&#45; [%thread] %logger Line:%-3L - %msg%n</pattern>
            <charset>UTF-8</charset>
        </encoder>
        <!-- 日志记录器的滚动策略，按日期，按大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- 日志归档 -->
            <fileNamePattern>${logPath}${logName}-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <!--日志文档保留天数-->
            <maxHistory>15</maxHistory>
        </rollingPolicy>
    </appender>

    <springProfile name="dev">
        <root level="debug">
            <appender-ref ref="CONSOLE" />
        </root>
    </springProfile>

    <springProfile name="test">
        <root level="info">
            <appender-ref ref="CONSOLE" />
            <appender-ref ref="FILE" />
        </root>
    </springProfile>

    <springProfile name="prod">
        <root level="info">
            <appender-ref ref="GELF"/>
            <appender-ref ref="FILE" />
        </root>
    </springProfile>
    <!-- 屏蔽日志 -->
    <logger name="org.springframework.jms.listener.DefaultMessageListenerContainer" level="OFF" />

</configuration>
```

### 全链路日志总结

#### nginx 配置

nginx 作为反向代理时，可以获取到客户端真实ip，user-agent等字段
最重要的是，nginx生成的 `$request_id` 是全局唯一的，可以作为 `trace_id` 实现全链路

在 `nginx.conf` 文件中新增配置
```
http {
    # 修改日志配置
    log_format  main  '$remote_addr:$remote_port $proxy_protocol_addr:$proxy_protocol_port- $remote_user [$time_local] "$request" '
                      'trace_id:"$trace_id"'
		              '$status $body_bytes_sent "$http_referer" '
		              'request_id:$request_id  x_req_id:"$http_x_request_id"'
                      '"$http_user_agent" "$http_x_forwarded_for"';

    # 支持下划线横杠
    underscores_in_headers on;
}
```

在 server 配置中新增字段

```
server{
    set $trace_id "${request_id}";
    if ($http_x_request_id != "" ){
            set $trace_id "${http_x_request_id}";
    }

    # header字段中新增这两个字段
    # $request_id 是唯一的，通过header传递出去
    proxy_set_header x-request-id $request_id;
    proxy_set_header x-real-ip $remote_addr;

}
```

#### springboot 接口拦截器

在拦截器中获取 nginx 在 header 中添加的关键字段

```java
    private void saveRequestLogBean(HttpServletRequest request, String token){
        String traceId = request.getHeader(Constant.X_REQUEST_ID);
        // 放入线程变量内
        LogUtils.setRequestLog(RequestLogBean
                .builder()
                .traceId(traceId)
                .userAgent(request.getHeader(Constant.USER_AGENT))
                .authorization(token)
                .requestIp(request.getHeader(Constant.REQUEST_IP))
                .URI(request.getRequestURI())
                .build());
        log.info("new request，traceId => {}", traceId);
    }
```

`RequestLogBean` 存入 ThreadLocal 中，是线程安全的

```java

@Data
@Builder
public class RequestLogBean {
    private String traceId;
    private String requestIp;
    private String URI;
    private String userAgent;
    private String upstream;
    private String authorization;
}

public class LogUtils {

    // 此处字段对应 logback-spring.xml 中 GELF 配置的字段
    private static final String TRACE_ID = "trace_id";
    private static final String USER_AGENT = "user_agent";
    private static final String REQUEST_IP = "request_ip";
    private static final String URL = "request_url";

    private static final String TOKEN = "request_token";

    private static ThreadLocal<RequestLogBean> traceIdThreadLocal = new ThreadLocal<RequestLogBean>();

    public static RequestLogBean getRequestLogInfo(){
        return traceIdThreadLocal.get();
    }

    public static void setRequestLog(RequestLogBean requestLog){
        traceIdThreadLocal.set(requestLog);
    }

    public static void remove(){
        traceIdThreadLocal.remove();
    }
}
```

这样从 nginx 获取的唯一 request_id 就存在内存中了，使用时可以通过方法获取

#### 结合 MDC和logback 配置日志参数

`RequestLogBean` 中的字段都是关键字段，结合MDC可以很方便的输出到日志中

```java
    /**
    修改设置方法
    **/
    public static void setRequestLog(RequestLogBean requestLog){
        traceIdThreadLocal.set(requestLog);
        MDC.put(TRACE_ID, requestLog.getTraceId());
        MDC.put(REQUEST_IP, requestLog.getRequestIp());
        MDC.put(USER_AGENT, requestLog.getUserAgent());
        MDC.put(URL, requestLog.getURI());
        MDC.put(TOKEN, requestLog.getAuthorization());
    }
```

将值设置到MDC中去之后，要在logback文件中配置

**输出MDC参数的写法为：%X{mobile}，其中的字符串为设置的MDC属性名**

在 GELF 日志中可以配置 staticField 字段，方便查询
关键字段如: traceId,userId,userAgent等，都是用来匹配筛选日志的

```xml
    <appender name="GELF" class="de.siegmar.logbackgelf.GelfUdpAppender">
        <!-- Graylog服务的地址 -->
        <graylogHost>${graylog.graylogHost}</graylogHost>
        <!-- UDP Input端口 -->
        <graylogPort>${graylog.graylogPort}</graylogPort>
        <!-- 最大GELF数据块大小（单位：字节），508为建议最小值，最大值为65467 -->
        <maxChunkSize>508</maxChunkSize>
        <!-- 是否使用压缩 -->
        <useCompression>true</useCompression>
        <encoder class="de.siegmar.logbackgelf.GelfEncoder">
            <!--原始主机名（对应graylog中source字段），如果未指定，将自动检测-->
            <!--<originHost>logback-graylog</originHost>-->
            <!-- 是否发送原生的日志信息 -->
            <includeRawMessage>false</includeRawMessage>
            <includeMarker>true</includeMarker>
            <includeMdcData>true</includeMdcData>
            <includeCallerData>false</includeCallerData>
            <includeRootCauseData>false</includeRootCauseData>
            <!-- 是否发送日志级别的名称，否则默认以数字代表日志级别 -->
            <includeLevelName>true</includeLevelName>
            <!--这个控制message字段，默认值为%m%nopex，表示只输出message，不输出任何堆栈跟踪（nopex）-->
            <shortPatternLayout class="ch.qos.logback.classic.PatternLayout">
                <!--标准日志格式-->
                <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%X{trace_id}] [%thread] %-5p [%file:%line] - %m%n</pattern>
            </shortPatternLayout>
            <!--这个控制full message字段，内容基本上和message一样，所以这里直接配置行分隔符，就会忽略该字段，默认为%m%n-->
            <fullPatternLayout class="ch.qos.logback.classic.PatternLayout">
                <pattern>%n</pattern>
            </fullPatternLayout>

            <!-- 配置应用名称（服务名称），通过staticField标签可以自定义一些固定的日志字段，用于进行日志分类 -->
            <staticField>app_name:${graylog.app_name}</staticField>
            <!--请求链路-->
            <staticField>trace_id:%X{trace_id}</staticField>
            <staticField>request_ip:%X{request_ip}</staticField>
            <staticField>request_url:%X{request_url}</staticField>
            <staticField>user_agent:%X{user_agent}</staticField>
            <staticField>request_token:%X{request_token}</staticField>
        </encoder>
    </appender>
```

#### dubbo Filter

dubbo 接口的调用日志使用 dubbo Filter对象来处理

[dubbo Filter 参考](https://blog.51cto.com/Saintmm/5544141)

dubbo接口调用时，需要传递 traceId 才能实现真正的全链路，如果通过参数传，那太麻烦了，所以使用dubbo RpcContext 的隐式传输

[dubbo源码-隐式传参](https://blog.csdn.net/CPLASF_/article/details/123016476)

这样就能顺利将 traceId 传到 provider 内，实现了真正的全链路

```java
@Slf4j
@Activate(group = {CommonConstants.PROVIDER, CommonConstants.CONSUMER})
public class GdyMallProviderDubboFilter implements Filter {

    public final static String TRACE_ID = "TRACE_ID";
    public final static String REQUEST_ID = "trace_id";

    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {

        String interfaceName = invoker.getInterface().getName();
        String methodName = invocation.getMethodName();
        String REQ_SERVICE = interfaceName + "." + methodName;
        String SOURCE_IP = RpcContext.getContext().getRemoteAddressString();
        long startTime = System.currentTimeMillis();
        String ARGUMENTS = JSON.toJSONString(invocation.getArguments());
        Result result = null;

        String traceID = "";

        if (RpcContext.getContext().isConsumerSide()) {
            // 消费者
            traceID = LogUtils.getRequestLogInfo().getTraceId();
            RpcContext.getContext().setAttachment(TRACE_ID, traceID);
        }else{
            // 生产者
            traceID = RpcContext.getContext().getAttachment(TRACE_ID);
            // provider 在拿到traceId后，一定要调用 MDC存储，否则后面的日志不会打印出 traceId
            MDC.put(REQUEST_ID, traceID);
        }

        try {
            result = invoker.invoke(invocation);
            if (result.hasException()) {
                log.error("Provider.dubbo 服务发生异常：traceID:[{}] called by [{}] service [{}] method [{}] arguments [{}] fail",
                        traceID, SOURCE_IP, interfaceName, methodName, ARGUMENTS);
                log.error("Provider.TraceFilter occurs exception", result.getException());
            }
        } catch (Exception e) {
            log.error("Provider.dubbo异常：traceID:[{}] called by [{}] service [{}] method [{}] arguments [{}] exception [{}] ",
                    traceID, SOURCE_IP, invoker.getInterface().getName(), ARGUMENTS, invocation.getMethodName(),
                    e.getClass().getName() + e.getMessage());
        } finally {
            log.info("Provider.dubbo返回：traceID:[{}]  消费方 [{}]  接口 [{}]  请求值 [{}]  返回值 [{}]  耗时 {} 毫秒",
                    traceID, SOURCE_IP, REQ_SERVICE, ARGUMENTS, JSON.toJSONString(new Object[]{result.getValue()}), System.currentTimeMillis() - startTime);
        }
        return result;
    }
}
```
