---
title: 'Software-Test'
date: 2024-04-01
permalink: /posts/2024/04/Software-Test/
tags:
  - Real Work Practice
---

software testing knowledge and experience.

# Take away notes

**Tips1: 同一类型的测试（eg：网页登录）可以逐步积累自己的测试用例，后续可以根据需要进行选择，逐步完善。**

# 测试基础知识

* 测试目标：保证系统在**各种应用场景下（正常+异常）**的功能是符合设计要求的。
* 等价类划分：将所有可能的输入数据划分成若干个子集。每个子集中如果任意一个输入数据对于揭露代码中的潜在错误具有同样的效果，那么这个子集即为等价类。**后续测试只需要从等价类中选一个进行测试**就可以覆盖整个子集。
* 边界值分析法：**选取输入、输出的边界值进行测试。**因为通常大量的软件错误是发生在输入或输出范围的边界上，所以需对边界值进行重点测试，通常选取正好等于、刚刚大于或刚刚小于边界的值作为测试数据。
* **一个质量过硬的软件系统，除了显示需求外，非功能性需求也需要关注。**
  * 非功能性需求：主要涉及安全性、性能、兼容性三大方面。
* **大多数测试是不可穷尽的：受限于时间和经济成本**

## 如何设计一个好的测试用例

* “好”的测试用例定义：一个完备的集合，**能够覆盖所有等价类以及各种边界值，**与能否发现缺陷无关。【等价类划分需要准确+完备。】
* 常用测试用例设计方法：
  * 等价类划分：【eg：学生成绩的取值范围是 0~100 之间的整数，考试成绩及格的分数线是 60。】
    * 有效等价类1:0-59之间的任意整数。
    * 有效等价类2：60-100之间的任意整数。
    * 无效等价类：小于0的负数 | 大于100的整数 | 非整数 | 其他字符串。
  * 边界值处理：根据需求的边界值，重点测试-等于、刚刚大于、刚刚小于边界值的情况。
  * 错误推测：根据对被测软件的理解、过往经验及个人直觉，推测出软件可能的缺陷，有针对性的设计和使用测试用例。
* 从软件功能需求出发，**全面、无遗漏的识别出测试需求**是至关重要的，这将直接关系到测试覆盖率。
* 对于识别出的每个测试需求点，需要综合运用等价类划分、边界值分析和错误推测方法来全面地设计测试用例。
* 只有深入理解被测试软件的架构，才能设计出“有的放矢”的测试用例集，去发现系统边界以及系统集成上的潜在缺陷。
* 必须深入理解被测软件的设计与实现细节，深入理解软件内部的处理逻辑。

## 单元测试

对软件中**最小可测试单元（函数或者类）在于程序其他部分相隔离**的情况下进行检测和验证。

### 如何做好单元测试

* 提炼代码基本特征，总结产生错误的原因。【循环的结束条件、每个if的分支是否考虑完全】
* 单元测试用例：输入数据+预计输出。
* **驱动代码**：调用被测函数的代码。
* **桩代码/mock代码**：代替被测函数调用的真实代码的临时代码。
* 并不是所有代码都需要单元测试，通常只有底层模块or核心模块才会采用。

## 自动化测试

* 只能替代手工测试中执行频率高、机械化的重复步骤，不能完全替代手工测试。
* 自动化测试比手工测试脆弱，无法应对被测对象的变化。
* 自动化测试用例开发的工作量远大于单次手工测试，因此只有当测试用例有效执行次数>5次时，才能收回自动化测试的成本。
* 自动化测试多用于发现回归测试中的问题，手工测试发现的缺陷数量通常更多。
* **适合自动化测试的项目**
  * 需求稳定、不会频繁变更。
  * 研发和维护周期长，需要频繁执行回归测试。
  * 需要在多平台上重复运行相同测试的场景。

## 测试覆盖率

* 需求覆盖率：测试对需求的覆盖程度，保证测试可以覆盖每个需求，确保产品质量。
* 代码覆盖率：至少被执行了1次的条目数占整个条目数的百分比。
  * 代码覆盖率：代码覆盖率。【行覆盖率、判定/分支覆盖率、条件覆盖率】
  * 函数覆盖率：条目数是函数。
* 代码覆盖率的价值：找出潜在的遗漏测试用例，并有针对性的进行补充，同时还可以识别出代码中那些由于需求变更等原因造成的不可达的废弃代码。
  * 代码覆盖率越高越能说明你的测试用例设计是充分且完备的，但你也会发现测试的成本会随着代码覆盖率的提高以类似指数级的方式迅速增加( 70% 的代码覆盖率，可能只需30 分钟的时间。90%，可能花的时间就远不止 30 分钟了。)
  * 仅单元测试阶段对代码覆盖率有较高的要求。
* 代码覆盖率的局限性
  * 100%的覆盖率 ≠ 软件质量极好：代码本身的缺陷和未知输入和未知处理情况等。
  * 低覆盖率一定代表代码质量不好。

# 代码测试

## 基本理念与方法

* 常见代码错误类型
  * 语法特征错误：IDE能发现部分，但有的不会影响编译，只会在运行阶段出错。
  * 边界行为特征错误：代码执行过程中发生异常，崩溃或超时。【边界条件上。】
  * 经验特征错误。
  * 算法\部分算法错误：和预先设计的功能不一致。
* 代码级常用测试方法：静态、动态测试。
  * **自动静态扫描工具：Sonar、pylint（python）**

# 性能测试

* 最常用的三个指标：并发量、响应时间、系统吞吐量。
  * 响应时间定义：应用系统从请求发出开始，到客户端接收到最后一个字节数据所消耗的时间。【前段展示时间+系统响应时间】
  * 吞吐量：所有对吞吐量的讨论都必须以“单位时间”作为前提。
* 三者的关系：
  * 空闲区间：系统并发数较少时，系统吞吐量也较低。
  * 线性增长区间：当系统整体负载并不是很大时，随系统并发用户数的线性增长，系统吞吐量也随之线性增长。
  * **拐点**：当系统处理能力逐渐趋于饱和，每个用户响应时间逐渐变长，不再是线性增长。
  * 过饱和区间：随系统并发用户数的增长，系统处理能力达到过饱和状态。此时，如果继续增加并发用户数，最终所有用户的响应时间会变得无限长。相应地，系统的整体吞吐量会降为零，系统处于被压垮的状态。
* 性能测试一般设计在线性增长区间内，压测通常在拐点上下，甚至过饱和区域。
* 后端常用测试工具：**Jmeter、loadrunner**

# 测试数据创建方法

## on-the-fly-实时创建

* 在测试用例的代码中实时创建要使用到的测试数据。
* 所有测试数据由测试用例自己维护，不依赖任何用例外的数据，最大程度避免了脏数据。

## out-of-box-开箱即用

* 测试用例中提前创建好需要的测试数据，但若被提前修改则此数据会变成脏数据。
* 不适用于只能一次性使用的测试数据场景。

## 综合运用

* 死水数据：相对稳定，不会在使用过程中改变状态，且可以被多次采用的数据。
  * 死水数据并不是绝对的，由测试目的决定。
* 活水数据：只能被一次性使用，或经常修改的测试数据。

* **绝大多数测试数据准备场景：仅需要一个所有参数都使用了缺省值的测试数据，或者只对个别几个参数有明确的要求，而其他参数都可以是缺省值的测试数据。**

# 测试基础架构

* 定义：执行测试过程中用到的**所有基础硬件设施及相关的软件设施**。
* 


------

