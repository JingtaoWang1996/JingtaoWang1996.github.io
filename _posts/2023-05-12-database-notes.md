---
title: 'database-notes'
date: 2023-05-12
permalink: /posts/2023/05/database-notes/
tags:
  - cool posts
  - category1
  - category2
---

Some database usage experience.

# 数据库

* 数据库重点是：以SQL为代表的关系型数据库（Oracle，MySQL,Postgres），noSQL代表的非关系型数据库

* NoSql 数据库千奇百怪，主要为了解决数据类型繁多的问题。

* 数据是整个系统或服务的关键点。

## 数据库设计

* 对于指定的应用环境，构造/设计优化的数据库逻辑模式和物理结构，并据此建立数据库设计及应用系统，使其能够有效的存储和管理数据，满足用户需求。

* 目标: 提供信息基础设施和高效运行环境。

* 数据库设计是一种经验的反复实施，设置质量与设计人员的经验和水平有直接关系。

* 必要步骤：需求分析（确定好需求） 确定库与库之间的逻辑关系à逻辑关系图à具体表的字段结构

# Redis

​     key-value 内存型数据库，Redis is short for “Remote Dictionary Server” ,一个开源的使用ANSI and C 编写的 支持网络，可基于内存及**持久化日志的key-value型数据库**。

​    特点：

* 支持多种数据类型：String，list，set，zset（sorted set）hash
* 支持push、pop、add、remove 及其他更加丰富的操作。
* 支持不同排列方式，且周期性将更新数据写入磁盘或追加的记录文件中

## 安装配置

* 主从复制与哨兵模式

​          主从复制：master 更新后的数据同步到slave（master 写为主，slave读为主）

​          主从复制的优势：读写分离，容灾备份

​          常见主从配置：1主2从

### centos 安装redis

* yum install redis

​       ---- 换源的问题 见“centos踩坑记录“

* service redis start  启动redis服务

* service redis status 查看redis状态

## redis-cli 命令

基本操作

* 进入客户端：redis-cli
* 输入密码进入： auth 密码

 相关命令

* set/get/keys *

  *  存入键值： set key value
  *  查询键值：get key
  *  查询redis 所有键值：keys *
  *  正则匹配查查询所有键值：keys *正则表达式* （eg: keys *monitor#* monitor#开头的所有数据）

* 批量操作：mget\mset\pipline

  *mget/mset list -- 所有键组成一个list进行批量查询，返回一个对应key的value构成的list

## 问题记录

**1、** **could not get resource from pool**

Possible solution1：资源是否释放。

Possible solution2: redis_maxIdle 和 maxtotal参数值大小是否合适，可适当添加这两个参数值的大小，尤其是 maxidle

**2、** **远程长时间连接不上**

1） bind 127.0.0.1：只允许本机连接

2） protected mode 设置了yes

---- 解决方案

1） vim /etc/redis.conf

2） # 找到 bind 127.0.0.1 将其注释

3） # 找到 protected-mode yes 将其改为 protected-mode no

4） 重启 service redis stop  service redis start 

# Mysql

所有操作命令都需要加------**“；”**

## 关系型数据库（RDBMS) & NoSql

