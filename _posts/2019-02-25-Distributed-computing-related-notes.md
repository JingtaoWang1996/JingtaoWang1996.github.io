---
title: 'Distributed-computing-related-notes'
date: 2019-02-25
permalink: /posts/2019/02/Distributed-computing-notes/
tags:
  - cool posts
  - category1
  - category2
---

Distributed computing related notes included.

# 对比传统单体部署

* **将处理错误的代码当成正常功能代码来处理**
* 对比传统单体架构

|              | 传统单体           | 分布式                   |
| ------------ | ------------------ | ------------------------ |
| 部署         | 不经常&容易部署    | 经常发布&部署复杂        |
| 故障影响范围 | 大                 | 小，分布式隔离性更好     |
| 架构设计     | 难度小             | 难度随服务器数量指数增加 |
| 系统性能     | 响应快，吞吐量小   | 响应慢，吞吐量大         |
| 运维         | 简单               | 复杂                     |
| 扩展性       | 差                 | 好                       |
| 上手难度     | 应用逻辑学习曲线大 | 架构逻辑学习曲线大       |
| 系统管理     | 开发成本           | 服务治理和调度           |

# 架构思想-amazon

* 所有团队的程序模块都要通过 Service Interface 方式将其数据与功能开放出来。
* 团队间程序模块的信息通信，都要通过这些接口，不允许其他通信方式（eg：A直接访问B的数据库等），**只能调用这些Service interface**。
* 任何技术都可使用。
* 所有的service interface 做好设计成为能对外开放的接口。

经典资料

* 8条分布式被推翻的基本假设：网络稳定、传输延迟为0、带宽无穷大、网络是安全的、网络拓扑不变、只有一个系统管理员、数据传输成本为0、整个网络同构。

<details>
    <summary>经典图书</summary>
        An introduction to distributed systems【分布式系统提纲】
        Distributed Systems for fun and profit【免费电子书】
        Distributed Systems: Principles and Paradigms
        Scalable Web Architecture and Distributed Systems
        Principles of Distributed Systems【苏黎世联邦理工教材：分布式用到的算法】
        Making reliable distributed systems in the presence of software errors
        Designing Data Intensive Applications
</details>
# 关键理论&概念

## ACID

* A-atomicity 原子性：事务里的所有操作，要么完成，要么不做，只要有一个操作失败，整个事务就失败，此时回滚。
* C-consistency 一致性：数据库处于一致状态，事务的运行不会改变数据库原本的一致性约束。
* I-Isolation 独立性：并发的事情不会相互影响，如果一个事务访问的数据正在被另一个事务修改，只要另一个事务未提交，它访问的数据就没有影响。
* D-Durability 持久性：一旦提交后的事务，它所做的修改将会永久保存在数据库上，即使宕机也不会丢失。
* 一旦下单就减少库存，直到撤销or操作完成之后才释放库存。

## CAP 

对于一个分布式计算系统来说，不可能同时满足以下3点，最多2个

* 一致性Consistency：所有节点同一时间具有相同的数据【要么获得最近写入的数据，要么获得一个错误。】
* 可用性Availability：保证每个请求不管成功或失败都有响应。【每次请求都能获得一个非错误的响应，但不保证返回是最新写入的数据。】
* 分隔容忍Partition tolerance：系统任意信息的丢失或失败不会影响系统运行操作【尽管任意数量的消息被节点间的网络丢失或延迟，系统仍然继续运行。】
* CAP 定理表明，存在网络分区的情况下，一致性和可用性必须二选一。没有发生故障的时候，一致性和可用性可以被同时满足，当网络出现故障情况时，需要维持系统按照正常情况进行运行。【CAP定理的一致性和ACID数据库事务一致性不同】

<img src='/images/img/CAP.png'>

