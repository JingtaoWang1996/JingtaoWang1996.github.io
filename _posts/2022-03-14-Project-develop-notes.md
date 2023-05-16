---
title: 'Project-develop-notes'
date: 2022-03-14
permalink: /posts/2022/03/Project-develop-notes/
tags:
  - cool posts
  - category1
  - category2
---

Some work experience on project developing.

# 关于测试

## 断点调试

* 不论java还是python的idea，都可以用debug模式进行断点调试

* 在代码前打上断点后，用**debug模式进入调试，方便看到每一个参数的具体值**
* 具体快捷键看设置

## 开发&测试&生产环境的差异

**测试和生产环境尽量一致，开发环境可以单独，但尽量一致**

具体遇到的问题记录如下：

* windows 2 linux
  * python代码放到Linux环境后，主函数意外的脚本定义的全局变量初始化时，可能出现无法调用的情况.[解决方式：尝试将该变量初始化定义到函数内部。]
  * windows selector 当中的eventloop 在linux当中相似，但最大取值不同。

## 性能测试

* 耗时：打印运行前后时间差（python：time.time();java: System.currentTimeMillis()）

* 压测：不是在常规条件下运行或测试，而是在资源匮乏的条件下进行测试，通常压测资源包括：内存，CPU, 磁盘空间和带宽.

## 测试类

**每一个功能（不论是接口还是具体功能）开发都需要一个独立的单元测试类（写在/Test****目录当中）**

Ps：测试完成后再合并，方便后续错误排查和定位。

## 单元测试

* **Python** **单元测试框架—uniittest**

​      Import unittest 函数库，对每个软件小功能进行测试，确保被覆盖的功能点正常。

# 其他

* git: 具体操作详见git_notes文档，**提交的版本最好是:测试和迭代稳定的版本、便于代码回溯**


------

