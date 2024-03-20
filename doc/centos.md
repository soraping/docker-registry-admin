### 安装系统软件

```bash
yum update -y
yum install git -y
yum install openssh-server -y
sudo yum install net-tools -y
sudo yum install -y yum-utils

# python3 环境支持
yum install python3
yum install python3-pip

# 注：安装失败，利用yum clean和yum list清理缓存

# 开始 ssh
# https://xiaoxiaomayi.com/vps/p/3371.html
# https://www.php.cn/faq/488397.html
```

### 安装 `ftp`
https://www.lmhack.com/article/26169.html
https://blog.csdn.net/xufei512/article/details/52037497
https://zhuanlan.zhihu.com/p/567456994
https://blog.51cto.com/heteacher/6239453

- 匿名开放模式：是一种最不安全的认证模式，任何人都可以无需密码验证而直接登录
- 本地用户模式：是通过Linux系统本地的账户密码信息进行认证的模式，相较于匿名开放模式更安全，而且配置起来也很简单
- 虚拟用户模式：是这三种模式中最安全的一种认证模式，它需要为FTP服务单独建立用户数据库文件，虚拟出用来进行口令验证的账户信息，而这些账户信息在服务器系统中实际上是不存在的，仅供FTP服务程序进行认证使用。这样，即使黑客**了账户信息也无法登录服务器，从而有效降低了破坏范围和影响。

```bash
yum install vsftpd -y

# 启动
systemctl start vsftpd.service

# 停止
systemctl enable vsftpd.service

# 配置账号及权限
# 新建ftp组
groupadd ftp
# 新建 ftpuser 用户，所属 ftp 组
# -d 指定用户根目录
# -s 指定shell脚本为/sbin/nologin，表示不允许shell登录
useradd -g ftp -d /home/ftpuser -s /sbin/nologin -m ftpuser


# 先备份原来的vsftpd配置文件，然后去掉里面的注释行，剩下的就是默认配置
cd /etc/vsftpd/
cp vsftpd.conf vsftpd.conf.bak
grep -v "#" vsftpd.conf.bak > vsftpd.conf
```

### 设置 `sftp`

```bash
# 创建一个主目录，并限制用户只能在该目录中工作
mkdir -p /home/sftp/
chown root:root -R /home/sftp/
chmod -R 755 /home/sftp/

# 创建一个组
mkdir -p /home/sftp/sftpuser1
groupadd sftp
# 创建一个用户，归属于 sftp 组
useradd -d /home/sftp/sftpuser1 -m -g sftp -s /sbin/nologin sftpuser1
# 设置密码
passwd 12345678
# 设置该用户权限
chown sftpuser1:sftp -R /home/sftp/sftpuser1
chmod -R 755 /home/sftp/sftpuser1

```

```bash
# 配置文件修改
vi /etc/ssh/sshd_config
```

```
# 注释掉下面的这行内容，因为配置的 for-sftp 用户没有登录 shell 的权限
## 不注释的话，登录的时候会返回报错：Received message too long 1416128883
# Subsystem sftp /usr/libexec/openssh/sftp-server
# 修改成下面的方式来打开 sftp 服务
Subsystem sftp internal-sftp
# Match User 后面的配置内容，只对 Match User 指定的用户生效，多个用户以逗号分隔
## 也可以配置成 Match Group，对指定的组生效，同样，多个组以逗号分隔
# Match Group sftp
Match User sftpuser1
# 指定 sftp 登录的默认路径
## 目录必须存在，否则 sftp 连接会报错
ChrootDirectory /home/sftp
# 指定 sftp 命令
ForceCommand internal-sftp

# 这将限制SFTP用户访问其主目录，并禁用任何TCP或X11转发
AllowTcpForwarding no
X11Forwarding no
```

```bash
# 重启 sftp 服务
sudo systemctl restart sshd
```

### 安装 `docker`

```bash
yum install -y yum-utils device-mapper-persistent-data lvm2

# 镜像地址换成aliyun的
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install docker-ce

systemctl start docker

# 修改docker存储位置
mkdir -p /home/docker-data/docker

# 不仅要设置镜像加速
# 还要配置镜像存储位置
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": ["https://01sy6s7g.mirror.aliyuncs.com"],
  "data-root": "/home/docker-data/docker"
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

# 开机自动启动
systemctl enable docker.service
systemctl disable docker.service

# 关闭docker重启服务
systemctl stop docker.sock

# docker-compose 安装
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 给权限
sudo chmod +x /usr/local/bin/docker-compose
```

### 安装 `jdk`

```bash
mkdir -p /opt/java
tar -zxvf jdk-8u171-linux-x64.tar.gz -C /opt/java/

vi /etc/profile

# java env
export JAVA_HOME=/opt/java/jdk1.8.0_171
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib/rt.jar
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

source /etc/profile
```

### 安装 `miniconda`

```bash
# 下载和安装miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 下载完成后在终端中安装
sh Miniconda3-latest-Linux-x86_64.sh

# 使以上的安装立即生效
source ~/.bashrc
```