* C+A: 2pc--关注一致性和可用性，需要非常严格的一致协议。Eg: 两段提交等等。不能容忍网络错误或节点错误，一旦出现则整个系统拒绝写入请求。
* C+P:Paxis--一致性和分区容忍性，大多数节点一致即可，少数节点在没有同步到最新版本之前会变成不可用的状态。
* A+P: Gossip--只关心系统可用和分区容忍，因此系统不能达成一致性。需要给出数据冲突，给出数据冲突就需要维护数据版本。

## BASE

允许和容忍系统出现暂时性问题。

* 在用户下单时，大家都可以同时操作，但不真正分配库存，而是通过系统异步批量处理订单，可能出现超卖的情况。

## 分布式锁

多线程情况共享资源需要加锁防止数据写乱。在分布式的情况下，一般可以使用数据库DB、Redis、ZK等实现。分布式锁需要满足以下几点：

* 安全性：任意时刻只能有一个客户端获得锁（排他）
* 避免死锁：客户端最终一定可以获得锁，即使之前客户端崩溃或网络不可达。
* 容错性：只要服务集群中大部分节点存活，client就可以加锁。

**可能的问题-冲突判断**（以redis锁为例）

* Redis 为了避免client占住锁不放，设置了一个时间，到达时间节点后将锁释放，但如果当前客户端A因其他原因阻塞超过锁阻塞时间，释放之后被B申请时，A结束之后会将B的数据冲掉。
  * 通过增加**单调递增的版本号**来解决上述情况，低于当前记录的版本号则拒绝写入。
  * 上述版本号可直接在数据库中保存，不需要单独计数。

## 配置中心

* 除了代码以外的**软件配置信息**：数据库的用户名和密码、线程池大小、队列长度等运行参数、日志级别、算法策略；**软件运行环境参数**：Java内存大小、应用启动参数、操作系统参数配置等。

  非分布式的情况下，常把这些配置信息写在一个配置文件中，但在分布式的情况下，配置文件不好管理。于是，引入配置中心（分布式必要组件）。

* 设计重点：统一规范化所有的服务配置参数和配置项，如果不能更新，则回退到上一个配置版本。

  *  区分软件配置：静态配置（软件启动时刻的配置，运行时不会修改）和动态配置（软件运行时的配置）
  * 每个配置项：key/value
  * 操作层和平台层由运维和架构师来配置，需要有统一的系统命名，确保不会冲突。
  * 配置参数中，如果有依赖第三方组件的配置，强烈建议不要放在配置中心，而是放在服务发现系统当中（语义清楚、减少因运行环境不同导致的差异）。
  * 对于不同的运行环境中的配置差异：**开发和测试环境日志级别**Debug，生产环境则是warning**或error**级别。
  * 配置需要有一个整体的版本管理：记录每次的版本变动，最好能和版本号做关联
  * 配置管理工具来对不同环境下的情况进行配置。

* 配置录入后，发出变更通知，控制器读取最新配置后更新

  * 变更通知组件：分布式环境下，服务器太多，直接推送不现实，通过Pub/Sub 方式更经济。
  * 通过订阅反向拉取：能够校验请求者的权限。
  * 配置变更控制器的位置：每一台主机上，提高执行成功率。
  * 操作系统层和平台层变更最好模块化，便于维护同时减少复杂度。
  * 通过标准运维脚本实现，让应用方提供应用变更时候的脚本动作。

# 技术栈

* 提高性能

  | 加缓存   | 负载均衡 | 异步调用     | 数据镜像   | 数据分区   |
  | -------- | -------- | ------------ | ---------- | ---------- |
  | 缓存系统 | 网关系统 | 异步系统     | 数据镜像   | 数据分区   |
  | 缓存分区 | 负载均衡 | 消息队列-kfk | 数据同步   | 分区策略   |
  | 缓存更新 | 服务路由 | 消息持久化   | 读写分离   | 数据访问层 |
  | 缓存命中 | 服务发现 | 异步事务     | 数据一致性 | 数据一致性 |

  * 缓存系统：提高系统访问能力
  * 负载均衡：系统水平拓展，多台机器共同分摊流量请求
  * 异步调用：通过消息队列来对任务做排队处理，减少前端请求峰值，增加系统吞吐量（以实时性作为代价，且需要对消息做持久化。）

