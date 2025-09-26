---
title: 'Backbone network detection'
date: 2025-09-10
permalink: /posts/2025/09/Backbone-network-detection/
tags:
  - Real Work Practice
---

权威服务器相关文献阅读

骨干网探测：基于starlink骨干网探测的笔记



# 关于骨干网

## 所包含的节点及类型定义

* **pop点（point of presence）**
  * POP是指一个网络服务提供商或互联网服务提供商（ISP）设置的**网络接入节点**。它通常包含路由器、交换机、防火墙、传输设备和其他网络设备，是用户与骨干网之间的接口。
  * **骨干网的接入点**：用户通过pop接入骨干网
  * 连接范围：
    * 用户设备、数据中心到核心骨干网
* **Public Exchange Point （公共交换节点 AKA   Internet Exchange Point-IXP）**
  * IXP是指位于特定地点的基础设施，提供了一个平台，使得多个ISP、CDN及其他大型网络能够直接交换流量，而无需通过更远距离的**第三方网络**（如大型骨干网运营商）进行中转。简单来说，公共交换点是一个**物理和逻辑上的交汇点**，供不同网络提供商直接互联交换流量。
  * 连接范围：
    * 多个ISP、CDN之间的连接，优化不同网络之间的流量交换，避免流量必须通过更远距离的中介网络。

## 连接关系

* **POP2IXP**

  * 一个pop点可能同时连接到多个IXP
    * **多重互联需求**：为了提升网络的冗余性、带宽和可靠性，STARLINK可能需要连接多个IXP，以便通过不同的互联平台与不同的网络进行流量交换。每个IXP可能连接不同的网络运营商、ISP或内容提供商，连接到多个IXP有助于增加互联的灵活性。
    * **优化网络拓扑**：连接多个IXP使得网络能够从不同的物理和地理位置交换流量，避免依赖单一IXP可能带来的瓶颈。特别是当网络运营商在多个城市或地区部署POP点时，通过多个IXP提供灵活的流量交换方式。
    * **降低故障风险**：如果一个IXP发生故障或出现拥堵，连接到多个IXP的POP点可以提供冗余路径，保障流量在不同IXP之间的自由流动，增强网络的**容错性**和**可用性**。
    * **接入不同网络的需求**：不同IXP提供不同的连接机会。例如，某些IXP可能主要连接本地或区域性网络，而其他IXP则可能有更多国际或跨国网络连接。通过连接到多个IXP，POP点可以实现更广泛的网络互联。

  * 不同的pop点可能连接到同一个IXP
    * **跨地域连接**：许多大型IXP都设有多个物理位置或交换平台，网络运营商通过在不同地点设置POP点来实现跨地域的**高效互联**。通过将不同POP点连接到同一个IXP，网络能够**跨地域地实现流量交换**，而不需要通过更长的骨干网络路径或中转网络。
    * **集中交换流量**：不同POP点通过同一个IXP进行互联，允许网络运营商集中管理流量交换和对等互联。这种方式可以减少跨地域传输的延迟，并优化网络性能。
    * **扩展互联和冗余**：对于需要大规模网络互联的ISP或跨国公司，多个POP点通过同一个IXP进行连接，有助于提供更高的**带宽容量**和**冗余性**。即使某个POP点出现故障，其他POP点依然可以继续通过IXP保持正常的流量交换。

## 连接关系收集方式

* **PeeringDB**：PeeringDB是一个公开的数据库，包含了很多互联网交换点和它们与其他网络（包括ISP、CDN等）的互联信息。你可以查询Starlink是否公开了与某些IXP的对等连接信息。

* **BGP路由数据**：BGP路由公告能够帮助你了解不同网络如何互联。通过查看Starlink的BGP路由信息，尤其是它的AS（Autonomous System）号码，你可以分析Starlink的流量路径以及它连接的主要IXP。

* **网络运营商公开报告或新闻**：Starlink和相关的互联网服务提供商可能会发布关于网络拓扑、连接IXP和扩展计划的公告。关注这些公开的信息也能帮助你了解Starlink的网络结构。

* **Traceroute分析**：通过执行Traceroute命令，你可以追踪从Starlink连接的用户到达目标网站时经过的网络节点，从中推测Starlink可能与哪些IXP或其他网络进行连接。

# Topology Discovery for Public IPv6 Networks

* ICMP-based probing 不能立即应用在ipv6上的原因:
  * ipv6地址空间更大
  * ipv6不同的scope-based addressing scheme and modified protocols

* This paper presents Atlas，a system that facilitates the automated capture of IPV6 network topology information from a single probing host. 
* Some initial probing results of 6Bone，currently the largest public ipv6 network
* One of the significant differentiators of **Atlas as a topology discovery tool** is, therefore, its comprehensive accounting of network phenomena in ensuring the accuracy of its infered topologies

