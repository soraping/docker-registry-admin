#!/bin/bash

BASE_DIR=/home

# nginx
mkdir -p $BASE_DIR/mydata/nginx/conf/conf.d
mkdir -p $BASE_DIR/mydata/nginx/logs
mkdir -p $BASE_DIR/mydata/nginx/cert
mkdir -p $BASE_DIR/mydata/nginx/www
docker run --name nginx -p 9001:80 -d nginx > /dev/null
docker cp nginx:/etc/nginx/nginx.conf $BASE_DIR/mydata/nginx/conf/nginx.conf > /dev/null
docker cp nginx:/etc/nginx/conf.d $BASE_DIR/mydata/nginx/conf/conf.d > /dev/null
docker cp nginx:/usr/share/nginx/html $BASE_DIR/mydata/nginx/ > /dev/null
docker stop nginx > /dev/null
docker rm nginx > /dev/null
echo "nginx 数据卷创建完成"

# nacos
mkdir -p $BASE_DIR/mydata/nacos/logs
mkdir -p $BASE_DIR/mydata/nacos/conf
mkdir -p $BASE_DIR/mydata/nacos/data
echo "nacos 数据卷创建完成"

# registry
mkdir -p $BASE_DIR/mydata/registry/data
touch $BASE_DIR/mydata/registry/config.yml
auth_dir=$BASE_DIR/mydata/registry/auth
mkdir -p $auth_dir
# create htpasswd
htpasswd -Bbn admin admin123 > $auth_dir/htpasswd
echo "registry auth 密码输出完成"

# 项目
arrayProjects=("user-info" "mall-system" "mall-product" "mall-order" "mall-payment" "mall-sale-support" "ride-web")
for project in ${arrayProjects[@]};
do
  mkdir -p $BASE_DIR/mydata/$project/logs
done

echo "项目数据卷创建完毕!"