* 提高稳定性

| 服务拆分           | 服务冗余             | 限流降级 | 高可用架构 | 高可用运维 |
| ------------------ | -------------------- | -------- | ---------- | ---------- |
| 服务治理，服务调用 | 服务调度、弹性伸缩   | 降级控制 | 多租户系统 | 自动化运维 |
| 隔离故障，模块复用 | 故障迁移，防单点故障 | 服务熔断 | 灾备多活   | 全栈监控   |

# 关键技术-全栈监控&服务调度

## 全栈监控

* 需要完成的功能：监控、关联分析、跨系统
* 具体监控：主机和底层资源（cpu、内存等）、中间件状态、应用层（访问量、吞吐量、响应时间等）；同时添加好标准化的日志及日志分析
* 好的监控：故障快速定位、关联聚合指标后展示

## 服务调度

* 定义服务的关键程度（基于对业务的理解）

* 微服务是服务依赖最优解，至少：**服务不能有依赖环**，若有：考虑通过消息中间件等解环。

* 服务状态&生命周期：通过服务中心中间件来管理。

* 整个架构版本管理：VersionSet in Amazon(一堆服务版本集所形成的整个架构的版本控制)

  ​    除了各个项目的版本管理之外，还需要再盖一层版本管理（Build过Linux分发包的话，Linux分发包中各个软件的版本上会再盖一层版本控制，毕竟分发包也有版本依赖，同时解决版本兼容性的问题。）

## 调度

### 流量调度

* 自动调度，无需人工干预，在弹性计算扩容较长事件窗口内或底层资源消耗殆尽的情况下，保持系统平稳运行。
* API gateway：高性能语言、集群技术、业务逻辑简单，服务化(Admin API 来不停机管理变更配置)
* 状态数据的调度：通过第三方服务进行存储。
* 分布式事务一致性问题：各个节点上的数据备份问题，数据冗余解决数据不丢失的问题。（备份、master-slave、master-master、多阶段提交、Paxos）
  * 凡通过业务补偿或在业务应用层上做的分布式都是两阶段提交

### 数据调度

* 分布一致性真正算法：**Paxos**(Lesile Lamport 1990 提出的基于消息传递且具有高度容错性的一致性算法)
* 逻辑钟和向量钟（检测响应的数据冲突）：分布系统钟为了解决消息有序问题而布置的时钟，**由于不同的机器有不同的本地时间，同步这些时间相对困难导致消息乱序。因此，每个系统维护一个本地计数器，每执行一个事件，计数器**+1，跨系统传递时，接收端同步更新自己的计数器。

# 幂等性-去除重复请求

* 幂等设计：一次或多次请求某个资源应具有相同的副作用。
  * 系统解耦隔离后，服务间的调用可能会有三个状态：success, failed,timeout.前两者是明确的状态，第三种不知道是什么状态。【超时可能产生副作用：订单超时是多创建一笔？还是多扣一次钱？】
  * 处理方式：下游系统提供相应查询接口。上游timeout后，下游差一次，查到就不做了，没查到再重复；**幂等性：**查询交给下游系统，上游只管重试，下游保证次和多次重试一致。
* 幂等设计具体实现
  * **全局id**：同一笔交易使用相同的id来保证幂等性。（ID的分配：使用id冲突极小的算法--UUID、snowflake【Twitter提出，long型64位id】）
  * **过滤收到的id是否重复**：幂等性要求下游对收到的id进行存储，用于后续查询。
* http幂等性
  * HTTP get 方法获取资源，无副作用，是幂等的。
  * http head 和 get 本质是一样的，区别在于head 只有头部信息，也是幂等的。[可以用来判断某个资源是否存在—用head 做探活]
  * http options：获取当前URL所支持的方法，幂等。
  * http delete：删除资源，同样幂等。
  * http put：用于创建或更新操作，幂等性。

