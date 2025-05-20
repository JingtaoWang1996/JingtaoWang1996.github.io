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
* Zone transfer often used in large organizations and especially important for multiple servers

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

* **Protection I -Only allow trusted-nameservers****【DNS 配置中进行设置】**

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

## How to make a DNS zone transfer test 

* dig 命令获取目标域名的所有权威服务器

  ```
  $ dig +short ns amazon.com
  ns1.amzndns.co.uk.
  ns1.amzndns.com.
  ns1.amzndns.org.
  ns2.amzndns.net.
  ns2.amzndns.org.
  ns2.amzndns.com.
  ns2.amzndns.co.uk.
  ns1.amzndns.net.
  ```

* 使用dnsrecon进行探测: linux 默认安装了dnsrecon，可以先直接执行dnsrecon确认是否已安装

  * dnsrecon同时配置了brute force的字段功能，比dig方便

  ```
  $ dnsrecon amazon.com
  dnsenum VERSION:1.2.6
  
  -----   amazon.com   -----
  
  
  Host's addresses:
  __________________
  
  amazon.com.                              900      IN    A        205.251.242.103
  amazon.com.                              900      IN    A        54.239.28.85
  amazon.com.                              900      IN    A        52.94.236.248
  
  
  Name Servers:
  ______________
  
  ns2.amzndns.co.uk.                       10       IN    A        204.74.120.1
  ns1.amzndns.co.uk.                       3421     IN    A        156.154.67.10
  ns1.amzndns.com.                         2757     IN    A        156.154.64.10
  ns1.amzndns.org.                         10       IN    A        156.154.66.10
  ns1.amzndns.net.                         10       IN    A        156.154.65.10
  ns2.amzndns.com.                         2664     IN    A        156.154.68.10
  ns2.amzndns.org.                         10       IN    A        156.154.150.1
  ns2.amzndns.net.                         10       IN    A        156.154.69.10
  
  
  Mail (MX) Servers:
  ___________________
  
  amazon-smtp.amazon.com.                  10       IN    A        3.222.250.144
  
  
  Trying Zone Transfers and getting Bind Versions:
  _________________________________________________
  
  
  Trying Zone Transfer for amazon.com on ns2.amzndns.co.uk ...
  AXFR record query failed: REFUSED【正常情况进行了配置的部分是会对于之前的name servers跳出拒绝AXFR】
  
  ```

* dig命令也可以请求axfr记录

  ```
  $ dig @ns2.amzndns.com. amazon.com axfr
  ; <<>> DiG 9.18.30-0ubuntu0.22.04.2-Ubuntu <<>> @ns2.amzndns.com. amazon.com axfr
  ; (2 servers found)
  ;; global options: +cmd
  ; Transfer failed. 【如果成功进行了传输，则会打印出信息】
  ```



### zone transfer 成功的情况-zonetransfer.me

* **dig ns zonetransfer.me +short**

  ```
  $ dig ns zonetransfer.me +short
  nsztm1.digi.ninja.
  nsztm2.digi.ninja.
  ```

