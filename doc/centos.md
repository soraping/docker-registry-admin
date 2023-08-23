### 安装系统软件

```bash
yum update -y
sudo yum install -y yum-utils
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

# 先备份原来的vsftpd配置文件，然后去掉里面的注释行，剩下的就是默认配置
cd /etc/vsftpd/
cp vsftpd.conf vsftpd.conf.bak
grep -v "#" vsftpd.conf.bak > vsftpd.conf
```

### 安装 `docker`

```bash
yum install -y yum-utils device-mapper-persistent-data lvm2

yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

yum install docker-ce

systemctl start docker

sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": ["https://01sy6s7g.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

# 开机自动启动
systemctl enable docker.service
systemctl disable docker.service

# 关闭docker重启服务
systemctl stop docker.socke

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