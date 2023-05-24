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

# Postman

# Nignx


------

