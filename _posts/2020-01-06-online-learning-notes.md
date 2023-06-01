---
title: 'Online-learning-notes'
date: 2020-01-06
permalink: /posts/2020/01/Online-learning-notes/
tags:
  - cool posts
  - category1
  - category2
---

Online learning notes：coursera, etc.

[no ladder possible solution](https://blog.csdn.net/weixin_44491401/article/details/124091938)

# Machine Learning Yealing

## 基本点

* 优化策略的意义：正确优化策略带来的优化方向能对模型效果有直接提升，反之浪费测试时间。

* ML发展点：**数据量**越来越大、**计算资源**充足、加入神经网络基础后，随神经网络规模变大（**模型参数变多**），模型效果更好的概率更大。

* 设置开发集&测试集：避免自行采集的训练和测试集效果显著，但实际使用后效果变差（实际数据质量等方面达不到要求）。

  * 训练集: 训练算法
  * 开发集（实际情况数据，规模、样本数尽可能大）：调整参数
  * 测试集：评估算法性能。

  PS: **开发和测试集数据应该服从相同分布**，否则训练模型的提升对实际情况毫无意义。【开发集好，测试集差===算法过拟合，需要更多数据】

  PPS: **对于全新问题，通常通过开发集评估当前方法是否合适or需要被放弃**

* 单值评估指标进行优化（single-number evaluation metric）：precision、recall、F1等

* 满意度指标&优化指标：**优化指标是在满意度指标基础上形成的**

  * eg：既在乎准确度又在乎运行时间，则设定一个可接受参数限制（运行时间<100ms)再调整另一个-->【运行时间：满意度指标；准确度：优化指标】

* 开发集、测试集的指标修订

  新项目开展时，需尽快确定开发集和测试集，便于确定模型明确目标【Doing is better than always thinking】

## 基础误差分析

* 如果一开始不能设计构建出完美系统，那就从基础版本模型系统开始逐步迭代。

* 误差分析：检查被算法误分类开发集样本，找到误差原因进而确定改进方案优先级。

* 根据开发集评估想法的可行性需要将可能的提升率与时间成本比较看是否值得。

* 并行评估：将各种可行的方法创建成表格，同时观察误分类样本进行对比。

  eg：100个开发集的误分类样本

  | 图像 | 狗   | 大猫 | 模糊 |                    |
  | ---- | ---- | ---- | ---- | ------------------ |
  | 1    | yes  |      |      | 比特犬             |
  | 2    |      |      | yes  |                    |
  | 3    |      | yes  | yes  | 狮子在雨天拍的图片 |
  | 4    |      | yes  |      | 数目后的美洲豹     |
  | ...  |      |      |      |                    |
  | 占比 | 8%   | 43%  | 61%  |                    |

  以上表为例，处理大猫能够得到43%的改进，模糊类能够达到61%

* 开发集中，被误标注的数据值得被修正。

## 偏差与方差（非统计定义）

* 偏差和方差的对比（两大误差来源，都是优化方向）
  * **偏差bias**：算法在训练集上的错误率。--【提高性能】
  * **方差variance**：算法在开发集比测试机表现差多少。 --【更好的泛化】
  * 偏差和方差将协助你决定是否该添加数据，并合理安排时间及策略去提升性能。当训练集的准确度无法达到目标的时候，此时并不能期望实际应用的准确度高于训练集，此时应有限考虑优化算法。拥有更多误差是无害的，但并不一定随时有帮助。
* 与最优错误率比较
  * **最优错误率=不可避免的误差**：在一个复杂任务中，即使人也无法完全识别的情况下，最终模型的效果一定低于最优错误率，否则存在overfitting的问题（当可避免的偏差已经优于最优错误率时，此时优化方向应该是提高泛化程度（方差）而不是减少偏差）。
  * 最优错误率（贝叶斯错误率）的获取：人类手工标注。
* 偏差与方差的处理
  * 较高可避免偏差：通过增大模型规模（添加层数、神经元数量来增大NN大小）。
  * 较高方差：增大训练集数量（覆盖类型更多的情况下训练）。
