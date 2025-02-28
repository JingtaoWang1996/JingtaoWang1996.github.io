---
title: 'DNS cache probing'
date: 2025-02-25
permalink: /posts/2025/02/DNS-cache-probing/
tags:
  - Real Work Practice
---

DNS缓存探测相关内容：

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

  ## 具体原因-见Trufflehunter的文章

# Paper1：Trufflehunter: Cache Snooping Rare Domainsat Large Public DNS Resolvers

* [source code](https://github.com/ucsdsysnet/trufflehunter)：探测大型DNS公共解析器缓存方式

## target：大型DNS公共解析器缓存的方式

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
* 复杂的多级、负载均衡缓存结构无法让我们能够进行**准确估计**包含某个域名的缓存数量
* **一次探测只能知道一个缓存在一个Pop点的缓存情况（但无法知道是哪个缓存or哪个Pop点）**
  * 同时也不知道这个cache是frontend cache，a backend cache or both （如果两者配置了同步机制的话）
  * Cache entry is shared between caches？
* 

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

### 缓存探测方式

* Most direct way of snooping a cache ：query a domain with RD flag unset **dig +norecurse example.com **

  * 这样的结果能够防止step3中的backend resolver发起递归解析，从而只查询step2中front cache & backend resolver独立缓存中的cache。【结果如文中图2所示】

    * cache hit：若响应的**answerSection**中包含非零ttl，则表示当前缓存命中

    

* 

## Snooping PDNS caches can provide a lower-bound on the number of active users 

* 统计PDNS中有多少缓存包含了特定的域名，那么就能估计一个该域名同时访问的active 用户数量。
  * **这个active user 是否也可以作为替换探测命中率的思路？**
  * rare domain 在每一个cache中有，则表示对这个域名至少有一个active user【因此是lower-bound】
  * 按说一个城市的市政府网站，也就在那个城市的人会进行访问，也算是rare domains，popularity 可以用来对比几个domain 在这台服务器上的访问数量

## How to analyzed and modeled resolvers's caching aritectures

* When a resolver operate independent caches, **primary indicator that a response is coming from a particular cache is the TTL in the response**
  * **请求使得响应的缓存被填满：maximum TTL（TTL returned by the 权威服务器）**
  * TTL 能够揭示从哪个缓存提供的服务：**因为ttl每秒会-1，那么间隔N秒收到的响应，且ttl也有N秒的差异，则表示来自同一缓存**

## 缓存估计方式

* 多次进行非递归探测后，观察ttl的值落在几条TTL line上，可以确定目标缓存服务器中有多少个缓存包含这个域名
  * TTL line：
* 三种不同的frontend cache architecture【**每一种不同的结构都会带来缓存上的差异**】
  * OpenDNS 、Quad9：缓存没有共享的，因此会出现多条ttl line
  * Cloudflare:[Introducing DNS resolver 1.1.1.1](O´ lafur Guðmundsson. [n.d.]. Introducing DNS Resolver, 1.1.1.1 (not a joke).
    https://blog.cloudflare.com/dns-resolver-1-1-1-1/.[):  shared frontend cache、use knotDNS‘s resolver（这个类型的resolver有一个shared backing database for its frontend cache）
    * 这个结构的问题：the lower-bound of number of users accessing a domain on Cloudflare will be very conservative-**At most one user within a TTL interval at a POP**
    * 根据实验结果，向1.1.1.1请求的域名，最终会回到一条ttl线上。【这种share one cached，反而能够通过ttl进行估计】
  * GPDNS[GPDNS: performance benifit](Google. 2018. Google Public DNS: Performance Benefits. https://developers.
    google.com/speed/public-dns/docs/performance?hl=zh-cn[): load-balanced-frontend cache and backend resolvers
    * 当一个请求在一个frontend cache中没有获得目标域名的记录，那么GPDNS就会创建一个新的独立frontend cache【动态缓存创建】
    * 根据文章中图6的实验结果可知，大部分请求的解析都是在同一个ttl，但同时也还有其他没在这个ttl line上且也不是新开一个max_ttl的line的东西。[ref1-原文59引用](Peeling the Google DNS Onion)   [ref2-原文62引用](On Measuring the Client-Side DNS Infrastructure)  这篇文章里的也没有说清楚原因，且ref了前面两个引用
      * 原文59的这种引用，还有被称为ghost cache的情况，且使用了词汇 “unexplained”
    * **GPDNS的策略：frontend caches在 recursive 和 non-recursive的情况下，都会将数据填入新的 frontend cache**

# Paper2: DNSScope: Fine-Grained DNS Cache Probing for Remote Network Activity Characterization

* [source code](https://github.com/DNSScope/DNSScope/tree/main?tab=readme-ov-file):

## target: 构造了一个DNSScope工具用于探测目标网络的时间特性

* we advance DNSScope，a fine-grained DNS cache probing framework by tackling three challenges：sample sparisity、observational distortion（观察扭曲），cache entanglement（缓存纠缠）
  * DNSScope工具综合 “统计学习”、“自监督迁移学习” 来得到获得网络的**时序迁移特征**。
  * 此工具能够较准确的获得时变的 **DNS query arrival rates** on recursive DNS resolvers.
* **CRI： cache refresh interval    &      QAR:  query arrival rate** 
  * 一个域名越频繁的在一个RDNS上被请求，那么这个域名对应的CRI越小，同时对应这个域名的popularity越高。
  * 当一个域名的ttl较大时，在一个small time window 中，CRI通常非常稀疏，甚至是仅为1.
* DNS cache probing与被动流量分析的优势：privacy-preserving   & 更轻量化

### 关于Cache entanglement

* **A real-world RDNS resolver may deploy multiple caches behind it for load balancing [20-22]. Query for the same domain name are served by diffrent caches.**
  * Therefore，the remaining TTL values of the same domain in different caches may be inconsistent
  * [9-11] 包括之前看过的Geographic web usage estimation by monitor dns caches文章中提到的方法无法区分具体响应是来自哪个缓存。
* 解决方法-**anchor-port probing**
  * **对探测包设定不同类型的源端口。对于包含特定源端口的探测包将会被确定性分配到特定的缓存当中。**
  * anchor port probing 将探测包的
* 因此，具有特定源端口的探测数据包将确定性地分配给特定缓存。我们枚举不同的源端口以覆盖 R-DNS 解析器上的所有缓存，并为每个缓存提取 CRI？【**源端口一定的探测包，RDNS一定会交给某个固定缓存进行解析吗？】**
  * **anchor-port probing 将探测包的source port 与到达的RDNS的具体缓存进行映射**，source port 到 cache的mapping有两种 **Empirical measurement**
    * Persistent mapping：**源ip、源端口、域名一致的探测包会被映射到相同的缓存？？？这个需要确定**
    * one-off mapping：两个连续的探测包，如果源ip、源端口、域名一致且探测时间在一定threshold内，则会被分配到相同的cache
  * 
* anchor-port probing + different strategies = probe multi-cache RDNS resolver.

## 和之前方式的比较

* 之前的方法：
  * 计算目标域名在目标服务器上的平均 QAR，基于缓存刷新间隔CRI+较长时间的数据分析。
  * 无法获得这段观测时间内随随时间变化的请求特征。
* 当前方法：关注随时间变化的请求特征。

## 探测方式

* one can send non-recursive DNS queries to an RDNS resolver to ask it to return an answer **based on its cache entries（缓存条目）**
* By sending **non-recursive** DNS query to an RDNS **periodically，cache refresh intervals can be observed**
* 计算QAR for **domain names of interests**
  * 主动探测一定有一个域名列表需要给出，然后域名列表关联到城市。
* 本文通过在一个包含5w个用户的网络中进行Anderson-Darling test(验证数据集是否服从正态or指数分布)
  * conclusion：0.95 confidence that DNS query intervalss of 86.1%的domains 是**分段指数分布**。==》DNS query arrivals can be reasonably modeled as a 具有时变的非齐次泊松分布

## DNSScope-DNS cache probing阶段

* 图2提到的结构分为2个阶段，第一部分DNS cache probing是为关注对象。
* DNSScope probes remote RDNS resolver and **continuously tracks（还是需要持续进行监测目标RDNS上的目标域名） the cache state changes for domain name of interests to extract CRIs.(每个城市一个域名方便映射)**
* 对于不同类型的RDNS，DNSScope 采用不同的策略进行探测，解决cache entanglement问题。
* 

# Paper3:  DNS cache-based user tracking



# 其他文章

* 《Inferring Relative Popularity of Internet Applications by actively Querying DNS Caches》
  * 分析方法
    * method1: simply **determine the cache hit rate over the period of time.** [2003 年的文章，和之前的初步想法一致，目标是LDNS，没有考虑多层结构的ttl不同的情况]
    * method2：分析cache gap，但目标是他们学校的服务器，从日志分析，这个就变成了流量分析。
  * 
* 




------

