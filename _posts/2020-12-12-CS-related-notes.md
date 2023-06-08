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

* 访问顺序示例：要访问www.baidu.com，首先向全球13个根服务器发起请求，询问com域名的地址，然后再向负责com域名的名称服务器发送请求，找到baidu.com，这样层层递归，最终找到我们需要的ip地址**】-----** **从右到左访问，. | .com | .baidu |**

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

* CDN(content Delivery Network): 让用户能够更快得到请求数据【下载加速】---**<u>简单的说，cdn就是用来加速的，它能让用户就近访问数据，这样就能更快的获取到数据。[电商本地仓]</u>**

  eg：服务器在北京，深圳的用户想要获取服务器上的数据就需要跨越较长距离，这显然比北京用户直接访问北京服务器延时更长。如果在**深圳建立一个CDN服务器，上面缓存一些数据**，深圳用户直接访问这个cdn服务器，如果服务器上有数据就直接返回，这样大大提升速度。因此很多运营商已经将CDN下沉到地市级，进一步减轻骨干网络压力。**[以存储换时延/带宽]**

* CDN 是构建在现有网络基础之上的虚拟网络，依靠部署各地的边缘服务器，通过中心平台的负载均衡，内容分发，调度等功能模块，使用户就近获取所需内容，降低网络拥塞，**关键技术主要有内容存储（缓存）和分发技术（发送数据到用户）。**

* 互联网服务提供商都有CDN服务提供，[参见](http://f5.pm/go-9564.html)

与 DNS 的关系：

* **基于CDN** **是就近访问的原则，如何知道用户所在位置，从而分配最佳CDN节点？**

   **基于 DNS服务来定位：** 当用户使用dns服务时，可根据使用的LDNS服务器来进行定位【当调度服务器看到他是来自深圳电信的LDNS服务器，则判断该用户来自深圳电信，则调度他取访问深圳电信的CDN服务器】**通过dns服务我们可以很快的定位到用户位置，然后分配最佳的cdn**节点。

* 存在的问题：北京联通的用户使用深圳电信的LDNS，调度服务器会分配深圳电信的CDN服务器----个人觉得不是一个问题，因为在实际情况当中，机器的位置是可以移动的。

  * 针对上述问题，还有另一种调度方式：https 调度。当用户访问服务器时，服务器先分析用户IP地址，然后服务器给用户返一个302重定向，将离用户最近的服务器存在location中，用户再去请求这个cdn服务器得到最佳CDN节点----- 【这就是我上面的理解，机器时可以被移动的。】的优点：定位更加准确，不会因为LDSN造成访问偏差，缺点时需要一次额外的https访问请求，较小的文件花费这个时间比较不划算。

  * 最佳方案时先进行CDN定位，再进行https 纠错。

工作过程

* 当用户请求一个文件时，CDN工作过程如下：
  * DNS 请求当地local DNS
  * 当地local DNS递归的查询服务器的gslb
  * 服务器根据local DNS 分配最佳节点，返回ip
  * 用户获得最佳接入ip，访问最佳节点
  * 若该节点没有用户想获取的内容，则通过内部路由访问上一节点，直到找到文件或到达源站。
  * 节点缓存该数据，下次请求该文件时可以直接返回。
* CDN使用缓存后的网站访问变化：
  * 用户向浏览器提供域名
  * 浏览器调用域名解析库对域名进行解析，解析函数库一般得到的是该域名对应的CNAME记录。为得到实际IP地址，需再次对获得的CNAME域名进行解析以得到实际的IP地址；此过程使用全局负载均衡DNS解析，根据地理位置信息解析对应的IP地址，使用户就近访问。
  * 解析得到CDN缓存服务器的IP地址后向缓存服务器发出访问请求；
  * 缓存服务器根据浏览器提供的域名，通过Cache内部专用DNS解析得到此域名的实际IP地址，再由缓存服务器向此实际IP地址提交访问请求；
  * 得到内容后，一方面本地保存，以备使用，二方面返回给客户端，完成数据服务。
  * 客户端得到由缓存服务器返回的数据以后显示出来并完成整个浏览的数据请求过程。

技术手段及网络架构

* 实现CDN的主要技术手段是**高速缓存，镜像服务器**。可工作于DNS解析，和HTTPS重定向两种方式，通过Cache服务器，或异地镜像站点完成内容传送与更新。
  * 基于DNS位置判断准确度在85%，基于HTTPS位置判断方式在99% 以上，但https需定位两次，对传输文件较小的情况，https 耗时可能出现较长的情况，因此，多采用两种方式混合。
  * 一般情况下，各Cacha服务器群用户访问流入数据量与Cache服务器到原始网站取内容的数据量在2：1-3：1之间，即分担50%-70% 到原始网站重复访问的数据量（图片，流媒体文件等内容）；对于镜像，除去数据同步的流量，其余均在本地完成，不访问原始服务器。
  * 镜像站点（mirror site）服务器是经常可以看到的，它让内容直截了当的分布，适用于静态和准动态数据同步。但购买和维护新服务器的费用较高，还必须在各地区设置镜像服务器，配置专业技术人员进行管理与维护。大型网站在随时更新各地服务器的同时，对带宽的需求也会显著增加，因此一般的互联网公司不会建立太多镜像服务器。
  * 高速缓存手段的成本较低，适用于静态内容。Internet统计表明，超过80%的用户通常访问20%的网站内容。在这情况下，缓存服务器可满足大部分客户请求，原始的www服务器只需要处理20%的非缓存请求和动态请求。于是，高速缓存手段大大加快了客户请求的响应时间，降低了原始WWW请求的服务器负载。
  * 根据美国IDC公司调查，缓存的市场正在以每年近100%的速度增长。
  * CDN网络架构主要分为两部分：中心和边缘，中心指CDN网管中心和DNS重定向解析中心，负责全局负载均衡，设备系统安装在管理中心机房；边缘主要指异地节点，CDN分发的载体，主要由Cache和负载均衡器组成。

## Anycast 单、多、广播




------

