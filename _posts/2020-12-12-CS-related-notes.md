---
title: 'CS-related-notes'
date: 2020-12-12
permalink: /posts/2020/12/CS-related-notes/
tags:
  - cool posts
  - category1
  - category2

---

CS related notes lists.

# 硬件相关

## 网线头颜色排列

* **标准T568A** **绿白、绿、橙白、蓝、蓝白、橙、白棕、棕**

* **T568B:** **绿白、橙、白橙、蓝、白蓝、绿、白棕、棕**

* **橙白、全橙、绿白、蓝、蓝白、绿、棕白、棕**

* 超五类和六类网线接法（T568B）：橙白、橙、绿白、蓝、蓝白、绿、棕白、棕

* 超五类和六类的水晶头不同，不能通用

* PC连接HUB: A端和B端都用标准568B接法：橙白、橙、绿白、蓝、蓝白、绿、棕白、棕

* PC连接PC: 1) A端：橙白、橙、绿白、蓝、蓝白、绿、棕白、棕 2)B端：绿白、绿、橙白、蓝、蓝白、橙、棕白、棕
* 口诀：鼻下铜上握水晶，从左到右记心中，橙白全橙绿白蓝，蓝白全绿棕白棕

## X86 & ARM 架构区别

* CPU 从最基本的逻辑角度来分类：复杂指令集CISC、精简指令集RISC,[参考](https://blog.csdn.net/jmppok/article/details/17121515?utm_source=blogxgwz4)
  * 复杂指令集CISC：直接下达“复杂”命令；
  * 精简指令集RISC：拆分复杂命令成为基本命令执行
  * CISC:高密度运算任务；RISC：简单重复劳动
* ARM: advanced RISC machine
* 两者区别--- X86: 高性能，高功耗； ARM: 小尺寸、低功耗

# 网络相关

## 交换机配置

* 以huawei交换机为例，在PC上将ip配置到同一网段后按照说明书quick start 进行处理。

## windows 系统配多个ip及删除

* 网络->更改适配器选项->以太网->属性->Internet 协议版本4（选中后属性）->高级->添加->增加合适的对应网段后一路确定or关闭即可。

## 虚拟机网络搭建-vmware

* vmware 虚拟网络指通过vmware 虚拟技术生成的网络，组成：虚拟主机、虚拟交换机、虚拟网桥、虚拟NAT设备、虚拟DHCP服务器、虚拟网卡。可以根据需要创建虚拟交换机（最多10个），将多个虚拟机连接到统一虚拟交换机上。

打开vmware虚拟机，在菜单栏“编辑”下的“虚拟网络编辑器”中会看到VMnet0（桥接模式下的虚拟交换机）、VMnet1（仅主机模式下的虚拟交换机）、VMnet8（NAT模式下的虚拟交换机）。

主机上对应有VMware Network Adapter Vmnet1 和 VMnet8 两块虚拟网卡，分别作用于“仅主机”和NAT模式下。【控制面板->网络和Internet->网络连接】

PS: 在网络连接中，可以看到这两块虚拟网卡，如果将这两块卸载了，可以在vmware“编辑”下的“虚拟网络编辑器” 中点击“还原默认设置”，重新将虚拟网卡还原。

vmware提供的[三种工作模式](https://blog.csdn.net/weixin_42442713/article/details/80903173)

* 桥接: 将主机网卡与虚拟机网卡利用虚拟网桥进行通信。

  * 在**桥接作用下，类似于把物理主机虚拟为一个交换机**，所有桥**接设置的虚拟机连接到这个交换机的一个接口上**。物理主机同样也插在交换机上，所以所有桥接下的网卡与网卡都是交换模式的，相互可以访问而互不干扰。

  * **虚拟机ip必须和主机在同一网段且子网掩码、网关DNS也需要与主机网卡一致**。

  * cmd->ifconfig 确定系统：主机ip、默认网关、子网掩码等信息。设置完成后，使用ping命令ping外网ip，能ping通则桥接模式设置成功。

    PS: 若网络环境IP资源很少或对IP管理比较严格的话，那么桥接模式就不太适用。

* NAT（网络地址转换模式）：IP 资源紧缺，但希望虚拟机联网

  * 借助虚拟NAT设备和虚拟DHCP服务器，使得虚拟机可以联网。
  * 根据主机上查询到的信息对参数进行设置。

* HostOnly（仅主机模式）:

  * 为NAT模式去除了虚拟的NAT设备，然后使用VMware Network Adapter VMnet1虚拟网卡连接VMnet1虚拟交换机来与虚拟机通信的，**Host-Only模式将虚拟机与外网隔开**，使得虚拟机成为一个独立的系统，只与主机相互通讯。
  * 如果要使得虚拟机能联网，我们可以将主机网卡共享给VMware Network Adapter VMnet1网卡，从而达到虚拟机联网的目的。

虚拟机连外网的配置：

* 无线网络连接（右键“属性”）->点击"共享"，选择“VMWARE NETWORK Adapter VMnet1"

* Vmware station10：编辑->虚拟网络编辑器->添加网络->确定->选择对应的VMNET信息

PS: 类型是“仅主机”的应该直接就是虚拟交换机

# IO 模型

* 4种常见IO模型：同步IO (synchronous)、异步IO(asynchronous)、阻塞（blocking）、非阻塞IO（同步 ≈ 阻塞，异步≈非阻塞）

以linux 下 network IO(read 操作)，调用系统内核为例（step1：等待数据准备；step2：数据从kernel拷到process当中）

## Blocking IO

* linux当中，默认情况所有的socket都是blocking的。
* 典型的读操作流程：用户调用recvfrom，kernel就开始IO第一个阶段：准备数据。对于network IO来说，很多数据一开始还没有到达（比如：还没有收到一个完整的UDP包），这时候kernel就要等待足够的数据到来，在用户进程这边，整个进程会被阻塞。当kernel数据准备好之后，它就会将数据从kernel拷贝到用户内存，然后kernel返回结果，用户进程才解除blocking状态，所以blocking的特点就是在IO的两个阶段都被block了。 

## Non-blocking IO

* 可以通过设置socket，将其变成non-blocking socket 执行读操作。

* 用户发出read 操作时，若数据没准备好，那么socket不会block进程，而是立即返回一个error（invalid state）。当返回error时，用户就知道数据未准备完，可以再次发送read操作。一旦kernel数据准备好了，并且又再次收到了用户进程的system call，就立即将数据拷贝到用户内存，然后返回。【用户进程需要不断主动询问kernel当中数据是否准备好了。】

* 网络IO的时，非阻塞IO也会进行recvfrom调用，检查数据是否准备好，非阻塞将大的整片时间的阻塞分成N多的小阻塞，所以进程不断有机会被CPU光顾，循环重复上述过程，直到得到数据，在这个过程当中，整个数据还是轮询重复的。
* 数据拷贝阶段，进程仍然是出于阻塞状态

## Asynchronous IO

* 用户进程发起read操作后，立刻开始去做其他的事情。从kernel角度，当它收到一个异步IP读取时，首先它会立刻返回，不会对用户进程产生任何block，然后kernel等待数据准备完成后将数据拷贝到用户内存，当这一切都完成之后，kernel会给进程发送一个signal，告诉它read操作完成。
* 异步 I/O 模型的发展技术是： select -> poll -> epoll -> aio -> libevent -> libuv。
* 异步编程当中：无法使用返回码/抛异常（主进程开子进程，返回码/异常在子进程当中），有必要的话通过函数往回回调返回码和抛异常。

## IO multiplexing --- 同步IO

* event driven IO,[select、epoll] 的好处在于单个process 就可以同时处理多个网络连接的IO。
* 基本原理：通过select 和 epoll **不断轮询**所有socket，当某个socket数据到达，通知用户进程。

* 用户进程调用select，整个进程会被阻塞，kernel监视所有select负责的socket，任何一个socket数据准备好了，select就会返回，此时用户进程再调用read操作，将数据kernel拷贝到用户进程。

* 相比阻塞IO，多路复用的问题存在需要使用两个系统调用的情况（多一个select socket的调用），select的好处在于可以同时处理多个connection【当处理的连接数不是很高的话，使用select和epoll的webserver不一定比multithreading +blocking IO的web server性能好，可能延迟更大】

* 在多路复用的IO模型当中，对于每一个socket，一般都设置为non-blocking 

# DNS 相关

## 服务器搭建

* centos 搭建DNS解析服务器(使用named-ckeckconf -z 命令无输出则无错误),[参考](https://blog.csdn.net/qq_40707090/article/details/123561997)
* DNS服务器是否支持DOH测试命令：curl -H 'accept: application/dns-json' 'https://rubyfish.cn/dns-query?name=www.google.com&type=A

### 虚拟机搭建bind服务器

[ref1](https://blog.csdn.net/liang12360640/article/details/45219637),[ref2](https://www.jb51.net/article/33941.htm)

* 基本环境级网络配置：VMware+Ubuntu20.04

* bind9 安装：su root ->apt-get install bind9

* 配置虚拟机网络vmware：

  * 编辑->虚拟网络编辑器 ->修改“桥接模式（将虚拟机直接连接到外网）”【已桥接至后面的“自动” 修改为的Intel ethernet connection，连接网卡】

  * 修改ipv4地址（ubuntu可以通过界面-wired settings-wired 修改ipv4地址、网关、掩码）

    PS: 网关和掩码可以cmd运行“ipconfig/all”获取；

    PPS: ip自动获取需要从DHCP修改为manual

* 创建DNS根区文件：

  * vim /etc/named.conf(添加域名sword.cn 正向解析区域，见图中"Zone定义部分")

    <img src='/images/img/DNS1.png'>

    PS:这样添加文件应在 /etc/bind/下面，若写明/var/named/xx 文件会在/var/named/下面

  * named-checkconf命令：检查预防是否正确

  * rndc-confgen> /etc/rndc.conf

  * mkdir /var/named

  * 创建对应域名的根区文件

    <img src='/images/img/DNS2.png'>

    PS: 必须按章上述格式完全一致来，最后两行先写NS记录，再写其他记录

    Named-checkzone 192.168.1.sword /var/named/192.168.1.sword (不一定需要)

* 开启服务：service named start or named -u cetc21

* 更改DNS区文件(/etc/bind 下面的sword.cn文件)后重启服务：rndc reload

* 使用dig命令进行验证: 确保测试机和虚拟机之间能够直接ping通

## dig 命令

[参考1]( [https://ww w.jianshu.com/p/18359188f3e4](https://www.jianshu.com/p/18359188f3e4)),[参考2](https://www.cnblogs.com/ginvip/p/6365605.html)

### 常见记录

* A：域名的ipv4地址
* AAAA: 域名的ipv6地址
* CNAME: 域名存在的别名
* NS: 域名服务器记录

### 使用示例

* 命令格式：dig 域名 要查询记录类型 @服务器ip  【dig -6 域名 类型@目标服务器ipv6】

* 若不指定目标服务器ip，则依次从 /etc/resolv.conf里选择nameserver 作为DNS目标服务器。

  **ps：若dig不通，除了联网排查外，还需要考虑 /etc/resolv.conf 是否缺少解析服务器**

  **pps：若代码修改 /etc/resolv.conf 后出现dig无法解析的情况，可能原因是最后缺少一个空格。**

* 结果说明（重点关注）

  * rcode: status  NOERROR---查询结果正常返回。
  * Answer/Authority/Additional section: 返回的解析结果
  * querytime：解析时间
  * server：目标服务器ip

* 命令格式中加入：+short,则只显示制定域名的解析结果，不包含其他信息【dig +short 域名】

* 跟踪整个查询过程加入：+trace,显示整个查询过程

* 反查ip对应的域名：dig -x 8.8.8.8 +short

* 仅查某section：dig qq.com +nocomments +noquestion +noauthority +noadditional +nostats

## CDN & DNS




------

