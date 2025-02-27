---
title: 'DNS cache probing'
date: 2025-02-25
permalink: /posts/2025/02/DNS-cache-probing/
tags:
  - Real Work Practice
---

DNS缓存探测相关内容：

# 《Trufflehunter: Cache Snooping Rare Domainsat Large Public DNS Resolvers》

* [source code](https://github.com/ucsdsysnet/trufflehunter)

## target：大型DNS公共解析器缓存探测的方式

* Through controlled experiments，we infer the **load-balanced multi-layer distributed caching architectures** of the four most popular resolvers
* 1st to model the behavior of these cache architectures and how they related to user access. Building on these models, the paper demonstrate that it is possible to snoop public DNS PoPs and estimate how many caches contain a specific domain.
* 工具的核心：**Trufflehunter consistently <u>underestimates cache occupacy</u>，it can provide a <u>lower bound</u> estimation of 他和prevalence of domains** 
  * **提供大型DNS服务器中目标域名的缓存情况下限**

## Why public resolver are important

* **imporve reliability** [ref](Michael Horowitz. 2007. OpenDNS provides added safety for free. https://www.
  cnet.com/news/opendns-provides-added-safety-for-free/)
* **small-scale ISPs have also switched to public DNS to avoid the operation and maintenance cost of providing their own DNS resolver**(eg: Google Public DNS has a formal vetting process where ISP can request to remove GPDNS‘s rate limit，so they can have their entire customer base use GPDNS as their primary resolver)[ref](Google. 2020. Google Public DNS FAQ. https://developers.google.com/speed/public-dns/faq#isp)
* security reason
* improve performance

## PDNS cache snooping challenge 

* However, public DNS resolvers consist of many independent caches operating in independent Points-of-Presence (PoPs), which makes them among the most challenging DNS resolvers to cache snoop.[**公共解析器每个入网点都有单独的缓存**]

* 公共DNS服务器提供很多碎片化缓存 & 在多个cache resolver instance之间进行负载均衡[ref1](Amit Klein, Haya Shulman, and Michael Waidner. 2017. Counting in the Dark: DNS Caches Discovery and Enumeration in the Internet. In Proc. IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)) [ref2](Lior Shafir, Yehuda Afek, Anat Bremler-Barr, Neta Peleg, and Matan Sabag. 2019. DNS Negative Caching in the Wild. In Proc. ACM SIGCOMM Conference Posters and Demos.)
  * **cache resolver instance?**
  * Even if a user recently resolved a domain with a public DNS resolver, subsequent requests to that domain may not be serviced from a cache.

## How a typical query is cached in a public DNS resolver's hierarchy

**通常情况下一个请求是如何在公共解析器中被查询的步骤**

<img src="/images/img/GPDNS缓存策略.png">

* step1: user direct their query to one of the public DNS service's PoPs by sending the request to one of the service's anycast IP address [ref](Giovane C. M. Moura, John Heidemann, Moritz M¨uller, Ricardo de O. Schmidt, and Marco Davids. 2018. When the Dike Breaks: Dissecting DNS Defenses)

  * 以GPDNS为例，8.8.8.8 就是谷歌公共解析器的anycast IP，只要向他发送请求，都会转到google的DNS’s的pop点。
  * PoP点在地理位置上实际是全球分布的（distributed geographically around the globe）
    * This paper's experiments proves that PoPs operate their caches independently.
  * As of May 2020， GPDNS has 33 PoPs worldwide; Cloudflare has 46 PoPs in U.S; Quad9 has 27 PoPs in US;OpenDNS has 11 PoPs in the U.S & Canada

* Step2：**Within a PoP, a query is load-balanced to a pool of frontend caches for the backend caching DNS resolvers.**[如文中图1所示，**进入公共解析器后，首先基于缓存的负载均衡，在缓存池中选择一个cache**] 

  * ref-原文ref17:**Passive Observations of a Large DNS service:2.5 Years in the Life of Google**
    * 这篇引用文献分析了GPDNS的2.5年，共37亿条请求得到如下结果（abstract）：
      * 1st：GPDNS has PoPs in many countries，traffic is frequently routed out of country
      * 2nd：end user are often served by suboptimal Pop

  * 进入公共解析器后，load balancer selects from the pool of frontend caches 基于多个缓存的负载分布。

* Step3：如果选择的缓存不包含所查询的域名，则这个查询会通过第二个负载均衡器被导入backend resolver，公共解析器下第二层的backend resolver每个也有自己的缓存，

* **PS：在执行完前面3步，或者 public DNS 递归的获得响应后，会保留缓存的3个地方：1）fronted cache pool 2）back resolver自己的cache中都会保留下缓存记录； 3）user侧自己的local cache**

## Snooping PDNS caches can provide a lower-bound on the number of active users 

* 统计PDNS中有多少缓存包含了特定的域名，那么就能估计一个该域名同时访问的active 用户数量。
  * **这个active user 是否也可以作为替换探测命中率的思路？**
  * rare domain 在每一个cache中有，则表示对这个域名至少有一个active user【因此是lower-bound】
  * 按说一个城市的市政府网站，也就在那个城市的人会进行访问，也算是rare domains，popularity 可以用来对比几个domain 在这台服务器上的访问数量
* 

# 配置了CDN的DNS服务器缓存探测的影响

## 具体现象

* 执行的测试命令：dig www.buenosaires.gob.ar a @114.114.114.114
* 执行的测试设备
  * 上海云服务器：106.14.209.62
  * 成都服务器：22
* 执行结果：
  * 上海地区的ttl基本维持在3600及以下
  * 成都的服务器,则会出现43200等更长的ttl

## 可能的原因分析

**在使用CDN的DNS服务器时，缓存行为通常会因为地理位置不同而有所不同**，因为CDN的DNS解析会根据不同的节点和服务器来优化响应速度，进而导致不同的ttl。

* **地理位置差异：**

  - **CDN分布：** CDN通常会根据地理位置部署多个节点来加速内容分发。当请求来自不同地区时，CDN会选择最接近的服务器进行响应，这可能导致TTL的不同。
  - **本地缓存：** 上海和成都的CDN节点可能具有不同的缓存策略。例如，上海的CDN节点可能缓存时间较短（3600秒以内），而成都的CDN节点可能因为缓存更新的策略，缓存时间更长（如43200秒）。

  **DNS解析策略：**

  - **本地DNS缓存：** 各地的DNS服务器缓存策略不同，也可能影响TTL的设置。上海地区的DNS服务器可能配置了较短的TTL，而成都的可能为了减少频繁的DNS查询，设置了更长的TTL。
  - **CDN负载均衡：** 如果<u>CDN节点检测到某些节点负载较高，可能会返回带有较长TTL的记录，以减少流量压力</u>，或者根据流量优化策略调整TTL。

  **CDN的缓存刷新机制：**

  - CDN服务提供商可能会<u>根据不同地区的流量和需求调整缓存更新的频率</u>。成都节点可能会有较少的请求频率，因此它设置了较长的TTL。

  **中间DNS缓存：**

  - 如果DNS查询过程中经过了多个中间DNS服务器（如ISP的DNS服务器），这些中间DNS服务器可能会缓存TTL较长的记录，从而影响最终的TTL。

## 如何判断一个服务器是否为CDN服务器








------

