### 配置ssh免密
`ansible` 使用普通用户管理被控端，也可以直接用root用户控制被控主机

- **控制端，被控制端都需要创建ansible用户**

```bash
# 新增用户
useradd ansible

# 设置密码
echo '123456' | passwd --stdin ansible
```

- **所有受控主机的 ansible 用户都必须添加 sudo 权限**

```bash
vim /etc/sudoers

# 免密，而且有 sudo 权限
ansible ALL=(ALL)       NOPASSWD: ALL
```


- 配置受控主机

```bash
vim /etc/ansible/inventory

[web]
192.168.1.1
192.168.2.2
```

- 主控端生成公私密钥，并将公钥发送给受控机

```bash
# 切换用户
su ansible

# 生成密钥文件 /home/ansible/.ssh 文件夹内
ssh-keygen -t rsa

# 切换到 root
su root

# 查看密钥文件
ll /home/ansible/.ssh

# 将公钥发到受控机
ssh-cpoy-id -i /home/ansible/.ssh/id_rsa.pub ansible@192.168.1.1

ssh-cpoy-id -i /home/ansible/.ssh/id_rsa.pub ansible@192.168.2.2
```

### 安装

### 模块

### 剧本

### 角色

### 模版