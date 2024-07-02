---
title: 'Git-command'
date: 2024-07-01
permalink: /posts/2024/07/FullStackEngneering/
tags:
  - Notes
---

About Full Stack Engineers

# Intro

* 全栈的出现：web技术的发展和自然而然引发的分工。【A full stack web developer is someone that does design, markup, styling, behavior, and programming.】
* 全栈不是全能，**广泛的 Web 技术（包括网络、前端、后端 MVC、持久化技术等多个层次。）才是一名通常意义上的全栈工程师最该专注的核心内容**

# HTTP protocol history

## http/0.9

* 1991 年，HTTP 在最开始的 0.9 版就定义了协议最核心的内容，从功能上看只是具备了如今内容的一个小小的子集。
* 它非常简单，不支持请求正文，不支持除了 GET 以外的其它方法，不支持头部，甚至没有版本号的显式指定，而且整个请求只有一行，因而也被称为“The One-line Protocol”。比如：GET /target.html.

## http/1.0

*  1996 年，HTTP 1.0 版本就稳定而成熟了，也是如今浏览器广泛支持的**最低版本 HTTP 协议**。
* 引入了返回码，引入了 header，引入了多字符集，也终于支持多行请求了。方法只支持 GET、HEAD、POST 这几个。
* 每一组请求和响应的交互，都需要完成一次TCP的连接和关闭操作，在使用频率较低时没有暴露多大问题。
* 第一个具备广泛实际应用价值的协议版本。

## http/1.1--目前最广泛的协议

* 1999 年，著名的 RFC2616，在 1.0 的基础上，大量帮助传输效率提升的特性被加入。
* 从网络协议分层上看， TCP 协议在 HTTP 协议的下方（TCP 是在 OSI 7 层协议的第 4 层，而 HTTP 则是在最高的第 7 层应用层，因此，前者更加“底层”一点）。
* 采用**http长连接**：避免http1.0时候，每一组请求和响应的交互都需要完成一次TCP的连接和关闭操作。【长连接：打开一次TCP连接，可以被连续几次报文传输重用，减少资源占用和重复。】

* 长连接开启的情况下，使用content-length or Chunked 头。【Chunked头分块传输编码大大提高了HTTP交互的灵活性。】
* 其他: 更全面的方法、更全面的返回码、对指定客户端缓存策略的支持、对content negotiation的支持等。

## http/2

* 在http/1.1的基础上，保持兼容性的前提下包含以下重要改进：
  - ALPN机制: 允许客户端来选择使用的 HTTP 版本。
  - 支持HTTP 头的压缩：在 HTTP/2 以前，HTTP 正文支持多种方式的压缩，但是 HTTP 头部却不能。
  - 支持多路复用：允许客户端同时在一个连接中同时传输多组请求响应的方法。
  - 服务端将网页必要资源一次性 push 到客户端，而不是每次客户端确认缺什么再来索取，节约加载时间。

# HTTPS

* https出现的原因---基于http无法满足复杂的需求：数据加密传输的安全性需求、服务器消息即时推送的交互模式需求等。【因此，需要引入其他协议来：增强、填补HTTP协议所不擅长的空白领域；】

## SSL（Secure Socket Layer）/TLS（Transport Layer Security）

* 解决HTTP明文传输过程中存在的：拦截、伪装、篡改问题。
* HTTP + SSL/TLS = HTTPS
* 事实上一开始只有SSL，后来在SSL3.0之后，其被标准化并通过RFC2246以SSL为基础建立了TLS的第一个版本。

## 对称性和非对称性加密

* 对称性Symmetric Cryptograph：加解密使用相同的密钥。
  * 优点：简单、加解密速度快。
  * 缺点：加解密使用相同密钥，如何安全传递密钥是一个问题。
* 非对称性加密Asymmetric Cryptograph：数据加解密使用不同的密钥---**公钥public Key+私钥 private Key**。
  * 公钥、私钥同时生成：公钥可以公开和传播，私钥不能。
  * 经过公钥加密的数据需要私钥才能解密，反之亦然。
* 性能较差，但加解密的密钥相对独立，可以放心传播。

## TLS 连接建立原理

**TLS通过非对称加密技术来保证握手过程的可靠性；通过对称加密技术来保证传输过程的可靠性。**

* step1-Client Hello：客户端向服务端打招呼，并携带信息：**客户端产生的随机数A**、**客户端支持的加密方法列表**。

* step2-Server Hello：服务端向客户端回复，并携带信息：**服务端产生的随机数B**、**服务端根据客户端的支持情况确定出的加密方法组合Cipher Suite。**

* step3-Certificate，Server Key Exchange，Server Hello Done：服务端在打完招呼之后紧接着告知：

  * Certificate，证书信息（包含服务端生成的公钥）。
  * 客户端收到信息，验证证书有效后，公钥也就同样可信。接着客户端再生成一个**随机数C**（Pre-master Secret），此时共有的随机数A、B、C根据约好的加密方法组合生成**新的密钥X（Master Secret）**而由 X 可继续生成真正用于后续数据进行加密和解密的对称密钥。因为它是在本次 TLS 会话中生成的，所以也被称为会话密钥（Session Secret）。简言之：
    * 客户端随机数 A + 服务端随机数 B + 客户端 Pre-master Secret C → 会话密钥

* Step4-Client Key Exchange、Change Cipher Spec、Encrypted Handshake Message：接着客户端告诉服务端：

  - Client Key Exchange，本质上它就是上面说的这个 C，但使用了**服务端通过证书发来的公钥加密（上面是客户端发来的证书）**；
  - Change Cipher Spec，客户端同意正式启用约好的加密方法和密钥了，后面的数据传输全部都使用密钥 X 来加密；
  - Encrypted Handshake Message，快速验证：这是客户端对于整个对话进行摘要并加密得到的串，如果经过服务端解密，和原串相等，就证明整个握手过程是成功的。

  服务端收到消息后，用自己私钥解密上面的 Client Key Exchange，得到了 C，这样它和客户端一样，也得到了 A、B 和 C，继而到 X，以及最终的会话密钥。

* 于是，客户端和服务端都得到了能够加密解密传输数据的对称密钥——会话密钥。


------

