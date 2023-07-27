### mysql8 镜像

```bash
docker run -d -v /home/mydata/db/data:/var/lib/mysql -v /home/mydata/db/conf:/etc/mysql/conf.d --name mysql8 -e TZ=Asia/Shanghai -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 mysql:latest
```

```bash
docker exec -it mysql bash
mysql -uroot -p
```

```bash
create user 'wiki'@'localhost' identified by '{$ Your Password}';
create user 'wiki'@'%' identified by '{$ Your Password}';

create database `wiki`;

grant all privileges on wiki.* to 'wiki'@'localhost';
grant all privileges on wiki.* to 'wiki'@'%';

flush privileges;

alter user 'wiki'@'%' identified with mysql_native_password by '{$ Your Password}';

```



```bash
docker run -p 3315:3306 --name mysql5.7 -v E:\\mydata\\mysql\\conf:/etc/mysql/conf.d -v E:\\mydata\\mysql\\log:/var/log -v E:\\mydata\\mysql\\data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
```



### wiki2 镜像
```bash
docker run -d -p 8017:3000 --name wiki -e "DB_TYPE=mysql" -e "DB_HOST=192.168.1.34" -e "DB_PORT=3306" -e "DB_USER=wiki" -e "DB_PASS=123456" -e "DB_NAME=wiki" -v /home/mydata/wiki/conf:/conf -v /home/mydata/wiki/data:/wiki/data ghcr.io/requarks/wiki:2

```


### nginx

```bash
docker run -p 9002:80 --name nginx -d -v E:\mydata\nginx\conf\nginx.conf:/etc/nginx/nginx.conf -v E:\mydata\nginx\conf\conf.d:/etc/nginx/conf.d -v E:\mydata\nginx\log:/var/log/nginx -v E:\mydata\nginx\html:/usr/share/nginx/html nginx:latest
```


### docker-registry

```bash
mkdir /home/mydata/registry
mkdir /home/mydata/auth

# apt -y install apache2-utils
yum install -y httpd-tools
htpasswd -Bbn admin admin > /home/mydata/auth/htpasswd


```

```bash
docker run -d -p 5001:5000 --name myRegistry -v /home/mydata/myregistry/data/registry:/var/lib/registry -v /home/mydata/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" --restart=always --privileged=true registry
```

```bash
vim /etc/docker/daemon.json

# "insecure-registries": ["ip:5001"]

systemctl daemon-reload

systemctl restart docker
```

```bash
docker pull hyper/docker-registry-web

docker run -d -p 5002:8080 --name registry-web --restart=always --link myRegistry -e registry_url=http://localhost:5001/v2 -e registry_name=localhost:5001 hyper/docker-registry-web:latest
```


### 使用证书安装 docker-registry

```bash
docker run -d -p 5001:5000 --restart=always --privileged=true --name myRegistry \
		-v /home/mydata/myregistry/conf/registry-srv.yml:/etc/docker/registry/config.yml \
        -v /home/mydata/myregistry/data/registry:/var/lib/registry  \
		-v /home/mydata/myregistry/auth/auth.cert:/etc/docker/registry/auth.cert \
		-e "REGISTRY_AUTH=htpasswd" \
		-e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
		-e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
		registry



docker run -d -p 5001:5000 --restart=always --privileged=true --name myRegistry -v /home/mydata/myregistry/conf/registry-srv.yml:/etc/docker/registry/config.yml -v /home/mydata/myregistry/data/registry:/var/lib/registry  -v /home/mydata/myregistry/auth/auth.cert:/etc/docker/registry/auth.cert -v /home/mydata/myregistry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" registry

```


```bash
docker run -it -d -v /home/mydata/myregistry/conf/registry-web.yml:/conf/config.yml -v /home/mydata/myregistry/auth/auth.key:/conf/auth.key -v /home/mydata/myregistry/db:/data -p 5002:8080 --name registry-web 127.0.0.1:5001/register-web
```

```bash

docker run -d -p 443:443 --restart=always --privileged=true --name myRegistry -v /home/mydata/myregistry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/tianji.top.crt -e REGISTRY_HTTP_TLS_KEY=/certs/tianji.top.key -v /home/mydata/myregistry/registry:/var/lib/registry -v /home/mydata/myregistry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd registry

```

```bash

# HTTP基本认证之 Basic Auth
# 说明：base64encode(admin:123456)=YWRtaW46MTIzNDU2

docker run -d -p 5002:8080 --name registry-web \
	-e REGISTRY_URL=http://118.192.66.57:5001/v2 \
    -e REGISTRY_TRUST_ANY_SSL=true \
	-e REGISTRY_READONLY=false \
    -e REGISTRY_BASIC_AUTH="YWRtaW46YWRtaW4xMjM=" \
    -e REGISTRY_NAME=118.192.66.57:5001 hyper/docker-registry-web


docker run -d -p 5002:8080 --name registry-web -e REGISTRY_URL=http://118.192.66.57:5001/v2  -e REGISTRY_TRUST_ANY_SSL=true  -e REGISTRY_READONLY=false -e REGISTRY_BASIC_AUTH="YWRtaW46YWRtaW4xMjM="  -e REGISTRY_NAME=118.192.66.57:5001 hyper/docker-registry-web

```


