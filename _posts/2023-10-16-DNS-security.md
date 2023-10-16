---
title: 'DNS-security-related-notes'
date: 2023-10-16
permalink: /posts/2023/10/DNS-security-related-notes/
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

# Ref 




------