* 偏差与方差的tradeoff：尽可能不影响一方的情况下优化另一方。
* **减少可避免偏差的方法：**
  * 加大模型规模：一定程度上过拟合训练，减少偏差，若方差增加时，可通过**加入正则化能够抵消方差增加**。
  * 修改模型架构。
  * 减少或去正则化：避免偏差，增大方差。
  * 根据分类结果对输入特征进行增删。
  * 增加训练数据：优化方差，对偏差无效

* **方差减少方法**：

  * 增加训练数据
  * 加入正则化
  * 减小模型规模：降低方差但增大偏差。
  * 加入提前终止：降低方差但增大偏差。

* learning curve --- bias & variance

  学习曲线：随训练样本的数量增大，开发集合误差逐渐减小，靠近期望误差。【通过学习曲线能够避免花费几个月时间收集数据最后不管用的情况】

  <img src='/images/img/学习曲线.png'>

* training curve --- bias & variance

  训练误差曲线：评估添加数据带来的影响。（训练集增大，开发集和测试集误差减小，但训练集误差可能会上升）。

* 学习训练曲线解读

  <img src='/images/img/学习训练曲线1.png'>

  上图中error趋于平稳，不太可能通过增加数据量来达到预期性能。

  <img src='/images/img/学习训练曲线2.png'>

  加入训练误差后可以看出，增加数据后，training error 逐渐趋于稳定。

  <img src='/images/img/学习训练曲线3.png'>

  增加数据，缩小开发集的error

## 不同分布上进行训练和测试

* 通常：新数据和原数据整合后再统一进行处理达到“相同分布”的目的。
* 大数据时代，即使训练集和开发测试集不属于同一个分布，仍然希望用它来学习，因为可以提供大量的信息，但也存在新的问题。
* 如何决定是否使用不同分布的新数据：早期算法，直接合并两类数据会导致算法表现更差，但当模型足够大，反而可以在数据合并之后提升算法性能**（模型足够大为前提）**。
* 是否添加不一致的数据：不一致的参数中是否包含决定性的因素（eg：纽约房价&底特律房价，则两种样本之前没有参考价值）
* 数据&权重：假设20w互联网图片，5k用户图片，40：1的数据比例。这种情况可以通过权重将数据拉平（20w全部增加1/40的权重，确保图片重要性一致)
* 训练集泛化到开发集：训练集低误差难以泛化到不同分布的高误差数据集上，则尝试增加泛化数据样本，找到分部之间的差异来解决问题。
* 人工合成获取无法获取的数据：**合成过程需要考虑数据是否具有代表性。**

## 梯度检验：gradient checking

梯度下降训练过程，存在：cost function 下降，但最终prediction不理想的情况，此时适合采用gradient checking 来确保梯度下降算法正确，确认正确后，具体训练迭代时关闭检验部分。

<img src='/images/img/梯度检验示例图.jpg'>

* 仅用于验证梯度下降算法参数等是否正确，**正式训练时需要关闭gradient checking，因为很占据计算资源**。

## 其他

* 模型优化方向：列出可行操作后，论证选择最可行的方向进行优化

* 优化之前可以先做一个demo测试，进一步论证方向是否可行：同样需要开发、验证、测试三集合数据：60%，20%，20%

* SVM 参数选择：核函数中：
  $$
  e^{||x-l||^2/2σ²}
  $$
  

  * C = 1/λ: large C/small λ--小偏差，大方差；small C/large λ--大偏差，小方差；
  * σ² : large σ² --大偏差，小方差，函数更加平稳；small σ²--小偏差，大方差 ，函数更陡更集中

* Dimensionality reduction

  * 减少存储、计算资源占用，方便区分、统一数据，同时降维后的数据直观了解方便建模。
  * PCA: 找一个更低维度的平面将数据进行投影，降低数据维度。
  * 降低后的维度选择：前后误差均值在1%范围内

* 特征选择和变化：假如所取的特征不服从某个分布，例如Gaussian Distribution，则可以**将特征做log变换或者开根号变换使得最终的图像更加符合高斯分布。**

