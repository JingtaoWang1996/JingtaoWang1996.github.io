---
title: 'DNS Info Collection'
date: 2025-05-20
permalink: /posts/2025/05/DNS-Info-Collection/
tags:
  - Real Work Practice
---

DNS Info Collection: zone transfer、brute force





# Zone Transfer

* DNS zone transfer using the **AXFR protocol**  to replicate DNS records across DNS server.
  * **AXFR protocol: Simplest mechanism to replicate DNS records across DNS servers.**
    * Edit Information on one server and using AXFR to copy information to other servers. 
  * If you do not protect your servers, malicious parties may use AXFR to get information about all your hosts.

## Why Is DNS Zone transfer needed

* If **a DNS server for a zone is not working(authority server)** and cached information has expired, then the domain is inaccessible to all services(web、mail、etc.,)
  * **therefore, each zone should have at least two DNS servers(Authority Server).**
    * 基于DNS运行冗余性原则-RFC2182规定：每个DNS zone 应该**至少配置两个权威服务器**，多个服务器应该位于不同的物理网络位置，避免单点故障。
* However, a zone may be large and may require frequent changes. If you **manually edit zone data** on each server separately, it takes a lot of time and **may cause potential mistakes.**

* AXFR: a client-initiated request. You can edit information on the primary DNS server and then use AXFR from the secondary DNS server to download the entire zone. 

## How to Initiate a DNS Zone Transfer 

* Initiating an AXFR zone-transfer request from a secondary server can simply using dig command

  * 首先获取目标域名对应的权威服务器名称

    ```
    $ dig +short ns zonetransfer.me(想要initiate zone transfer的域名)
    nsztm1.digi.ninja.
    nsztm2.digi.ninja.
    ```

  * 执行zone transfer

    ```
    $ dig axfr zonetransfer.me @nsztm1.digi.ninja.
    ; <<>> DiG 9.8.3-P1 <<>> axfr zonetransfer.me @nsztm1.digi.ninja. 
    ;; global options: +cmd zonetransfer.me. 7200 IN SOA nsztm1.digi.ninja. robin.digi.ninja. 2017042001 172800 900 1209600 3600 
    (...)
    ```

## AXFR Vulnerability and Prevention

* AXFR offers no authentication, so **any client can ask as a DNS server for a copy of the entire zone**

  * Unless some kind of protection is introduced, an attacker can get a list of all hosts for a domain, which gives them a lot of potential attack vectors.

* Protection I -Only allow trusted-nameservers**【DNS 配置中进行设置】**

  ```
  # /etc/named.conf 
  acl trusted-nameservers {
    192.168.0.10; //ns2 
    192.168.1.20; //ns3 
  }; 
  zone zonetransfer.me { 
    type master; 
    file "zones/zonetransfer.me"; 
    allow-transfer { trusted-nameservers; };
  };
  ```

* Protection II-Using **transaction signatures（TSIG**） for zone transfer to prevent IP spoofing attempts

* 





# Brute Force









# Reference

* Ref1: [Next Stop,the Cloud: Understanding Modern Web Service Depolyment in EC2 and Azure](https://pages.cs.wisc.edu/~rist/papers/nextstopcloud.pdf)

* 








------

