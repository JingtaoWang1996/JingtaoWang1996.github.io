---
title: 'Middle-ware-notes'
date: 2021-05-26
permalink: /posts/2021/05/Middle-ware-notes/
tags:
  - cool posts
  - category1
  - category2
---

Some usage experience collection：

* Automated Tools:  Docker、Supervisor、Ansible

* Middle-ware: Kafka、ZK、Nignx、Postman

# Docker

* **当系统资源是限制的时候：使用docker虚拟，提高资源总数**
* Docker相当于虚拟机
* **Docker在开发完毕之后可以将环境统一拷贝部署，减少环境因素的影响。**

## 概述

* Docker相当于虚拟机Docker[官网](https://www.docker.com/)，Github Docker [源码](https://github.com/docker/docker-ce)
* 开源的应用容器引擎（开发、交付、运行应用程序的开放平台），基于GO开源。
*  Docker打包应用及依赖到一个轻量级可移植容器中，发布到任何流行的linux机器上（沙箱机制，相互之间不会有任何接口，性能开销低 。17．03 后分为社区版和企业版。
* Dockerhub 下载对应环境的安装包
* 优点：服务于基础架构分离，快速交付；**确保开发、测试、生产环境一致性**，可移植性强

## 架构

* 镜像image：相当于一个root文件系统，比如官方镜像 ubuntu:16.04 就包含了完整的一套 Ubuntu16.04 最小系统的 root 文件系统。
* 容器container：容器即为镜像的实例，镜像为定义的类，容器为实例。容器可以被创建、启动、停止、删除、暂停等等。
* 仓库repository：代码控制中心、用来保存镜像。

## 安装配置

Ubuntu、centos、windows具体安装参见：[安装配置](https://www.runoob.com/docker/ubuntu-docker-install.html)

### 编译安装

* 下载docker并传入机器：[参见]( https://download.docker.com/linux/static/stable/x86_64/)

* 编译安装步骤：[参见](https://docs.docker.com/engine/install/binaries/)

​        * 下载：目前15机器上有

​        * tar xzvf /path/to/<FILE>.tar.gz

​        * sudo cp docker/* /usr/bin/

​        * sudo dockerd &

​        * docker –version 验证

## 打包python项目到docker

**Docker 每次装完基本环境都commit一下，方便后续回溯**

* 拉取镜像：docker pull python：3.8

* 查看镜像：docker images

* 创建容器：docker run --net=host -it --name=名称 python：3.8 /bin/bash

* 删除容器：docker rm -f 容器名称

* 查看创建的容器：docker ps -a 

  * image:使用的镜像
  * containerId：容器ID
  * Status：容器状态（created/restarting/running/up/removing迁移中/pause/exied/dead)
  * ports: 容器端口及使用的连接类型
  * names：z自动分配的容器名称
  * command：运行命令

* **保存容器成为镜像（每一步结束确认正确之后就可以执行一次）**：docker commit 容器Id 新镜像名称：tag

* 进入容器后安装python依赖(有网的情况)：pip3 install xxx

* 本地代码拷入docker：

  * 查看创查看docker ID：  docker ps -a

  * docker 当中新建目录：mkdir /DNS/

  * 本地文件复制到docker容器中:

    docker cp 服务器文件路径 容器ID（或容器名称）：容器内路径

    docker cp /DNS/activeDNS 容器ID:/DNS

* 镜像创建docker：  docker run --net=host -it 名称:tag bash==docker run --net=host -it basic:latest bash

* 镜像暴露端口启动docker： docker run -it -d --name dnstest -p 53:53/tcp -p 53:53/udp 镜像名称:tag

* docker 挂载宿主机目录执行：docker run -it -v /宿主机绝对路径目录:/容器内目录 镜像名

## Docker file

Docker 可以通过docker file 自动构建镜像，docker file 本身是一个文本文档，其中包含了用户创建镜像的所有命令和说明。[参考](https://zhuanlan.zhihu.com/p/387855002)

* 变量：用 $variable_name 或者 ${variable_name} 表示

  * ${variable:-word}表示如果variable设置，则结果将是该值。如果variable未设置，word则将是结
  * ${variable:+word}表示如果variable设置则为word结果，否则为空字符串。
  * 变量前加 \ 可以转义成普通字符串：\$fooor\${foo}，表示转换为$foo和${foo}文字。

* From：初始化一个新的构建阶段，并设置基础镜像

  * FROM 镜像名称：tag  可以直接使用之前打包好的本地镜像
  * eg: FROM python：3.8
  * 单个docker file 可以多次出现From，以使用之前构建阶段作为新阶段的依赖

    包含参数的三类示例： 

    FROM [--platform=<platform>] <image> [AS <name>]

    FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]

    FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]

  * AS name表示构建阶段命名，在后续FROM和COPY --from=<name>说明中可以使用这个名词，引用此阶段构建的映像
  * digest是根据镜像内容产生的一个ID，只要镜像的内容不变digest也不会变
  * tag或digest值是可选的。如果您省略其中任何一个，构建器默认使用一个latest标签。如果找不到该tag值，构建器将返回错误。
  * --platform标志可用于在FROM引用多平台镜像的情况下指定平台。例如，linux/amd64、linux/arm64、 或windows/amd64

* ENV: 配置环境变量  ENV <key>=<value> ...

  设置的环境变量将持续存在，可以使用docker inspect 来查看，使用docker run –env <key> =<value> 来更改环境变量的值

* EXPOSE：指定docker监听端口，可以指定端口监听tcp还是udp，若不指定，默认为TCP：EXPOSE 端口/协议

* RUN: **空一格之后增加linux指令**

  eg：RUN /bin/bash -c ‘mkdir /dnsHP’

  * Run <command>(shell形式，命令在shell中运行，默认 /bin/bash -c 在linux 上，cmd /S/c windows 上以使用\（反斜杠）将单个 RUN 指令延续到下一行
  * RUN在下一次构建时，指令缓存不会自动失效。可以使用--no-cache标志使指令缓存无效
  * Dockerfile 的指令每执行一次都会在 docker 上新建一层。可以使用&& 符号连接命令，这样执行后，只会创建 1 层镜像 Eg：run /bin/bash -c ‘cd /dnsHP && python3 v1.py’

* ADD:复制新文件、目录或远程URL: --- <src>可以指定多个资源，但如果他们是文件或目录，则它们的路径被解释为相对构建上下文的源，也就是**workdir**

* Volume：创建具有特定名称的挂载数据卷,避免重要数据因容器重启而丢失： VOLUME /var/log

* EntryPoint：指定容器启动程序和参数【不会被docker run的命令行参数指定的指令覆盖，需要覆盖则要通过docker run --entrypoint 来指定】

  * ENTRYPOINT ["python3"，“参数1”，“参数2”]
  * ENTRYPOINT command param1 param2

* Copy：语法同ADD，用于复制文件。copy 只能从执行docker build所在的主机上读取资源并复制到镜像中，而add指令还支持通过URL从远程服务器上读取资源并复制到镜像中。

* Workdir：创建工作目录的命令，只有通过workdir创建的目录才会一直存在。

* stopsignal：发送容器退出系统调用的信号，具体signal可以为任意无符号数

* onbuild: 将触发指令添加到镜像中，以便稍后在该镜像用作另一个构建基础时同时进行，也就是另个一dockerfile FROM了这个镜像的时候执行。

  * ONBUILD ADD . /app/src
  * ONBUILD RUN /usr/local/bin/python-build --dir /app/src

## docker-compose yml 文件编写

docker-compose 单机多容器编排工具，适用于单机部署多个容器，[参考](https://blog.csdn.net/doubiy/article/details/118997661)

docker-compose 创建并启动容器命令：

* Docker-compose up 创建并启动容器
* Docker-compose up –d 以后台形式创建并启动容器
* Docker-compose -f xxxxx.yml  up 指定创建并启动容器使用的yml文件
* **docker-compose ps :查看通过docker-compose创建的容器，此方法不显示docker run 创建的容器**
* **docker-compose images：仅查看通过docker-compose得到的images，其他方式创建的镜像通过docker images查看**
* docker-compose stop/start 停止和启动 docker-compose,yml 文件中定义的容器。
* docker-compose down 停止并删除 docker-compose,yml 文件中定义的容器及network配置不删除volume。
* docker-compose logs docker-compose.yml 容器名称  查看某个容器的日志 

PS: docker-compose 的命令需要在有docker-compose.yml 文件的目录才可以执行，否则使用docker-compose 命令会报错；并且只有该yml文件执行了up操作（创建了该docker-compose.yml 定义的容器之后才可以看到对应容器，否则报错）



**具体编写**

* version:指定版本

* service：该指令下面写该yml文件中需要定义的container信息，service下面一级就是指定该容器名称：

  ```
  services： # 定义container
    mysql： # container 名称为mysql
      image：“mysql：5.7” # image来源
  ```

  

* images：指定该容器使用的image 和build 2选1

*  build：指定该容器使用的image通过哪个目录下的DockerFile文件进行构建，.表示当前目录的Dockerfile文件，build和image二选1

* port：指定宿主机和端口的映射关系，可以指定多个

* networks: 指定使用的网络信息，相当于docker network create命令，可指定多个。Network指令下一级指令就是网络名称，配合subnet指定网段信息。

  * ipv4_address: 和network配合使用，指定container在该网络中的ip。

* volumes：指定数据挂载信息，相当于docker volume create，可指定目录或文件映射，也可指定数据挂载记录和容器中的目录映射（这种一般指定的容器中目录是该容器Dockerfile文件中VOLUME指令指定的目录）如果指定数据挂载记录的映射需要通过volumes定义数据挂载记录，可指定多个。

* environment：指定容器可选参数值信息

  ```
  注意：
  1、yml文件的格式层级关系是缩进2个英文状态的空格，不能用缩进符等代替空格。
  2、若指令后需要写值必须是英文冒号+英文空格+值如：restart: always
  3、若是写多个值的指令（复数s），冒号后换行使用 –指定具体值
  4、Service下面定义的container只能docker-compose 命令使用，docker命令只能docker ps进行查看。
  ```

## 其他相关命令

* 获取容器Id/名称：docker ps -a

* [导入导出](https://blog.csdn.net/qq_44273583/article/details/11438736)

  * 对应关系：export--import  save--load

  * export & import：

    导出--docker export 容器ID >名称.tar

    导入--docker import – 名称 < 导出名称.tar

    docker images 查看

* Docker外执行docker内的命令

  * docker start 容器名称
  * docker exec -it 容器id /bin/bash -c '容器内路径及命令'

* docker进入exit的容器中

  * 启动docker：docker ID start
  * 进入docker：docker exec -it 容器ID /bin/bash

* 启动守护进程：systemctl start docker

* docker run 加端口映射启动：docker run --name 容器名称 -p 主机port:容器port/udp -p 主机port:容器port/tcp –d docker images 

* 删除镜像：docker rmi 镜像id

* 查看docker 内存占用：docker stats

## 问题记录

* docker警告：WARNING: IPv4 forwarding is disabled. Networking will not work.

  在docker映射之后爆出上面错误，因为没有开启转发

​       解决方案：

​       * Vim /etc/sysctl.conf，新增下面一行：Net.ipv4.ip_forwad = 1，重启network 和docker服务

​       * systemctl restart network && systemctl restart docker，查看是否修改成功：sysctl net.ipv4.ip_forward

*  OCI runtime exec failed: exec failed:解决方法（无法进入容器）

​        使用命令：docker exec –it 容器ID /bin/sh

# kafka

## 概述

* 消息系统：将数据从一个应用传递到另一个应用，只关注数据，不关注具体如何传递。常见两种模式：

  * **点对点发模式**：消息持久化到某个队列中，可以包含优先级，每个数据被消费1次
  * **发布订阅模式**（大部分系统、kafka采用的方式）：类似kafka通过topic进行消费，

* Kafka 是一个分布式，分区，多副本，多订阅者，**基于zookeeper** 协调的分布式消息系统

* 设计目标：以时间复杂度为O（1）的方式提供消息持久化能力；高吞吐率；**支持消息分区，分布式消费，同时保证每个partition** **内消息顺序传输**；数据离线和实时处理；

* 优点

  * 解耦：消息中间件，将消息生产者部分和消费者部分的代码逻辑相互解耦。
  * 冗余：partition之间有备份，在消息完全处理完值钱。
  * 扩展性：在网络开销等方面允许的情况下，增加消费者、生产者提高吞吐量。
  * 并发性+异步处理：多个消费者同时消费多个partition+允许用户将消息存入队列，需要时在处理。
  * 顺序性+缓冲：**充当系统中耗时不同任务的缓冲层用于处理任务。**

* 缺点

* 相关定义

  * broker： kafka集群中包含一个或多个服务器，服务器节点称为 broker，broker 存储topic当中的数据。
  * topic：消息逻辑存储参数
  * partition：一个topic包含多个分区用于存储信息，便于多个消费者对应消费。

* 消息存储方式：

  * 硬盘顺序写入的方式来存储文件。

  * 内存映射: 即使顺序写入，硬盘的访问速度还是更不上内存。所以kafka的数据并不是实时写入硬盘，而是通过分页存储来利用内存提高I/O 效率。

## linux 安装配置步骤

以22安装单节点为例,[参考](https://www.cnblogs.com/biehongli/p/10216309.html)

* 下载kafka[安装包](https://kafka.apache.org/downloads), 选择  binary download

* 解压文件：tar -xzf xxx.tgz

* vim ./config/server.properties, 放开这一行

  ```
  listeners=PLAINTEXT://localhost:9092
  ```

* 先后台启动zk: nohup ./bin/zookeeper-server-start.sh config/zookeeper.properties >/dev/null 2>&1

* 在ps 确定zk启动的基础上，基于server.properties 启动kafka:

  * nohup ./bin/kafka-server-start.sh config/server.properties >/dev/null 2>&1 &

  * ps -ef|grep kafka 

* 

## producer 参数调优

除去必要的：kafka配置、参数值、topic等，其他可能影响kafka发送效率的可调整参数：

* batch_size: 默认16KB，积累到一个batch的数据量后统一发送
* linger_ms: 发送延迟，单位ms. 当缓存空间中达到batch_size 和 linger_ms 任意一个之后就发送。
* compression_type: 数据压缩方式，lz4>snappy>gzip（发1w条，加了压缩参数后用时从 2.7s降到0.67s

## consumer 参数调优

必传参数

*  bootstrap_servers=dns_conf.hosts, # Kafka服务器的地址和端口
* group_id=dns_conf.consumer_group_id, # 消费者组标识符

可选参数

* value_deserializer=lambda x: x.decode('utf-8'), # str类消费者消息能够直接decode

性能参数

* max_poll_records=5000, # 一次poll能获取的最大数据量
* max_poll_interval_ms= 300000 # 控制消费者两次拉取时间的最大轮训间隔，**若在这个时间段内没有消费到任何消息，就会任务失去了心跳链接，触发重平衡过程**，默认5min【控制连接问题】

​       PS: 若max.poll.records 在这个interval_ms时间内没有完成，就会触发rebalance

* fetch_max_wait_ms=5, # 每多少ms拉去一次数据，默认500ms，往小调能够增加拉取频率，提高消费效率
* fetch_max_bytes=10485760, # 设置每次拉取的最大数据量为 100MB，server端可返回给consumer的大小
* max_partition_fetch_bytes=5242880 # 设置单个分区的最大数据量5MB=1024*1024*5

### 重复消费的问题

出现重复消费的场景

* 消费过程中，进程被kill掉或者发生异常
* consumer消费时间过长：在consumer定义的两次消费间隔max.poll.interval.ms 之中，若无法消费完消息，consumer就会主动发起“离开消费组“的请求。

解决方案：

* 增加数据标识符
* 消费重试机制--spring-kafka 有，但kafka-python 只能通过代码逻辑实现

## 操作命令

cd 到kafka解压后bin目录的上一级：eg /opt/wjt/kafkaxxxxx/，[参考](https://blog.csdn.net/ytp552200ytp/article/details/119914474)

* **查看当前存在的所有消费组**：./bin/kafka-consumer-groups.sh -bootstrap-server localhost:9092 --list
* **查看某个消费组消费状态及lag**：./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group 消费组名称 --describe
* 命令消费数据：
  * **从头手动消费kafka数据**：./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic名称 -from-beginning
  * **手动消费数据**：./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic名称
* topic 相关类：
  * **创建topic**：./bin/kafka-topics.sh --create --zookeeper localhost:2181 --topic test --partitions 1 --replication-factor 1
  * **查看topic list**：./bin/kafka-topics.sh --list --zookeeper localhost:2181
  * **删除topic**：./bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic topic名称
  * **查看topic 分区**：./bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic topic 名称
* producer 压力测试：./bin/kafka-producer-perf-test.sh  --topic test --record-size 500 --num-records 100000 --throughput -1 --producer-props bootstrap.servers=localhost:9092

## 问题记录

* kafka producer 生产者不断发送的过程中，如果延迟过小，则容易产生丢包的情况。Linger_ms 参数需要正常设置。 同时，kafka 丢包问题还可能因为代码运行时间不够，导致丢包情况。

* Linux kafka python 包当中Producer 需要放在脚本内部调用，放在全局变量的位置容易产生 producer 无法发包的情况。

* **No brokers available**: 最大可能的原因---/etc/hosts 文件当中的 IP 和别名对应关系不对：要么是别名被修改【这个是最大的可能】or kafka挂了

* 启动kfk命令之后，报错：configured broker id 0 doesn't match stored broker id 2 in meta.properties

​      解决方法：根据报错修改Server.properties 里面的broker.id 和zk当中的不一致

* Connection to node -1 (/127.0.0.1:9092) could not be established. Broker may not be available
  * kafka server 配置 & kafka 服务是否还在正常运行

# Zookeeper

[官网](https://zookeeper.apache.org/)

## 概述

* 分布式应用程序中心/协调服务，提供的功能包括: 配置维护、分布式同步、组服务等。
* 目标：封装好复杂易出错的关键服务，将接口、性能高效、功能稳定的系统提供给用户。
* 提供JAVA 和C接口，代码版本提供了分布式独享锁、选举、队列接口（选举只有JAVA版本）

## 安装配置

* [官网下载](https://zookeeper.apache.org/releases.html)，注意选择stable版本
* 单机启动：参见kafka linux 安装配置步骤
* 集群启动: 【待测试】
* [可视化客户端配置]([https://issues.apache.org/jira/secure/attachment/12436620/ZooInspector.zip](https://links.jianshu.com/go?to=https%3A%2F%2Fissues.apache.org%2Fjira%2Fsecure%2Fattachment%2F12436620%2FZooInspector.zip)) 解压后进入build目录执行命令：java -jar zookeeper-dev-ZooInspector.jar

# Postman

[官网及下载](https://www.postman.com/)

* **接口测试转发工具，可以模拟用户发起各类HTTP**请求，将请求数据发送到服务端，获取对应的响应结果。[get、post、delete、put类请求]
* Postman 与浏览器的区别在于浏览器不能输出Json格式，而postman可以更直观看到接口返回结果。

# Nignx

* 高性能的HTTP和反向代理web服务器，同时也提供了IMAP/POP3/SMTP服务。
* 内存占有率小、并发能力强、可在大多数Linux上编译运行，同时也是优秀的邮件代理服务器。

## 安装配置

* 下载对应版本的压缩包 D:\173\nginx-1.22.1\：
* nginx 相关配置
  * 配置文件：conf 目录下的nginx.conf
  * 默认监听端口：80
  * 查看端口是否被占用：netstat –ano| findstr 0.0.0.0：80

* 启动nginx：
  * 运行 nginx.exe, 黑色弹窗一闪而过就完成了
  * win+R 切到nginx 目录后 start nginx
  * 查看nginx 是否成功启动：浏览器输入: localhost：80

* 停止 nginx：
  * 快速停止：nginx –s stop
  * 正常退出nginx –s quit 

# supervisor 

基于python的自动化运维工具，[参见](https://www.cnblogs.com/zhoujinyi/p/6073705.html)

## 安装配置

* 命令安装： easy_install supervisor  |  pip install supervisor |  apt-get install supervisor
* supervisor配置文件：/etc/supervisor/supervisord.conf
  * supervisor 不会直接跟系统的句柄数修改，需要修改配置文件中的minfds 参数，[参见](https://www.jianshu.com/p/56e278f2fb7d)
  * supervisor 本身的日志路径也在这个文件中
* 服务管理的配置文件: /etc/supervisor/conf.d/*.conf
  * 根据需要将自动监控的服务仿照上述路径下最开始的.conf文件作为扩展名
  * 根据示例文件配置好：命令、参数、**日志路径**等等

## 运行启动

* 修改或更新配置后需先运行：supervisorctl update（出现 dnspython: add to group xxxx 表示dnspython 添加成功并开始运行）
* supervisorctl restart/start/stop xxxxx：重启、启动、停止xxxx任务
* supervisorctl status：确认运行状态

# Ansible--批量运维工具

* 自动化运维工具：批量系统配置、批量程序部署、批量运行命令等

* 基于paramiko开发，本身没有批量部署的能力，基于ssh和远程通讯完成。
* 只需要在**主控端部署ansible环境**，被控机器无需任何操作，默认使用ssh 对设备进行管理。
* 基于playbook(.yml文件格式)定义部署方式

## 安装配置

* pip3 install ansible

* yum install epel-release -y & yum install ansible –y

* 安装目录

  * 配置文件目录：/etc/ansible/
  * 执行文件目录：/usr/bin/
  * Lib库依赖目录：/usr/lib/pythonX.X/site-packages/ansible/
  * Help文档目录：/usr/share/doc/ansible-X.X.X/ 
  * Man文档目录：/usr/share/man/man1/

* 配置文件：【需从多个地方查找配置文件】

  * 检查环境变量 ANSIBLE_CONFIG 指向的路径文件：export ANSIBLE_CONFIG=/etc/ansible.cfg；
  * ~/.ansible.cfg，检查当前目录下的ansible.cfg配置文件；
  * /etc/ansible.cfg检查etc目录的配置文件；
  *  /etc/ansible/ansible.cfg or(/etc/ansible/ansible/ansible.cfg 常见参数配置：

  ```
  inventory = /etc/ansible/hosts		#这个参数表示资源清单inventory文件的位置
  library = /usr/share/ansible		#指向存放Ansible模块的目录，支持多个目录方式，用冒号隔开
  forks = 5		#并发连接数，默认为5
  sudo_user = root		#设置默认执行命令的用户
  remote_port = 22		#指定连接被管节点的管理端口，默认为22端口，建议修改，能够更加安全
  host_key_checking = False	#是否检查SSH主机的密钥，True/False。关闭后第一次连接不会提示配置实例
  timeout = 60		#设置SSH连接的超时时间，单位为秒
  log_path = /var/log/ansible.log		#指定一个存储ansible日志的文件（默认不记录日志）
  ```

## hosts 文件配置

* hosts 文件用于配置被控节点主机列表，包含：ip、密码、用户名、所属操作部分等

* 文件位置（常见路径）：/etc/ansible/hosts/ 

* 基本定义方式如下：

  ```
  [active] # 组名1,下面是具体主机的ip列表,默认通过ssh连接
  192.168.253.159
  192.168.253.160
  
  [all] # 至少需要ip,本组第一个为包含hostname、user、密码的全部情况
  33.22.11.22 hostname=node1 ip=33.22.11.22 ansible_ssh_user=root ansible_ssh_pass=xxxx
  4.5.6.7 hostname=node1 ansible_ssh_user=root
  ```

## ansible 相关命令

在hosts文件所属路径下，[参考](https://www.cnblogs.com/amber-liu/p/10403512.html)

* **批量执行命令**（如dig）：**ansible -i hosts_all all -m shell -a “dig cn. ns @2001:dc7:9d0e::3”**

  命令格式： ansible -i <hosts文件名><hosts文件里面需要执行命令的group> -m shell -a <执行的shell命令>

  在ansible 配置了具体文件的路径下执行ansible脚本

  * 单个文件分发： ansible -i hosts_24 active -m copy -a "src=./控制节点文件路径 dest=目标服务器路径"

  ​       src：要分发文件的路径，dest：目标目录，具体服务器在ansible配置文件中进行了配置

  * 配置的具体目录下执行下述目录supervisor 启动

  ​       ansible -i hosts_24 active -m shell -a "ansible kafka -m shell -a 'supervisorctl restart dnspython'

命令集：

* **/usr/bin/ansible　　Ansibe AD-Hoc 临时命令执行工具，常用于临时命令的执行**
* /usr/bin/ansible-doc 　　Ansible 模块功能查看工具
* /usr/bin/ansible-galaxy　　下载/上传优秀代码或Roles模块 的官网平台，基于网络的
* **/usr/bin/ansible-playbook　　Ansible 定制自动化的任务集编排工具**
* /usr/bin/ansible-pull　　Ansible远程执行命令的工具，拉取配置而非推送配置（使用较少，海量机器时使用，对运维的架构能力要求较高）
* /usr/bin/ansible-vault　　Ansible 文件加密工具
* /usr/bin/ansible-console　基于Linux Consoble界面可与用户交互的命令执行工具
* ansible-doc -l                  #获取全部模块的信息
* ansible-doc -s MOD_NAME       #获取指定模块的使用帮助

## 常用模块

* 主机连通性测试：ansible web -m ping (ping字段返回值为pong则说明正常联通)

* shell 模块：支持在被控节点调用shell解释器运行命令：ansible web -m shell -a “具体的shell命令”

* command模块：被控主机执行命令，并返回结果：ansible web -m command -a "具体命令"

* copy模块：将文件复制到远程主机，同时支持给定内容生成文件和修改权限，其相关选项如下：

  * src：被复制到远程主机的本地文件。可以是绝对路径，也可以是相对路径。如果路径是一个目录，则会递归复制，用法类似于"rsync"
  * content：#用于替换"src"，可以直接指定文件的值
  * dest：#必选项，将源文件复制到的远程主机的绝对路径
  * backup：#当文件内容发生改变后，在覆盖之前把源文件备份，备份文件包含时间信息
  * directory_mode：#递归设定目录的权限，默认为系统默认权限
  * force：#当目标主机包含该文件，但内容不同时，设为"yes"，表示强制覆盖；设为"no"，表示目标主机的目标位置不存在该文件才复制。默认为"yes"
  * others：#所有的 file 模块中的选项可以在这里使用
    * eg1: 复制文件  # ansible web -m copy -a 'src=~/hello dest=/data/hello'
    * eg2： 给定内容并生成文件：# ansible web -m copy -a 'content="I am keer\n" dest=/data/name mode=666'

* ### ansible 批量更新脚本

  1、 在ansible 配置了具体文件的路径下执行ansible脚本

  2、 单个脚本分发

  ansible -i hosts_24 active -m copy -a "src=./combDataUpdateFromRedis0526.py dest=/DNS/activeDNS/combDataUpdateFromRedis0526.py"

  src：要分发文件的路径，dest：目标目录，具体服务器在ansible配置文件中进行了配置

  3、配置的具体目录下执行下述目录supervisor 启动

  ansible -i hosts_24 active -m shell -a "ansible kafka -m shell -a 'supervisorctl restart dnspython'

## 问题记录

* 报错信息：“msg“: “Invalid/incorrect password: Permission denied, please try again.“，[参考](https://blog.51cto.com/u_15233520/5222515)
  解决方案：若提示密码错误，则将密码加双引号

# logstash

[官网](https://www.elastic.co/cn/logstash/) 

免费且开放的服务器端数据处理管道，能够从多个来源采集数据，转换数据、然后存库

## 搭建

Elasticsearch是当前主流的分布式大数据存储和搜索引擎，可以为用户提供强大的全文本检索能力，广泛应用于日志检索，全站搜索等领域。Logstash作为Elasicsearch常用的实时数据采集引擎，可以采集来自不同数据源的数据，并对数据进行处理后输出到多种输出源，是Elastic Stack 的[重要组成部分](https://cloud.tencent.com/developer/article/1549890)

* [下载安装](https://cloud.tencent.com/developer/article/1549890)
* 架构：基于logstash构建的日志收集处理体系是基于消息的，整个系统由4个组件组成。
  * shipper 搬运者，将事件发送到logstash，一般来说在应用服务所在的机器上只需要部署改组件。
  * broker and indexer 收集事件并进行处理，完成数据过滤，数据格式化等，然后传输到制定存储系统或者本地数据持久化。【一般由logstash担当】
  * search & storage 用于存储和搜索事件。
  * web interface 网络接口，通过web界面向用户展示数据。

![img](file:///C:\Users\ADMINI~1\AppData\Local\Temp\msohtmlclip1\01\clip_image002.jpg)

Logstash 一般当做indexer 和 broker。

Logstash 当做shipper则是自收自发的模式，**tpot standard****模式**

Logstash 只收，ssh定时传数据到制定

# flink

## 安装配置

* 最新稳定版：1.11.2

* [maven 依赖](https://flink.apache.org/zh/downloads.html)

  ```
  <dependency>
   <groupId>org.apache.flink</groupId>
   <artifactId>flink-java</artifactId>
   <version>1.11.2</version>
  </dependency>
  <dependency>
   <groupId>org.apache.flink</groupId>
   <artifactId>flink-streaming-java_2.11</artifactId>
   <version>1.11.2</version>
  </dependency>
  <dependency>
   <groupId>org.apache.flink</groupId>
   <artifactId>flink-clients_2.11</artifactId>
   <version>1.11.2</version>
  </dependency>
  ```

  




------