* 关注特别大或者特别小的特征值，这很可能对数据区分有帮助。

* learning with large dataset：**It's not who has the best algorithm wins, it's who has the most data.**

# Intro 2 statistic

* **The empirical rules**

  若数据服从自然分布，则正态分布的数据服从如下经验：

  * 2/3 of the data within one standard deviation of mean.
  * 95% of the data within two standard deviation of the mean.
  * 99.7% fall within 3 standard deviations of the mean 。

* **Normal approximation:正态估计**

  finding areas under the normal curve to find the percentage.

* **Law of large number **

  当独立随机变量数量增加时，它们的**平均值会趋向于其期望值的现象。**（在实验条件不变的情况下，**重复试验多次，随机事件的出现的频率近似于它的概率**）

* **Central limit Theorem**

  当随机变量数量增加时，**它们的和的分布逐渐趋近于正态分布**。

  关键点：

  * 考察的统计量一定是：**sum**
  * 样本数量必须足够大
  * 独立同分布的 r.v.

* **Square root law 应用**

  Toss a coin 100 times. How many tails do you expected? Give or take how many?

  ```python
  tails,head =1,0
  P(1)=P(0) = 0.5
  μ = 0*P(0)+1*P(1) = 0.5
  expected NUMBER OF TAILS = E(SUM)*μ = 100 * 0.5 = 50 
  give or take:SE(SUM) = √100*μ = 5
  σ² = (tails-μ)^2*0.5+(head-μ)^2*0.5=0.25
  SE(percentage) = 0.5/√100 = 0.05 = 5%
  ```

  * the standard error of the sample mean goes to zero as the sample size increase.
  * Thus, the sample mean will be close to its expected value μ as the sample size is large.

* 相关性度量

  * correlation coefficient measure: the **strength** of linear relationship；**direction** of relationship
  * 相关性系数r仅用于确定”线性相关度“，r=0表示非线性相关。

* 残差图（residual plot) 

  用于确定预测模型正确度或是输入数据需要修正的修正度。

## Hypothesis Testing

两类关键假设定义：（通过提出与H0相对应H1，然后通过实验努力拒绝H0，如果实验结果不满足H0，那么就拒绝H0，接受H1。）

* Null hypothesis--H0：普遍接受的事实（**努力通过研究使得这个假设变得无效化**）
* Alternative hypothesis - H1：备选假设，与H0相反的可能性。

示例：toss a coin 10 times a get 7 tails. Is it sufficient to conclude that the coin is biased?

* **Null hypothesis：nothing extraordinary is going on**--- P(T) = 0.5

* **Alternative hypothesis: opposite to H0** -- P(T) !=0.5
* hypothesis testing processed by collecting data and evaluate whether the data are compatible with H0 or Not.

 其他补充定义

* test static：measures how far away the data from what we would expect if H0 were True.
* **p-value**(observed significance level)：判定假设检验结果的一个参数，极端值情况下可以确保H0为真，**The smaller p-value， the stronger the evidence against H0**
  * **P-value less than 5%, then the result is called statistically significant.**

### 多重检验/多重假设检验

* 多重检验：通过多重比较之后，降低因为偶然误差导致的单次假设p-value值极小的情况发生。
* 多重假设检验：通过p-value 对假设的检验，主要是通过人为设定的阈值来进行，但随着检验总次数无限放大，会导致false positive 概率增高，因此引入多重假设检验来进行校正。
  * Bonferroni correction：拒绝所有false positive 发生的可能性，通过对p值进行校正来消除false positive。【校正公式：p*(1/n)   p –原始阈值 n 总校验次数】

# Discrete Optimization

* 时间复杂度：当问题规模扩大后，程序需要的时间增长有多快【不管数据规模多大，花费时间一定，O(1) 常数级别时间复杂度：数据量多大，时间就有多长。】

  PS: 通常选择的算法都是多项式级复杂度；非多项式时间复杂度，除非数据量较小，否则易超时。

* **P类问题**：若一个问题可以在多项式时间内找到它的解法，这个问题为P类问题。

