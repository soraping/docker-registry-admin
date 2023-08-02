### docker-compose 部署 graylog


### graylog 配置


### springboot 集成


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
                .userAgent(Constant.USER_AGENT)
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




