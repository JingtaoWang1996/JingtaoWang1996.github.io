---
title: 'CS-related'
date: 2020-12-12
permalink: /posts/2020/12/CS-related-notes/
tags:
  - Technical Refer notes
---

CS related notes lists.

# Windows Tricks

## 快速删除.txt的上万行

* 光标放在要删除部分的结尾位置。
* 拖动右侧上下滑动条到要删除的开头位置。
* 按住shift后鼠标点击要删除开头位置。【此时要删除部分已全部变为蓝色】
* 删除后保存即可。

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

## 忘记密码的情况

* [通过console 口重置密码](https://baijiahao.baidu.com/s?id=1786808074819409427&wfr=spider&for=pc)

  * COM口，通过moba-session-series-COM---设置9600波特率。

  * **在BootROM/BootLoad下配置清除Console口密码启动后，修改Console口密码**
    如果您记得BootROM/BootLoad菜单密码，能正常进入BootROM/BootLoad菜单，则可以通过BootROM/BootLoad菜单清除Console口登录密码，并在交换机重新启动后设置新的Console口登录密码，然后保存配置（因涉及重启设备，会中断当前业务，请在业务允许的情况下操作，且设备启动过程中不要对设备进行下电操作）。请按照如下步骤进行配置：

    * 准备一根Console线缆并通过设备的Console口连接交换机，连接成功后重启交换机（Console登录设备方法请参考[S交换机如何通过Console口登录](https://app.huawei.com/weiknow#)）。

    * 当界面出现以下打印信息时，及时按下快捷键“**Ctrl+B**”或“**Ctrl+E**”并输入BootROM密码，进入BootROM主菜单。
      * S系列框式交换机打印信息： 
        Press Ctrl+B to enter boot menu ... 1 
        Password: //输入BootROM密码
        E系列和S系列盒式交换机打印信息： 
        Press Ctrl+B or Ctrl+E to enter BootROM menu ... 2 
        password: //输入BootROM密码 

    * 在BootROM/BootLoad主菜单下选择“**Clear password for console user**”清除Console口登录密码。

    * 根据交换机的提示，在BootROM/BootLoad主菜单下选择“**Boot with default mode**”启动设备（此处不要选择“**Reboot**”选项，否则此次清除密码将失效）。 
    * 完成系统启动后，通过Console口登录时不需要认证，登录后按照系统提示配置验证密码（V200R009及之后版本，完成系统启动后，通过Console口登录时认证方式为None，系统启动后不会提示配置验证密码 ）。

    * 登录交换机后，用户可以根据需要配置Console用户界面的认证方式及密码。修改Console口登录的密码请参考方法一的步骤2。

    * 为了防止重启后配置丢失，保存配置。

      <HUAWEI> **save**

    ​       The current configuration will be written to the device.

    ​       Are you sure to continue?[Y/N] **y**

    ​       Now saving the current configuration to the slot 0.

    ​       Save the configuration successfully.

* [ref2-配置http](https://www.cnblogs.com/fyy-hhzzj/p/7810542.html)

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

## 心跳机制

* 心跳包：定时发送一个自定义结构体（心跳包），让对方知道自己还活着，以**确保连接有效性。**
* TCP 已经实现了可设置参数的心跳机制，如果设置了心跳，那么TCP就会在一定时间内发送你设置次数的心跳，并且此信息不会影响你自己定义的协议。

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

### DOH&DOT

#### DOH&DOT&DNSSEC服务器搭建

DOH 服务器安装，[ref1](https://blog.csdn.net/qq_39378221/article/details/103245108),[ref2](https://www.aaflalo.me/2018/10/tutorial-setup-dns-over-https-server/)

* ubuntu20.04 +dnscrypt安装

  * sudo add-apt-repository ppa:shevchuk/dnscrypt-proxy
  * apt-get update & sudo apt install dnscrypt-proxy

* 安装成功后会出现：/etc/dnscrypt-proxy,显示监听地址：127.0.0.53:53

* vim /etc/dnscrypt-proxy/dnscrypt-proxy.toml 文件的server_name字段：**server_names = ['cloudflare']**

* 重启dnscrypt-proxy服务：sudo systemctl restart dnscrypt-proxy

* DOH服务器包[下载链接](https://pan.baidu.com/s/1au3-AbPOcMo6wqyyVqeZJg):密码fgnl，下载号之后，执行：dpkg -i doh-server\_*_amd64.deb

* cd  /etc/dns-over-https/doh-server.conf 修改参数：

  ```
  listen = ["127.0.0.1:8053"]
  upstream = ["127.0.0.53:53"] //dns-proxy监听地址
  ```

* 修改完成后重启doh服务：sudo systemctl restart doh-server

nignx安装（反向代理服务器，将收到的https请求解码并发送到doh-server上）

* 安装 nginx：add-apt-repository ppa:ondrej/nginx

* apt-get update & apt install nginx-full
* 配置 nginx：sudo add-apt-repository ppa:ondrej/nginx  & sudo apt install nginx-full

* 将如下内容放入 /etc/nginx/sites-available/dns-over-https

```
upstream dns-backend {
server 127.0.0.1:8053;
}

server {
listen 80;
server_name dns.example.com;
root /var/www/html/dns;
access_log /var/log/nginx/dns.access.log;
location /dns-query {
proxy_set_header X-Real-IP **$remote_addr**;
proxy_set_header X-Forwarded-**For** **$proxy_add_x_forwarded_for**;
proxy_set_header Host **$http_host**;
proxy_set_header X-NginX-Proxy true;
proxy_http_version 1.1;
proxy_set_header Upgrade **$http_upgrade**;
proxy_redirect off;
proxy_set_header X-Forwarded-Proto **$scheme**;
proxy_read_timeout 86400;
proxy_pass http://dns-backend/dns-query ;
}

}
```



#### 判断服务器是否支持DoT, DoH

* DNS over TLS：基于TLS进行报文加密的DNS请求，侧重于DNS交互报文的加密性。

* 判断依据：（端口直接搜到）

  * DOH:是否通过RFC8484制定的经过TLS 加密的http 链接提供DNS解析。

  * DOT:是否通过RFC7858制定的经过TLS 加密的TCP 连接提供DNS解析。

  * [阿里云公共DNS](https://developer.aliyun.com/article/757592)

  * 使用Zmap 或Nmap 扫描网络端口后，找到853开放的服务器，向他们发送DoT,能够从853端口正常返回值，则表示该服务器支持DoT

  * DOT: DNSserver 能在默认853端口监听和接收TCP 连接，能够从853端口接收TCP 连接的默认为支持DOT。[若使用853以外的端口，需要在DOT client 中增加设定，默认使用853端口]。

    3) DOH：443 端口同时和HTTPS 数据流访问共享，单独定位解析相对困难，通过当前已知的模板扫描全网所有的URL得到服务器是否支持DOH。

#### 判断DNS服务器是否支持随机化端口号、DNSSEC、TXID、0X20

从端口号、transaction ID、域名上增加随机过程提高DNS缓存中毒过程中猜测的难度。

* [随机化端口号1](https://mohen.blog.csdn.net/article/details/110558422)、[随机化端口号2](https://zhuanlan.zhihu.com/p/92899876?utm_source=wechat_session)：微软提出的基于2008年卡明斯基发现的DNS漏洞的缓解方案。DNS服务每次通信时都在1024-65536端口号中随机选一个和对方建立通信连接（端口号，QueryID，域名同时匹配才接收对方的消息，增加攻击信息加塞的猜测难度---攻击信息必须赶在真实信息返回之前猜对端口号、QueryID进行加塞【请求有顺序，域名可以直接从问题中得到，故实际需要猜测的仅仅是端口号】。攻击信息加塞成功后，原本真实的信息就会被抛弃。）
  * 测信道攻击(side-channel attack)：利用主信道传输加密信息以外的透露出的其他情况（功耗、声音、热量、辐射等等）来得到主信道当中可能存在的敏感信息。
  * Conclusion: 随机化端口号和其他基于随机化的防御措施主要用抵抗缓存信息加塞带来的缓存污染问题，只要保证加塞的攻击信息在真实信息之后返回即可视为防御成功。

* TXID(transaction ID) :[随机化产生TXID保证DNS信息和请求的安全](https://msrc-blog.microsoft.com/2008/04/09/ms08-020-how-predictable-is-the-dns-transaction-id/):16bit entity primarily used as a synchronization mechanism between DNS servers and client. (Can be consider as an intial Sequence number for DNS query/ response exchange. )
  * TXID:通过算法随机生成来增加TXID猜测难度，防止DNS的入侵和破坏。
  * 随机生成TXID的算法主要是PRNG算法生成，但攻击者可以根据连续的状态估计后面的TXID（上面的10001，10002后面就是10003，10004）
  *  PRNG 算法----可以看出TXID大概率可估计（或至少可以大概率缩小真实TXID搜索空间,同时发送几千个不同TXID的DNS反馈，很大概率能够直接猜中。）

* 0X20 encoding(Georiga Tech ccs 2008)-----随机大小写域名: DNS-0X20是一种未被标准化的防伪机制。基于本身存在的transaction ID 容易被猜测伪造的情况下考虑：将DNS请求包中的域名随机大小写，加上DNS server 需要遵守RFC1034规范，按照回应的域名需要按照请求的域名原样返回，增大了DNS缓存投毒难度。【攻击者如果想记录发出去的包中域名是大写还是小写就需要一致维持一个session】在ASCII码表中，大写字母从0X41开始，小写字母从0X61开始，刚好相差OX20.
* Google 在构建public server（8.8.8.8）时，仅仅将在白名单中的DNSserver使用0X20 encoding，即使在这样的情况下，这样的请求也占了近70%[参考](https://developers.google.com/speed/public-dns/docs/security)
* DNScookie----RFC7873[ref](https://kb.isc.org/docs/aa-01387)：DNS cookie is an extended DNS option. It allows the client to detect and ignore off-path spoofed responsed, and the server to determine that a client’s address is not spoofed.

* DNSSEC（domain name system security extensions）:用于验证对域名查找的相应，不会为这些查找提供隐私保护，但会阻止攻击者操控对DNS请求的相应或在该响应中投毒。【在DNS请求过程的各个阶段信息中增加一段信息用于验证，并在整段DNS请求过程中】

## dig 命令

[参考1]( [https://ww w.jianshu.com/p/18359188f3e4](https://www.jianshu.com/p/18359188f3e4)),[参考2](https://www.cnblogs.com/ginvip/p/6365605.html)

dig 命令调试网络情况：dig **-debug** baidu.com

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

## IPV4/IPV6 安全性能分析

* 地址范围：ipv4-2^32; ipv6 -2^128,相较而言ipv6更难获取。
* 协议安全方面：
  * ipv4：未对地址字段提供任何保护及验证手段，因此ipv4地址可以被修改（IP地址欺骗）
  * ipv6 ：提供安全认证方式-主要有是三个基本部分组成： AH—Authentication Header 协议（分组头认证协议，提供信息源的身份认证，以及数据完整性测试----只涉及认证，不包括加密）；ESP---Encapsulating Secure Payload封装安全有效净核协议（为IP层提供加密保护及数据源身份认证，AH 只提供认证，ESP包含加密）；IKE（internet key exchange protocol） 用于约定加密算法密钥等等。
* 数据源认证：ipv4无法对数据源进行认证，无法判断IP包在传输过程中，该报文在链路上是否被劫持或更换。
* TCP序列号欺骗：由于传输层TCP序列号可预测，因此攻击者可以构造一个TCP报文序列，对网络中某个可通信节点进行攻击。   
* ipv6在安全方面的优势：主要采用安全IP(IPSec)

# Anycast 、单、多、广播

## 单播Unicast

* **封包在计算机网络的传输过程中，目的地址为单一目标的一种传输方式**。每次只有两个实体相互通信，发送端和接收端都是唯一确定的。是应用最为广泛，通常所使用的网络协议或服务大多采用单播传输，例如一切基于 TCP 的协议。

* 单播地址：在 IPv4 网络中，0.0.0.0 到 223.255.255.255 属于单播地址。

* 优点：服务器及时响应客户机请求； 针对客户不同请求发送不同的数据，易实现个性化服务。

* 缺点：

  * 服务器针对每个客户机发送数据流，服务器流量＝客户机数量×客户机流量。在客户数量大、每个客户机流量大的流媒体应用中服务器不堪重负。

  * 金字塔结构带宽，城际省际主干带宽仅仅相当于所有用户带宽之和的 5％。如全使用单播协议，将造成网络主干不堪重负。现在的 P2P 应用就已经使主干经常阻塞，只要有 5％ 的客户在全速使用网络，其它用户网速将严重受损，而主干网络带宽在短时间内扩展 20 倍不可能。

## 多播Multicast

* **把信息同时传递给一组目的地址。**
* 优点：使用策略高效（消息在每条网络链路上只需传递一次，只有链路分叉时，消息才会被复制。）
* 地址：多播组可以是永久的也可以是临时的。多播组地址中，有一部分由官方分配的 **永久多播组**（ IP 地址保持不变，组中的成员构成可以变化-数量任意，也可以为0。）
  * 没有保留下来供永久组播组使用的 IP 多播地址，可以被临时多播组利用。
  * 以太网传输单播 IP 报文的时候，目的 MAC 地址使用的是接收者的 MAC 地址。在传输多播报文时，传输目的不再是一个具体的接收者，而是一个成员不确定的组。所以使用的是多播 MAC 地址。多播 MAC 地址和多播 IP 地址对应的。IANA 规定，多播 MAC 地址的高 24 位为 0x01005e，低 23 位的 MAC 地址为多播 IP 地址的低 23 位。由于 IP 多播地址的后 28 位中只有 23 位被映射到 MAC 地址，这样就会有 32 个 IP多播地址映射到同一 MAC 地址上。
* 多播地址分配
  * 224.0.0.0-224.0.0.255 为预留多播地址（永久组）
  * 224.0.1.0-224.0.1.255公用多播地址
  * 224.0.2.0-238.255.255.255为临时组地址，全网范围有效
  * 239.0.0.0-239.255.255.255 为本地管理组多播，仅特定本地范围内有效。
* 优点：
  * 需相同数据流的客户端加入相同的组共享一条数据流，节省了服务器的负载。
  * 多播协议根据接受者的需要对数据流进行复制转发，因此服务端的服务总带宽不受客户接入端带宽的限制。IP 协议允许有 2 亿 6 千多万个（268435456）组播，其提供的服务可以非常丰富）此协议和单播协议一样允许在 Internet 宽带网上传输。
* 缺点：
  * 与单播相比，没有纠错机制，发生丢包错包后难以弥补，但可通过容错机制和QoS加以弥补。
  * 需要相同数据流的客户端加入相同的组共享一条数据流，节省了服务器的负载。

## 广播

* **封包在计算机网络中传输时，目的地址为网络中所有设备**的传输方式。（所有设备也限定在一个范围之中，称为广播域)
* 并非所有计算机网络都支持广播，例如 X.25 网络和帧中继都不支持广播，而且也没有在整个互联网范围中的广播。IPv6 亦不支持广播，广播相应的功能由多播代替。
* 地址：以太网和 IPv4 网都用全 1 的地址表示广播，分别是 ff:ff:ff:ff:ff:ff 和 255.255.255.255
* 优点：设备简单，成本较低；服务器流量负载极低。
* 缺点：
  * 允许服务器提供数据的带宽有限，客户端最大带宽＝服务总带宽。(有线电视客户端线路支持 100 个频道（如果采用数字压缩技术，理论上可以提供 500 个频道），即使服务商有更大的财力配置更多的发送设备、改成光纤主干，也无法超过此极限。)
  * 禁止在Internet宽带网上传输。
  * 无法提供个性化服务。

## 任播 Anycast

* RFC1546中提出，从IPV4单独分一块任播地址。一种无状态，尽力而为的服务。

* 实际应用中，任播是一种网络寻址和路由的策略。采用将一个单播地址分配到处于 Internet 中多个不同物理位置的主机上，发送到这个主机的报文被路由到路由协议度量最近的目标主机上。
* 优点：负载均衡，防止DDos攻击，提高响应速度。
* **AnyCast DNS**：一个IP地址可以应用于多个服务器，AnycastDNS 意味着一组DNS服务器中的任何一台都可以响应对这一个组IP发起的DNS查询。通常由地理位置最近的一台提供响应，减少延迟，提高DNS解析服务正常运行时间。
* 允许多台服务器使用相同的ip或一组IP地址

# Whois 

* whois 信息[在线验证网站](https://whois.chinaz.com/)
* 定义：用来查询域名IP以及所有者等信息的传输协议。 
* 主要关注：域名是否已被注册？如已注册，注册域名详细信息：域名所有人、域名注册商等信息。
* 通常使用TCP协议的43端口，每个域名/IP的whois信息由对应的管理机构保(whois.parse.WhoisCN 管cn. 的域名和IP信息）

- 不同域名后缀的whois信息需要到不同whois数据库查询。（com 结尾的域名whois信息由verisign管理、中国国家顶级域名cn. 由cnnic管理）
- 目前国内提供WHOIS查询服务的网站：万网、站长之家

* whois 系统组成:client + server 系统
  * client ：提供访问系统的接口、生成查询并传给server、接收传回的响应并以可读形式输出。
  * server：接收client端请求并发回响应数据，默认43端口监听TCP数据。一般来说可以接受3种类型的信息查询：联系人、IP、域名。对同一查询，server端输出应该具有一致性和稳定性。

* whois 工作过程：server监听43端口，当用户搜索上述三种信息之一时，server建立一个与client的TCP链接，然后接收用户请求的信息并根据此信息查询后台域名数据库，如果存在响应的记录，将相关信息：反馈给client。Server输出完毕后，client关闭链接，一个查询过程结束。

* python 获取whois 数据

  * [python-whois库](https://pypi.org/project/python-whois/),[使用示例]([https://github.com/relip/pythonwhois#:~:text=python%20To%20get%20whois%20data%20of%20example.com%2C%20import,contains%20whois%20server%20address%20and%20the%20whois%20data](https://github.com/relip/pythonwhois#:~:text=python To get whois data of example.com%2C import,contains whois server address and the whois data).)

    ```python
    import whois
    print(whois.whois("baidu.com"))
    ```

  * 使用python-whois库，已经验证：com\net\org\cn\uk\cc\hk 均能正常查询到whois数据。

    PS: com\net\ 以 qq.com 和 qq.net. 为例，需要在海外服务器上才能够正常查询值，国内服务器，无法拿到这两个的值，已经在硅谷的机器上得到验证。

# BGP

* [边界网关协议](https://blog.csdn.net/qq_34307082/article/details/102519468)（boundary gateway protocol）: 互联网上最广泛的域间路由协议，主要功能是在自治系统之间交换可达信息。
* 传输层协议：TCP    &      服务端口：179
* BGP 数据的理解：将广域网抽象成一个城市，其中包含的城域网抽象成城市中的小区：
  * 小区中的每栋楼象征着一个个局域网，他们之间的路由信息由小区物业统一管理，要去哪一栋楼，只需要查物业的路由表就行。
  * 现在这个小区旁边又来一个新小区，结构与老小区相同，因此小区内部访问没有问题。两个小区互相访问，则需要通过两个小区物业互相分享一下路由表即可。
  * 随着新小区的越来越多，**互相分享路由表**即为BGP协议的工作原理。
* 三个表：
  * 路由表：存放本网络中的路由信息表
  * 邻居表：保存所有BGP邻居的信息
  * BGP表：保存从每个邻居学到的路由信息

## 扫描&报文&识别解析

* 报文类型及对应的意义
  * open 报文：用于建立BGP的对等连接。
  * update报文：用于在对等体之间交换路由信息。
  * Notification 报文：中断BGP连接。
  * keepalive 报文：保持bgp连接。
  * Route-refresh：改变路由策略后请求对等体重新发送路由信息
* 扫描请求包：**无论什么请求包都可以得到BGP服务器响应包，且响应信息可解析。**
* 扫描响应包：WIRESHARK抓包后能够明显看出，不同的报文（只有OPEN、只有Notification、Open+Notification）

识别及解析

* 得到BGP服务器的响应信息之后发现，BGP协议的响应报文中有Maker位，32个F, 16对ff（即“ffffffffffffffffffffffffffffffff”），可以通过下表识别相应信息中是否以此开头，对BGP协议进行识别。识别位后第三个16进制数表示响应类型（wireshark抓包）：

  | 十六进制数 | 响应类型      |
  | ---------- | ------------- |
  | 01         | OPEN          |
  | 02         | Update        |
  | 03         | Notification  |
  | 04         | Keepalive     |
  | 05         | Route_refresh |
  | 06         | capabilit     |

* Open 类型（建立对等连接）

  * 以下位数表示以标志位阶数为开始进行计数
    * 1，2 位表示响应信息长度
    * 3位表示相应的类型
    * 4 位表示BGP协议版本
    * 5，6 位表示AS编号
    * 7，8 位表示连接时间
    * 9-12 位表示BGP识别码：

* Notification 类型（中断连接）

  * 以下位数表示以标志位阶数为开始进行计数
    * 1，2 位表示响应信息长度
    * 3位表示相应的类型
    * 4 位表示主要错误识别码【具体识别码查询当前的标准定义】
    * 5为表示辅助错误识别码【具体识别码查询当前的标准定义】

* AS路径：每个AS通过BGP更新消息向其它AS通告到其本地前缀的路由和从其邻居学习得到优选路由，这样的消息提供了关于如何通过有序AS跳数的列表来达到目的地的信息，称为AS路径。

## 可达性信息

* BGP路由器在路由信息库(RIP) 中维护可达性信息，这些可达性信息存放在3个集合当中：
  * Adj-RIBs-In: 从邻居AS的入站更新消息中学习得到的路由信息；
  * Loc-RIB: 通过应用本地策略（例如，最短路径、与邻居的对等关系）从Adj-RIB-In中选择的路由；路由器将路由信息存放到路由表中以确定在哪里转发分组。
  * Adj-RIBs-Out：从Loc-RIB中选择的路由，路由器将向其邻居通告这些路由；对于每个邻居，路由器基于本地策略（例如，对等关系）创建特定的Adj-RIB-Out。

## 数据采集-looking glass 命令

* 一些运营商收集其路由器上生成的BGP路由信息，用于监视、故障排除和研究的目的。
* BGP的looking glass 给用户有限的权限例如，只读:来访问一个路由器的命令行接口，或允许用户下载路由器的当前状态的ASCII码格式的输出。
* Looking glass 是一个交互式探索，而非系统和连续的数据采集。**数据采集可以通过：**
  * 使用分布式系统（路由收集器）与被监控路由器建立BGP对等会话来实现
  * 通过专门为监控目的设计的协议，例如OpenBMP(IETF草案中定义的BGP监控协议的开源实现，支持JunOS和Cisco IOS的最新版本)。该协议允许用户周期性地访问路由器中的Adj-RIBs-In，或者监视其BGP对等会话。虽然OpenBMP可以很容易地部署在AS中以监视其BGP路由器，但是**目前还没有项目公开这些数据，但路由收集器通常用于此目的。
* 一个BGP数据搜集器和一个Vantage Points建立一个session,保持运行状态并接收新路由信息。
* 通常与收集器的BGP会话会被配置维客户-提供者的关系，即好像探测点正在向收集器提供传输服务。在这种情况下，探测点被称为全馈送，因为它将向收集器通告Adj-RIB out（出口路由信息）该Adj-RIB-Out包含其Loc-RIB中的整个路由集。通过这种方式，**收集器在每个瞬间都知道探测点将用于到达因特网其余部分的所有首选路由**-该路由器可见的因特网拓扑图的部分视图。
* 相反，部分馈送探测点将通过其Adj-RIB-Out仅提供其Loc-RIB中的路由的子集，例如，到其自身网络的路由或通过其客户学习的路由。不幸的是，公开提供收集者所获取信息的项目没有将探测点标记为完全或部分馈送，因为与收集者的对等通常是在自愿的基础上建立的，并且探测点行为可以不经通知而改变。因此，必须从数据（例如，Adj-RIB-Out的大小）动态地推断确定与收集器共享的Adj-RIB-Out的策略。

## 常用数据源

* [Routeviews](http://www.routeviews.org/routeviews/)：18个收集器，分布在全世界，共380个探测点，数字每年增加，每2小时保存一个RIB dump，每15分钟保存一个Updates dump。以IETF标准化的二进制格式保存RIB dump和Updates dump，称为多线程路由工具包（MRT）路由信息导出格式。档案可以追溯到2001年使得纵向研究能够理解互联网基础设施的演变及其在其他领域的影响。
* RIPE RIS: 13个收集器，分布在全世界，共600个探测点，数字每年增加，每8小时保存一个RIB dump，每5分钟保存一个Updates dump。以IETF标准化的二进制格式保存RIB dump和Updates dump，称为多线程路由工具包（MRT）路由信息导出格式。档案可追溯到1999年，使得纵向研究能够理解互联网基础设施的演变及其在其他领域的影响。

* 分析来自多个探测点的数据对于大多数互联网研究来说是非常重要的。因为每个路由器对互联网拓扑结构都有有限的视角，即使当完全馈送时，探测点也只是共享部分信息（首选路由）。此外，通过路由基础设施可见的宏观互联网现象（例如：停机、网络攻击、对等关系、性能问题、路由泄露、路由漏洞）等根据地理、拓扑、路由操作系统影响路由器。这种分布式和详细的路由平面部分视图，也会产生大量的数据，仅2015年就超过2TB.

## 两台本地虚拟机搭建BGP测试环境

Station1: R1:10.38.2.252  Station2：R1:10.38.2.251

Step1：两台虚拟机网络配置见：DNS相关->服务器搭建

Step2：vmware 搭建虚拟化网络 见：虚拟网络搭建

Step3: 建立BGP 拓扑图

Step4: python 抓TCP包

# 蜜罐

* [DNS 协议蜜罐]()(https://github.com/jekil/UDPot)

* 根据需要确定是否要配置DNS服务器

* 网卡重定向命令：

  ```
  iptables -t nat -A PREROUTING -i 网卡名 -p tcp --dport 53 -j REDIRECT --to-ports 5053
  ```

# 服务状态

* 状态：保留程序的一些数据或上下文。
* 有状态服务：数据本地化，读写延迟降低; 更高可用性和一致性; 客户端的请求落在同一个实例上。
  * 有状态服务的自动化伸缩实例：Fb:Scuba内存数据库；Uber：Ringpop Node.js的根据地理位置分片路由请求的库；微软：Orleans
* 无状态服务：方便运维和扩展，因为没有状态，可随意增加/减少节点,降低代码复杂度及bug数。
* 虽然无服务有上述优势，但现实一定存在状态：1）程序调用结果，服务组合，服务配置顺序等
  * 因此，为了达到无服务，需要将状态保存到其他地方。【eg：不太重要的就redis，重要的mysql/zk/etcd 等高可用的强一致性存储或者分布式文件系统中。】

* 负载和数据均衡：使用Gossip协议（各个节点互相散播消息来同步数据），这样新增或者减少节点可以很容易重新分配数据；使用一个路由节点通过一定策略来实现对所有数据的映射。

## 背压 back pressure

* back pressure：原本来源于工程：当气流或者液体在管道中运输时，由于管道变细或者受到其他阻碍，导致出现下游向上游的逆向压力。【cs：数据传输过程中，由于下游buffer满了，导致上游无法继续接收数据的现象。】

* 因为所有资源都有瓶颈，假如部署的代码支持1w人同时在线，当10001人同时在线就超过最大承受压力。上游服务大量请求下游服务，当下游服务到达瓶颈处理不过来就出现上述问题。

* 如何处理back pressure
  * 下游通知上游：已到达峰值，不要请求过快；
  * 若上游请求不可控：下游通过“丢弃”请求的方式确保系统不会崩溃。

## 容错

因为调度服务就需要调度服务状态+操作对应数据，数据量大时操作相对困难。

* 很多系统的高可用设计在数据运行时就复制（zk、kafka、Redis等）：强制使用两阶段提交
* 上述系统多指集群状态下的数据系统。即使采用了上述方法，仍然需要考虑一个节点挂掉后，在另外的地方重新恢复这个节点所带来的系统可用性等问题。

## 异步通信设计

* 高吞吐量下，异步通信效果远好于同步通信。
* 同步：**同步调用需要被调用方吞吐量不低于调用方的吞吐**【多个地方同时调用】否则被调用方性能不足拖死调用方；同步必须等待，消耗资源。

* 异步：**增加系统吞吐量+解耦更加彻底。**

* 三种异步通信方式
  * 请求响应方式：sender and receiver 被请求方收到后直接返回一个未来状态（发送方定时轮训，问一下干没干完；发送方注册一个回调方法，接收方处理后回调请求方。（先从商家跳转到支付宝或银行，商家会把回调的 URL 传给支付页面，支付完后，再跳转回商家的 URL。
  * 通过订阅的方式：接收方订阅发送方的消息（kafka），从队列中获取。
  * 通过broker方式：发送方/接收方都往broker发取消息。所有部分都不需依赖，有总线即可。

* 事件驱动设计----使用broker来实现较多。
  * pros：服务之间的依赖没有了，各个服务之间是平等的，都可以被重用和替换。
  * 开发、测试、运维都是高度隔离的。
  * 服务通过事件关联，因此不会相互阻塞。
  * 服务之间增加Adapter 相对容易。
  * 服务之间的吞吐量不必相互关联，可以按照自己的处理速度进行处理。

* 异步通讯设计重点
  * 解耦服务间的依赖，最佳方式是通过broker机制。【分布式无顺序，不丢消息】
  * 解耦是为了让各个服务隔离性更好。
  * 异步可以获得更大吞吐量，各个服务间的性能不受干扰独立。
  * 利用broker 方式可以将抖动吞吐量变为均匀吞吐量—“削峰”
  * 服务相对独立，部署和运维上都可以做到独立不受其他服务的干扰。
  * 服务通过消息交互，需要一个总控方维护一个业务流程状态变化逻辑，以便系统故障后知道业务到达了哪一步。【常见银行业务对账系统，T+1, 保证数据是对的】

# 区块链相关

## Bitcoin

几个特征：

* 去中心化：没有中心服务器、不受个人控制、整个系统由用户端PC构成，不是想发布就能发布.
  * 中心化：所有信息由一台中心服务器保存。
  * 去中心化：所有参与交易的机器都看得到这笔交易相关的所有交易信息。
* 数据防篡改：所有交易记录全量保存，并公开给所有人，而且被全量加密和校验，**数据篡改成本大！（并不是不能篡改）**
* 货币发行量固定：不会随意印钞票，导致通货膨胀。

对应的优点：不需要银行等中间机构，可通过不受任何人控制的p2p系统进行完全自由和可信的交易。

对应的缺点:实现难度大，价值低。

去中心化交易流程：

* 需要交易的用户把交易传到网络中
* 网络上的“记账节点”，通过比拼算力的方式竞争记账权，“挖矿”
* 获得记账权的节点，将带交易记录进行计算打包，并向全网广播。收到新的记账包的节点会对其进行验证，验证通过后加入自己的区块。

注意点：

* 整个bitcoin 的世界没有服务器，完全靠个人电脑拼出来的分布式系统
* 网络中任何节点都是不能信任的，任何一个节点都可能作恶
* 任何人都可以拿到所有数据，所以数据需要容易验证是否被篡改+数据篡改困难

**基于上述两点，bitcoin使用了两个重要技术：区块链、工作量证明共识机制**

## 区块链

Blockchain：包括一个个区块，每个区块都有一个ID & 包含一组交易信息，这些区块通过记录前一个区块的ID形成一条链。

<img src='/images/img/block_chain.png'>

* **每块ID****都是通过内容生成的，内容一变，ID就会完全不一样
* 一个ID变了，其他ID跟着变化，确保合法性。（修改成本较大，篡改成本大）
* 越旧的区块篡改成本越大，越安全；越新的区块越不安全。

## 工作量证明共识机制

**在可信任分布式系统当中，到中心化网络之后会变成不可行的。因此引出以下几个问题：**

* **以谁的数据为准：**任何节点可以修改数据，若以大多数节点为正确数据的情况下，只要控制了一半以上节点，就可以认为整个网络数据被控制。

* **大多数不应该是人数：**代码可以模拟无穷多人

* **意见分歧：**同一时间多个人告诉我数据应该这么修改，以谁是正确？

**解决方案：proof of work** **“挖矿”**

* 实质：大规模计算找到符合系统要求的区块ID（暴力穷举），需要付出大量的算力和电力。

解决的问题：

* **修改几乎不可能：**生成一个区块需要大量的时间和算力，因此带来的修改成本极大。

* **能掌握51%****的算力几乎不可能：**控制大多数人的算力成本也高。

* **分歧：**如此大算力找到的ID有效降低了冲突概率，即使出现了，也是多个合法版本，时间长了以后多数人选择的一个版本就是最终版本。

## hash-确保改了一个bit全部都要改

区块链的地址编码使用secure hash---安全散列。使用hash算法主要作用：

* 生成ID，该ID几乎不会重复

* 数据特征码，任何一个bit更改了，整个hash值就不同了（发布软件或者信息的时候附带一个校验码，如果进入hash得到的值不同，那么信息被篡改）

  ps：MD5、SHA-xxx 也是hash的一种

* 区块链协议格式—对区块头做两次sha-256的hash求值即可得到最终hash/

## bitcoin 交易模型

比特币区块中的交易数据，其实也是一个链，其中包含（input交易支出方和output交易收入方）

* 一个交易可以有多个output（把钱汇给多个人），但一个output只能有一个源input。（Eg: 假设Fred 给了Alice2个bit币，Ted给Alice2个bit币，当前alice有5个bit，但当她想给Bob4个的时候，由于input和output需要一致，所以需要将另一个收入方定为自己。）
* 于是，一笔交易可能会包含大量的input和output，这样循环传递下去就成了一个交易链。 查看你是否还有余额只需要从UTXO确认即可。

## 去中心化的共识机制

**拜占庭将军问题:如何确保攻击指令一致**

* 限制一段时间内的网络提案数（增加提案成本）
* 放宽最终一致性确认：按照最长链路进行拓宽。（出现分路，随机选择一个直到某一条路特别长）
* 容错上限：在部分同步网络环境中，协议最多可以容忍1/3拜占庭故障（1/3的不一致节点）；异步环境，确定性质的系统无法容忍错误，但随机算法仍可以1/3;同步的网络环境中，协议可以容忍100% 的拜占庭故障，但超过50%恶意节点的时候，会增加限制条件。

**proof of work**

* bitcoin挖矿最初从“pricing via processing or combatting Junk mail”提出，用于限制垃圾邮件
* hashcrash 要求对方的邮件头经过hash后满足一定的规律，当大量发送有邮件+满足条件时，CPU计算hash碰撞消耗过高，会引起警觉。
* 对于可信邮件服务器，放入白名单之后就不需要hashcrash。
  * 通过消耗对手能源的手段来阻止一些恶意攻击或是垃圾邮件的滥用情况。

**------------------------提高篡改成本、解决分歧、提高提案成本----------------------------------------**

**Dpos机制--中心化**

不定时选择一小群节点，在这一小群节点当中创建、验证、签名和监督。

## 智能合约

* 银行资金托管业务（信用比第三方高）
  * 受政府监管、较为安全的资金管理流程
  * 以太坊合约：将合约代码本地编译成功后发布到区块链上->矿工打包记录到某一个区块当中，需要调用时向这个区块发送一笔交易。

* 合同的bug:代码合同的bug一旦被执行后果难以补救。

## 加密和挖矿

每个人只能发起：自己向别人付钱；不能发起别人向别人/自己付钱。

* 比特币加密方法：密钥对/签名/证书

密钥对

* 非对称加密：信息加解密时，使用不同的密钥。公布出其中一个密钥，另一个留存

数字签名

* 密钥对引出的问题：其他人使用公钥伪装成第三方给我发送信息，如何识别？

​       eg：Mike 发信息，hash加密后得到一个hash串（digest）->私钥加密后得到Digest密文，这个密文就叫数字签名。->Mike将信息公钥加密后**连同数字签名**一起发给我—>我用我的私钥解密解密后，用Mike的公钥解密得到数字签名digest，然后sha 或md5加密，若结果和digest一致，则未被篡改。

证书：

* 假如Jack手上的密钥被更换且攻击者中间劫持了信息并通过更换的密钥对更改信息，此时Jack会被认为信息未被篡改【中间人攻击】

* 为了避免上述情况发生，只能找一个大家都相信不作恶的权威机构来认证公钥，这个权威机构将自己的私钥和mike的公钥及其相关信息加密后生成一个证书。因此mike的信息经过自己的公钥加密后再通过机构进行加解密再到jack

bitcoin加解密

* 每一笔交易的from和to 都是用户的公钥（公钥做账户）
* 交易发起方用自己的私钥加密交易信息，并制作签名，收入方用公钥做解密验证。

   PS: 无机构的原因---区块链需要更换半数以上节点。

bitcoin挖矿

* SHA-256(SHA-256 (Block Header)) < Target

   区块hash算法中，需要确保上述公式成立。区块头中唯一可以更改的就是Nonce，其他可以修改的：timestampe时间字段Merkle root交易信息。要找到某个数字让整个的hash小于target（决定了计算出来的hash前面有多少个0）因此，hash本身就是一个随机数，要让它满足一定的规律（前几个都是0）只能暴力破解。【hash碰撞】---0越多，难度越大

* 一般的挖矿流程: 获取之前的区块链信息—>从“待记账区”获取一组交易数据->形成区块头—>穷举Nonce并计算区块头hash是否满足条件—>一旦某矿工成功打包一个区块，他就会告诉其他矿工。收到消息的矿工会停下手上的工作，开始验证，验证后，广播给其他矿工。




------