# 业务补偿

​        现实生活中，大多数情况无法做到强一致的ACID，特别是需要跨多个系统的时候。若仍要保持一致性，需要多个系统统一协调，大概率无法完成。因此，遇到类似情况，当每一部分条件无法满足或者是有变化的时候，需要从业务上进行相应的补偿。补偿机制大致如下：

* 幂等性：一个事务超时or失败，需不断尝试，最终不行or请求变化则需恢复或启动业务更新机制。
* 业务补偿需要：清楚的描述业务需要达到的状态 & 条件不满足需要退回的状态
* 业务补偿可以串并行执行。
* 已经完成的事务进行整体修改，可以考虑构成一个修改的事务。

重点：

*  努力完成业务流程【包含重试、幂等机制；小心维护和监控整个过程的状态（同一个维护系统当中便于检测管理）】
* 如果无法完成，启动补偿机制，回滚业务流程。【业务补偿和业务逻辑强相关，无法通用】

# 数据库扩展

## 读写分离

* 读多写少：可将数据库集群模式中的多数台用于读取，少数用于写入（同时负责读取的数据库可进一步划分为负责不同部分的服务）
* 读少写多：与上述相反。
* 优点：各业务读取数据库分离-防止一个业务挂掉导致所有服务拖死 & 分摊数据库负载。

## 分库分表

一般来说影响数据库性能的问题：写入的IO操作（业务层优化）数据量大小（数据库分库分表）

* 分库的策略：按照特定的某个规则进行数据分库（eg：地理位置、日期等）
* 数据访问层：用于数据路由的中间件，将不同服务的查询要求送入不同库（对前端服务不变）但在具体操作过程仍然会有跨库的麻烦产生。
* 分表的策略：1）按数据种类分 2）按照范围来分:保证同一分片的数据是统一的 3）按租户ID来分，方便查询 4）hash散列算法来分，降低形成热点的可能性。

**数据库扩展设计重点（业务层）**

* 数据库和应用服务一同拆开---一个服务一个库（服务之间用接口通讯，不直接访问库）
* 水平分片: 一张表中的一些字段放到一张表，另一些字段放到另一张表
* 垂直分片:分离经常修改和不经常修改的数据，不会导致修改部分数据的时整个库被锁影响性能。
* sharding 水平分片：
  * 随数据变化，需要定期重新分片保证均匀；
  * 分片是静态的，数据访问不可预期，因此需要经常性调整分片，这样成本过高，因此最好使用索引表来分片（数据索引动态记录到一张表中，方便灵活调度数据）
  * 代码从多个分片中检索数据查询，使用并行任务提取数据后，再进行聚合
  * 尽量减少多个分片中的数据查询操作。

# 相关设计思路

## 容错

弹力设计（system resilience measurement）：容错能力、可伸缩性、一致性、应对大流量的能力。

* 系统可用性测量（系统在不健康，甚至出错的情况下能够维持运行的能力）：

  ​                                  **Availability = MTTF/(MTTF+MTTR)** 

  * MTTF: mean time to failure，平均故障时长（多长时间出现一次故障）
  * MTTR:mean time to recover，平均恢复时间（故障出现到恢复的时间）

  | 系统可用性      | 宕机时间/年 | 宕机时间/月 | 宕机时间/周 | 宕机时间/天 |
  | --------------- | ----------- | ----------- | ----------- | ----------- |
  | 90%（1个9）     | 36.5d       | 72h         | 16.8h       | 2.4h        |
  | 99%（2个9）     | 3.65d       | 7.2h        | 1.68h       | 14.4m       |
  | 99.9%（3个9）   | 8.76h       | 43.8m       | 10.1m       | 1.44m       |
  | 99.99%（4个9）  | 52.56m      | 4.38m       | 1.01m       | 8.66s       |
  | 99.999%（5个9） | 5.26m       | 25.9s       | 6.05s       | 0.87s       |

* 有计划不可用：日常任务、运维、升级。

