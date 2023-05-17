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

# kafka

# Postman

# Nignx


------

