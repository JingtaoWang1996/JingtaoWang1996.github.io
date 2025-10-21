---
title: 'Starlink paper notes'
date: 2025-10-10
permalink: /posts/2025/10/Starlink-paper-notes/
tags:
  - Real Work Practice
---

Starlink相关论文阅读笔记



# A Large-Scale IPv6-Based Measurement of the Starlink Network 

**Brief Intro: 基于Starlink的Router都已经native 配置了IPv6，因此，可以基于IPV6协议，从starlink自己提供的feed.csv上扫描IPv6网段中活跃的ipv6地址，同时根据城市和国家聚合展示**

## Intro

* Starlink has already supported native IPv6 across all routers. Therefore，we propose leveraging public IPv6 address as probing targets. 
  * Probing targets: IPv6 prefix from Starlink GeoIP database[ref2]
* Considering that only data packets with both source and destination address within the Starlink are forwarded between Starlink PoPs, we adopt the inside-out approach with probes connected to Starlink networks to investigate the Starlink backbone network.
  * **8 Starlink dishes to perform traceroutes to Starlink's public IPv6 address.**
    * **Q：这是否表示需要连接到Starlink之中的dishes才能实现所有扫描出来的都是Starlink的活跃用户终端**
    * [6、7] reveals the access network and backbone network of Starlink in IPV4, **Which requres at least one probe associated with each Starlink PoP to verify the mapped Starlink backbone network**, 没有dish 或者 RIPE Atlas probe节点，就无法**验证**
* We determine the associated PoP of an IP address by examining its DNS PTR records, and use the traceroute path to deduce the connections between Starlink PoPs.
  * Using this method, identify most of the pops from peering DB & Google Map 

* The statistical results shows that 61% of Starlink users are located in North America, and the geolocation allocation of Chicago has the most Starlink User.
* By associating a user with its corresponding PoP via its DNS PTR record, we **quantify the number of users served by each PoP.**
  * <u>**通过将Starlink的feed.csv中的活跃ip进行反查后，可以统计每个pop serve的用户数量。**</u>

## BackGround

* Most Starlink Satellite are above 550km in the 53° inclination（倾角） 

* Starlink subscribers in rural areas must rely on Inter-Satellite Links（ISL） to ensure connectivity，as there are no nearby GS for the serving satellite.

### Topology of Starlink Network

**订阅Starlink的用户的整个流量在Starlink网络中的动向[文中Fig1]**

* **Traffic forward path:** Starlink subscriber->User router->User dish ----(phased-array antennas in <u>Ku-band</u>)---->satellite (<u>connect to multiple terminals simultaneously with multiple antennas subdivided into beams</u>)--(ka-band links)-->GS
* **The starlink network adopts a one-hop bent-pipe routing approach given the dish & GS are both within the visible range of the same satellite，Otherwise， ISL need to be used.**
  * **Q: 这是否说明，如果要判断一个连线关系，是否可以同时目标点+最近的GS都在25°的仰角内筛选后，保留相同的卫星，作为可以构成链路的初步筛选。**
* The GS relays the traffic to POP through terrestrial connections. Subsequently, the traffic is routed across Starlink's backbone network, which comprises multiple backbone routers. 
* The final step, the traffic exists the Starlink network and reaches its destination via Internet Exchange Points (IXP) or Internet Service Providers (ISP)

## Starlink Network Measurement 

### Discovering Starlink user routers 

* For normal Starlink subscribers，**a CGNAT ipv4 address from the 100.64.0.0/10 prefix is assigned to the WAN side of User router**

  * **Starlink 在 IPv4 中广泛采用运营商级 NAT（CGNAT），用户路由器的 WAN 口通常分配自 100.64/10 地址段，该地址段是非公网地址，不能在互联网上被直接访问**
  * In the case of IPv6, each user router delegates a /56 prefix to its LAN clients
    * **Starlink 已在所有用户路由器上原生支持 IPv6**，并为其 LAN 客户端分配一个 /56 前缀。

  * 通过对地址结构的深入分析，ref2研究者发现 Starlink 用户路由器的 IPv6 地址具有显著规律：第 57–127 位恒为 0，第 128 位恒为 1。因此，在给定的 /40 前缀范围内，仅需枚举第 41–56 位，即可生成候选的 /56 子前缀地址。以西雅图地区为例，GeoIP 提供的前缀为 2605:59c8::/40，通过固定部分比特位并逐步枚举，可以构造出候选地址，如 2605:59c8:0000:0000::1、2605:59c8:0000:0100::1，直至 2605:59c8:00ff:ff00::1。利用 XMap 等高效扫描工具对这些候选地址进行探测，就能得到活跃的 Starlink 用户路由器 IPv6 地址。