* 无计划宕机：系统故障、数据中间故障、自然灾害。

* 故障是正常&常见且不可预测的，容错设计之初就是要考虑 "隔离"来防止故障蔓延。

  * 以服务种类来隔离 & 以用户来隔离（多租户模式： 对于大客户，单独设置专门的服务实例，小客户共享实例，在服务隔离的情况下，确保资源的节约）。

  * 每个服务都有一个自己的数据库（物理隔离），同时准备好对外暴露提供服务。

  * 业务到达每一步可以暂停保存，以确保恢复之后可以从当前位置继续。

* 隔离设计的重点：隔离业务的大小和颗粒度的定义; 系统的复杂度和成本；与设计模式配套使用；运维复杂度；监控系统。

## 重试

对于暂时性故障，服务不稳定时增加重试机制（error 重试无意义）

需要注意：

* 设置重试最大次数&重试时间：之后报错。
* 重试之间应该有间隔：避免过快导致网络负担加重。
* Exponential backoff 指数级退避：每重试一次需要的休息时间都会加倍，方便调用方有更多时间来处理请求。

## 熔断

错误太多或者短时间内无法修复时采取熔断，减少错误导致的等待和对系统的影响。

熔断器模式：

* 调用失败计数器，达到阈值，程序断开报错
* 达到一定失败数量时可以阶段性操作，避免偶发性问题。

重点：

* 明确需要熔断的错误类型及对应的策略；
* 日志监控+手动重置
* 测试服务是否可用：定时检查服务是否恢复，用以切换到闭合状态。
* 考虑并发+资源分区+重试错误的请求。

## 限流

* 保护系统不会在过载的情况下出现问题。

* 常见场景：数据库访问的连接池、线程池、Nginx下用于限制瞬时并发连接数的limit_conn模块等

* 策略：限制并发访问速度--一旦到达限制，触发相应的限流行为。常见限流行为如下：
  * 拒绝服务Denial of service DOS：将多出来的请求拒绝掉，统计访问量最多的客户端请求，将该客户端拒绝。【同时避免恶意攻击】
  * 服务降级：关闭或者将后端服务做降级处理，可以让服务有足够的资源来处理更多的请求。[停掉不重要的服务or不再返回全量数据，只返回部分数据]
  * 特权请求：资源不够的时候，只能将资源分配给更高级的用户。
  * 延时处理：在这种情况下，一般会有一个队列来缓冲大量请求，队列满之前队列中缓冲，队列满之后，拒绝掉服务。缓冲队列多用于缓解压力，应对短时峰刺请求。
  * 弹性伸缩：自动化运维方式监控系统服务。

* 限流实现方式：维护一个计数器，来判断是否达到最大请求。也可以通过不同算法实现请求响应的限制。
* 基于时间的动态限流：当无法获取阈值时候，可以考虑通过动态限流的方式来达到目的。[通过记录每次请求响应时间，计算10s内请求时间排序后90%的位置大致是多少来确定当前性能。]
* 设计要点：
  * 设计之初就考虑，防止后期难以加入；限流模块性能必须要足够好，否则延迟过大无意义；限流需要一个手动开关；对于拒绝的请求需要一个返回码
  * 突发流量的应对方案 & 限流节约成本。
  * 防止多租户的场景下，某一租户将资源耗尽。
  *  确保系统在某速度下的响应时间及可用性。【对外界IO无依赖情况下可以做到】

## 降级

* 解决资源不足和访问量过大的问题：当资源和访问出现矛盾时，在有限资源下，对系统进行降级操作，暂时牺牲掉部分东西确保系统平稳运行。