#### nacos

```bash
docker  run --name nacos -p 8848:8848 -p 9848:9848 -p 9849:9849 --privileged=true --restart=always -e JVM_XMS=128m -e JVM_XMX=128m -e MODE=standalone -e PREFER_HOST_MODE=hostname -v /home/mydata/nacos/logs/:/home/nacos/logs -d -e SPRING_DATASOURCE_PLATFORM=derby nacos/nacos-server
```

#### 镜像构建

参考 https://css.dandelioncloud.cn/article/details/1567522126343401473

```
FROM adoptopenjdk/openjdk8-openj9:alpine-slim
MAINTAINER tianji
ADD ./target/mall-system-1.0-SNAPSHOT.jar mall-system-1.0-SNAPSHOT.jar
VOLUME /tmp
ENV JAVA_OPTS="-server -Xms512m -Xmx512m"
ENV PROFILES_ACTIVE="prod"
RUN echo "Asia/shanghai" > /etc/timezone
EXPOSE 30004
ENTRYPOINT java $JAVA_OPTS -Xshareclasses -Xquickstart -Djava.security.egd=file:/dev/./urandom -jar /mall-system-1.0-SNAPSHOT.jar \
    --spring.profiles.active=$PROFILES_ACTIVE
```

```
version: '3'
services:
  mall-system:
    image: 192.168.1.42:5000/mall-system
    build:
      context: ./mall-system
      dockerfile: Dockerfile
```

```bash
# 执行命令
docker-compose up -d --build mall-system
```

#### 拉取镜像并执行

```
# 服务器批量部署
# 默认拉取 latest
# 等做了部署工具后，这个文件就不能在使用
# ssh 登录服务器，执行 docker-compose -f docker-compose-test.yml up -d
# 启动单个service 执行 docker-compose -f docker-compose-test.yml up mall-product -d

version: '3'
services:

  nginx:
    image: nginx
    restart: always
    privileged: true
    container_name: nginx
    ports:
      - 8080:80
      - 8443:443

    volumes:

      # 先创建一个容器，将其中的重要文件目录复制出来，再挂在数据卷
      # docker run --name nginx -p 9001:80 -d nginx
      # docker cp nginx:/etc/nginx/nginx.conf /home/nginx/conf/nginx.conf
      # docker cp nginx:/etc/nginx/conf.d /home/nginx/conf/conf.d
      # docker cp nginx:/usr/share/nginx/html /home/nginx/

      - E:\mydata\nginx\html:/usr/share/nginx/html
      - E:\mydata\nginx\www:/var/www
      - E:\mydata\nginx\logs:/var/log/nginx
      - E:\mydata\nginx\nginx.conf/:/etc/nginx/nginx.conf
      - E:\mydata\nginx\cert:/etc/nginx/cert
      - E:\mydata\nginx\conf.d:/etc/nginx/conf.d

    environment:
      - NGINX_PORT=80
      - TZ=Asia/Shanghai

  nacos:
    restart: always
    image: nacos/nacos-server
    container_name: nacos
    deploy:
      mode: relicates
      resources:
        limits:
          cpus: "0.50"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
    ports:
      - 8848:8848
      - 9848:9848
      - 9849:9849

    privileged: true
    environment:
      NACIS_AUTH_ENABLE: "true"
      NACOS_AUTH_TOKEN_EXPIRE_SECONDS: 18000
      JVM_XMS: 128m
      JVM_XMX: 128m
      JVM_MS: 64m
      JVM_MMS: 64m
      MODE: standalone
      NACOS_REPLICAS: 1
      PREFER_HOST_MODE: hostname
    volumes:
      - E:\mydata\nacos\logs:/home/nacos/logs
      - nacos-conf:/home/nacos/conf

  mall-product:
    image: 192.168.1.42:5000/mall-product:0.0.2
    ports:
      - 30003:30003
      - 20882:20882
    container_name: mall-product
    restart: always
    volumes:
      - E:\mydata\logs\mall-product:/log
    environment:
      PROFILES_ACTIVE: test
      DUBBO_IP_TO_REGISTRY: 192.168.1.42
      DUBBO_PORT_TO_BIND: 20882


volumes:
  nacos-conf:
    driver: local
    driver_opts:
      type: 'none'
      device: 'E:\mydata\nacos\conf'
      o: 'bind'
```

```bash
docker-compose up -d mall-product
```