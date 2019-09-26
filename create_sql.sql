### 创建数据库 ###
create database ipproxy default charset=utf8;

### 进入数据库 ###
use proxy_db

### 创建数据表 ###
create table proxy(
  id varchar(40) primary key,
  ip varchar(80)
);