* 一般来说降级需要牺牲掉的东西有：
  * 一致性：从强一致性变为最终一致性。这个世界上大多数系统并不需要强一致性，因此将强一致转为最终一致能够有效降低资源消耗。【eg: 采用异步的方式将单条服务构建成多条一致】   PS：功能降级一般会损害用户体验，因此可以加入“系统当前繁忙，您的订单已收到，我们正努力为您处理订单中，我们会尽快给您发送订单确认通知……还请见谅”等友好提示。
  * 停止次要功能：停止访问不重要的功能，从而释放更多资源。【因为停掉部分功能会影响用户体验，因此恢复后最好给用户一些补偿（eg：积分卡等）】
  * 简化功能：eg:全量数据改为部分数据。【一般API会有两个版本，一个返回全量，一个返回部分/最小可用数据】

* 设计要点：
  * 降级条件：吞吐量、响应时间、失败次数等。满足条件后用自动化脚本进行处理。
  * 功能降级：确定好可以牺牲的功能和必须保证的功能。
  * 降级功能开关可配置：相应的在对外API名称上有区别。

* 降级属于应急情况，所以降级的业务流程可能因为长期不使用而产生bug，需要平时做一些演练。

## 缓存

* 为了解决类似于（后端数据库查询开销、分布式远程调用）开销较大，在业务允许的情况下，使用缓存（类似DNS分布式请求中的缓存）

三种缓存模式：

* Cache aside 更新模式：（自行维护应用代码）
  * 失效：先从cache提取数据，若没有，再读库，返回给调用方的时候放入cache一份。
  * 命中：若直接命中，则从cache中读取后返回。
  * 更新：先将数据存库，成功后再让缓存失效。（避免脏数据出现）
* Read/Write Through 更新模式
  * 查询中更新缓存，当缓存失效的时候，cache自己调库更新。
  * read through：缓存失效的时，cache 侧自己读取缓存数据。
  * write through：数据更新时，若没命中，则直接更新数据库，然后返回，若命中，则更新缓存，同时cache自助更新。
* Write Behind caching（文件系统 page cache 算法）
  *  在更新数据的时候，只更新缓存，不更新数据库，缓存会异步的批量更新数据库。
  * 优点：IO操作加快（直接操作内存），异步还可以合并同一个数据的多次操作，提高性能。
  * 可能出现的问题：数据不是强一致的，且可能会丢失，因此一定程度上需要tradeoff。

设计重点：

* 缓存已经成为高并发高性能架构的关键组件。（Redis可以作为选择之一：数据类型丰富），分布式架构下：最好是有一个外部集群(内存足够大—内存不够可以用切片技术分到不同机器上、网络带宽足够、因为缓存是一个内存和IO密集型应用)
* 缓存好坏通过命中率体现（命中率高说明缓存有效，一般来说80%以上就算很高了，因为热点数据通常都只是少数，没有必要将所有数据放入缓存）
* 缓存通过：强一致性来提高性能，因此并不是所有业务都适合缓存。

* 缓存更新周期：tradeoff过长过短都不好
* 缓存使用：LRU策略，当内存不够需要数据被清出时，先清除最不活跃的数据。（能够将最经常访问的数据调到最前面来）key-value非顺序结构中维护一个次序（eg：访问频率排序）

## 异步处理--系统统一调度

* 增加系统吞吐量、提高容错性、利用好资源&减少等待时间。
* 程序读写文件异步：将数据hold一小会儿，将同类型的请求合并之后再进行写入和读出（硬盘向一个方向转1次就可以解决，不必来来回回的转）
* 具体设计：
  * 一个前台系统记录用户转发请求（记录只需要追加），收到请求并记录后立刻给用户端一个反馈“请求已收到，正在处理”，但等待一定时间再将记录到的请求集体转发。
  * 之后出现一个推和拉模型pull（worker定时取任务） & push（分任务） 
  * 任务处理完成之后给发起方回传一个状态，确保没有丢任务。
  * 任务发起方需要定时重发超时任务。
  * 强一致性下，业务层只做两段提交，数据层需要Raft/paxos 算法，但现实生活中不一定都需要强一致性（而是：最终一致性）。

## 边缘计算

