---
title: 'DNS-security-related-notes'
date: 2022-10-13
permalink: /posts/2022/10/DNS-security-related-notes/
tags:
  - cool posts
  - category1
  - category2
---

DNS security related notes：DOH.



# 背景

* DNS安全问题：隐私、域名劫持、重定向、钓鱼等
* [DNS流量被用于非安全目的的过度审查、监管和其他非法目的证据](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/pearce)

# DNS隐蔽隧道攻击

几乎所有的网络应用都依赖DNS作为前置条件，防火墙通常开放53端口供DNS服务正常运行，客户端可以连接到内部的DNS服务器或者外部DNS服务器。这就从根源上导致了 **DNS被攻击者视为天然的、优质的隐蔽通道** 。

## 简单DNS隧道攻击流程【假设本地服务器已被控】

<img src="/images/img/DNS隧道图.png">

<img src="/images/img/隧道传递控制命令.png">

<img src="/images/img/隧道传递窃密信息.png">

* 攻击者首先接管控制一个目标域名的DNS AUTHORITY SERVER
* 被控客户端将C&C数据或目标数据通过编码、加密、混淆等方法嵌入到一个DNS请求的子域名中。
  * 目标数据：admin密码等。
* 在缓存域名的TTL窗口期中，只要请求的域名&子域名不重复，就不会查询缓存，直接转到权威服务器。
* 权威服务器通过NS指派解析到攻击者控制的域名服务器，攻击者收到C&C的数据或目标数据。
  * **此时已获取具体密码等信息泄露。**
* 攻击者在响应数据包里同样可以嵌入C&C数据或目标数据，送达客户端。
  * **返回的响应中，可以包含可执行的控制命令。**

## DNS隧道背景

* **可以利用传输数据的记录类型**:A、PTR、AAAA、NS、CNAME、TXT、MX、NULL、SOA、DNSKEY

* DOH之前的隧道工具：

  |          | DNS2tcp      | DNSCAT2                 | Iodine                         |
  | -------- | ------------ | ----------------------- | ------------------------------ |
  | 隧道类型 | TCP-over-DNS | ip-over-DNS             | ip-over-DNS                    |
  | 记录类型 | TXT、KEY     | A、TXT、CNAME、MX、AAAA | NULL、TXT、MX、CNAME、A、SRV等 |
  | 编码方式 | Base64       | Hex16                   | Base32、Base64、Base128等      |
  | 特点     | 无周期性轮询 | 灵活交互                | 支持edns扩展协议。             |

基于DoH协议构建隐蔽隧道，可实现：

* 通信内容可**基于HTTPS协议加密**。
* **与高可信DoH服务通信**（非本地DNS服务器）不会引发异常行为，**避免基于DNS的恶意行为检测机制**。

*基于DOH和**

利用DoH隧道实施数据外传的首款恶意软件Godlua在2019年被披露[6]；利用DoH实施数据外传的APT组织（APT34）在2020年被披露[7]；其他利用DoH隧道技术进行攻击的研究和开源项目参考[8][9][10]。

# DNS加密方案

## DNSSEC

[DNS SECurity](https://www.dnssec.net/.) 

* 通过增加签名&验证签名机制以保护DNS数据完整性。
* DNS数据依然是明文，不能解决DNS数据机密性的问题。

## DNSCrypt

* [DNSCypt](): 开源社区发起、**解决DNS数据完整性和机密性**，没有提出RFC标准建议，对网络应用支持有限。

## DOT

[DNS over TLS](https://datatracker.ietf.org/doc/html/rfc7858)

* 2016年正式发布RFC标准。
* 通过TLS协议对DNS请求和响应进行加密和封装，工作于853端口。
* 缺点：DOT在853端口专门提供服务，容易被防火墙和其他安全设备识别、审查和阻断。

## DOH

[DNS over HTTPS ](https://datatracker.ietf.org/doc/html/rfc8484)

* DOH 将DNS请求和响应数据包用HTTPS加密，阻止第三方对明文DNS数据包的窃听和篡改。
* 能良好融合HTTP生态，网络应用对DoH支持也相对容易。
* 已得到Cloudflare、Google、Quad9、Alibaba 等公开DNS解析商&主流浏览器的支持。

# DOH 工作方式

<img src="/images/img/DOH工作方式.png">

* DoH允许服务端先把DNS响应push给客户端（早于客户端发起DNS请求），降低DNS服务时延，改善网络应用的性能。【以上图DOH工作方式为例，若DOH为代理，可早于client查询请求到代理443之前现象DOH解析服务器发送请求，不必等待第一步。】
* **DoH将DNS请求和响应封装到HTTP请求的主体**。
* 客户端跟递归服务器之间建立一个**TLS会话，通过HTTPS协议传输封装了DNS请求的HTTP请求**。

## 与传统DNS解析相比

* DOH 通过443端口的加密HTTPS连接接收DNS查询将其发送到兼容DOH的DNS解析服务器，不是在53端口发送纯文本。【DOH在常规HTTPS流量中隐藏DNS查询】
* 基于上述从443端口发出，DOH就会在常规HTTPS流量中隐藏DNS查询，避免**第三方监听者嗅探流量**。

## DOH&隐蔽隧道攻击

DoH虽然具备绝佳的隐私保护能力和安全能力获得用户的青睐，也由于 **DoH被用于隐蔽隧道攻击而遭到政府机构和安全机构的警惕关注** 。





# Ref 

* [ref1](https://www.shangyexinzhi.com/article/6844502.html)：DOH、隐蔽隧道工具等。
* 


------