* **NP类问题**：可以在多项式时间内**验证一个解**的问题(多项式时间内猜出一个解。

  * NP类问题不是非P类问题，P属于NP类问题，但P=NP? 还无法证明。

* **NP完全性的两个特性**：

  * we can check a solution quickly in a polynominal time.
  * if we can solve one NP complete quickly, we can solve them all.
  * **Find the best solution approach to the real answer, but not the global yes one.**

* **NPC类问题**

  * 约化reducibility：**问题A可以约化为问题B == 问题B的解法可以解决问题A**（问题B的时间复杂度高于问题A）
  * NPC类问题定义：**存在一个NP问题，所有的NP问题都可以约化成它**，解决了这一个问题就解决了所有NP问题，这就是NPC类问题。

  <img src='/images/img/NPC问题图.png'>

## Knapsack problem 背包问题

* 问题模型：给定一组物品，每种物品都有自己的重量和价格，**在限定的总重量内，选择物品使得价格更高**

* Greedy algorithm 2 solve knapsack prob--possible solutions:

  * Take the most valuable items 1st.
  * Take the small one at 1st, them bag as many item as possible
  * Use value density to decide bag order: dollars/weight

* How to model optimization problem:

  * define a description of the problem.

  * choose some **decision variables**(they typically encode the result we are interested in)

  * express the **problem constraints** in term of these variables.

  * express the **objective function**
    $$
    max ∑v_ix_i, i∈I\\
    s.t ∑w_ix_i≤K \\
    x_i∈{0,1},i∈I
    $$
    v-value，w-weight，x-choose or not
  
* Binary knapsack：背包问题的所有value只能取 0 or 1
  $$
  l≤∑w_kx_k≤u,k∈R \\
  x_k∈\{0，1\}
  $$
  eg: 10≤2x1+3x2+4x3+5x4≤12 , decision variable 只能取0，1

  **前后向图**来决定某一个decision variable 是否取0

  * 前向图：取值默认为1，根据权重进行调整

  <img src='/images/img/前向图.png'>

  * 后向图：根据限制条件排除不可能的情况

  <img src='/images/img/后向图.png'>

## Dynamic Programming

### Recurrence Relations - DP 计算方式及步骤

* Bellman Equation
  * Assume we know how to solve **O(k,j-1) for all k in 0,k**
  * We want to solve **O(k,j)**
  * If wj≤k, there are two cases:1) we don not select j, the best item is O(k,j-1) 2) we select j, the best solution is vj+O(k-wj,j-1)
  * Conclusion: **O(k,j) = max(O(k,j-1), vj+O(k-wj,j-1)) if wj≤k,else O(k,j) = O(k,j-1)**
* Dp 步骤：从状态0开始迭代计算，直到达到需要的状态。

### Branch&Bound--分支定界法

​        求解整数规划的常用方法，根据实际是否取用该变量构建树状图之后：通过判定<u>**树状图到子节点是否超过边界条件or是否当前选择步骤无法超过之前的最佳结果**</u>来确定剪枝缩短搜索空间范围，进而进行深度和广度优先搜索。

* branching：将问题划分为子问题
* bounding：找到每个子问题的最优解
* Optimization Tips：以背包问题为例，如果能够取部分值达到更优解，那么可以不必局限于是否必须取或不取。

<img src='/images/img/分支界定图.png'>

### Search Strategy -- 深度和广度优先搜索

* depth-first 深度

  当前节点估计比之前最佳方案差时，对该节点进行剪枝，不再计算后续节点的可能。

* best-first广度

  同理深度。

* least-discrepancy

## Constraint Programming--CP约束编程

* Use **constraints to reduce the set of values** that each variable can take
* **Remove value that cannot appear in any solution**
* make choice when no more deduction can be performed
* The choice can be wrong, which means backtracks is needed.

模型构建方法

* 尽可能描述清楚问题并表达清楚期望的架构。
* 尽可能提供所有的限制条件。

限制条件的作用

* 减小解的搜索空间
* 最终解的可行性确认（是否违反某一个限制条件）

一些限制的定义