* 在数据量逐渐增大的过程中，统一由数据中心处理逐渐不现实。分析速度的实时性要求也导致必须考虑边缘计算（数据中心成本越来越高）。
* 相对于数据中心而言（数据中心将所有服务集中在一个机房中完成处理：统一管理运维、较好网络保障，但仍然需要类似CDN的网络节点将数据推送到里用户近的地方）。若**边缘节点拥有可定制的计算能力，可以在边缘节点上处理部分逻辑，则可以极大提高数据中心的性能和扩展性。**
* 成本消耗：几十万用户-百级QPS-10台服务器；上百万用户-千级QPS-50台服务器；上千万用户-1w到10wQPS-700台；上亿-百万级QPS-上万台服务器（当架构复杂后，就需要做很多非功能的东西，比如：缓存、队列等等。因此将数据不断边缘化拆分后，运维成本快速下降。）

* 边缘计算的场景：
  * 实时响应的业务：离用户很近、可以实时响应本地请求
  * 简单公司业务逻辑：秒杀、抢红包等
  * 收集并结构化数据：图片视频中的文字信息抠出来在传回数据中心。
  * 实时设备监控：线下设备数据采集和监控。
  * P2P去中心化数据采集:作为一个服务发现的服务器，让本地设备进行P2P通信。
  * 云资源调度/聚合：服务调度+API数据等聚合输出

## 边车模式--控制和逻辑分离

* 边车：摩托+边车拓展现有业务和功能，做到控制和逻辑分离。多为agent。
* 对应用无入侵，不受语言和技术限制，控制和逻辑分开部署。
* 不适用与语言相关的协议。

## 服务网格-service mesh

* 专注于处理服务和服务之间的通讯，构造可靠稳定的架构设施，多用于轻量级服务代理合并。
* 实际为网络7层协议模型中的第四层TCP协议，将底层网络通信方面内容接管。
* 边车sidecar模式集群后成为service mesh。
* 设计重点：sidecar的基础上+流量调度。
* 不侵入业务逻辑，但运维成本大。

## 网关模式

为减少运维成本，在服务集群当中增加一个gateway，简化架构。

一个网关需要的功能：

* 请求路由：因为不再是sidecar，所以网关一定要有请求路由功能，也方便调用端。
* 服务注册：为了能够代理gateway后面的服务，并把请求发到正确位置上，网关应该有服务注册功能（后端服务实例可以提供服务的地址注册、取消注册，多为API接口，HTTP请求，这样Gateway就可以根据接收到的请求决定发到后端哪个服务上）
* 负载均衡：因为一个网关可以接受多个服务实例，所以网关还需要在对等服务实例上做负载均衡。Round-Robin轮询等
* 弹力设计：考虑前面弹力设计部分的内容。
* 安全：SSL加密及证书管理、授权、数据校验等，错误处理越靠前越好（接入组件进行维护）
* 灰度发布：对相同服务不同版本实例进行倒流，同时收集相关数据，提升软件质量。
* API聚合：通过网关将多个单独请求聚合成1个请求。将多个请求的结果拼装后返回。
* API编排：微服务架构下，使用网关来控制走完整的业务流程需要调用一系列API。

网关设计重点：

* 高性能：网关不应该成为技术瓶颈。高性能（C\C++\GO\Java）。网关对后端的请求以及对前端服务，使用异步非阻塞IO来确保不会导致延迟等性能问题。
* 高可用：所有流量或调用需要经过网关，它的稳定直接关系到所有服务的稳定，因此需要：集群化、服务化（不间断的情况下修改配置）、持续化。
* 高扩展：对于业务逻辑的多变，需要确保网关是可扩展的。

整体架构方面：

* 不要在网关耦合后端服务功能。将后端服务单独放置在一块。
* 网关应该靠近后端服务，并和后端使用同一个内网，保证低延迟。
* 网关做容量扩展为前端分担流量，提高性能。
* 服务发现：做一个时间不长的缓存，不需要每次请求都去查询相关服务。
* 数据加密、校验用户请求、检测异常访问。

# 应用场景

## 秒杀--12306/演唱会（单条热点数据）