#### A regular pattern in the IPv6 address of Starlink User router 

IPv6的地址是128位， <u>**此规仅限于 /40的网段下**</u>

* **The 57th -127th bit values are set as 0,**
* **The 128th bit is set as 1.**
* If the Starlink users in a certian region are assigned /40 prefix in feed.csv [ref2], we only need to focus on the remaining bits 41-56 to identify active Starlink user router's IPv6 address.
  * For example, Seattle,USA, the GeoIP database provides the prefix **2605:59c8::/40.**
  * We begin with 2605:59c8:0000:0000::1 (with the gray segments fixed) and then continue with 2605:59c8:00**00:01**00::1,upto2605:59c8:00**ff:ff**00::1.
    
    * 对于/40的网络，只有上面加黑的部分是需要变化的，后面的57-128位是固定的
* PS:前40位已经确定，57-128位已经确定，只需要确定41-56位即可
  
        * 基于这个规则下获取的ipv6地址再集合Xmap可以更快的发现active IPV6 address 
        * **考虑通过掩码构建其他非/40网段的扫描**

### XMAP

[xmap-git](https://github.com/idealeer/xmap)

**安装配置---从源码安装**

ref：https://blog.csdn.net/gitblog_00047/article/details/142606578

* 安装环境：47.236.28.227；

```具体执行的安装步骤
cd /leo/
git clone https://github.com/idealeer/xmap.git
cd xmap
sudo apt-get install build-essential cmake libgmp3-dev gengetopt libpcap-dev flex byacc libjson-c-dev pkg-config libunistring-dev
mkdir build
cd build
cmake .
make -j4
sudo make install
```

* 验证方式：xmap --version

#### ipv6扫描命令

* 目标环境上验证：xmap -6 2606:4700:4700::1111  
* 查看参数配置：xmap -h

#### TODO：具体需要使用的参数计算

### Enumerating Starlink Pops 

Starlink PoPs spread all over the world, and user traffic will be tunneled to its home PoPs before entering the public Internet. 

* 通过域名反查的形式：dig -x xxxx，将活跃的ipv6反向映射到具体的pop点名称中

  目前经过DNS反查后，有以下两个类型的反查域名，其中 * 代表pop名称【by 郝楠】

  * customer.\*.pop.starlinkisp.net
  * customer.\*.isp.starlink.com

### Mapping Starlink backbone network

Starlink uses its backbone network to route user traffic between different PoPs. **To investigate tehe Starlink backbone network,we need to determine connections between these pops**

* **Probe active user routers directly from a Starlink dish**, as routing through other ISPs' network would bypass the backbone network. **【pop之间的具体连接关系还是需要有一个Starlink dish】**

  * When probing user routers from a starlink dish，the **traffic passes through the user router's home pop** and **gateway** before reaching the target user router. 
    * 会先经过home pop【customer.xxxxx.isp.starlink.com---feed.csv当中的】
    * 还会经过gateway【后续会被识别的】

  * **<u>Identify the third-to-last hop as the backbone router within the home pop of the target user router</u>**
    * <u>ICMP包的倒数第三跳确定为**目标用户路由器**主干网内的主干路由器</u> 
  * To determine the associated home PoP of the target user router, we perform a reverse DNS lookup  on this third-to-last hop
    * 倒数第三跳通过域名反查后最终获得具体的pop点名称

* Home pop & pop

  * Home pop：通常指家庭接入点，ISP为家庭设置的接入点，通常在较小范围内提供服务。
  * pop：一个城市的ISP建立的一个pop，允许多个用户连接到互联网
  * 多个home pop 可以视作构成一个pop的一部分

* However，a pop may contain multiple backbone router for performance reason，meaning data packets might pass through more than one hop within the same PoP

  * 数据包在同一个pop内可能经过多跳

* To identify additional backbone routers，we deduce that **the router belong to the same pop if the latency between them is small (< 5ms)**

* Starlink uses **multiprotocol Label Switching (MPLS)** to reach its customers. 【？落地第三跳之后再这么用好像是】

  * MPLS：为每个数据包分配一个固定的标签，数据在转发时，路由器和交换机会检查标签来决定如何转发数据，而不是使用ip查找路由表

    * 标签分配原理
      * 数据包进入MPLS网络时，会被分配一个标签，这个进入的标签由进入MPLS网络的路由器（Label Edge Router）分配【标签分配基于某些规则：路径、服务类型、流量类型】
    * 标签交换
      * 一旦数据包获得标签，后续的路由器（Label Switch Router）通过查找标签来决定如何转发数据包，而不需要查看ip地址，每个LSR根据标签来快速转发数据包（将标签更新为另一个标签）
    * 标签剥离
      * 数据包到达目的地的Label edge router时，标签被剥离，数据包通过传统的IP路由继续转发到目标主机。

    * MPLS的优势
      * 高效的流量转发（避免进行负载的ip路由查找）
      * 路径控制（label的分配可以基于具体的路径给出）
      * 多协议支持、延迟优化

* 基于MPLS tunnel传递的ICMP信息可能导致RTT的延长，因此最佳办法是：**traceroute directly to the backbone routers** to obtain more stable latency measurement between backbone router
* Deduce the connection between pop and backbone router 
  * 2 probes from RIPE atlas & 6 Starlink dishes 
    * 2 probes from RIPE: Santiago,Chile & North Carolina 
    * 6 dishes: VICTORIA,CA；Lincoln，US；Brisbane，Au；Bruhl，Germany；Kanazawa Japan；Salt Lake City，USA；
    * **We only use Starlink dishes as probes and do not locate a Starlink dish in each pop**

* Source: https://ki3.org.cn/#/starlink-network 
  * 可以在上面的数据源中找到pop之间的连线结果【基于popName，可以映射到地图上，但是没法更新】

### Statistics on measurement results

* distribution of Starlink users：北美用户最多
* Starlink pops and their served users：基于上面提到的方法，可以将活跃的ipv6用户终端地址【有Starlink内部节点的情况下】按照延时归类到各个pop当中（<5ms）
* While Starlink users in most regions are served by a certain pop, users in 44 regions are served by serveral Pops.
  * Users in Sao Paulo are served by:  Santiago-sntochl1、Lima-limaper1、Sao Paulo-splobra1、Buenos Aires-bnssarg1、mmmiflx-1，bgtacol1 【基于hn扫描的结果，至少包含bgtacol1、bnssarg1、limaper1、splobra1】
  * Pops are assigned different network prefixes in the same region：**【已经进行过验证-hn的pops.json】**
    * splobra1：2803:9810:4300::/40
    * bgtacol1：2803:9810:5380::/42
    * mmmiflx1：2803:9810:a100::/40

* IPv6 address assignment strategy：
  * 57-127bit：设置为0
  * 128bit：设置为1
* **IPv6  address of Starlink gateway：**
  * gateway的ipv6地址pattern：2620:134:b0fe:x ::y **【前48位已经确定】**
  * **49-64bit：range from 0x0248 - 0x0253**
  * **65-116bit：设置为0**
  * **117-128bit：range from 0x000 - 0x057** 
  * gateway ipv6 规则示例：【将ip地址转为二进制后判断具体的位数是否满足即可】
* GATEWAY的ipv4和ipv6地址的映射关系：
  * **2620:134:b0fe:x ::y  == 172.16.x.y** 
  * PS：类似郝楠neo4j中的结果可以看出哪些gateway的地址池比较大，然后能够提高性能
* **The IPv6 address blocks assigned to Starlink PoPs are 2620:134:b0ff::/116 and 2620:134:b004::/116.**



PS: HN的源码1010扫描结果：1792w，清华的数据0929：454w？？？？

* 不只是有终端的！

* https://ki3.org.cn/#/starlink-network.
  * wjt397618242@163.com
  * Cetcwjt13191！
* 

## Ref

* ref1-Starlink has already supported native IPv6 across all routers：https://www.starlink.com/support/article/1192f3ef-2a17-31d9-261a-a59d215629f4
* ref2-Probing target/geolocation of its customer address: https://geoip.starlinkisp.net/feed.csv
* ref3-Peering DB【包含了Pop的准确信息】：https://www.peeringdb.com/asn/14593
* ref4-Google Map【包含的了Gateway的相关参数，pop的没有详细信息】：
  * https://www.google.com/maps/d/viewermid=1805q6rlePY4WZd8QMOaNe2BqAgFkYBY&ll=26.881954600485006%2C32.65665003578902&z=4


------