* Reification：The ability to transform a constraint into a 0/1 variable. (variable = 1 if constraint is True)

* Global constraint：capture combinatorial substructure.

  * make more easier and more natural to explain to others.
  * convey problem structure to solver that does not have to rediscover it.
  * give the ability to exploit dedicate algorithms.
  * Discover in-feasibility earlier & Make search more efficient.

* **Symmetry breaking**: 许多问题自然带有搜索空间&结果对称的特性，在结果搜索时，只需要搜索对称结果一半的部分即可，不需要全部搜索，这样能够明显减少搜索空间及时间。

* **Redundant constraint**：不对模型解数量产生影响的前提下的其他限制条件。

* **First fail principle**：try 1st where you are most likely to fail, if fails, fails early!(若有m件任务需要全部解决才算成功，则优先解决最困难的一件，否则最困难的一件没有成功整件事情还是失败)

  

### magic series

* 问题模型：A series S = （S0,S1,...,Sn) is magic if Si represents the number of occurrences of i in S

  |             | 0    | 1    | 2    | 3    | 4    |
  | ----------- | ---- | ---- | ---- | ---- | ---- |
  | occurrences | 2    | 1    | 2    | 0    | 0    |

* redundant constraints: 最大值 = series长度；确定序列中一个值，其他值就会同步改变。

### magic square 

* 问题模型：在一个n*n的矩阵中填入数字，每行每列不同，但行、列、对角线和相同
* 思路：计算得到需要得到的和之后，二分查找减小搜索空间。

### Car sequencing-- 制造顺序安排

* 问题模型：根据流水线上每个制造步骤能够连续执行的次数及休息间隔制定最佳制造方案（A步骤执行2次休息1次，B步骤执行3次休息2次）。
* **Dual Modeling**
  * 将对于某个问题的不同模型方法进行组合后（限制条件等全部组合），大概率优势互补且得到全新的思路。

### Scene allocation --电影场景分配

* 问题模型：一部电影每天最多拍摄k个镜头，该电影的每个演员都已被安排拍摄某些镜头，且每个演员每天出现在现场都需要支付工资，问：如何将总支出最小。
* 思路：镜头安排的顺序上没有对称，但是在天数上可以达到-值对称
* 具体实现：镜头S，天数D
  * 对于S1，将其安排在D1后；
  * 对于S2,  余下的天数当中选择
  * 对于排序：已经用掉的天数+未被安排的一天新的，构成天数序列【减少搜索空间，不必每一个天数排序都试一遍。】

### BIBD(Balanced Incomplete Block Designs)

* 问题模型：
  * 输入：(v,b,r,k,l)
  * **输出：一个值全部为0/1的v行b列的矩阵，其中每行有r个1，每列k个1，任意两列乘积是1**
* BIBD对称性：满足上述条件的矩阵，任意教皇两行or两列，依然是满足条件的解法。
* 减少对成性搜索的方法：根据字典大小-lexicographic order（从上到下or从左到右序列值增大）

### Euler Knight Problem

* 问题模型：国际象棋棋盘上的骑士能够走完棋盘且每个位置只能走一次。
* 思路：从最容易失败的位置：角落开始，**每次的下一步每次选择余下步数最少的位置，**最终尝试连线。

### 8-queen problem

* 问题模型：国际象棋棋盘上放置8个皇后让他们无法互相攻击，皇后可以横竖斜走。
* <u>思路：1）国际象棋棋盘8*8，因此，每一列上都必须要有一个皇后被放置。2）**基于CP，棋盘上每次放置一个皇后之后，减少棋盘上可以继续放置的空间。**</u>【此处不带图，可直接搜索】
* decision variable：每一行用一个decision variable来进行描述，便于模型构建和限制条件描述。

### Four color map theorem --四色定理

* <u>**四色定理：如果在平面中划出一些相邻有限区域，那么一定可以用“四种”颜色来给这些区域染色，使得相邻区域两个颜色不相同。**</u>（every map can be colored with just 4 colors-1st computer proven theorem)

