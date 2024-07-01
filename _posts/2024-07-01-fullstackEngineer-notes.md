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


------

