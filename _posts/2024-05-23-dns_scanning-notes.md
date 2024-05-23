---
title: 'Git-command'
date: 2024-05-23
permalink: /posts/2024/05/dns-scanning/
tags:
  - Real Work Practice
---

DNS 各类服务信息的扫描、收集。

# 本地测试环境

## centos服务器基于bind9搭建dns服务器

* ip：172.16.151.41
* 操作系统：centos7，[centos7搭建bind参考](https://www.kancloud.cn/wenshunbiao/wenshunbiao/871609)
  * ps：若除本机外都访问不了，则大概率是防火墙的问题（测试情况是：firewalled没有添加规则）
  * 若修改配置之后，需执行后续命令重新启动服务加载配置：service named restart 

## 测试环境域名数据配置

* 测试域：仅配置 yumaozdy.com 
  * zone 文件夹中配置：www.yumaozdy.com
* 测试命令：dig www.yumaozdy.com @172.16.151.41

## 预期效果

* 服务器配置成功后，执行[测试命令](dig www.yumaozdy.com @172.16.151.41)，**指定解析服务器后**，看到根区文件配置的数据。
* [**不指定解析服务器**](dig www.yumaozdy.com)，则基于/etc/resolve.conf 中的nameserver配置得到真实情况的响应结果。

# 转发器

* 定义：这台DNS发现非本机负责的查询请求时，不再向根域发起请求，而是直接转发给**指定的**一台或者多台服务器。自身并不缓存查询结果。[参考](https://www.cnblogs.com/kebibuluan/p/15033442.html)
  * **此定义需要相对于某个域名来说，而非单独的是否是递归服务器，间接解析器也需要针对特定的域名来说**

* 准确判断方式

  * vim /etc/named.conf 中是否配置了forwarders, 如果有则该DNS服务器被配置为转发器。

  *  vim /etc/named.rfc1912.zones 中zone的type是否为forward；若是，则该区域将被视为转发区域。示例：

    ```
    zone "example.com" {
      type forward;
      forwarders { 8.8.8.8; 8.8.4.4; }; // example.com 区域被配置为转发区域，任何对该区域的查询都将被转发到指定DNS服务器。
    };
    ```

## 测试步骤

* /etc/named.conf中配置了forwarder{223.5.5.5;}的情况为第一次查询，去掉配置后为第二次查询，对比两者结果不同。

* 测试命令：dig www.baidu.com @172.16.151.41 **41测试服务器中仅配了yumaozdy.com的域名，baidu.com 会被转发**

* 测试结果：

  * 配置了forwarder的情况，能正常解析。
  * 去掉forwarder后，无法获得解析结果。

  <img src="/images/img/bind未配置域名是否配置转发的解析结果.png">

  <img src="/images/img/是否本服务器负责解析的域名测试结果.png">

## 转发器与间接解析器的区别

<img src="/images/img/转发器与间接解析器的区别.png">

* 是否提前配置了转发目标来确定，配置了就是转发器，没配置就是间接解析器。

# 间接解析器

## 间接解析器的定义

<img src="/images/img/间接解析器的定义.png">

* 类似于转发器的定义，间接解析器也是**针对于特定的域名**来进行定义。

# dig 命令查询bind服务器版本号

* [参考1](https://cloud.tencent.com/developer/article/1526792)  、[参考2](https://www.wallcopper.com/network/879.html)

  * **说明：若无输出则表示版本信息被隐藏。**

* dig查询bind版本号命令：

  * dig CHAOS TXT version.bind @ns-server
  * dig -t txt -c chaos VERSION.BIND @ns-server

* 测试结果：根据本地测试环境搭建的bind服务器，执行命令进行测试：

  * dig +noall +answer txt chaos VERSION.BIND @172.16.151.41

    <img src="/images/img/dig查询bind版本结果.png">

# dns服务器是否配置了dnssec

* dnsrecon库
  * 安装：pip3 install dnsrecon
* 




------

