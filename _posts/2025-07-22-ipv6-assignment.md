---
title: 'ipv6-assignment'
date: 2025-07-22
permalink: /posts/2025/07/22/
tags:
  - Real Work Practice
---

ipv6 assignment(on Starlink)

# ipv6 assignment on Starlink

[official reference-what IP address does Starlink provide](https://www.starlink.com/gu/support/article/1192f3ef-2a17-31d9-261a-a59d215629f4?srsltid=AfmBOor7__s7CETprRRfgaBZ3fcLyGvGiTiBd733FpHvcGJRW8a_9lfc)

* Starlink offers two ipv4 policies:
  * Default-uses Carrier-Grade Network Address Translation（CGNAT）using private address space from **100.64.0.0/10** prefix assigned to Starlink clients via DHCP.
  * Public: Network Address Translation（NAT）translates between private and Starlink public ipv4 addresses.
* Starlink supports native IPV6 across all Starlink routers, **kit versions-套件版本 & service plans **. All ipv6 compatible Starlink router clients are assigned ipv6 address.

* Starlink public ipv4 policy is an **optional configuration** available to Local and global priority customer. A public ipv4 is reachable from any device on the Internet and is assigned to Starlink network clients using DHCP.
* Although truly static IPs are not available, a reservation system retains the public IPV4 address and IPV6  prefix even when the system is off or reboot.  
  * 没有静态地址，但是预留系统会在用户关机或者重启时**保留公共ipv4 地址和ipv6 前缀**
* However **relocating the Starlink or software updates may change these address**

* Public IPv4 addresses are available to the Local and Global Priority service plans. The public IPv4 option can be enabled from the account dashboard, see instructions [here](https://support.starlink.com/?topic=13f0056c-6f6d-5a55-623c-fe94ad9947c5). Note: Starlink WiFi routers do not support port forwarding or firewall rules for IPv4 or IPv6.

* Each Starlink is allocated one IPv4 address via DHCPv4 and a delegated /56 IPv6 prefix via DHCPv6-PD.

## Starlink will allocate:

- **One public IPv4 address for the customer’s wide area network (WAN)**, provisioned via Dynamic Host Configuration Protocol (DHCP) for routers/firewalls using IPv4.
- **One IPv6 /64 prefix for the customer’s wide area network (WAN)**, provisioned via Stateless Address Auto Configuration (SLAAC) for routers/firewalls using IPv6.
- **One IPv6 /56 prefix for the customer’s local area network (LAN)**, provisioned to routers capable of issuing a **DHCPv6-PD request.**

IP addresses are also available through the Starlink APIs. For more information, see [here](https://www.starlink.com/support/article/90109cc2-c7ec-31ff-d160-0a87f16ef759).

# DHCPv6-PD

DHCPv6-PD:  DHCPv6-**prefix Delegation-前缀代理**

* 一种前缀分配机制，在RFC3633中得以标准化。在一个层次化的网络拓扑结构中，不同层次的ipv6地址通过手动配置，但手动配置的ipv6地址扩展性不好，不利于统一规划管理。通过DHCPv6前缀代理机制，下游网络设备**不需要再手工指定用户侧链路的IPv6地址前缀**，它只需要：
  * **向上游网络设备提出前缀分配申请**，上游网络设备便可以分配合适的地址前缀给下游设备。
  * 下游设备把获得的前缀(一般前缀长度小于64)进一步自动细分成64前缀长度的子网网段。
  * 把细分的地址前缀再通过路由通告(RA)至与IPv6主机直连的用户链路上，实现IPv6主机的地址自动配置，完成整个系统层次的地址布局。

## DHCPv6-PD 工作原理

* step1：DHCPv6-PD client发送solicit报文，请求DHCPv6 PD 服务器为其分配地址前缀
* step2：如果Solicit报文没有携带Rapid commit选项 or Solicit报文携带了Rapid commit选项，但服务器不支持快速分配过程，则 DHCPv6 Server 回复Advertise报文，通知客户端可为其分配的ipv6地址前缀。
* step3：如果DHCPv6 client 接收到多个服务器回复的Advertise报文，则根据Advertise报文中的服务器优先级等参数，选择优先级最高的一台服务器，并向该服务器发送Request报文，请求服务器确认为其分配地址前缀。
* step4: DHCPv6 PD 服务器回复 Reply报文，确认将ipv6前缀分配给DHCPv6 PD客户端使用。

## ipv6地址/前缀的分配与更新原则

**路由器中多配置了DHCPv6**

DHCPv6服务器按照如下次序为DHCPv6客户端选择IPv6地址/前缀

* 选择IPv6地址池：DHCPv6 server 的接口可以绑定IPv6地址池，DHCPv6 client 将选择该IPv6地址池为接口下的DHCPv6 client分配地址/前缀。
* 对于存在中继的场景，DHCPv6服务器的接口可以不绑定IPv6地址池，而是根据报文中第一个不为0的“link-address”字段（标识DHCPv6客户端所在链路范围），选择与地址池中已配置的网络前缀或IPv6地址前缀属于同一链路范围的地址池。
* 选择IPv6地址/前缀（确定地址池后，DHCPv6服务器将按照下面步骤为DHCPv6 client 分配IPV6地址/前缀）：
  * 如果**地址池中为客户端指定了地址/前缀**，优先从地址池中选择与客户端**DUID**匹配的地址/前缀分配给客户端。
  * 如果客户端报文中的**IA选项携带了有效的地址/前缀**，优先从地址池中**选择该地址/前缀分配给客户端。**
  * 如果该地址/前缀在地址池中不可用，则另外分配一个空闲地址/前缀给客户端。如果IPV6前缀长度比指定分配长度大，则按指定分配长度来分配。
  * 从地址池中选择空闲地址/前缀分配给客户端，保留地址、冲突地址和已被分配的地址不能再分配给客户端。其中，保留地址包括：未指定地址、组播地址、环回地址、链路本地地址、NSAP和任播地址（RFC2526中定义）等。
* DHCPv6 服务器支持预留IPV6地址，即保留部分ipv6地址不参与动态分配。

## DHCP端口

* **Client listen for DHCP message on UDP 546** 
* **Servers and relay agents listen for DHCP message on UDP 547**
  * 往目标路由器的546/547端口模仿DHCP server发送路由包？

## DUID

* DHCP unique identifier(DUID) is used by a client to get an IP address from a DHCPv6 server.
* DUID has **a 2-byte DUID type field**, and a variable-length identifier field up to 128 bytes.  Its actual length depends on its type.

* The server compares the **DUID with its database** and delivers configuration data to the client. 

## ref

* [intro](https://support.huawei.com/enterprise/zh/doc/EDOC1000178148/459891c4)

# Stateless Address Autoconfiguration  （SLAAC）

* IPV6 hosts may automatically **generate** IP addresses internally using SLAAC or they may be **assigned** configuration data with DHCPv6-PD

SLAAC can automatically configure IPV6 host parameters on an IPV6 host **without the need for manual configuration or a DHCP server**

* SLAAC automatically configures an ipv6 address on an IPv6 hosts
* Stateless： no centralized server tracking address assignments，corresponding MAC address， and lease time.

## How does SLAAC work 

how an ipv6 host obtains IPV6 network parameters via SLAAC

### Step0: Link-local IPV6 address assignment 【prerequisite】

* as soon as an ipv6 host is connected to an ipv6 network, it automatically **generates its own IPV6 link-local address.**
  * link-local addresses are in the form of **fe80::/64**
* link-local address are generated in various ways depending on the operating system or fireware of the IPV6 device question.
  * **eg1:Cisco devices use EUI-64, which generates an address using the interface’s MAC address as part of the algorithm,**
  * **eg2: Windows computers generate them randomly.**
* link-local ipv6 address生成后，client performs duplicate address detection, 确保这个link-local address没有重复，如果有重复则重新生成后再开始SLAAC的步骤。

### Step1：Router solicitation and router advertisement

* The ipv6 host sends out and RS message using its newly obtained link-local address. 
* The RS message solicits any router that may be on the segment for an ipv6 global unicast prefix. 
* The **FF02::2（所有路由器的多播地址,RS报文的目的地址）** **all routers** multicast address is used as the destination of the RS message.
*  **Only IPv6 routers will receive this message because only IPv6 routers belong to this multicast group（ff02::2）**
  * ipv6 routers会返回一个RA信息，包含其控制的ipv6 prefix、network prefix length. 【PS: 大概率是一个/64的前缀，同之前的例子】

**RS报文**

* RS（**Router Solicitation**）报文是 IPv6 协议中 **邻居发现协议（Neighbor Discovery Protocol, NDP）** 的一种报文类型，属于 ICMPv6 协议的一部分。
* 由主机发送，用来主动请求本地链路上的路由器发送 RA（Router Advertisement）报文。

* 场景说明：

  * 当一个ipv6主机刚刚连接到网络上时，它并不立即直到网络上是否又路由器，因此它会发送一个RS报文到ff02::2，询问："有没有路由器可以告诉我网络配置信息"

  * 路由器收到RS报文后，回复一个RA报文，包含：ipv6前缀信息（SLAAC自动配置地址）、默认网关信息、是否使用DHCPv6等
  * 主机根据收到的RA报文参数，自动生成ipv6地址**【根据step0的例子，不同类型的操作系统等生成ipv6地址的方式不同】**

### Step2：Global unicast address configuration

* 在step1中，**入网的ipv6主机已经获得了路由器分配的前缀和网络长度(/64)，接下来只需要确定其ipv6地址的最右64位即可**

  * eg：router 提供的前缀 2001:1234 ::/ 64 ,再确定右侧的64位即可。

  * **Q：如何获取路由器的ipv6地址前缀？假定发送一个RS报文进行请求？？？**

* 基于操作系统 or ipv6的固件信息不同，会有不同的生成方式：

  * eg：ref-intro中的host随机选择了::2 作为最右侧64位ip地址，因此最终通过SLAAC生成的地址为2001：1234::2/64

* The router may specify its own address as the host's default gateway,depending on whether we configure the router to do so or not.



### Step3: Duplicate address detection for the global unicast address 

* RUN duplicate address detection on the network, 只要没有重复的ip地址，那么host已经有：
  * ipv6 global unicast address
  * a prefix length
  * a default router

## SLAAC on starlink

* starlink路由器: 定制版**OpenWrt（Linux内核）**，通过自动固件更新系统推送新版固件。
* 固件更新版本（根据starlinkTrack）的更新日志：
  * 20250714：2025.07.07.mr56060
  * 20250712：2025.07.07.cr56060
  * 20250709：2025.06.30.mr55627
* SLAAC中，当starlink用户接收到路由器发来的RA中的prefix/64后，**前缀+接口ID生成完成的ipv6地址**，接口ID有两种生成方式：
  * EUI-64将mac地址转为64位接口标识符
  * RFC 4941中的ipv6隐私拓展，使用临时地址替代MAC，防止通过MAC跟踪设备[无法预测，防追踪]
  * PS：SLAAC的随机接口ID是通过内核专用算法生成的带隐私保护的伪随机64位值，防止通过ipv6地址识别或追踪设备身份。

## ref

[intro](https://www.catchpoint.com/benefits-of-ipv6/slaac-ipv6)



# CGNAT

Carrier-Grade Network Address Translation











# NAT 

Network Address Translation
















------

