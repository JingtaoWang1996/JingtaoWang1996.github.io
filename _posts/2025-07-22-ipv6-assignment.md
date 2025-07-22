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













# CGNAT

Carrier-Grade Network Address Translation











# NAT 

Network Address Translation
















------