* 具体步骤：

  * 计算每个区域的相邻区域个数
  * 选择相邻个数最多的区域先上色（确保相互之间颜色不同）or **只剩1个颜色选择的优先。**
  * 重复上述步骤，直到所有区域被填上色

  <img src='/images/img/四色定理地图.png'><img src='/images/img/四色定理地图2.png'>

  Notes：起始为中间黑色部分，红色的虽然相邻5个，但5个互相之间相邻的只有4个，且**相隔一个可以使用相同颜色**，如图中两个黄色部分

### All different 类问题

* 问题模型：在所有给定的decision variable 中，保证**每个变量取值不同**，是否有解
* 思路: 建立假设表，每次假设一个decision variable 的值之后，根据假设去掉搜索空间，直到有解or冲突。
* 问题例子：X1∈{1，2}，X2∈{2，3}，X3∈{1，3}，X4∈{2，4}，X5∈{3，4，5，6}，X6∈{6，7}，在每个值取值不同的情况下，x4是否能取2

### The perfect square problem

* 问题模型：给定一系列正方形的顶点坐标，看他们是否能够再中间不留空白的情况下拼成一个大正方形。
* 思路：最终的形状必须要满足的性质
  * 4个角上1个点，余下的要么两个正方形相邻，要么4个顶点合并。
  * 3个正方形的情况，更大可能是两个相邻边+一个长边。
  * redundant constraint：大正方形随便一条线经过的所有正方形长度之和等于大正方形边长。
  * 每次放了一个正方形之后就考虑在它旁边放哪个正方形更合适。

## Local Search

* move from configuration 2 configuration by doing local move.(从任意情况开始，通过局部移动来实现对满足条件的限制结果搜索。)
* **移动后是否采纳主要取决于限制和冲突情况是否减少**
* 选择local move的时候，从包含限制条件最多/冲突最多的地方开始。
* 局部搜索无法确保获得全局最优解
* 常见移动：交换、
* 搜索空间不连续的情况：对当前搜索空间进行交换，直到搜索空间能够连接。
* Tabu search 禁忌搜索：跳出局部最优的方法之一，标记已搜索过的局部最优解，避免重复搜索，同时跳出局部最优解。
* **Simulated annealing模拟退火**：随机选择开始点，每次选择一个移动步骤，然后判断是否接受（好优化则接受，坏优化则一定概率接受）直到最终的函数值越来越小。

### Warehouse location problem

* 问题模型：给定仓库位置、造价、顾客位置及到每个仓库的距离，选择哪几个warehouse 开放使得**造价最低、顾客总距离最低**

### Travel salesman problem

* 问题模型：给定很多城市坐标，visit 每个城市1次不重复，使得总路径最小
* K-opt：选择n调路径，进行对应更换，用于缩短最终距离
  * 找到每一个点附近最近的点，先构成连接，然后逐渐去掉冲突（某个点有两个点相连的情况，找到附近一个没有被链接且距离最近的点进行替换解决冲突）

### Graphic coloring

* 问题模型：用最少的颜色，完成上千节点的着色工作，s.b. 相邻节点颜色不同
* 思路：
  * 初始化一定的颜色数量k，尝试进行着色，若不满足则增加数量；若满足则逐渐减少颜色总数，并调整着色，直到最终取得最优颜色数量
  * 若颜色存在冲突，可以通过交换颜色来优化确认是否最优点。
  * 优化：主客交换、队伍交换、轮次交换 来解决冲突

### Sports Scheduling

* 问题模型：赛程安排，constraint（转播收益、主客数量、队伍总路程，不能连续主场or客场 & ；两个队伍不能连续碰）--objective：优化总路程

## Linear programming 

* 问题模型示例：
  $$
  min~c_1x_1+...+c_nx_n\\
  s.b~ a_{11}x_1+...+a_{1n}x_n≤b_1 \\
  ...
  a_{m1}x_1+...+a_{mn}x_n≤b_m
  $$

  * min = - max
  * non-linear constraint 不能用在linear programming 当中。
  * discrete value variables can not used in linear programming
  * 等于的限制条件可以同步为：大于等于+小于等于

