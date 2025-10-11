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

### XMAP

[xmap-git](https://github.com/idealeer/xmap)

**安装配置**



### Proposed method 







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

