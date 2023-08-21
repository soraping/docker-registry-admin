### 配置说明

https://blog.csdn.net/wangmx1993328/article/details/80941870

### 异常

- Nginx 启动报 [emerg] bind()to 0.0.0.0:8090 failed (13: Permission denied)

```bash
# 查看 http 允许访问的端口
semanage port -l | grep http_port_t

# 将要启动的端口加入到如上端口列表中
semanage port -a -t http_port_t -p tcp 8090

# 如说是用docker配置的nginx，一定要重启docker
systemctl restart docker
```