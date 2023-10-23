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
* 

# Ref 

* [ref1](https://www.shangyexinzhi.com/article/6844502.html)
* 


------

