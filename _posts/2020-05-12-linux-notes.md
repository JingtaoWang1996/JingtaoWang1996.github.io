---
title: 'linux-notes'
date: 2020-06-15
permalink: /posts/2020/06/linux-notes/
tags:
  - cool posts
  - category1
  - category2
---

Some linux usage experience.

# 常用客户端工具

## mobaXterm

破解版可无限保存ssh记录

### 问题记录

* linux 服务器连接断开

  * 修改 /etc/ssh ssh_config 与 sshd_config 区别

    ssh_config 是针对客户端的配置文件  &  Sshd_config 是针对服务器的配置文件

  *  sshd_config 可以配置是否需要密码登录：PasswordAuthentication yes

* ssh 连接报错：Network error software caused connection abort

  * vim /etc/ssh/sshd_config 
  * 找到 TCP KeepAlive yes 把前面的 # 去掉
  * 找到ClientAliveInterval 参数去掉前面的#【该参数指定了服务器端向客户端请求消息的时间间隔，默认是0，不发送。ClientAliveInterval 60 表示每分钟发送一次，然后客户端相应，这样就保持长连接，比较奇怪的地方是，这里需要服务器主动发出请求，而不是客户端。正常情况下，ClientAliveCountMax】

# 文件操作命令

* 统计某文件中某内容出现次数：grep -o 内容 文件名 \| wc -l
* 统计某文件行数：wc -l 文件名
* 查看某文件中某内容对应的行：grep -n "内容" 文件名
* 复制文件：cp 当前文件路径 新复制文件路径 
* 将某个文件前m行移到另一个文件中：head -m a.txt > b.txt
* 删除文件/文件夹
  * 删除文件：rm -f 文件路径
  * 删除文件夹：rm -rf 文件夹路径 
* 移动/重命名文件
  * 重命名文件：mv 当前文件名称 重命名名称
  * 移动文件到目标路径，询问是否覆盖重复文件：mv -i 当前文件路径 目标文件路径
  * 移动文件到目标路径，直接覆盖重复文件：mv -f 当前文件路径 目标文件路径
  * 移动文件到目标路径，备份目标路径重复文件：mv -b 当前文件路径 目标文件路径

* 文件解压
  * tar.gz 文件：tar -zxvf Python-3.8.5.tgz
  * .zip 文件： unzip 文件名
  * unrar e xxx.rar

* 查看文件第n行内容：
  * 第1行：head -n 1 文件名
  * 第m行： head -m 文件名 

* 文件编辑：vim
  * 进入并编辑：cd到指定目录    vim 文件名     按insert 或 i 之后开始编辑
  * 退出：先按ESC之后      直接退出（：q）强制退出（：q!）保存并退出（：wq）
  * **切换到编辑模式在复制粘贴文件**：按照1）vim 进入之后   按i（进入编辑模式）ctrl+c/v

* 文件or 日志搜索（关键词匹配）：tail -f 
  * 实时刷新日志：tail -f 文件名 \| grep 关键词
  * 实时刷新日志的最新100行：tail -100f 文件名 \| grep 关键词

* 传文件/文件夹: scp
  * 远程服务器上的文件复制到本机: scp root@ip:/path/ /localpath
  * 远程服务器上的文件夹复制到本机：scp -r root@ip:/path/ /localpath
  * 本地文件复制到远程服务器：scp /localpath root@ip:/path
  *  本地文件夹复制到远程服务器：scp –r /local/path root@ip:/path
  *  直接从本地电脑上传文件到远端服务器：scp -p 9854 /cygdrive/待上传文件本地目录 root@localhost：/上传的目标路径
* vim 之后删除某一行：在esc状态下，直接dd，表示删除当前行。

# 进程操作命令

* 查看进程状态：ps -ef\|grep 进程字段or文件名（eg: ps -ef\|grep python3)

  执行后的参数说明例子：

  | 用户名 | pid    | child_pid | CPU占比 | 进程开始时间 | \    | 使用CPU时间 | 进程名  | 文件名 |
  | ------ | ------ | --------- | ------- | ------------ | ---- | ----------- | ------- | ------ |
  | root   | 进程号 | 进程号    | cpu占比 | 具体时间     | \    | 具体时间    | python3 | a.py   |

* 杀死、批量杀死进程

  * 杀死某个进程：kill -9 pid
  * 正常退出某个进程：kill -15 pid
  * 批量杀死某个文件名对应的所有进程（cd 到文件所在路径后）：pkill -f 文件名 

