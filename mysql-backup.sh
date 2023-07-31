#!/bin/bash

# mysql root 账号
DB_USER="root"
DB_PASS="123456"
DB_PORT=8306
# 备份后目录
BACKUP_DIR="/home/databak"

# 保留多少天的日志
DAY_LOG=21
# 时间目录
DATE=$(date +%Y-%m-%d)

# 备份日志
BACKUP_LOG="${BACKUP_DIR}/mysqldump-backup-${DATE}.log"


# 创建备份目录
if [ ! -d "$BACKUP_DIR/$DATE" ]; then
  mkdir -p $BACKUP_DIR/$DATE
fi

echo "开始备份，具体查看备份日志 $BACKUP_LOG"

echo "==========数据库备份开始==========" >>$BACKUP_LOG

for dbname in $(/usr/local/mysql/bin/mysql -P$DB_PORT -u$DB_USER -p$DB_PASS -A -e "show databases\G"|grep Database|grep -v schema|grep -v test|awk '{print $2}')
do
  sleep 1
  /usr/local/mysql/bin/mysqldump -P$DB_PORT -u$DB_USER -p$DB_PASS $dbname > $BACKUP_DIR/${DATE}/$dbname.sql

  # 判断是否正常执行备份命令
  if [[ $? == 0 ]];then
    # 进入备份目录
    cd $BACKUP_DIR/${DATE}
    # 查看当前sql文件的大小
    size=$(du $BACKUP_DIR/${DATE}/$dbname.sql -sh | awk '{print $1}')
    echo "备份时间:${DATE} 备份方式:mysqldump 备份数据库:$dbname($size) 备份状态:成功！" >>$BACKUP_LOG
  else
    cd $BACKUP_DIR/${DATE}
    echo "备份时间:${date} 备份方式:mysqldump 备份数据库:${dbname} 备份状态:失败,请查看日志." >>$BACKUP_LOG
  fi

done

# 打包压缩
cd $BACKUP_DIR
tar -czvf $DATE.tar.gz $DATE

du $DATE.tar.gz -sh | awk '{print "文件:" $2 ", 大小: " $1}'

# 删除原始备份文件
rm -rf $BACKUP_DIR/$DATE

echo "==========数据库备份结束==========" >>$BACKUP_LOG

# 删除前两次之前的记录
find $BACKUP_DIR -name "*.tar.gz" -type f -mtime +$DAY_LOG -exec rm {} \;