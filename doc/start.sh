#!/bin/bash

BASE_DIR=/home
BASE_DATA_PATH=$BASE_DIR/docker-data

# nginx
mkdir -p $BASE_DATA_PATH/nginx
mkdir -p $BASE_DATA_PATH/nginx/logs
mkdir -p $BASE_DATA_PATH/nginx/cert
mkdir -p $BASE_DATA_PATH/nginx/www
docker run --name nginx -p 9001:80 -d nginx > /dev/null
docker cp nginx:/etc/nginx/nginx.conf $BASE_DATA_PATH/nginx/nginx.conf > /dev/null
docker cp nginx:/etc/nginx/conf.d $BASE_DATA_PATH/nginx/conf.d > /dev/null
docker cp nginx:/usr/share/nginx/html $BASE_DATA_PATH/nginx/html > /dev/null
docker stop nginx > /dev/null
docker rm nginx > /dev/null
echo "nginx 数据卷创建完成"

# mysql
mkdir -p $BASE_DATA_PATH/mysql
docker run -d --name mysql -p 3306:3306 mysql:latest > /dev/null
docker cp mysql:/etc/mysql/my.cnf $BASE_DATA_PATH/mysql > /dev/null
docker cp mysql:/etc/mysql/conf.d $BASE_DATA_PATH/mysql/conf > /dev/null
docker stop mysql > /dev/null
docker rm mysql > /dev/null

# nacos
mkdir -p $BASE_DATA_PATH/nacos/logs
mkdir -p $BASE_DATA_PATH/nacos/conf
mkdir -p $BASE_DATA_PATH/nacos/data
echo "nacos 数据卷创建完成"

# registry
mkdir -p $BASE_DATA_PATH/registry/data
auth_dir=$BASE_DATA_PATH/registry/auth
mkdir -p $auth_dir
# create htpasswd
htpasswd -Bbn admin admin123 > $auth_dir/htpasswd
touch $BASE_DATA_PATH/config.yml
echo "registry auth 密码输出完成"



echo "项目数据卷创建完毕!"