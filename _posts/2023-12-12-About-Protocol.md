---
title: 'Network-Protocol‘
date: 2023-12-12
permalink: /posts/2023/12/Network-protocol/
tags:
  - Theoretical Ground
---

Network protocol note conclusion.

# 网络协议综述

* 协议三要素：语法（内容符合一定的规则和格式）、语义（内容有一定意义）、语序（执行的先后顺序）。

## 具体示例

**以电商购物为例**---常用的网络协议

* 应用层：DNS(找到访问ip地址)、http\https(传输访问内容：查询的信息or买多少等)
  * next：经过应用层封装后的内容交给下一层（传输层），通过socket编程实现。
* 传输层：UDP【无连接协议-只管发出1次，不管是否能够到达】，TCP【面向连接的协议-确保所发出的数据包能够到达，无法到达就重新发送】
  * TCP 协议一般监听两个端口：浏览器监听端口、电商服务监听端口。【通过端口判断收到的包下一步发送到哪个进程进行处理。】
  * next：传输层封装完毕后，浏览器将数据包交给操作系统的网络层。
* 网络层：IP协议。通过源ip和目的ip确定数据包的传输路径，进行数据传输。
  * 首先将ip地址发给网关：**通过ARP协议，确认gateway的MAC地址**
* MAC层：确定网关MAC后，将IP包交给MAC层，网卡再将包发出去。【因为包中包含MAC地址，因此能够到达网关】
  * 网关的实质-路由器：通过本身存储的路由表，判断这个包下一步应该发送到哪一个路由器，最终到达目的ip的网关，然后重复上述步骤解码提取得到传输的内容。
* 收包过程：通过路由表最终到达目标ip后，逐层解包得到传输内容。
  * TCP 层：对于收到的每个包，都会回复一个包收到的说明，沿着传输过来的路返回。【为了丢包重传的情况做准备，一定时间内没收到消息就重传-tcp的3次握手。】

**各层包封装示例如下**

| MAC头-MAC层       | 客户端电脑mac：xxxx，网关mac：xxxx                         |
| ----------------- | ---------------------------------------------------------- |
| IP头-网络层封装   | 客户端ip-源ip：192.168.1.101；电商服务器ip：106.114.138.24 |
| TCP头-传输层封装  | 浏览器端口：12345，电商应用端口：443                       |
| HTTP头-应用层封装 | POST,URL,HTTP 1.1，正文格式：json，正文长度：1234          |
| 内容              | 我要买xxx，买多少                                          |

## 网络分层

* 网络分层的原因：复杂的程序都要分层，每一层专注做本层的事情。
* 层与层之间的关系**：<u>只要在网络上跑的包，都是完整的，可以有下层没有上层，绝不可能有上层没有下层。（应用层可以没有，但只要想发送到网络上，ip层和MAC层一定有。）**</u>
* **二层设备**：<u>收进整个网络的包，各层协议都有。只去掉MAC头，看是丢弃、转发还是保留</u>。
* **三层设备**：<u>**MAC头去掉后，再把IP头摘掉**，确认是需要丢弃、转发，还是保留。</u>

## CIDR-无类型域间选路

解决前期前期积累IP分类不够用的情况：将**32位的IP地址一分为二-网络号+主机号**

* eg：10.100.122.2/24，这种表示形式即为CIDR。【24的意思，32位ip中，前24位是网络号，后8位是主机号】
* 伴随CIDR存在的两个地址：
  * **广播地址：** 10.100.122.255
  * **子网掩码：** 255.255.255.0
* 以10.100.122.2/24 为例，（子网掩码） AND （IP地址：10.100.122） = **网络号**（10.100.122.0）。












------
