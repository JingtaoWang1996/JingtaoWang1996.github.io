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

## docker file 

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

* 

# kafka

# Postman

# Nignx


------

