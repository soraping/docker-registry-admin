### 安装系统软件

```bash
yum update -y

sudo yum install -y yum-utils


```

### 安装 `ftp`

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
yum -y install docker

systemctl start docker

sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://01sy6s7g.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

# 开机自动启动
systemctl enable docker.service

# docker-compose 安装
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 给权限
sudo chmod +x /usr/local/bin/docker-compose
```

### 安装 `jdk`

### 安装 `miniconda`

```bash
# 下载和安装miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 下载完成后在终端中安装
sh Miniconda3-latest-Linux-x86_64.sh

# 使以上的安装立即生效
source ~/.bashrc
```