* 后台不挂断运行代码：nohup

  * nohup 可以不挂断同时执行多个代码  & 执行后的打印全部存入nohup.out文件，一直积累不自动删除

  * 命令格式：nohup 解释器 文件名 & (eg:nohup python3 new_main.py & 或 nohup java -jar xxx.jar &）

  * 输出重定向：nohup 输出重定向到 /dev/null() 后不会产生 nohup.out 文件

    ​    eg: nohup python3 new_main.py >/dev/null 2>&1 & 

* 查看后台运行任务：jobs -l 
* 查找某个进程pid：pidof python3

# 系统资源查看命令

* 端口占用：netstat –anp\|grep 端口号
* 端口是否已对外开放: netstat -ntulp \| grep 端口号
* 指定端口是否已开放：firewall-cmd –query-port=666/tcp（yes 已开启）
* cpu信息：lscpu
* linux 系统版本号：cat/proc/version
* 服务器cpu数
  * 物理CPU：cat /proc/cpuinfo\|grep “physical id”\|sort –u\|wc –l
  * 每个物理CPU中的核数：cat /proc/cpuinfo\|grep “cpu cores”\|uniq
  * 逻辑cpu：cat /proc/cpuinfo\|grep “processor”\|wc -l
  * Cpu名称型号：cat /proc/cpuinfo\|grep “name”\|cut –f2 –d:\|uniq

* 内存占用

  * 最大命令：free -h   【free -h -s 2 每2s自动执行一次该命令】

  * 某个进程的内存占用：ps -aux\|grep python3(进程名)

  * 更详细的内存占比： cat /proc/进程号/status: VmRSS为进程所占用的内存

  * top命令，之后按M：所有进程按照内存占用大小排序

    top 命令，之后按P：所有进程按照CPU占用排序。

* 磁盘占用情况：df 

  执行之后可以用于查看具体文件的占用

  * 返回根目录：cd /
  * 确认具体那个文件占用磁盘较大：du -h -x --max-depth=1

​         PS: df -h 没有发现大文件之后的查询思路：**lsof -n grep deleted**，找到对应进程号后杀掉[参考](https://www.cnblogs.com/muchengnanfeng/p/9554993.html)

* 进程运行在哪个逻辑CPU上：ps -eo pid，args，psr \|grep nginx
* linux 下的python console 交互
  * 查看当前python连接：ll /usr/bin/grep python
  * 进入命令行模式：python3
  * 退出命令行模式：ctrl+D

# 网络相关命令

* 通断性：ping ip （python 多目标异步发送icmp包进行ping的库：multiping）
* 网络跳数：traceroute ip/域名
  * 说明：通过向目标主机发送一条消息并通过会带来判断主机状态，遍历由源主机到目的主机的交互线路上所有的路由器并判断状态，一般以30为最大TTL，即以该线路上不超过29台路由器为前提进行遍历。
  * 基本原理：当路由器收到一份IP数据报，若该报文的ttl字段是1，则该报文的生存周期消耗殆尽，本路由处理后还未到达目标主机则需要将该数据丢弃，并给信源主机发送一份ICMP超时报文（包含中间路由器地址），这意味着：通过发送一份TTL字段为n的IP数据报给目的主机，就得到了该路径中的第n个路由器的IP地址，那么我们使IP数据报的TTL字段值从1开始递增，就可以获得所有中间路由的IP地址。由于已经到达目的主机，因此不会再发送ICMP应答报文，通过区分收到的ICMP报文是超时报文（type = 11）还是应答报文（type = 0）以判断程序应该何时结束。[每一次发包ttl从1开始增加，在一次traceroute过程当中，从源主机出发，每次经过1个路由则ttl-1，为0时返回本次所有路由状态，然后进入下一次发包。]
  * **最大30跳**，每个记录1跳，每一跳表示一个网关，3个时间表示发送的三个包网关相应后的返回时间。 

* mtr命令：（ping+traceroute)

  * 命令格式：mtr ip

    ![mtr示例](./img/mtr示例.png)

    查看traceroute 路径，丢包率，平均解析时延等，通过这条命令结合实际情况观察路径上的丢包情况等。

* 网络是否通畅\|：\| ip

  * 通过url执行上传或下载

  * \| --h  查看help 文件命令执行方式。

  * \| --k  跳过ssl 认证环节。

  * \| –data-urlencode()  url 编码的数据

  * \| url：port/path  查看当前路径内容。

    使用示例

  * \| –k https://ip:443

* bgpdump：linux解析bgp报文命令，[安装步骤](https://blog.csdn.net/weixin_35708669/article/details/89442180)

* iptable

  ifconfig 确定网卡名称后

  * 53的tcp 和 udp **重定向**到5053

    iptables -t nat -A PREROUTING -i enp125s0f0 -p tcp --dport 53 -j REDIRECT --to-ports 5053

    iptables -t nat -A PREROUTING -i enp125s0f0 -p udp --dport 53 -j REDIRECT --to-ports 5053

  * 查看iptable 规则：iptables -t nat -L -v -n

  * 删除某条规则

    规则行号：iptables -t nat -L -n --line-numbers

    根据num行号确定删除规则： iptables –t nat –D INPUT 第几条规则

​              PS: 若报错iptables：index of deletion too big，则需要明确要删除的表（ iptables -t nat -D PREROUTING 第几条规则）

* 防火墙操作

  * 查看防火墙状态: systemctl status firewalled

  * 开启防火墙：systemctl start firewalled // service firewalled start

  * 关闭防火墙：systemctl stop firewalled

    若遇到无法开启防火墙的情况

  * 先 systemctl unmask firewalled.service

  * 再 systemctl start firewalled.service

* telent：telnet ip port

# 其他命令

## ssh 建隧道

* 建隧道例子：ssh -f -N -L 9988:211.144.18.3:20022 root@10.42.25.13  
  *  将跳板机（211.144.18.3：20022）通过9988端口映射到本地13
  * ssh -f -N -L 9854:172.20.10.46:22 common@localhost -p 9988 
  * 将通过跳板机连接的目标服务器（172.20.10.46:22）通过9854端口映射到跳板机的端口9988，进而映射到本地

* 直接从本地电脑上传文件到远端服务器---完成上述映射之后: scp -p 9854 /cygdrive/待上传文件本地目录 root@localhost：/上传的目标路径

* 跳板机（13）传文件到远程目录下
  *  文件传到13 root 目录下
  *  scp -P 20022 dnspython.conf common@211.144.18.3:/home/common
  * 控制节点 /home/common 再scp

## 任务绑定CPU

当多个进程争抢一个CPU资源（或1个CPU资源分配了多个进程，前几个进程执行时资源耗尽）导致代码耗时不稳定，[参考](https://blog.csdn.net/qq_30683329/article/details/88779390)

* CPU 亲和力：CPU affinity是一种调度属性(scheduler property), 它可以**将一个进程"绑定" 到一个或一组CPU上**.在SMP(Symmetric Multi-Processing对称多处理)架构下，Linux调度器(scheduler)会根据CPU affinity的设置让指定的进程运行在"**绑定"**的CPU上,而不会在别的CPU上运行。**Linux调度器同样支持自然CPU亲和性(natural CPU affinity): 调度器会试图保持进程在相同的CPU上运行, <u>这意味着进程通常**不会在处理器之间频繁迁移,进程迁移的频率小就意味着产生的负载小。</u>

  因为**程序的作者比调度器更了解程序,所以我们可以手动地为其分配CPU核，而不会过多地占用CPU0，或是让我们关键进程和一堆别的进程挤在一起,**所有设置CPU亲和性可以使某些程序提高性能。

* CPU核心表示方法

  CPU affinity 使用位掩码（bitmask）表示，每一位都表示一个CPU

  最低位表示第一个逻辑CPU,最高为表示最后一个逻辑CPU

  CPU affinity 典型的表示方法是使用16进制：

  1）0x00000001   is processor #0

  2）0x00000003   is processors #0 and processor #1

  0Xfffffffff      is all processors

* 如何确定绑核成功

  top命令 -> F -> last used CPU ->ESC ->退回正常top界面，就可以看到哪些进程泡在哪些核上，若lastCPU一直保持不动，则绑核成功。

* Taskset 使用方法

  通过该命令，可以将一个启动的进程直接绑定在某个核上运行。

  * 命令格式taskset-cp cpu(cpu-list) pid

    eg：taskset -cp 1(1-3) 1927 将进程号为1927的进程绑定在核1/1-3上

  * taskset -h 查看具体参数说明

# 操作系统

centos、debian等操作系统使用时遇到的问题记录

## Debian 装GUI图形界面

* sudo su –
* 更新debian系统： apt update & apt –y upgrade
* GNOME 使用一下命令安装桌面环境【耗时】：apt –y install task-gnome-desktop
* 上一步完成后，分配graphical runlevel：systemctl set-default graphical.target
* 默认情况通过GNOME 显示管理器GDM禁用root用户登录，去掉限制：
  * vi /etc/pam.d/gdm-password
  * 注释掉：# auth  required pam_succeed_if.so user !=root quite_success
* 重启debian服务器：reboot
* 参考：搜索“如何为debian11安装图形用户界面GUI"

## Centos

### 修改最大链接数方法

* 暂时修改：ulimit -n 100001 【服务器重启后失效】

* 永久修改，[参考]( https://www.jianshu.com/p/1d3d368365bf)

  * vim /etc/security/limits.conf：在文件end of file 之后加上

    ```
    * soft nofile 65535
    * hard nofile 65535
    * soft nproc 65535
    * hard nproc 65535
    ```

  * ulimit -n： 查看确认最大链接数已被修改

### 问题记录

* centos yum 无法使用

  解决方案：/etc/yum.repos.d/ 下Centos-Base.repo 无法正常使用，需更新yum源，[参考](https://zhuanlan.zhihu.com/p/430561706)

* arm centos yum 无法正常使用---yum源只有x86

  解决方案：更新yum源，[参考](https://zhuanlan.zhihu.com/p/430561706)

## Linux

### 安装虚拟机

[参考](https://www.tecmint.com/install-vmware-workstation-in-linux/)

* 下载vmware workstation [安装文件](https://www.vmware.com/products/workstation-pro/workstation-pro-evaluation.html)

* 上传到15对应目录 /root/vmware/

* 修改权限否则报错: chmod a+x VMware…xx.boundle
* 安装: **./VMwarexxxxx.boundle**
* 启动vmware

# 系统配置相关

## /etc/hosts/

​      在通过服务器IP连接某个部署的文件或进程时，可直接使用IP 或 linux /etc/hosts/文件下写好的别名：

```
 vim /etc/hosts/
 --------------------
 ip 别名
```

## /dev/null

* /dev/null 称为空设备，是一个特殊的设备文件，它将丢弃一切写入其中的数据（但报告写入成功），读取该文件会立即得到一个EOF。类似于一个黑洞，常用于丢弃不需要的输出流。使用这些操作通常由重定向完成。

* 使用nohup 重定向的命令行方式： **nohup python3 new_main.py >/dev/null 2>&1 &**

## /etc/resolv.conf

若上述DNS配置文件无法解析DNS，则在**文件最后增加一个空格**：eg-- nameserver 8.8.8.8 

# shell 脚本

[参考内容](https://www.runoob.com/linux/linux-shell.html)

在一般情况下，人们并不区分 Bourne Shell 和 Bourne Again Shell，所以，像 **#!/bin/sh**，它同样也可以改为 **#!/bin/bash**

## 脚本运行

* cd 到脚本目录下后 执行 sh xxxx.sh
* 使用脚本绝对路径：sh /DNS/XXX.sh
* 增加权限后执行，cd到具体路径后：chmod +x ./test.sh #使脚本具有执行权限
* 将shell 脚本作为解释器参数运行（这种运行方式，不需要在第一行指定解释器信息， #！/bin/bash 这个）eg： /bin/sh test.sh              /bin/php test.php

## 脚本命令

* \#! 告诉系统其后路径所指定的程序即是解释此脚本文件的 Shell 程序。
* Shell 注释： 和python 一致，通过 # 注释
* echo 命令： shell 脚本的字符串输出命令，eg ：echo "Hello World !"，显示和输出命令
* shell字符串：单双引号，不用引号均可
  * 单引号：单引号当中的所有字符都会原样输出，单引号字符串引变量无效
  *  双引号：可以引变量，转义字符
* shell变量定义：不加美元符号定义，可重复定义已定义变量。
* 使用一个定义过的变量，只需要再其前面加美元符号即可： $
* **只读变量** 添加关键词 readonly 将变量定义为只读变量，只读变量的值不能被改变
* 脚本传参：执行shell 脚本向脚本传递参数，脚本内获取参数的格式： $n, n 为1个数字，1为执行脚本的第一次参数，2 为执行脚本的第二个参数

# 其他

## epoll 机制

 Epoll 是linux内核为了处理大批量文件描述而作了改进的poll，是linux下多路复用IO接口select/poll的增强版本，能够显著提高程序在高并发连接中只有少量活跃的情况下的系统CPU利用率。

* epoll的优点：
  * 支持一个进程打开大数目的socket描述。Select的一个进程打开的FD由FD_SETSIZE来设定，epoll没有这个限制，它所支持的FD上限是最大可打开文件数目，远大于2048.
  * IO效率不随FD数目增加而线性下降：由于epoll只会对“活跃”的socket进行操作，只有“活跃”的socket才会主动调用callback函数，其他idle状态的socket则不会。
  * mmap加速内核与用户空间的消息传递。Epoll 是通过内核与用户空间mmap同存一块内存而实现的。

## libev 机制

* 提供指定文件描述符合事件发生时调用回调函数的机制。Libev是一个事件循环器：向libev

* 注册事件，如socket可读事件，libev会对所注册的事件的源进行管理，并在事件发生时触发相应程序。

* gevent 方法spawn了一些jobs，然后通过gevent.joinall 将jobs加入到微线程的执行队列中等待其完成，设置超时时间为2s。执行后的结果通过检查gevent.greenlet.value 值来收集。
* Monket patching 的 python环境允许我们在运行时修改大部分对象，包括模块、类甚至函数。虽然这样做会产生“隐式副作用”，而且出现问题很难调试，但在需要修改python本身的基础行为时，monkey patching 就排上用场了。
  * 通过monkey.patch_socket()方法，urllib2模块可以在多微线程环境，达到与gevent共同工作的目的。
  * 事件循环：gevent和eventlet 类似，在一个greenlet中隐式循环。没有必须调用run() 或者dispatch() 的反应器（reactor），在wtisted中是有reactor的。当gevent的API函数想阻塞时，它获得Hub实例，并进行切换。
  * 提供的事件循环默认使用系统最快轮询机制，设置LIBEV_FLAGS环境变量可指定轮询机制。LIBEV_FLAGS =1 为select，2为poll，4为epoll，8为kqueue。

* Libev的API位于gevent,core下。注意libevAPI的回调在hub的greenlet上运行，因此使用同步greenlet的API，可以使用spawn() 和 event.set() 等异步API.



## C10k问题—操作系统处理高并发请求的问题

10 thousand clients problem

* problem raiser：Dan Kegel

* 技术层面定义c10k问题:设计不够良好的程序，其性能和连接数及机器的性能关系往往是非线性的。

  Eg：基于selector的程序在旧的服务器上能处理1000并发的吞吐量，但在2倍性能服务器上无法处理2000并发的吞吐量。因为策略不当时，大量操作的消耗和当前连接数n线性相关（单个任务资源消耗和当前连接数的关系是O（n））当服务程序对数以万计的socket进行IO处理，积累下来的资源消耗会相当可观。

* 问题本质: 操作系统的限制，传统同步阻塞IO模型处理方式都是requests per second，并发10k和100的关系区别在于CPU(创建的进程/线程多了，数据拷贝频繁-缓存IO,内核将数据拷贝到用户进程空间、阻塞；进程线程上下文切换消耗巨大，导致系统崩溃。

  解决问题的关键：减少CPU等核心计算资源消耗，从而榨干单台服务器的性能。

* 可能的解决方案: 每个进程、线程同时处理多个连接（IO多路复用）
  * 循环挨个处理连接，每个连接一个socket，当所有socket都有数据的时候，这种方法可行，但当某个socket的数据不ready的时候，整个应用阻塞等待。【DNS就是这个问题】
  * select 解决上面阻塞问题：在读取句柄之前，先查看确认状态，ready才进行处理。这样做的问题：小规模连接逐个检查句柄问题不大，大规模逐个检查状态就很慢。【selector 往往存在管理句柄上限。】
  * poll 解决select 的前两个问题，通过一个pollfd 数组向内核传递需要关注的事件消除句柄上限，同时使用不同字段分别标注事件和发生事件，来避免重复初始化。
  * epoll 解决逐个排查所有文件句柄状态效率不高的问题。假如调用返回的时候只给应用提供状态变化的文件句柄，就能提高排查效率。（当文件句柄数量达到10k的时候，epoll已经超过select 和 poll 两个数量级。）


------