相关[参考](https://www.runoob.com/mysql/mysql-tutorial.html)

* 数据以表格形式出现

* 每行为各种记录名称；每列记录名称对应的数据域
* 许多的行和列组成一张表单
* 若干表单组成database

RDMS 基本概念

* 数据库：关联表的集合

* 数据表：数据的矩阵

* 列：同一列当中包含了相同的数据类型的数据：eg邮政编码数据

* 行：一行是一组相关数据，数据类型可能不同：eg: 一条订阅数据。

* 冗余：存储多倍数据，降低了性能但提高了数据安全性。

* 主键：唯一，一个数据表只能包含一个主键，可以使用主键查数据**。**

* 外键：用于关联两个表。

* 复合键：将多个列作为作为一个索引键，一般用于复合查询。

* 索引：用于快速访问数据库中表的信息。数据库表中一列或多列的值进行排序的一种结构，类似书籍目录。

* 参照完整性：参照的完整性要求关系**中不允许引用不存在的实体**，与实体的完整性是关系模型必须满足的完整性约束条件，目的是保证数据一致性。

  ![mysql示例图](C:/Users/Administrator/Desktop/分方向笔记/notes/img/mysql示例图.png)

 例子如图：

1） 表头：每一列数据的名称（一列都是相同类型的数据）

2） 行：某条记录的具体信息，多种类型的数据集成。

3） 键：在当前列中唯一。

Nosql(not only sql) --- 关系型数据库的另一个例子：

* 主要用于超大规模数据存储，数据不需要固定模式，无需多余操作就可以横向扩展。

* nosql 数据分类

* RDBMS vs NoSQL

​         * RDBMS: 高度组织化结构化数据、结构化查询语言、数据关系存在单独的表中、数据操纵语言，定义语言、严格一致性、基础事务

​         * NoSQL: 没有声明性查询语言，没有预定义模式，键值对存储，列存储，文档存储，图形数据库存储，最终一致性，高性能、高可用性、可伸缩性、



**关系型数据库遵循ACID原则**

*  A (Atomicity) 原子性：事务里的所有操作，要么完成，要么不做，只要有一个操作失败，整个事务就失败，需要回滚。
*  C (consistency)一致性：数据库处于一致的状态，事务的运行不会改变数据库原本的一致性约束。
*  I (Isolation) 独立性：并发的事情不会相互影响，如果一个事务访问的数据正在被另一个事务修改，只要另一个事务未提交，它访问的数据就没有影响。
*  D(Durability) 持久性：一旦提交后的事务，它所做的修改将会永久保存在数据库上，即使宕机也不会丢失。

## 安装配置

linux 推荐使用rpm包安装

- **MySQL** - MySQL服务器。你需要该选项，除非你只想连接运行在另一台机器上的MySQL服务器。
- **MySQL-client** - MySQL 客户端程序，用于连接并操作Mysql服务器。
- **MySQL-devel** - 库和包含文件，如果你想要编译其它MySQL客户端，例如Perl模块，则需要安装该RPM包。
- **MySQL-shared** - 该软件包包含某些语言和应用程序需要动态装载的共享库(libmysqlclient.so*)，使用MySQL。
- **MySQL-bench** - MySQL数据库服务器的基准和性能测试工具。

​    查看mysql 是否成功安装：Mysqladmin –version 

rpm命令检测是否自带mysql：   rpm –qa | grep mysql 

* 如果有安装，可以自行卸载：rpm –e mysql  //普通删除  rpm –e –nodeps mysql  // 强力删除模式，如果普通删除提示有依赖文件的话

ubuntu 安装mysql，[参考](https://blog.csdn.net/hwx865/article/details/90287715)

* Default DB name ‘test’ that anyone can access.

* sudo apt-get install mysql-server

* sudo apt-get install mysql-client

* sudo mysql_secure_installation // mysql 初始化安全脚本，更改root密码等等

* 测试mysql：systemctl status mysql.service [以下为正常状态]

  ![mysql正常运行示例图](C:/Users/Administrator/Desktop/分方向笔记/notes/img/mysql正常运行示例图.png)

## 服务操作---命令结尾加上：；

* 启动数据库服务：sudo service mysql start or  sudo systemctl start mysql.service
* 重启数据库服务：sudo service mysql restart or  sudo systemctl restart mysql.service
* 停止数据库服务：sudo service mysql stop or  sudo systemctl restart mysql.service
* 使用root用户登录：mysql –u root –p // 15上输入密码 root
* 退出mysql命令行：mysql>quit
* 创建用户：CREATE USER 'username'@'host' IDENTIFIED BY 'password'; 

​      Username：用户名，password:密码，为空则不需要密码，host：指定登录主机，本地立可以localhost，任意远程主机，用通配符%（通配符登录需要明确的ip）

* 用户授权 GRANT privilege ON databasename.tablename TO ‘USERNAME’@’host’ WITH GRANT option;

* 上一步执行后需要刷新授权：flush priviledges;
* 设置与更改用户密码：ALTER USER 'username'@'host' IDENTIFIED BY 'password' PASSWORD EXPIRE NEVER; 

* 删除用户：DROP USER ‘username’@‘host’

## 数据操作---命令结尾加上：；

* **创建数据库**(登录root后)：CREATE DATABASE 数据库名;
* 删除数据库：DROP DATABASE 数据库名;
* 查看所有数据库：show databases;
* 查看当前使用的数据库：select database();
* 选择某个数据库：use 数据库名;
* 查看数据库使用的端口：show variables like ‘port’;
* 查看数据库的表信息：show tables;
* 查看表结构：show columns for table_name;
* 查看数据文件存放路径：show variables like '%datadir%';
* 查看数据库最大连接数：show variables like '%max_connections%';
* 查看数据库当前连接数，并发数：show status like ‘%Threads%’
* 创建数据表：CREATE TABLE table_name (column_name,column_type);

```mysql
CREATE TABLE IF NOT EXISTS `runoob_tbl`(
   `runoob_id` INT UNSIGNED AUTO_INCREMENT,
   `runoob_title` VARCHAR(100) NOT NULL,
   `runoob_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `runoob_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

PS: 创建表‘runoob_tb1’ 并判断是否存在，同时括号的当中设定表的key & value， primary key 用于定义“主键”,Engine =InnoDB 设置存储引擎，DEFAULT CHARSET =utf8，**创建时，表中所有key不需要引号**

* 删除数据表：DROP TABLE table_name; 

* 插入数据：INSERT INTO table_name（field1,field2,…filedN）VALUES (value1,value2,…valueN);

* 查询某个table中的所有数据or 数据： select * from 表名[where 条件]；

  PS: where 语句后跟条件，可以用and / or 增加更多条件

* 更新语句：UPDATE table_name SET field1=new-value1, filed2 [where 条件]

  *可同时更新一个或者多个字段，可在单独的表中同时更新数据。

  PS:注意SET 之后的column的值需要引号才不报错；

  PPS: where 条件可以增加‘大于等于小于‘符号作为判定条件。

* 删除语句DELETE: DELETE FROM table_name [where 条件] *若不做条件指定，则删除table当中的所有记录

* like 语句：WHERE colum_name like ‘模糊条件’

  eg: select * from table_name where 列名 like 'MWA%'

  ps: 模糊前后不确定长度和内容的字段用%代替

* Union 操作符：连接两个以上的SELECT 语句结果到一个结果集合中，多个select 语句会删除重复的数据。【可以select不同的表进行查询】

  ```mysql
  SELECT expression1, expression2, ... expression_n
  FROM tables
  [WHERE conditions]
  UNION [ALL | DISTINCT]
  SELECT expression1, expression2, ... expression_n
  FROM tables
  [WHERE conditions];
  ```

PS: 如果使用UNION ALL 则集合之后的结果可能会有重复

* 排序语句ORDER BY: 设定想要的输出结果的顺序

​        select * from table_name [where 条件] order by column_name;

​        PS: 默认升序排列，可以在order by 列名 后加ASCE，DESC 明确升序和降序排列。

​               Select * from student3 order by math; student3 的数据按照math数值升序排列;

​               Select * from student3 order by math DESC; 降序排列

* Group by 语句： 根据一个/多个列对结果进行分组，可使用COUNT,SUM,AVG等函数

## 操作特例

* **NULL** **值处理：**

​       IS NULL/IS NOT NULL：当列的值为NULL或者非空,此运算符返回true

​       <=>: 比较操作符（不同于 =），当比较的两个值相等或者都为 NULL 时返回 true。

* **事务：**

​       主要用于处理操作量大、复杂度高的数据。

​       Eg: 在人员管理系统中，你删除一个人员，你既需要删除人员的基本资料，也要删除和该人员相关的信息，如信箱，文章等等，这样，这些数据库操作语句就构成一个事务！

* ALERT 命令

​        ALTER TABLE 表名 DROP i；// 删除表中的i字段

​        ALTER TABLE 表名 ADD I 类型；

​        ALTER + MODIFY/CHANGE 修改值/类型等

​        ALTER TABLE testalter_tbl RENAME TO alter_tbl; // 修改表名

* [索引](https://www.runoob.com/mysql/mysql-index.html)：能够大大提高Mysql的检索速度.

* 临时表：存储临时数据、仅当前连接可见，连接关闭后自动删除释放空间。[具体情况](https://www.runoob.com/mysql/mysql-temporary-tables.html)

  create temporary table 表名

* 复制表：

  Show create table 已存在表名 // 获取表完整结构

  Create table table_name; // 修改表名并创建克隆表；

  将数据库中创建的新克隆表clone_tbl并复制数据；

* [导入导出数据](https://www.runoob.com/mysql/mysql-database-export.html)：

  导入：mysql -u用户名  -p密码  < 要导入的数据库数据(runoob.sql)

  导出：select * from table_name INTO OUTFILE ‘文件路径（到具体文件名称)

* [处理重复数据](https://www.runoob.com/mysql/mysql-handling-duplicates.html)

​       通过设置主键来确保数据不重复

## 鉴权

* 认证：决定用户是否可以连接mysql，使用预先创建的用户名和密码，尝试本地或远程链接Mysql。Mysql验证用户名和密码，如果用户名存在&用户名和密码匹配，就表示认证成功。否则拒绝链接。

* 鉴权：决定用户链接mysql之后可以执行哪些操作，用户只能执行自己有权限的操作。

  1） 管理员操作：创建删除用户、创建角色、终止数据库实例等全局性操作。

  2） 数据库和数据库对象操作：对某个数据增删改查操作，也包括对数据库中的表、索引或者试图的增删改查操作。

* 权限授予：grant : GRANT INSERT,UPDATE,XXXX ON customer.address TO 'root@localhost'

* 权限撤销：revoke ：REMOVE INSERT,UPDATE,XXXX ON customer.address from 'root@localhost'

# Mongo

基于分布式文件存储的开源数据库，，介于关系型和非关系型数据库之间。高负载的情况下，添加多节点可以保证服务器性能；【将数据存为一个文档，键值对形式（数据），json（文档），字段可以包含其他文档，数组，文档数据。】

## 安装配置

* windows 平台[安装步骤](https://www.runoob.com/mongodb/mongodb-window-install.html)

* 进入[下载地址](https://www.mongodb.com/try/download/community)后，选择适合版本然后wget下载

  <img src="C:/Users/Administrator/Desktop/分方向笔记/notes/img/mongo下载图.png" alt="mongo下载图" style="zoom:75%;" />

  **PS: cat/etc/red-hat release** **进行查询centos****版本号**

   **Step1**：wget** **命令下载：**wget 链接

   **Step2**：解压：**  tar –zvxf xxxxxx.tgz   

    Ps: Linux rpm 文件则可以直接命令安装 rpm –ivh xxx.rpm

     上述命令如果缺少依赖则对照安装

   **step3**：解压包拷贝到指定目录**

    mv 解压完成的文件夹到 /usr/local/mongodb5

    cd /usr/local/mongodb5

   **step4:** **将mongoDB** **可执行文件添加到path****路径中：**

    export PATH = /usr/local/mongodb5/bin:$PATH

   **Step5**：创建数据库目录**

    默认情况下MongoDB 启动后会初始化以下两个目录：

  1） 数据库存储目录：/var/lib/mongodb

  2） 日志文件目录：/var/log/mongodb

  启动前将这两个目录设置为当前用户有读取权限

  Sudo mkdir –p /var/lib/mongo

  Sudo mkdir –p /var/lib/mongodb

  sudo chown `whoami` /var/lib/mongo # 设置权限

  sudo chown `whoami` /var/log/mongodb # 设置权限

   **Step6**：启动mongoDB****服务**

    **mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log –fork**

## pymongo 操作 mongodb

* 基本操作 & 增删改查数据

```
import pymongo


class mongoDB_connection:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017")  # 创建mongodb连接
        self.new_db = self.client["newDB"]  # 创建名称为newDB的数据库

    def checkDB(self):  # 输出所有数据库
        db_list = self.client.list_database_names()

    def checkCollections(self, db_name):  # 输出某个数据库中所有的list
        collection_list = self.client[db_name].list_collection_names()

    def createCollections(self):  # 创建collections
        return self.new_db["new_collections"]


a = mongoDB_connection()
data1 = {"a": "b", "c": "d"}  # json 格式数据
data2 = {"d": "e", "f": "g"}
my_col = a.createCollections()
# -----------------插入数据-------------
command1 = my_col.insert_one(data1)
print(command1.inserted_id)  # 插入完成后获得表中对应的id
command2 = my_col.insert_many([data1, data2])
print(command2.inserted_ids)  # 插入完成后的所有id
# -----------------查询数据---------------
command3 = my_col.find_one(data1)
# 查询集合中的所有数据
[print(x) for x in my_col.find()]
# 指定条件查询
criteria = {"key": "value"}  # 查询条件可以改用修饰符、正则匹配等
my_col.find({criteria})
# 查询指定字段的数据
[print(x) for x in my_col.find({}, {"a": 1, "b": 2})]
# limit限制查询条数
my_col.find().limit(3)
# -----------------修改数据---------------
myquery = {"a":1}
myupdate = {"a":1000}
my_col.update_one(myquery,myupdate) # 将第一条满足查询条件的数据进行更新
my_col.update_many() # 更新多个

```

## shell 命令执行参数

* 连接client：mongo
* 切换到admin数据库：use admin
* 查看当前数据库状态：db.stats()
* 显示当前mongo版本：db.version()
* 查询所有数据库名称：show dbs
* 数据库迁移：mongodump -h host:ip -d 数据库名称 -u 用户名 -p 密码 --authenticationDatabase admin -o 导出路径
* 数据恢复：Mongorestore -h host:ip -d dbnameNew --

# Neo4j

 图数据库，以cypher语句往里存的时候，能够达到10^8数量级，有索引及散热的条件下能够在ms级完成查询。

## 安装配置

* [下载地址](https://neo4j.com/download-center/)

* 安装：[3.x 对应java8， 4.x 对应java11]

​       * tar -xzvf neo4j-community-3.5.0-unix.tar.gz

​       * cd /neo4j/neo4j-community-3.5.0/bin

* 配置修改：cd /neo4j-community-3.5.0/conf  54，71，74 行去掉注释。

## 启动命令

* cd /neo4j/neo4j-community-3.5.0/bin

* 执行相关命令：./neo4j start(stop/console/restart/status)
* 网页打开 ： 10.42.25.12：7474
* 第一次访问账号和密码均为：neo4j ，修改后：neo4j / meiyoumima123

# sqlite

实际是一个软件库，无服务器、零配置、事务性的SQL数据库引擎。SQLite源代码不受版权限制。[参考](https://www.runoob.com/sqlite/sqlite-tutorial.html)

## 安装配置

* 安装sqlite3 ：sudo apt-get install sqlite3
* 确认安装成功: 键入Sqlite3后成功进入命令行模式

### Sqlite3具体命令

* 基本特点: 1)  **命令都是由.(点号)开始**   2)  Sql 语句必须由;结束  3) 正常情况下命令行是 sqlite > 开头，如果进入…>的状态，需要输入;结束返回正常状态。

* 基本命令: Sqlite3 xxxx.sqlite3 进入数据库
* 列出所有表：.tables
* 查看表结构：.schema
* 查看表数据：select * from table_name

​       优化显示: .header on   |   . mode column

* 写入数据命令: insert into 表名 values(v1,”v2”,….) # 字符串用“”，数字直接写


------