* 场景抽象：页面有倒计时按钮，倒计时到了才可以下单，下单前填写校验码防止脚本代抢。

* 技术上：

  * 前端不断向祸胎发送请求，每次返回倒计时时间or抢票url。
  * 100w人不停点击的并发量 100WTPS
  * 所有请求都会集中在同一条数据库记录上，无论如何分表分库，对单条热点数据效果不大。

* 解决方案**---CDN 抗流量过滤用户请求，保护数据中心**

  * 100万用户同一时间打开一个页面几乎不可能，因此要用到CDN（content delivery network）
  * 使用CDN之后，这100万个用户就会被几十甚至上百个CDN边缘节点分担了。（**在CDN当中，需要将小服务部署到CDN节点中（统计在线人数定时返回数据），当知道大约多少人在线之后，在快要开始时，向各个CDN服务节点传一个概率值，eg：0.02%，开始时，每1w人放2人进去，剩下的直接返回秒杀结束。总数200个的并发量完全扛得住。）**

* 12306

   因为商品不确定，因此无法使用上述CDN解决秒杀的办法。

  * **分时段放票：人肉分流**
  *  预售：收集好需求，通过增加车厢和车次来解决问题。
  * 最后: 概率抽签
  * 内部自留

* 双11：不属于秒杀的情况，想尽可能多卖出商品且不超过库存+银行操作+库存查询。

    为了确保一致性，就必须要使用高并发框架将各个系统性能不断优化

* 边缘计算：随着数据量越来越多，请求量越来越大，将原本放在数据中心处理的业务逻辑，下放部分到边缘节点（类似于上述CDN节点），能够极大提高系统性能。

# 部署升级策略

* 停机部署 Big Bang Recreate：现有版本停机、部署新版本---新老版本互不兼容的情况下；能够保证新版本完全一致性；对用户影响较大（事先挂公告，选择用户少的时候更新）。
* 蓝绿部署Blue/green stage：部署好新版本后，将流量从老版本切过来.---无需停机、实时发布、避免新旧版本同时在线；资源浪费（需要双倍）、服务中有状态会产生问题。
* 滚动部署Rolling update/Ramped：逐步升级现有服务。---当新应用部署上线后，删除旧的部分，逐渐替换+缓慢发布。容易出现新老版本同时在线、新版本未在生产线上验证后就上线、运维判断版本难度大、流量无法直接全部切换。
* 灰度部署canary：切部分用户到新版本，没问题后再扩大，直到全部倒入(又叫“金丝雀部署”：矿井中哪怕有一丝瓦斯都会停止唱歌，浓度大时死亡).该技术大多用于缺少足够测试/可靠测试、对新版本稳定性缺乏信心的情况下。
* AB测试: 同时上线两个版本，做相关比较。测试应用功能的表现方法（受欢迎程度、可用性等），AB测试是对功能不确定的情况下同时上线两个版本比较功能情况。（在不知道新版本是否获得用户青睐的情况下，需要收集一定数据才能直到）

# 需要注意的问题

* 异构系统标准性：软件、应用、通信协议、数据格式、开发和运维过程是否标准。
* 好的配置管理应该分为3层：底层&操作系统、中间层和中间件、最上层&业务应用。
* 服务依赖性问题：**整个服务依赖链中的稳定性由最差的决定**
  * 非关键服务被关键服务依赖，则非关键业务可被定义为关键业务。
  * 一个服务链上的某个服务挂掉，整个链条可能会一起挂掉。
* 服务治理：定义出服务关键程度，关键业务或服务调用的主要路径。同时确保：应用层上的业务隔离以及数据库上的隔离。
* 多层架构的运维复杂度更大：系统通常分为4层（基础层-硬件设备、平台层-服务中间件层、应用层-业务软件、接入层-接入用户请求的网关等）
  * 任何一层出问题都会导致服务整体出问题
  * **<u>不要相信上游系统不出问题，不能因为对方系统问题，把我们系统影响到</u>**。


------
