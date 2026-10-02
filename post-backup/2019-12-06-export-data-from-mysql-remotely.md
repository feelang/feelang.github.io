---
layout: single
title: 用命令行将远程服务器的 MySQL 表数据导出到本地
date: 2019-12-06
categories: Programming
tags:
  - Database
---

## 0x00 root 身份 ssh 登录到远程机器

```bash
$ ssh root@server_ip_address
```

* 「server_ip_address」换成你的远程服务器的 ip 地址

## 0x01 远程机器上进入 MySQL 控制台

```bash
mysql -u root -p
```

## 0x02 选择数据库

```sql
use your_db;
```

## 0x03 执行导出

```sql
select * from your_table_name into outfile 'file.csv' FIELDS TERMINATED BY ',';
```

* 「your_table_name」换成你自己的表名

如果你的 MySQL 配置了 `--secure-file-priv`，这时会报错：

```
ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement
```

解决方案是先查看 `secure_file_priv` 值：

```sql
SELECT @@secure_file_priv;
```

输出结果：

![](https://img-blog.csdnimg.cn/20191206003114868.png)

> 「secure_file_priv」值可能各不相同，不要直接拷贝这里的值。

然后修改 `SELECT` 语句的 `OUTFILE`：
```sql
select * from your_table_name into outfile '/var/lib/mysql-files/file.csv' FIELDS TERMINATED BY ',';
```

## 0x04 将远程文件 scp 到本地

退出远程服务器的控制台，在本地机器执行命令：

```bash
scp root@server_ip_address:/var/lib/mysql-files/file.csv .
```

这样就拿到了一个 CSV 文件，搞定。