* **dig @nsztm1.digi.ninja zonetransfer.me axfr**

  ```
  ; (1 server found)
  ;; global options: +cmd
  zonetransfer.me.        7200    IN      SOA     nsztm1.digi.ninja. robin.digi.ninja. 2019                                                                                                                                                                100801 172800 900 1209600 3600
  zonetransfer.me.        301     IN      TXT     "google-site-verification=tyP28J7JAUHA9fw                                                                                                                                                                2sHXMgcCC0I6XBmmoVi04VlMewxA"
  zonetransfer.me.        7200    IN      MX      0 ASPMX.L.GOOGLE.COM.
  zonetransfer.me.        7200    IN      MX      10 ALT1.ASPMX.L.GOOGLE.COM.
  zonetransfer.me.        7200    IN      MX      10 ALT2.ASPMX.L.GOOGLE.COM.
  zonetransfer.me.        7200    IN      MX      20 ASPMX2.GOOGLEMAIL.COM.
  zonetransfer.me.        7200    IN      MX      20 ASPMX3.GOOGLEMAIL.COM.
  zonetransfer.me.        7200    IN      MX      20 ASPMX4.GOOGLEMAIL.COM.
  zonetransfer.me.        7200    IN      MX      20 ASPMX5.GOOGLEMAIL.COM.
  zonetransfer.me.        7200    IN      A       5.196.105.14
  zonetransfer.me.        7200    IN      NS      nsztm1.digi.ninja.
  zonetransfer.me.        7200    IN      NS      nsztm2.digi.ninja.
  zonetransfer.me.        300     IN      HINFO   "Casio fx-700G" "Windows XP"
  _acme-challenge.zonetransfer.me. 301 IN TXT     "6Oa05hbUJ9xSsvYy7pApQvwCUSSGgxvrbdizjePE                                                                                                                                                                sZI"
  _sip._tcp.zonetransfer.me. 14000 IN     SRV     0 0 5060 www.zonetransfer.me.
  14.105.196.5.IN-ADDR.ARPA.zonetransfer.me. 7200 IN PTR www.zonetransfer.me.
  asfdbauthdns.zonetransfer.me. 7900 IN   AFSDB   1 asfdbbox.zonetransfer.me.
  asfdbbox.zonetransfer.me. 7200  IN      A       127.0.0.1
  asfdbvolume.zonetransfer.me. 7800 IN    AFSDB   1 asfdbbox.zonetransfer.me.
  canberra-office.zonetransfer.me. 7200 IN A      202.14.81.230
  cmdexec.zonetransfer.me. 300    IN      TXT     "; ls"
  contact.zonetransfer.me. 2592000 IN     TXT     "Remember to call or email Pippa on +44 1                                                                                                                                                                23 4567890 or pippa@zonetransfer.me when making DNS changes"
  dc-office.zonetransfer.me. 7200 IN      A       143.228.181.132
  deadbeef.zonetransfer.me. 7201  IN      AAAA    dead:beaf::
  dr.zonetransfer.me.     300     IN      LOC     53 20 56.558 N 1 38 33.526 W 0.00m 1m 100                                                                                                                                                                00m 10m
  DZC.zonetransfer.me.    7200    IN      TXT     "AbCdEfG"
  email.zonetransfer.me.  2222    IN      NAPTR   1 1 "P" "E2U+email" "" email.zonetransfer                                                                                                                                                                .me.zonetransfer.me.
  email.zonetransfer.me.  7200    IN      A       74.125.206.26
  Hello.zonetransfer.me.  7200    IN      TXT     "Hi to Josh and all his class"
  home.zonetransfer.me.   7200    IN      A       127.0.0.1
  Info.zonetransfer.me.   7200    IN      TXT     "ZoneTransfer.me service provided by Robi                                                                                                                                                                n Wood - robin@digi.ninja. See http://digi.ninja/projects/zonetransferme.php for more inf                                                                                                                                                                ormation."
  internal.zonetransfer.me. 300   IN      NS      intns1.zonetransfer.me.
  internal.zonetransfer.me. 300   IN      NS      intns2.zonetransfer.me.
  intns1.zonetransfer.me. 300     IN      A       81.4.108.41
  intns2.zonetransfer.me. 300     IN      A       167.88.42.94
  office.zonetransfer.me. 7200    IN      A       4.23.39.254
  ipv6actnow.org.zonetransfer.me. 7200 IN AAAA    2001:67c:2e8:11::c100:1332
  owa.zonetransfer.me.    7200    IN      A       207.46.197.32
  robinwood.zonetransfer.me. 302  IN      TXT     "Robin Wood"
  rp.zonetransfer.me.     321     IN      RP      robin.zonetransfer.me. robinwood.zonetran                                                                                                                                                                sfer.me.
  sip.zonetransfer.me.    3333    IN      NAPTR   2 3 "P" "E2U+sip" "!^.*$!sip:customer-ser                                                                                                                                                                vice@zonetransfer.me!" .
  sqli.zonetransfer.me.   300     IN      TXT     "' or 1=1 --"
  sshock.zonetransfer.me. 7200    IN      TXT     "() { :]}; echo ShellShocked"
  staging.zonetransfer.me. 7200   IN      CNAME   www.sydneyoperahouse.com.
  alltcpportsopen.firewall.test.zonetransfer.me. 301 IN A 127.0.0.1
  testing.zonetransfer.me. 301    IN      CNAME   www.zonetransfer.me.
  vpn.zonetransfer.me.    4000    IN      A       174.36.59.154
  www.zonetransfer.me.    7200    IN      A       5.196.105.14
  xss.zonetransfer.me.    300     IN      TXT     "'><script>alert('Boo')</script>"
  zonetransfer.me.        7200    IN      SOA     nsztm1.digi.ninja. robin.digi.ninja. 2019                                                                                                                                                                100801 172800 900 1209600 3600
  ;; Query time: 188 msec
  ;; SERVER: 81.4.108.41#53(nsztm1.digi.ninja) (TCP)
  ;; WHEN: Tue May 20 10:18:47 CST 2025
  ;; XFR size: 50 records (messages 1, bytes 2085)
  
  ```

  



 





# Brute Force









# Reference

* Ref1: [Next Stop,the Cloud: Understanding Modern Web Service Depolyment in EC2 and Azure](https://pages.cs.wisc.edu/~rist/papers/nextstopcloud.pdf)
* Ref2: [Basic Intro](https://www.acunetix.com/blog/articles/dns-zone-transfers-axfr/)

* Ref3: [zone transfer attack & test](https://gokhnayisigi.medium.com/what-is-a-dns-zone-transfer-attack-and-how-to-test-it-12bdc52da086)








------