### Geometry of linear programs

* convex set 凸集：在集合中随机找两个点，若他们**连线中所有点都在集合当中**，则该集合叫做凸集。(eg:集合是个五角星，两相邻角的顶点连线就在集合外)

* Convex combination：
  $$
  λ_1v_1+...+λ_nv_n~is~a~convex~combination~of~v_1,..,v_n \\
  if~ λ_1+...+λ_n = 1~ and~λ_i≥0
  $$

  * the intersection of convex set is a convex set
  * every point in a polytope is a convex combination of its vertices

* 根据条件划定搜索范围后，由objective function 在划定范围中判定最优解（使得目标函数最大or最小的解）

* Theorem：至少由一个点在搜索范围中能够使得目标函数最小。

### The simplex algorithm--单纯形法

* 应用简单，但最坏情况耗时可能是指数级的。

* Guarantee to find the global optimum

* 实例：--goal: be on the top of the world

  * the top of the world is the top of a mountain
  * the top of a mountain is a **Beautiful Fantastic Spot（BFS)**
  * can move from one BFS to anther BFS, repeat until at the top of the world

* 如何将不等式转化为等式
  $$
  a_{11}x_1+...+a_{1n}x_n≤b_1 \\
  ...
  a_{m1}x_1+...+a_{mn}x_n≤b_m \\
  ...增加一个常量S_i后转化\\
  a_{11}x_1+...+a_{1n}x_n+S_1 = b_1 \\
  ...
  a_{m1}x_1+...+a_{mn}x_n+S_n = b_m \\
  $$
PS: 上式中增加的使等式成立的常量Si--slack variables
  
* 选择好目标变量与待替换变量，当目标函数中所有变量的系数值均为正，即视为达到最佳情况。

### Matrix Notation

* Used to simplify the presentation of calculation in linear programming，利用矩阵性质来对线性规划中的变量进行表达，简化后续计算。
* 示例：

<img src='/images/img/matrix_notation.png'>

### Duality derivation & interpretation 二元性推导

* Duality Theory：address itself to the study of the connection between two related linear programming problem.

* prime & dual formation:

  * primal:

  $$
  min~cx \\subject~to~Ax≥b~\&~x_j≥0
  $$

  * dual:
    $$
    max~yb\\subject~to~yA≥c~\&~y_i≥0
    $$

  * 示例：

    <img src='/images/img/primal_dual.png'>

* Theorem：If prime has an optimal solution,dual format also has an optimal solution with same cost.

* Dual of the dual is prime.

* The primal objective function is always greater or equal than the dual. So primal find minimum, dual find optimal

* Primal always feasible, but dual not, until optimality;

* Dual always feasible, but primal not, until optimality;

* 不管是primal还是dual，两类问题出发只要有一个找到optimal结果，那么新增限制条件，可以从当前的primal or dual 出发继续求解。

## Mixed Integer Programming 整数规划

* 定义：**规划中的变量（全部or部分）限制为整数。**
* **线性模型中,变量限制为整数，则为整数线性规划**
* 整数混合模型大多选择0/1为变量
* eg：warehouse problem： 某个warehouse 是否开门的变量取值限制为：0-开门；1-不开门

模型优劣

* 同等objective model，**限制条件更少or不强于之前的限制条件**的一个，视为更好的模型
* 模型等价只能一句条件弱到强而非强到弱。

### Cutting plans --割平面法

* 增加线性条件 == 在搜索空间中进行平面切割

示例：

<img src='/images/img/cut_plan1.png'>

上述三个限制条件可在平面上得到如下值，红色为x2<=1的切割平面。

<img src='/images/img/cut_plan2.png'>

根据红色线切割后得到下图：

<img src='/images/img/cut_plan3.png'>

去掉不是整数点之后的切割平面后得到下图最终结果

<img src='/images/img/cut_plan4.png'>

Conclusion：从最开始的限制条件绘制平面后，逐步增加新的条件限制进行优化，得到整数点。

### Gomory Cut

* 对于

TO BE CONTINUE ...

  

  

  

  

  


------

