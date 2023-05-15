---
title: 'linux-notes'
date: 2020-06-15
permalink: /posts/2020/06/linux-notes/
tags:
  - cool posts
  - category1
  - category2
---

Some linux usage experience.

# 常用客户端工具

## mobaXterm

破解版可无限保存ssh记录

### 问题记录

* linux 服务器连接断开

  * 修改 /etc/ssh ssh_config 与 sshd_config 区别

    ssh_config 是针对客户端的配置文件  &  Sshd_config 是针对服务器的配置文件

  *  sshd_config 可以配置是否需要密码登录：PasswordAuthentication yes

* ssh 连接报错：Network error software caused connection abort

  * vim /etc/ssh/sshd_config 
  * 找到 TCP KeepAlive yes 把前面的 # 去掉
  * 找到ClientAliveInterval 参数去掉前面的#【该参数指定了服务器端向客户端请求消息的时间间隔，默认是0，不发送。ClientAliveInterval 60 表示每分钟发送一次，然后客户端相应，这样就保持长连接，比较奇怪的地方是，这里需要服务器主动发出请求，而不是客户端。正常情况下，ClientAliveCountMax】

# 文件操作命令

* 统计某文件中某内容出现次数：grep -o 内容 文件名 | wc -l
* 查看某文件中某内容对应的行：grep -n "内容" 文件名
* 




------

