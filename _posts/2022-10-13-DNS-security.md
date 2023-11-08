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
* [Brief Intro1](https://www.shangyexinzhi.com/article/6844502.html)：DOH、隐蔽隧道工具等综述类介绍。

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

# DOH

## 相关背景

* 2018, DOH was released 【enhance DNS performance + improve user privacy】
* DoH wraps DNS records(both requests and responses) in an HTTPS connection, providing 

### 与传统DNS解析相比

* DOH 通过443端口的加密HTTPS连接接收DNS查询将其发送到兼容DOH的DNS解析服务器，不是在53端口发送纯文本。【DOH在常规HTTPS流量中隐藏DNS查询】
* 基于443端口发出，DOH就会在常规HTTPS流量中隐藏DNS查询，避免**第三方监听者嗅探流量**。

### 三大使用方式

* 本地系统安装DOH代理：installing a proxy on a local system
* 应用加装DOH:implementing DOH within an application
* 本地DNS服务器加装doh代理：installing a proxy on the local name server

### DOH 恶意行为

DoH虽然具备绝佳的隐私保护能力和安全能力获得用户的青睐，也由于 **DoH被用于隐蔽隧道攻击而遭到政府机构和安全机构的警惕关注** 。

* 利用DOH的首款恶意软件：[Godlua](https://www.jianshu.com/p/8d573b0987c7)
* 利用DOH实施数据外传的APT组织apt34

## 工作方式

<img src="/images/img/DOH工作方式.png">

* DoH允许服务端先把DNS响应push给客户端（早于客户端发起DNS请求），降低DNS服务时延，改善网络应用的性能。【以上图DOH工作方式为例，若DOH为代理，可早于client查询请求到代理443之前现象DOH解析服务器发送请求，不必等待第一步。】
* **DoH将DNS请求和响应封装到HTTP请求的主体**。
* 客户端跟递归服务器之间建立一个**TLS会话，通过HTTPS协议传输封装了DNS请求的HTTP请求**。

基于DoH协议构建隐蔽隧道，可实现：

* 通信内容可**基于HTTPS协议加密**。
* **与高可信DoH服务通信**（非本地DNS服务器）不会引发异常行为，**避免基于DNS的恶意行为检测机制**。

# DOH Convert Channel Detection

## paper1：DNS流量识别+隧道+BOTNET检测

[Encrypted Covert DNS Queries for Botnets: Challenge and Countermeasures](https://arxiv.org/abs/1909.07099)

### 源码

[仅包含shell脚本](https://github.com/kpatsakis/covert_dns_queries)

### 背景+假设+focus

* Patsakis,2019,key point: traffic analysis【基于DNS隧道的DGA和僵尸网络检测】
* **之前的工作假设**：被控机需要使用生成域名连接C&C server【真实C&C server 被藏在大量生成域名之中】，因此在此过程可以阻断DNS请求，阻断之后不断尝试请求且解析失败的机器即为被控机。【**攻击者dns请求信道不会加密**】
* **Assumption**: DNS query performed by a compromised device are **transparent** to the network administrator and therefore can be monitored,analysed, and blocked.
  * 本文假设：**<u>已有被控主机</u>**，控制主机向被控主机**通过其他协议的tunnel传输加密后包含想要传输的信息部分的DNS请求**。
  * **不选择DNSCrypt 和 DNSCurve的原因：容易被防火墙检测并封禁。**
* **Focus**：The adversary uses DGA generates millions of pseudo-random domains
* **Contribution for this paper**：
  * 本文假设：botnet使用**DNS加密机制**和C&C server 通过注册白名单域名通信  & 并提出可行检测方式。
    * 实验证明：traffic analysis on the exchanged packets can led to very efficient detection.
    * **Hodrick-Prescotter filter**(HP滤波) can accurately classify bot-net based on DoH using a small amount of samples.

### 数据集

* synthetic dataset：[Alexa top1000 ](https://github.com/andrewaeva/DGA) registered domain+ [10类 DGA](https://github.com/andrewaeva/DGA) 生成的各1k non-registered domain。

  * 数据特征表：各个数据集名称、domain长度的min、max、average、stdev

    PS: unique value = max-min+1 【域名数据可以存在的长度最大数量】

  | dataset      | min  | max  | average | stdev | unique values |
  | ------------ | ---- | ---- | ------- | ----- | ------------- |
  | Alexa        | 4    | 28   | 11.349  | 3.237 | 22            |
  | Conflicker   | 8    | 16   | 11.755  | 1.983 | 9             |
  | CryptoLocker | 15   | 21   | 17.783  | 1.424 | 7             |
  | GOZ          | 20   | 35   | 28.241  | 2.431 | 16            |
  | Matsnu       | 28   | 40   | 30.527  | 2.038 | 13            |
  | new GOZ      | 26   | 32   | 29.885  | 1.087 | 7             |
  | Pushdo       | 11   | 11   | 11      | 0     | 1             |
  | Ramdo        | 20   | 20   | 20      | 0     | 1             |
  | Rovnix       | 24   | 38   | 26.794  | 2.622 | 15            |
  | Tinba        | 16   | 16   | 16      | 0     | 1             |
  | Zeus         | 26   | 32   | 29.878  | 1.038 | 7             |

  * Alexa 和 各类DGA，均取前1k个域名【共11000 domains of existing and non-existing domain】

### 实验步骤

**数据集模拟**

* **pydig**: 获取上述11个dataset的域名后，模拟DOH 请求(隐藏后的DNS请求)。【pydig测试完成】
* tcpdump：产生模拟流量的pcap文件，包含所有的流量包。
* tshark：过滤所有pcap文件中DOH相关的packet.
* 特征提取：parse pcap file and perform feature  extraction on each packet.
* **特征：sourceIP、targetIP、size of  each packet、protocol、tshark info**

**时序分析-Hodrick-Prescott(HP) filter**

* 通过短期价格波动的重要性来确定时间序列长期增长趋势。【最终目标，获得时序情况下的数据集特征的趋势】
* HP 滤波实验容易，但只有在严苛条件下才能做出最优估计：
  * 时间序列是二阶整合，否则HP滤波会得到偏离实际情况的趋势项。
  * 如果发生了单次的永久性冲击（permanent shock）或存在稳定的趋势增长率，HP滤波得到的周期项也会扭曲。
  * 样本中的周期项是白噪音，或者趋势项和周期项中的随机变化机制相同。
* **python实现：d-table** 

### 目标

构建high quality Indicator of compromise(失陷指示器) IoC 来实现利用DOH传递被控信息的bot检测。

### 结果

* By running ARMA(AutoRegressive Moving Average) estimation over all series. 获得当前时刻及之前4个时刻，1类正常+10类DGA的 coefficients
* Use ARMA coefficients as IoC，after prove each tuple can uniquely identify the bot。【Testing whether statistical difference between the different coefficients exis】

**ARMA-自回归移动平均**

* 时间序列预测&分类。
* python库：from statsmodels.tsa.arima.model import ARIMA

## paper2：基于时序的DOH隧道检测

[An Anomaly Detection Framework forDOH Tunnel Using Time-series Analysis](https://unbscholar.lib.unb.ca/items/494d0c85-2a33-45bf-ad7a-557532dd8779)

### 背景&假设

* **simulate DOH tunnel**：simulated environment covers : DOH within an application、DOH proxy on the name server in the local network、DoH proxy on a local system。

* **two-layer approach**：
  
  capture malicious and benign DoH traffic 
  
  * layer1：characterize DOH traffic from all traffic.
  * layer2：classify bengin & malicious traffic.
  
* Statistical feature: **Random Forest & Decision Tree** give the best classification and characterization results among prominent machine learning and deep learning classifiers at 2 layers.

* Time-series feautures: **LSTM** turns out to be the best classifier for DoH traffic classification and characterization at 2 layers.

* 本文回顾所有DNS攻击并关注与DOH相关的攻击，重点在于DOH三大使用方式的区别。

### DOH making DNS tunnels harder to detect * Page3

* DNS 将DNS traffic 放入 HTTPS中，使得DNS traffic在网络基础设施(如：防火墙)中难以被识别，导致之前的**“基于防火墙检测DNS packet中是否含有恶意域名、恶意信息等 ”**的方法过时。【防火墙不检验DNS内容和访问频率】
* DOH 推荐使用HTTP/2作为最小版本，malware 能使用http/2 **“一次连接传输多个doh请求和响应，隐藏frequency of DNS resolution",**  进一步减少探测DNS tunnel的方法。

### Contributions * 

* [Labeled dataset]():Including Bengin-DOH、Malicious-DOH、Non-DOH

* feature-based DOH anomaly detection framework: using time-series representation of traffic flow.

### Convert DNS Channel page12

**信息传入传出**

* **向外传输**的信息：采用一定的加密方式（如base32）加密后放入请求域名的sub-domain，传到被控DNS resolver中【**每次长度不超过253字节，域名的最大长度**】。多个请求合并后得到完整信息。
* **向内传输信息or命令**：通过base64或类似加密方式，放入DNS response的 TXT记录中.

**Simulation**

[Simulation ref2 paper2](https://unbscholar.lib.unb.ca/items/494d0c85-2a33-45bf-ad7a-557532dd8779): upgraded version of the traditional DNS tunnels that are already abused by malware as a convert method of communication.



## 实验步骤小结

* 模拟DOH 请求  * 
* 获取域名数据集
* 抓包doh请求获得流量pcap包
* 完成doh流量识别后，进一步区分这些DOH流量是否为隐蔽隧道攻击
  * TLS 指纹技术：实现DOH识别及隧道检测基础技术【在https客户端和服务端握手阶段，对**明文**数据包进行识别得到什么应用发起的https连接。】
    * CISCO 通过大规模TLS流量分析得到恶意软件；实际情况下的复杂场景，TLS分类器性能会下降。

## related works conclusion

**DGA detection Related works**：【除1以外都是通过DNS检测DGA的】

* Fast Flux approach 模拟CDN改变解析到自控DNS解析服务器的域名对应的ip信息防止被封【同时降低记录TTL，强制被控机定时进行请求改变对应ip】[ref1](T. Holz, C. Gorecki, K. Rieck, F. C. Freiling, Measuring and detecting fast-flux service networks, in: Proceedings of the Network and Dis-
  tributed System Security Symposium, 2008.) [ref2](O. Katz, R. Perets, G. Matzliach, Digging deeper - an in-depth analysis of a fast flux network, https://www.akamai.com/us/en/multimedia/
  documents/white-paper/digging-deeper-in-depth-analysis-of-fast-flux-network.pdf (2016))
* 判定域名是否属于DGA生成特征：entropy、length、lexical characteristics、whois、DNS 流量分析观察异常响应。[DNS traffic detect DGA](Y. Zhou, Q.-S. Li, Q. Miao, K. Yim, DGA-based botnet detection using DNS traffic, J. Internet Serv. Inf. Secur. 3 (2013) 116-123.) [Using DNS failure graph analysis to identify suspicious activity](N. Jiang, J. Cao, Y. Jin, L. E. Li, Z. Zhang, Identifying suspicious activities through dns failure graph analysis, in: The 18th IEEE International Conference on Network Protocols, 2010, pp. 144-153.) [throw-away traffic to bots](M. Antonakakis, R. Perdisci, Y. Nadji, N. Vasiloglou, S. Abu-Nimeh,W. Lee, D. Dagon, From throw-away trac to bots: detecting the rise of DGA-based malware, in: Proceedings of the 21st USENIX conference on Security symposium, USENIX Association, 2012, pp. 24-24.)
* 图推断检测问题：construct a host-domain graph from **proxy logs** to classify domains into benign or malicious with probability。[ref](P. K. Manadhata, S. Yadav, P. Rao, W. Horne, Detecting malicious domains via graph inference, in: M. Kuty lowski, J. Vaidya (Eds.),Computer Security - ESORICS 2014, Springer International Publishing, Cham, 2014, pp. 1-18.)
* 基于时间序列的信息进行聚类：[ref](Y. Gong, S. Qitian, Z. Zhang, A DGA odyssey PDNS driven DGA analysis, https://pc.nanog.org/static/published/meetings/NANOG71/1444/20171004_Gong_A_Dga_Odyssey__v1.pdf (2017))
* Detect APT malware infection based on malicious DNS and traffic analysis [ref](G. Zhao, K. Xu, L. Xu, B. Wu, Detecting APT malware infections based on malicious DNS and trac analysis, IEEE Access 3 (2015) 1132-1142.)
* [domain shadowing](D. Liu, Z. Li, K. Du, H. Wang, B. Liu, H. Duan, Don't let one rotten
  apple spoil the whole barrel: Towards automated detection of shadowed domains, in: Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, CCS '17, ACM, New York, NY, USA, 2017, pp. 537-552.):based on previously hacked domain.

**DGA检测方法**：【无法检测加密通信】

* [binary classification: LSTM+raw domain names as features](D. Tran, H. Mac, V. Tong, H. A. Tran, L. G. Nguyen, A lstm based framework for handling multiclass imbalance in dga botnet detection, Neurocomputing 275 (2018) 2401-2413.)
* [GAN](): 基于GAN生成的域名能够骗过之前的检测模型，同时生成器生成的域名能优化模型检测准确度。
* [smashword score](R. R. Curtin, A. B. Gardner, S. Grzonkowski, A. Kleymenov, A. Mos-
  quera, Detecting DGA domains with recurrent neural networks and side
  information, arXiv preprint arXiv:1810.02023): n-gram overlapping + whois lookup info 
* [恶意域名检测综述](Y. Zhauniarovich, I. Khalil, T. Yu, M. Dacier, A survey on malicious do-
  mains detection through DNS data analysis, ACM Computing Surveys 51 (4) (2018) 67:1{67:36.)：

* **DNS tunnel**：数据加密成DNS请求和响应绕过检测。
  * [Feederbot](C. J. Dietrich, C. Rossow, F. C. Freiling, H. Bos, M. Van Steen,N. Pohlmann, On botnets that use DNS for command and control, in: 2011 seventh european conference on computer network defense, IEEE,2011, pp. 9-16.) & [Morto](3https://www.symantec.com/connect/blogs/morto-worm-sets-dns-record) 使用TXT记录传输加密后的数据和命令。


------