## Probe deployment 主要涉及的两种方法

### Deploy multiple probe engines throughout the network

* paths are then probed from the individual points and the data later unified into a single topology graph. 

* This approach  does rely upon the **ability to deploy probe engines throughout the network**, which in many cases is not possible.

  

## A single probe engine can be used in conjunction with source routing facilities. 

* Both ipv4 and ipv6 provide the ability to perform source routing, which allows packet sender to specify one or more intermediate nodes that should be visited enroute to the final destination.

## Source routing 

* source routing in the ipv4 internet is largely disabled. (Some work shows that only 8% of routers are source-route capable.[ref 4](R. Govindan and H. Tangmunarunkit, "Heuristics for Internet map discovery," in Proc. INFOCOM 2000, March 2000.)
* **Source routing support in IPV6 routers is a mandated feature and hence mostly enabled.**

### With respect to traceroute

* Source routing allows one to discover paths between arbitrary pairs of network nodes, neither of which need to be the originating nodes. 
  * 可以发现任意一对网络节点之间的路由，且这俩节点之间不需要是起始节点。
* 基于论文中的Figure1：
  * **traceroute只能发现探测节点和目标地址之间的路由**
  * **source route：除了探测节点到目标节点之间的路由，还可以发现路径中间节点之间&目标节点之间的路由【详见论文中Figure 1】**
* <u>Q：是否已知starlink的两个不同目标地址，就可以一定程度上画出中间部分的路由情况。</u>

### Source route 应用在ipv6上可能遇到的问题

* A router manifests(表明) itself in paths by the IP address of one of its interfaces. **Each router is likely to have multiple physical interfaces.**
  * Therefore, one must identify difference address that belongs to same physical router,and therefore correspond to a single node in the topology. [一个router在拓扑中可以通过多个ip进行表示，需要将不同的ip进行去重对应到同一个物理设备上]
* The presence of router interface that are anonymous，they do not have configured network address and therefore cannot be uniquely identified.
  * **存在匿名路由器接口，因为它们没有配置网络地址，因此无法唯一识别**
  * **因此每一个匿名路由器接口在多条路由中需要被认定是不同的节点。**
* The existence of instable routing, which can significantly compromise the accuracy of path information.
  * Without carefully examination, routers not directly connected may appear as adjacent due to probe packets traversing different path.

## Back Ground for topology discovery in IPV6

* ipv6(RFC 2373 ) is designed to resolve address space shortages and provide fundamental support for security and Quality-of-Service.
* Among the many new features ipv6 provides, the most relevant to this paper are its **addressing scheme and its source routing capability.**
* Not all router interfaces need be configured with a unique global address, such as those connected by p2p links.

* IPV6 packets consist of a basic header and a number of optional extension headers. 
  * **routing header: （RFC 2460, routing header）supports the source routing features as mentioned above.**
  * The basic header contains: the address of the next specified router in the path; **The routing header contains a list of all other routers including final destination.**
  * Each intermediate router swaps the next address in the list with the current destination address in basic header.
    * This process is performed according to an embedded counter **Segments Left field**
    * **After a swap has occurred, the packet is then forwarded out to its next destination.**

### Source-routing 源路由

[ref](https://blog.csdn.net/m0_72410588/article/details/132504772)：<u>核心---</u>**允许数据包发送者指定它们在网络中所经过的路径，而不是依赖设备自行选择最佳路径。**

* 原理：在数据包首部添加一个源路由选项，该选项中包含了数据包需要经过的网络节点列表。当数据包通过网络时，每个节点根据源路由中选项的下一跳信息，将数据包转发给正确的下一跳节点，直到到达目的地。
* 应用：
  * 负载均衡：发包者选择合适的路径，从而实现负载均衡。
  * 安全性增强：通过指定特定节点的路径，增强数据包的安全性和隐私性。
  * Quality of Service control：通过在源路由选项中指定不同的路径，可以将关键业务数据包优先传输，确保其带宽和延迟满足特定需求。

### ICMP 

An integral part of both ipv4 and ipv6 is ICMP. 

* ICMPv4 and ICMPv6 are in many ways similar,but are nevertheless different protocol standards. 

* ICMP defines basic control messages that are used by routers and hosts to signal errors in packet handling.

* Two specific message types relevant to traceroute:

  **Hop limit exceeded in transit-传输跳数限制**

  * Send when a router detects a packets that has a hop limit(part of the basic header) that is bigger than one.

  **port unreachable**

  * Send when either a host or router's TCP/UDP protocol layer receives a TCP/UDP packet with an invalid(no listener on that port) port number 

* **Traceroute algo: repeatedly sending UDP probe packets to a given destination with a progressively increasing hop limit.**

  *  As the probe packets fall short of the final destination, in terms of insufficient hop limit. "Hop limit exceeded in transit" messages are returned by the intermediate routers. 

## The atlas probing and topology inference system

* Atlas consists of 4 components: 
  * A probe engine: correctly identify the network phenomena and retrieve accurate path info. 
  * A topology constructor: 基于上面获取到的信息进行画图，NP-hard problem.
    * Detailed Discuss can be found in [ref 7](B. Yao, R. Viswanathan, F. Chang, and D. Waddington, "Topology inference in the presence of anonymous routers," To Appear in INFOCOM'2003)
  * A topology verifier:  looks at the constructed topology and reasserts(**through additional probing**) the existence of the routers and links modeled by the graph.
  * An interactive visualization program 

### Seed selection

* To initiate the discovery process, Atlas relies on probing paths among a set of addresses known a priori which we term “seeds”. 【RIPE的atlas中的ipv6地址是已知的】
* It maintains a list of address pairs, each specifying a single via router and destination for a source-routed traceroute session.
* **The choices of seeds directly affects the coverage on can hope to achieve with the Atlas probe engine.** 
* The optimal choices of the seeds is all routers that exists at the edge of the network(non-transit)
  * 选择的seeds越靠边，最终发现的新的node就越多。
* 具体选择步骤：
  * Step1: 从6Bone的前缀中生成一些ipv6地址
  * Step2:向这些ipv6地址发送traceroute包，验证是否为真实的数据, <u>**如果是真实被使用的ipv6就可以作为candidate seeds**</u> 
  * Step3：进一步验证step2中地址
    * 是否 source-routing capable by using them as a via-router in a test trace. [将其用于中转路由器，验证其是否具备source-routing的能力]
    * 检查icmp处理是否合规
* If a router-level topology is desired, seeds should preferably be assigned to routers (not to end-systems)【郝楠活跃ipv6扫描及atlas的目标ip是终端，目前看】
* Increasing probe engine performance 
  * For each trace, the probe engine caches the hop distance to the via-router. If the same via-router is used in subsequent traces, then the cached distance provides the initial hop limit (as opposed to simply starting from one) and thus alleviates the need to re-probe the first leg.

## The network phenomena encountered by Atlas & The solution to handle them.

### Intermittent Router Non-responsive-间歇性路由器无响应

* 为了避免ICMP Dos attack，所有的ipv6 nodes must implement **rate limiting** on their outgoing ICMP messages. 
* Atlas避免发送频率过高触发这一现象的方法：
  * Time-backoff mechanism：Identical probe packets are repeately send with a given hop limit. 
  * Retransmission and avoids prolonged ICMP quenching. 
  * Dispersion of concurrent traces（分散并发追踪）：避免向同一个搜索区域发送过多的请求 

### Prolonged Router Non-Responsiveness -路由器长期无响应

* Some routers in fact have ICMP disabled for security reasons or that they are non-responsive due to long-term congestion. 
* 如果多次阻塞则，会在路径上直接跳过到下一个router，同时hop limit +1 【仅限于已知完整路由路径的情况下且无匿名路由的前提】

### Anonymous Interfaces 匿名接口

* Some interface may be configured with IPv6 site-local or link-local address only. Such an interface may be selected to originate the ICMP packet's source address. 
  * The majority of  routers **copy** the destination address of the original probe packet into the source address of the responding ICMP packets. 
    * 匿名接口会将响应包的destination作为最终的一条路由路径进行上报。【论文Fig1中X-Z-Y会变成X-Z-Z】

### Instable Routing 

From our own experience with the 6Bone, and IPv4-based experiments performed by others [10], routing is stable in most of the cases. Alternate paths exists typically for traffic engineering or load balancing purposes. 

* 更常见的路由协议（例如 OSPF 和 IS-IS）支持针对给定目的地的等权重多路径的概念。 **多路径路由策略在不同的实现中并没有标准化**。示例策略包括 对源地址和目标地址使用哈希算法、 循环或某些负载相关算法（RFC 2328）。
* 解决方式1：**Multiple probes** are dispatched for each hop in batches. For a hop result to be considered stable/accurate， Atlas must receive all replies for a given batch from the same router.
  * Not necessary to wait for a response to all packets in a batch,since ICMP quenching and congestion may be taking effect. 
  * If responses are received from different routers then instable routing is evident and the path is invalidated. 

* 解决方式2：将有疑问的节点通过traceroute经过所有的已知路径，基于探测结果判断路径稳定性同时进一步发现未知的subdomain
  * 探测工作量大、对节点要求高

### Address Equivalence-相同路由器的不同地址

* Router follow certain rules in selecting source address for their ICMP messages, since **routers typically have multiple global unicast address**, ICMP message that are generated by a single router **may not** always use the same source address.
  * As a consequence, two different traces across the same router may reveal different addresses and thus appear as two unrelated entities. 
* 可能的解决方案1：Mercator系统向其中一个可能等同的IPv6地址发送请求，如果从另一个IPv6地址收到”Port Unreachable“的响应则表示这个IPv6的地址是等同地址。
  * **Basic Assumption：All ICMP responses use the address of the interface closets to the probe engine.** 
    * For IPv6 routers this assumption does not hold: ICMPv6 规范明确规定， **被探测的地址应该用作 ICMPv6 响应的源地址**， 前提是该地址属于响应节点。 （RFC 2463）
* 可能的解决方案2：The Rocketfuel判断相同路由器IPv4地址的相关性基于IPv4包的序列号，但此方法不适用于IPv6,**因为IPv6不支持分片，因此IP包头中不在存在序列号字段。**
* Atlas系统的解决方案：【假设判断两个ip地址X和Y是否等价，P6左侧第三段】

### Restricted Routing Area 

* 从探测节点出发到目标IPv6地址的路径上，可能存在一定的区域无法从探测节点经过路由直达，**在无法从探测节点直达的节点区域中包含的几个中间路由，其相关的路由路径可能无法发现**
  * 假设已有路径：P-U-V-Y-Z-W,其中Y,Z may not be directly routable from P, consequently, a probe between Y-Z and a router revealed by some other path will fail.[Y-Z以及其他和 Y Z 相关的路径都无法被探测到]
  * The phenomenon is indicated by the receipt of the ICMPv6 messages ”Communication with destination administratively prohibited“ and ”no route to destination“
    * 该现象的主要原因1：防火墙避免路由器直接被访问，避免DDos攻击
    * 该现象的主要原因2：当在一个给定的管理域中，分配给路由器接口的地址没有在通过外部路由协议如BGP传播的路由中进行聚合时，**会导致路由表中出现过多单独条目，增加路由表大小，影响性能和可扩展性。**
* **Atlas is able to determine connectivity within restricted areas**
  * 寻找一个在restricted area边界上的router**（globally accessible & able to forward packets to routers within the restricted routing areas.）**[必须要明确直到这个router满足要求，目前看starlink估计不行]
  * 基于上述的节点，atlas执行 additional level source routing 
    * 首先将探测包发到restricted area中的某个边界节点上，边界节点将其转发到restricted area中间的某个路由器X当中，通过X可以进一步探测到内部的某些无法从P直接探测到的拓扑路径。

### Routing Loops 

* 由错误的路由表产生

## Preliminary results from simulation and probing the 6Bone

## Assessment of Effect Coverage 

* NS-2 simulator：Intended to support source-routing and Atlas-probing algo

* Simulating a single network topology of **1000 nodes and 3000 links takes approximately three days.**

* 最终实验只保留：50个nodes，其中10个是匿名节点；

  * 拓扑连接关系从50-120之间随机变化

  * 最终的模拟从tree-like 变为well-connected structure 
  * Average node degree of 4.8

* Node Coverage also increases according to the degree of connectivity of the topology being probed. 

  * The more seeds in use, the higher coverage it will get. 
  * 基于Fig10，最终coverage会收敛，因此并不是seed越多越好。

## Results from 6Bone 

* Beginning：426 seeds were gathered by probing addresses that were derived from prefixes. 
  * 类似的情况Starlink 可以从feed.csv or 活跃ipv6中生成
* 基于这些seeds，probing engine ran for **8 weeks, 发现了2420个router.**
* **由于IPv6-in-IPv4 隧道的广泛部署，任意两个节点之间的Maximum shortest path相对较小。**
  * Tunneling mechanism essentially provide "virtual hyper-links". 
    * **A single IPv6 hop may correspond to multiple underlying IPv4 Hops.** 因此，基于IPv4-IPv6的tunneling存在， a large physical distance are often mapped to a relatively small IPv6 hop distance. 
* Path or network topology info can be obtained from different sources, including routing protocols (eg:BGP,OSPF,IGMP), management protocol （SNMP) , Control protocol (ICMP)
  * BGP peers model the network through a router-level topology(RFC 2328)
* [The route Views project](University of Oregon, "Route views project," http://www.routeviews.org/.) collects BGP routing protocols information by the distribution of BGP peers. [The data collected by these servers is then used to construct an AS-level network topology]






------



