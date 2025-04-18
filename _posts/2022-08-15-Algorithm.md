---
title: 'Algorithm'
date: 2022-08-15
permalink: /posts/2022/08/Algo-notes/
tags:
  - Theoretical Ground
---

Algorithms related notes.

# 多层感知机模型MLP

Perceptron：二分类，确认输入是否属于某个特定类别。【输入层+输出层】

* 层数可配置：输入、输出层。

* 训练过程通过权重调整提高分类效果。
* 可配置学习效率参数η，调整训练过程与权重更新比例之间的关系。
* 通过SGD随机梯度下降方式，直到损失函数在可接受范围。

* 局限性：仅支持高维空间**线性分类问题**

**多层感知机模型MLP：Multi-Layer Perceptron**

* 前馈人工神经网络feedforward neural network。
* 多层感知机模型可解决感知机无法解决的异或问题。
* 结构：包含一个或多个在输入层和输出层之间的隐藏层（hidden layer）
  * 除输入层，每个节点都使用**非线性激活函数的神经元sigmoid**。
  * MLP任意层中的每个神经元都与它前一层中的所有神经元或者节点相连接，连接的强度由网络中的权重系数决定。
* 传递函数：sigmoid，tanh等

**训练步骤**

* 确定输入和当前权重下的输出。
* 实际输出和label计算得到误差。
* 根据误差函数更新权重，直到最终误差在可接受范围内。
* 训练过程中，误差反向传播back-propagation确保损失逐渐下降得到最终值。
* 通过平方项的形式，减少误差正负相互影响。

**经验参数**

* 训练样本数 = 10* 权重系数
* loss function 不再下降即可停止学习。
  * 与迭代次数相关
* 根据需要可设定其他训练结束的条件。

# 自组织映射Self Organizing Map

自组织映射  = 无监督+神经网络

* 降维：高维数据映射到低维，保留本身数据结构特征。**将输入转为一维或二维离散映射。**
* 各神经元系数通过竞争得到，基于数据专注于局部优化。
* 竞争学习>纠错学习：不取决于预设权重系数，通过竞争取得最优解。
* 可认为是一个：encoder-decoder模型

**自适应过程**

* 排序阶段：权重系数的拓扑排序形成。
* 收敛阶段：微调特征映射实现对输入模式的精确描述。只要算法参数没问题，自组织映射就能将完全无序的初始状态按照输入模式以有组织的方式重构。

# 模糊神经网络

**模糊神经网络（fuzzy neural network）**：常规神经网络+模糊输入信号+模糊权值。【利用神经网络实现模糊逻辑推理。】

* **模糊集合中，元素和集合间的关系不是非此即彼的明确定性关系，而是用做隶属度的函数定量表示**
  * 隶属度：百分之多少属于A类，百分之多少属于B类。
* **模糊数**：只有取值范围而没有精确数值的数。模糊数+精确数的运算结果是模糊数。

## 构成&训练

* 基本单元：模糊化的神经元。【输入和权重系数均为模糊数、传递函数也需要对模糊集合加权处理】
* 训练方式同传统的神经网络：min loss function。
  * 误差处理方法：**基于水平集的方法** & **基于遗传算法的方法**
  * 基于水平集的方法：**通过确定模糊集合的水平集对模糊数中的元素加以筛选。**
    * 假如一个模糊数包含三个元素 x、y 和 z，参数分别是 0.3、0.6 和 0.7，当截断点等于 0.5 时，这个模糊数的 0.5 水平集会把参数为 0.3 的元素 x 过滤掉，只保留参数大于 0.5 的 y 和 z。
    * 水平集方法的致命缺陷：缺乏理论依据。一个不加任何限制的模糊数肯定不能用有限个参数来描述。

* 若保持学习率参数不变，误差函数难以快速收敛。即使收敛也可能陷入局部最小值，在不同学习率参数下得到不同的局部最小值。
  * 引入“**共轭梯度（conjugate gradient）”的机制**：使训练过程尽可能能够找到全局最优解。
  * 最优学习效率通过：优化算法经过训练最终得到。

# 支持向量机SVM

SVM(Support Vector Machine): **二分类算法**，通过构建**高维空间的超平面**实现分类。

* 线性可分数据：SVM弱化为--线性可分支持向量机。【特例】
* **如果样本的属性数有限，那么一定存在一个高维特征空间使样本可分。**【将原始低维空间上的非线性问题转化为高维新空间上的线性问题】

**可选超平面中最优解：** 与两类别间隔同时最大，使得噪声干扰划分准确度影响最小。

**高维特征空间超平面描述方程**
$$
w^Tx+b = 0
$$

* w:  法向量，决定超平面方向。
* b：截距，决定超平面和高维空间中原点的距离。

**Maximum margine（基于上述超平面描述方程，样本到超平面距离）**
$$
r = \frac {w^Tx+b} {||w||}
$$
基于上述超平面方程的划分方式：
$$
w^Tx_i+b≥1-ξ_i, y_i = +1 \\
w^Tx_i+b≤1+ξ_i, y_i = -1
$$
说明，ξ_i 为松弛变量，考虑到边界情况部分点不支持硬间隔1的条件。

## 支持向量

**特征空间中，两类样本中距离划分超平面最近的点【这类点能让上式取等号】**

PS：详见[西瓜书](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://jingyuexing.github.io/Ebook/Machine_Learning/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0_%E5%91%A8%E5%BF%97%E5%8D%8E.pdf)

* **两个不同类支持向量**到超平面的距离之和为： 2/||w||。【因此对线性可分支持向量机，任务就是在满足划分方式的情况下找w，最大化距离之和。】
  * PS: max 2/||w|| == min 0.5||w||^2
  * 优化目标修改为：0.5||w||^2+C∑ξi, C>0 【惩罚函数：使间隔尽可能大，】

## 核函数 kernel function

​        使用支持向量机，低维空间到高维空间是通过核函数映射，非线性变换形式实现。假设原始空间是**低维欧几里得空间X**，新空间为**高维希尔伯特空间H**，则从 X 到 H 的映射可以用函数 ϕ(x):X→H 表示。核函数可以表示成映射函数内积的形式，即:
$$
K(x,z)=ϕ(x)⋅ϕ(z)
$$
核函数特点：

* **计算过程在低维空间完成**，避免高维空间复杂计算。
* 对给定核函数，高维空间H和映射函数ϕ取值不唯一。
* 一般核函数都是正定核函数
  * 正定核函数充要条件：函数中任意数据的集合形成的核矩阵都是半正定的。

**常用核函数**

* 线性核：
  $$
  K(X,Y)=X^TY
  $$

* 多项式核：
  $$
  K(X,Y)=(X^TY+c)^d
   ，c
   为常数，d≥1
   为多项式次数
  $$
  
* 高斯核：
  $$
  K(X,Y)=exp(−\frac{||X−Y||^2}{2σ^2})
  ，σ>0
   为高斯核的带宽
  $$
  
* 拉普拉斯核:
  $$
  K(X,Y)=exp(−\frac{||X−Y||^2}{σ})
  ，σ>0
  $$
  
* sigmoid核：
  $$
  K(X,Y)=tanh(βX^TY+θ)
   ，β>0,θ<0
  $$



# 聚类cluster

无监督学习，先划分数据再确定类别，属于同一类的数据之间需要进行相似性度量。

**相似性度量方式--距离（N维空间中两个样本点的距离）**

常用距离-闵可夫斯基距离：
$$
dist_{mk}(x_i,x_j)=(∑_{n=1}^N|x_{in}−x_{jn}|^p)^{\frac 1 p}
$$

* p 为 常数，p=2时，上式为欧式距离，即长度。

## k-means cluster

聚类问题转化为最优优化问题：让**所有样本到其聚类中心距离最小。**【贪心选择聚类中心】

**算法过程**

* 从数据集随机选取 k 个样本作为聚类中心。【**需要先确定聚类中心数量k**】
* 分别计算其余样本到这 k 个中心的距离，并将样本划分到离它最近的中心类。
* 所有样本聚类归属确定后，再**计算每个聚类中所有样本的算术平均数**，更新聚类中心，并将所有样本按照 新的中心重新聚类。
* 重复上述步骤，直到聚类结果不再变化。

## 分布聚类

**基于概率模型的聚类，核心思想是假定隐藏的类别是数据空间上的一个分布**。

* 每个类都是**最可能属于同一分布**的对象的集合。
* 类似数理统计获得样本的方式，每个类都由总体中随机抽i.i.d的样本组成。
* 缺点: 无法确定隐含的概率模型是否真的存在，因而常常导致过拟合的发生。

若将样本看作观察值，潜在类别看作隐藏变量，可认为**数据集是由不同的聚类产生**。因此，基于概率模型的聚类分析的任务是**推导出最可能产生出已有数据集的 k** 个类，并度量这 k个类产生已有数据集的似然概率。

## 密度聚类

核心思想：样本分布密度决定聚类结构。

* **每个样本集中分布的区域都可以看作一个聚类**，**聚类之间由分散的噪声点区分**
* 考察样本间可连接性，再基于可连接样本不断扩展聚类以获得最终结果。

### 利用噪声的基于密度的空间聚类

Density-Based Spatial Clustering of Applications with Noise，DBSCAN

* 通过距离在某一阈值内的点连接起来而形成聚类，连接对象仅限于满足密度标准的点。
* 密度可连接性：通过密度直达关系、密度可达关系、密度相连关系等标准定义。

# 降维学习

## 主成分分析PCA

Principle-Component-Analysis

* **利用正交变换将一组可能存在相关性的变量转换成一组线性无关的变量，这些线性无关的变量就是主成分**。
* 充分挖掘属性间的相关性，降低属性空间维度。
* **并不是选择性保留部分原始特征，而是利用特征之间的相关性构造新特征。**

# 深度广度优先搜索

**六度分割理论**：你与世界上的另一个人间隔的关系不会超过六度，也就是说平均只需要六步就可以联系到任何两个互不相识的人。

* 广度优先搜索Breadth-First-Search：从最近的范围开始遍历，然后逐渐向外。
  * 图结构下的广度优先搜索时间复杂度：O(边数)
  * 空间复杂度：O（顶点数）
* 深度优先搜索Depth-First-Search：一个点从近到远遍历完后，再对下一个点重复操作。【基本借鉴：回溯思想，搜索到无法进一步搜索了就回退，对下一个点进行搜索】
  * 图结构下的深度优先搜索时间复杂度：O(最深顶点数）
  * 空间复杂度：O（顶点数）
* 代码实现时需要注意：不同的数据结构中需要考虑【list存储已经遍历过的点、已经遍历过的搜索路径，防止重复访问】

# 字符串匹配

主串A（长度为n）中查找字符串B（长度为m），n>m，那么在主串A中就有n-m+1个长度为m的子串需要被一次匹配。

## 暴力匹配 Brute-Force BF-O(n*m)

* 基本思路：从A起始位置0开始，检查向后m长度的子串是否与B匹配，成功匹配后返回or全部搜索完后返回。
* 时间复杂度：最坏情况下O(n*m)【每一个位置都要比m次】
* 虽然时间复杂度高，但实际开发中常用原因：1）模式串和主串都不会太长，且极大概率不会到最坏情况；2）代码实现简单、出错概率低

## Rabin-Karp RK-O(n)

BF算法暴力匹配的基础上引入hash。

* 基本思路：通过hash对n-m+1个子串分别求hash值，将这些hash值与待搜索的hash值比较，看是否有相等值。

* 因为hash值是数字，数字之间的比较速度更快，效率更高。但每个子串都要计算hash时间也长【通过对hash算法进行有效设计来实现上述情况】。

  * 假设要匹配的字符串字符集中只包含K个字符，可以用一个K进制数来表示一个子串。
  * 这个K进制数转化为十进制数作为子串hash值。

  ```
  * a-z 字母，就用26进制数来表示[0-25]
    eg: "cba"=2*26^2+1*26+0*26^0=1353
  * 假设主串A中，仅包含26个字母，那么每次计算子串hash值时除了第一个需要完整计算，后续的都可以修改为：加下一个的hash值&减第一个的hash值
  ```

* 时间复杂度：O(n) [n个元素都遍历一次计算hash值]

* **基于hash值相等判断匹配的办法需要考虑hash冲突，当hash相等时，多一次对比子串和模式串B确认即可。**

## Boyer-Moore BM算法

KMP算法性能的3-4倍。

* **核心思想**：主串A不动，模式串从主串头开始类似“滑动窗口”方法，依次比较每一个位置，一旦有一个位置不满足，模式串就向后滑动一位重新从模式串第一位开始对应比较，直到匹配or搜索完。

  * **plus【跳过一些必定不匹配的情况减少查询提高效率】：<u>若比较的主串某一个位置的字符在模式串中一定不存在，则可以直接将模式串滑动到该位置的下一个为止，减少匹配</u>。**

* **算法原理：坏字规则&好后缀规则**

  * 坏字规则：bad character rule，最好情况下时间复杂度O(n/m)

    * **<u>按照模式串下标从大到小匹配</u>**，当某个字符无法匹配时，将其定义为“坏字符”；

    * 若坏字符不在模式串中，那么直接将模式串滑动到该坏字在主串中的下一位，减少匹配耗时。
    * 若坏字符在模式串中，则将模式串中**第一个**与该坏字符相等的字符串与之对其后在进行比较。

  * 好后缀规则：good suffix shift

    * **<u>按照模式串下标从大到小匹配</u>**，当某个字符无法匹配时，将前面已匹配的字符串定义为“好后缀”
    * 将好后缀在模式串中查找，若找到了除了后缀以外另一个匹配的子串，则将模式串滑动到该子串与主串对应的位置；若找不到另一个匹配的子串，就将模式串滑动到好后缀的后面一个为止继续匹配【可能出现错过匹配的情况】；
    * 对于上述可能错过的情况，观察好后缀的后缀子串是否能够与模式串的前缀子串匹配。

  * 两种方式的选择：max（好后缀滑动位数、坏字符滑动位数）

* **代码实现**【如何计算移动位置】

  ​       使用hash table ，存储每个字符串可能存在的下标位置（方便查找），与当前模式串位置比较，按照坏字符&好后缀标准进行选取。

## Knuth Morris Paratt-KMP 算法 

假设主串是a，模式串是b，遇到不匹配的情况时，能够将模式串向后多滑几位跳过一定不匹配的情况。

* **算法原理：坏字规则（同BM）&好前缀规则(从前向后匹配一致的部分)**

  * 当遇到坏字符时，将模式串向后滑动。滑动过程中，只要模式串和好前缀有上下重合（模式串首位还未滑动到坏字符位置之前）== 好前缀后子串和模式串前缀串比较，

  * **在好前缀的后缀子串中，查找最长的可以跟好前缀的前缀子串匹配的。**这样滑动的时候就可以直接向后滑动到1st和好前缀最长前缀子串匹配的位置后重新比较。
  * 最长可匹配后缀子串：好前缀所有后缀子串中，最长的可匹配前缀子串的后缀子串。
  * 最长可匹配前缀子串：同上相反。
  
  PS: 最长可匹配前后缀可以在匹配之前预处理计算。

### next数组/失效函数

用来存储模式串中每个前缀（都可能是好前缀）的最长可匹配前缀子串的结尾字符下标。

模式串：ababacd

| 模式串前缀              | 前缀结尾下标 | 最长可匹配前缀字符串结尾下标 | next       |
| ----------------------- | ------------ | ---------------------------- | ---------- |
| a                       | 0            | -1(不存在)                   | next[0]=-1 |
| ab                      | 1            | -1                           | next[1]=-1 |
| <u>a</u>b**a**          | 2            | 0（最长可匹配就是：a）       | next[2]=0  |
| <u>ab</u>**ab**         | 3            | 1（最长：ab）                | next[3]=1  |
| <u>ab</u>**<u>a</u>ba** | 4            | 2(最长：aba)                 | next[4]=2  |
| ababac                  | 5            | -1                           | next[5]=-1 |

PS: 最长可匹配前缀也是模式串前缀中的前后缀在比较

* next数组具体计算
  * 找到每一个前缀的所有后缀串，从长到短比较。
  * 通过动态规划寻找最长可匹配前后缀。

### 复杂度分析

* 空间复杂度：O(m) 。【大小为m的额外数组，与模式串大小相同】
* 时间复杂度：O(m+n)
  * 构建next数组：O(K*M)【m为模式串长度，K为每次计算匹配执行次数】
  * 借助next进行匹配：O(n)【最大长度n-1】

## AC自动机-Aho Corasick

**敏感词过滤-字符串匹配**

* 基本实现：通过维护一个敏感词字典，将输入的敏感词进行过滤【对于访问量极大，性能要求极高的情况，维护敏感词字典效果耗费及延时较大。】

* **多模式串匹配算法**：Trie树【一次性匹配多个字符串】，将敏感词构成一个Trie树结构即可实现多模式串匹配【预处理】。

**AC自动机：**建立在字典树的基础上，加入了辅助数组next，类似于KMP，使得匹配过程跳过许多必定不匹配的情况，提高匹配效率。

* 建立AC自动机：多模式串构成Trie树+在Trie树当中构建失败指针。
* 时间复杂度：近似O(n)

# 贪心Greedy algorithm

经典应用：霍夫曼编码HuffmanCoding、Prim&Kruskal 最小生成树算法、Dijkstra单源最短路径算法、

* 经典示例：背包问题Knapsack problem【给定能够容量重量为Xkg的背包，可装入不同物品，每种物品重量和总价值各不相同，如何选择使得总价值最大。】

* **核心思想：给定限制条件下，如何取变量值使得目标函数最大。**
* 贪心算法，不一定能找到全局最优。

## 实例1-分糖果

* Question：m个糖果和n个孩子，m<n。每颗糖果大小不等，这 m 个糖果的大小分别是 s1，s2，s3，……，sm；每个孩子对糖果大小需求不一样，只有糖果的大小大于等于孩子的对糖果大小的需求的时候，孩子才得到满足。假设这 n 个孩子对糖果大小的需求分别是 g1，g2，g3，……，gn，如何分糖果满足尽可能多的孩子。
* Solution：从需求小的孩子开始分配，能用等于需求的糖果就不用大于需求的，【**每次从当前剩下孩子中找到糖果需求最小的分：满足一个大孩子和小孩子对结果贡献度一样**】

## 实例2-钱币找零

* Question：面值不同的纸币【例：1 元、2 元、5 元、10 元、20 元、50 元、100 元】，张数分别是 c1、c2、c5、c10、c20、c50、c100。要用这些钱支付 K 元，最少要用多少张纸币？

* Solution：每次选择所有面值中最大但小于剩余需要支付面额值的一个支付，这样总使用钱币数最少。

  PS: 考虑动态规划，避免最终无法凑到需要找零的数字。

## 实例3-区间覆盖

* Question：假设有 n 个区间，区间起始点和结束点分别是 [l1, r1]，[l2, r2]，[l3, r3]，……，[ln, rn]。从这 n 个区间中选出一部分区间，这部分区间满足两两不相交（端点相交的情况不算相交），最多能选出多少个区间呢？
* Solution：首先获得最左端点lmin，最右端点rmax。将区间从小到大排序后，每次选择左端点和前面已覆盖区间不重合，右端点尽量小的【排序后：在不覆盖的情况下，从小到大选择覆盖区间范围最小的==数量最多】

## 实例4-huffman coding

* 一个包含1000字符的文件，每个字符占1byte（1byte = 8 bits),如何存储节省空间
  * Solution1：假设统计后发现这1000个字符只包含6种不同字符，而3个二进制位就可以存8中不同字符，因此这1000个字符只需要3000bytes即可。
* **Huffman coding**
  * 考虑字符之外，再考虑字符出现频率，根据出现评率不同选择不同长度编码【频率越高，长度越短，节省越大】
  * **各个编码不等长 & 一个编码不能是另一个编码的前缀**
  * 根据出现频率调整编码长度后，1000字符所需空间会进一步下降到3kbytes以下。
  * 将字符串按照出现频率由高到低构成树结构【从根到叶子，频率从高到底】

# 分治Divide and conquer

将原问题分解为n个规模较小，且结构与原问题相似的子问题，递归解决这些问题。

**应用示例**

* n个数据，期望从小到大排列：【完全有序数据--有序度：n(n-1)/2,逆序度：0】【倒序数据--有序度：0，逆序度：n(n-1)/2】
* eg：2,4,3,1,5,6 , 逆序对：2,1、3,1、4,3、4,1
* 代码实现：从头向后遍历，计算逆序总数or 将数组分为两部分A,B，单独计算A和B的逆序对+AB之间的逆序对后迭代计算。

# 回溯

概述：**<u>类似枚举</u>**的搜索尝试过程，在搜索尝试过程中寻找问题的解，**当发现已不满足求解条件时，就回溯（退回到上一个岔路口），尝试别的路径**。回溯法是一种选优搜索法，按选优条件向前搜索，已达到目标。

* 把问题的解空间转化成图或者树的结构表示，然后使用深度优先搜索进行遍历，遍历过程中记录和寻找所有可行解或者最优解。基本思想类同于：1) 图的深度优先搜索 2）二叉树的后续遍历
* **实现思路**：按照需求构建满足要求的递归序列，找准结束条件后，统一返回。

## 回溯的两个经典问题

* 0-1背包：背包问题+物品不可分割，装or不装
* 8-queen problem
* 正则表达式：判断通配符是否满足正则表达式定义，通过回溯确定目标字符串是否能够达到最大匹配。

# 动态规划DP

DP-  dynamic programming

动态规划同样也是优化问题【空间换时间】

* 只要**问题可以划分为规模更小的问题**，并且原问题的最优解中包含了子问题的最优解，则可以考虑用动态规划解决。（eg：后一步的总数=前面两步可能的总数之和）
* 实质：**将问题示例分解为更小的相似子问题，并存储子问题的解，子问题只求解1次，最终获得原问题的答案，以解决最优化问题的算法策略**
* 类似贪心问题，将问题归纳为更小、相似子问题，通过求解子问题产生一个全局最优解。另：贪心不断选择当前最优解来逐步近似全局最优；动态规划通过求解局部子问题的最优解来达到全局最优。
* 在dp问题中，每一个可选项只保留状态最好的一个往下计算，减少计算量。

## 适合动态规划的问题

* 一个模型：多阶段决策最优解模型【每一个子问题当中多个解选择其中的最优】
* 三个特征：
  * 最优子结构：问题最优解包含子问题的最优解。【dp通过逐层推导得到总问题最优解】
  * 无后效性：【推导下一阶段状态时，只关心前一阶段状态值，而不关心这个值是怎么来的】
  * 重复子问题：不同的决策序列到达相同阶段时，可能产生重复的状态【二维数组除了左上角起点外，都有很多种不同的可能性】

## 解题思路

Q：有一个 n * n 的矩阵,存储的都是正整数。棋子从左上角开始到右下角，每次只能向右或者向下移动一位。把每条路径经过的数字加起来看作路径的长度。从左上角移动到右下角的最短路径长度是多少呢？

**状态转移表法**

一般都是二维表（二维数组），根据题目条件计算当前阶段最优状态

​                           状态表当前= min(上方，左方)+原矩阵当前

最终右下角的值为最终解。

**状态转移方程**

* 状态转移方程是解决dp问题关键【上面那个公式实际也就是状态转移方程】

## 搜索引擎拼写纠错

* **编辑距离Edit distance**：量化两个字符串相似度

  **将一个字符串转化成另一个字符串，需要的最少编辑操作次数**（比如增加一个字符、删除一个字符、替换一个字符）。编辑距离越大，说明两个字符串的相似程度越小；相反，编辑距离就越小，说明两个字符串的相似程度越大。对于两个完全相同的字符串来说，编辑距离就是 0。

  * 根据所包含编辑操作种类不同，有多种距离计算方式。

# 拓扑排序

Q：如何确定代码源文件的编译依赖关系

一个完整的项目会包含很多代码源文件。编译器在编译整个项目的时，需要按照依赖关系，依次编译每个源文件。<u>编译器如何通过源文件两两之间的局部依赖关系，确定一个全局的编译顺序呢？</u>

Solution：**直观感受-有向图【图的拓扑排序有关】**

**原理：**根据依赖关系构成有向无环图（依赖中有环就无法工作了），

## 两种实现方法

* 深度优先遍历：
  * 通过邻接表构造逆邻接表后递归处理每个顶点。
* **Kahn算法：**
  * 找到图中入度为0的点，将其放入排序结果数组中
  * 从图中删除上面的点【将这个点指向的所有点的入度-1，本身入度设为-1】
  * 重复执行上面两步，直到全部排序完成。

* 时间复杂度：均为O(顶点个数+边的个数)

# 最短路径算法Shortest path Algorithm

Object：地图软件的路线规划问题

**地图建模**：将地图抽象成图---有权有向图

* 每个岔路口看做一个顶点，岔路口与岔路口之间看做一条边，路的长度就是边的权重。
* 单行道/双行道：有向图

**最短路线**：根据地图建模，问题抽象为**“有权有向图中两点最短路径”**，最短路径经典算法-Dijkstra

## Dijkstra

* 目标：寻找图中节点之间的最短路径，特别是一个节点到所有其他节点的最短路径。
* 场景：GPS设备使用此算法来寻找当前位置到目标位置最短路径。

**Basic notes**

* 从指定的节点出发，寻找与它图中所有其他节点之间的最短路径。
* 每次记录当前已知最短路径，并在寻找更短路径时更新。
* 一旦找到源节点与其他店之间的最短路径，那个节点会被标记为“已访问”并添加到路径中。
* 重复上述过程，直到图中所有节点都已添加到路径中，这样就可以得到源节点出发访问所有其他节点的最短路径方案。

**必要条件**：图权重必须为正，根据路径长度计算最短路径，避免负权重打乱计算更新。

### 算法示例

[参考](https://www.freecodecamp.org/chinese/news/dijkstras-shortest-path-algorithm-visual-introduction/)

* 初始化vertexes 数组，记录从初始顶点到每个顶点的距离dist，初始化每个值都为无穷大。
* 计算图中权重值之和得<u>到更小距离后更新数组对应的值</u>，重复计算遍历所有边之后，最终vertex数组中所有值即为起始点到图中其他点的最短距离。
  * 计算过程中，每次从图中未被记录到路径的点中到目标点最短的路径上进行扩展。
* 同时维护一个数组predecessor记录图中每个顶点的前驱顶点，通过递归方式打印路径；一个inqueue数组避免将一个顶点多次重复添加到优先级队列中,记录已经被访问的节点。
* 时间复杂度O(边数*log顶点数)

### 优化方案

* 大地图中找方案，最短路径也只会出现在两点之间&两点之间附近，并不会很发散，减少Dijkstra 遍历范围，提高效率。
* 对于较远的路线规划，可以先规划处大方向，再逐渐细化到必须经过哪几条路。

## 最少时间&最少红绿灯

将上述算法中权重值从路长修改为通过这段路需要的时间即可。

​     PS:拥堵情况的考虑

## 通过某段路的时间计算

路长、红绿灯个数、时间、拥堵情况【实验统计、交通部门合作获得】

# 位图BitMap

Q1：URL记录后去重。[添加url&查询url&上亿url内存存储效率高]

**简化版问题示例**

Q2: 1kw个整数，范围在1-1亿之间，如何快速查找某个整数是否在这1kw个数中。

* 申请大小为1亿，数据类型为布尔值的数组，这1kw个数在上述数组中对应下标位置设为true
* 是否存在某个值，只需看上述布尔值数组对应值是否为true即可。
* **<u>布尔值进一步优化：用一个二进制位bit表示，节省存储空间</u>**。

## 位运算表示二进制位

* 位图通过数组下标来定位数据，访问效率提高

* 每个数字用一个二进制表示，范围不大时，内存空间非常节省。

  Q2为例：

  * 散列表：1kw数据，32位整型，每个4字节，总共40MB。

  * 位图：1-1亿，只需1亿个二进制位，共12MB。

    PS: 若范围在1-10亿，则需要120MB，反而增大

## 布隆过滤器

位图的改进，解决范围过大时内存占用反而更多的情况

以Q2为例，1kw数据，范围1-10亿

* 申请大小1亿的位图，通过hash函数，将数据映射到1亿范围内。

  PS: f(x) = x%n,取模求余

* 对于可能存在的hash冲突，布隆过滤器通过多个hash函数一起定位一个数据，降低可能冲突的概率，但可能对存在情况误判。

# 概率统计

Q：朴素贝叶斯算法过滤垃圾短信、邮件、电话等

## Naïve Bayes

分类问题当中的基准模型，模型简单值得尝试，分类效果不一定好，可以用于基准方法。

* 基本背景：Naïve Bayes 是基于贝叶斯定理及特征条件独立假设的分类方法。
* 优点：所需估计参数少，对数据不敏感，算法理论简单。
* 缺点：需要假设模型的属性之间相互独立，实际中往往不成立。
* 三种贝叶斯模型及python实现

```
from sklearn.naive_bayes import GaussianNB,BernoulliNB,MultinomialNB
```

   **高斯（特征是连续变量，假设模型正态分布）、伯努利（离散特征）、多项（常用语文本分类，特征是单词，值是出现次数的情况）**

**贝叶斯公式**：
$$
P(A|B) = P(A*B)/P(B)=P(B|A)*P(A)/P(B)
$$
将垃圾信息定义为：Wn为目标词汇
$$
P(垃圾信息|W_1,W_2,...,W_n同时出现在一条信息中)    ~    (1)
$$
根据上述贝叶斯公式转换后得到某个信息是垃圾信息的可能性概率，若为独立事件，则上述公式(1)可以转化为:
$$
(1) = P(W_1在信息中|信息是垃圾信息)\\
      * P(W_2在信息中|信息是垃圾信息)\\
      *...\\
      *P(W_n在信息中|信息是垃圾信息)
$$
P(W_1,W_2,...,W_n同时出现在一条信息中) 的概率可通过计算非垃圾信息中次概率来反推上述贝叶斯公式要求的部分。

# 向量空间-简单推荐系统

简单音乐推荐系统实现

## 问题解析

**基于相似用户做推荐：**找到喜好相似的客户，将他们的歌曲推荐给你

* 喜好定义：根据收藏歌单相同歌曲的重合数量，超过某个阈值就认为两者相似。

* 喜好程度定义：通过用户行为对不同操作定义得分，得分越高喜好程度越高，示例：

  | 单曲循环 | 分享 | 收藏 | 搜索 | 听完 | 没听过 | 跳过 |
  | -------- | ---- | ---- | ---- | ---- | ------ | ---- |
  | 5        | 4    | 3    | 2    | 1    | 0      | -1   |

  通过上述得分定义后，对于不同用户在不同歌曲上的喜好程度得分，可以构建向量图；<u>根据向量图中两个用户之间的距离是否在某个阈值范围内确定喜好度是否相似</u>。

**基于相似歌曲做推荐**

通过计算歌曲之间的相似度仿照上述方式进行推荐，相似得分越高，越先推荐。

* 相似度定义1：歌手、节奏、情感等【需大量数据支撑】
* 相似度定义2：对于两首歌，如果喜欢听的人群都差不多，侧面就反映出，这两首歌比较相似。

# B+树-mysql数据库索引实现

**问题需求**

* 根据某个值查找数据：select * from table where column = 值；
* 根据区间查找某些数据：select * from table where column >值 and column < 值；

**解决方式**

类似于跳表，改进二叉搜索树构成B+树实现

## 二叉树改造为B+树过程

* 树中的节点并不存储数据本身，仅作为索引。
* **每个叶子节点串在一个链表上**，链表中的数据从小到大有序。【注意下图中，叶子节点的链表包含了所有的数据】

<img src="/images/img/二叉查找树改造为B+树.jpg">

改造后，若要查找某个区间的数据，只需：

* 区间起始值在树中查找
* 找到某个叶子节点后顺着链表向后遍历
* 直到链表中节点数值大于区间终值位置
* 所有遍历到的数据就是符合区间值的数据。

数据达到千万or上亿级别，将索引存在硬盘而非内存中，时间换空间。

二叉树可以进一步修改为m叉树减少树高度，降低磁盘IO操作。

## B+ 树特点

- 每个节点中子节点的个数不能超过 m，也不能小于 m/2；
- 根节点的子节点个数可以不超过 m/2，这是一个例外；
- m 叉树只存储索引，并不真正存储数据，这个有点儿类似跳表；
- 通过链表将叶子节点串联在一起，这样可以方便按区间查找；
- 一般情况，根节点会被存储在内存中，其他节点存储在磁盘中。

# A* 搜索-游戏自动寻路功能

**问题分析**

* 在地图中找到一条从起点到终点的路径，且这条路径需要**绕过所有障碍物&路线不能太绕**。
* 最短路径是理论上的最优解，但当地图非常大时，最短路径算法耗时会相当大，这种效率是无法接收的。
* 实际情况下，类似出行线路规划、游戏寻路等，不需要非得寻求最优解。可以使用线路质量&执行效率综合后的次优解。

## A* 搜索说明

 对Dijkstra的优化和改造。

* Dijkstra 每次搜索所有点中距离当前节点最近的点，因此可能出现部分搜索与目标点相反甚至越来越远的情况。
* 通过计算每次搜索点与目标终点之间的距离f(g)+起点到搜索点的距离h(g), f(g)+h(g) 综合判断当前值在优先级队列中的位置，防止搜索过程中的最近点位方向跑偏。

与Djikstra相比

* 除了和起始点记录的计算外，还加入了到终点的距离，两者综合作为评价标准，防止搜索方向跑偏，提高搜索效率。
* 能迅速找到较优路线，但不一定是最短。【A* 根据新加入的到终点的距离构建评价函数，每次选择最短的一旦走到终点就停止搜索】

## 游戏寻路中应用

* 利用 A* 算法解决这个问题，只需把地图抽象成图。不过，游戏中的地图并不像我们现实生活中，存在规划非常清晰的道路，更多的是宽阔的荒野、草坪等。所以，没法把岔路口抽象成顶点，把道路抽象成边。

* 另一种抽象思路：把整个地图分割成一个一个的小方块。在某一个方块上的人物，只能往上下左右四个方向的方块上移动。【有障碍就限制某个方向的移动】
* 把每个方块看作一个顶点。两个方块相邻，我们就在它们之间，连两条有向边，并且边的权值都是 1。所以，这个问题就转化成了，在一个有向有权图中，找某个顶点到另一个顶点的路径问题。将地图抽象成边权值为 1 的有向图之后，我们就可以套用 A* 算法，来实现游戏中人物的自动寻路功能了。

# 索引-海量数据中快速查找某数据

## 为什么需要索引

* 实际开发中，抛开业务和功能的外壳，本质都可以抽象为“对数据的存储和计算”。对应到数据结构和算法中，“存储”需要的就是数据结构，“计算”需要的就是算法。

* 存储的需求，功能上无外乎增删改查。一旦存储的数据很多，性能就成了这些系统关注的重点，特别是在一些跟存储相关的基础系统（比如 MySQL 数据库、分布式文件系统等）、中间件（比如消息中间件 RocketMQ 等）中。

* “如何节省存储空间、如何提高数据增删改查的执行效率”，就成了设计的重点。而这些系统的实现，都离不开**索引**。索引设计好坏，直接决定了这些系统是否优秀。

## 索引的需求定义

### 功能性需求

* **格式化还是非格式化数据**：对于非结构化原始数据，需要做预处理，提取出查询关键词，对关键词构建索引。

* **静态数据还是动态数据：**
  * 静态数据：不会有数据的增加、删除、更新操作。【构建索引只需考虑查询效率】
  * 动态数据：不仅要考虑到索引的查询效率，在原始数据更新的同时，还需要动态地更新索引。支持动态数据集合的索引，设计起来相对也要更加复杂些。

* **索引存储在内存还是硬盘：**内存中查询的速度肯定比磁盘中的高。但数据量很大，对应的索引可能也会很大，因为内存有限，可能就不得不将索引存储在磁盘中了。还有第三种情况，那就是一部分存储在内存，一部分存储在磁盘，兼顾内存消耗和查询效率。

* **单值查找还是区间查找：**
  * 单值查找：查询关键词等于某个值的数据。
  * 区间查找：查找关键词处于某个区间值的所有数据。

* **单关键词查找还是多关键词组合查找：**搜索引擎中构建的索引，既要支持一个关键词的查找，也要支持组合关键词查找。

### 非功能性需求

* **不管是存储在内存中还是磁盘中，索引对存储空间的消耗不能过大**。

* **考虑索引查询效率的同时，还要考虑索引的维护成本**。

## 构建索引常用的数据结构

* **散列表**增删改查性能非常好，时间复杂度是 O(1)。一些键值数据库，比如 Redis、Memcache，就是使用散列表来构建索引的。这类索引，一般都构建在内存中。

* **红黑树**作为一种常用的平衡二叉查找树，数据插入、删除、查找的时间复杂度是 O(logn)，也非常适合用来构建内存索引。Ext 文件系统中，对磁盘块的索引，用的就是红黑树。

* **B+ 树**比起红黑树来说，更加适合构建存储在磁盘中的索引。B+ 树是一个多叉树，对相同个数的数据构建索引，B+ 树的高度要低于红黑树。当借助索引查询数据的时候，读取 B+ 树索引，需要的磁盘 IO 次数非常更少。所以，大部分关系型数据库的索引，比如 MySQL、Oracle，都是用 B+ 树来实现的。

* **跳表**也支持快速添加、删除、查找数据。通过灵活调整索引结点个数和数据个数之间的比例，可以很好地平衡索引对内存的消耗及其查询效率。Redis 中的有序集合，就是用跳表来构建的。

* **布隆过滤器**有一定的判错率。但是，内存占用非常少。我们可以针对数据，构建一个布隆过滤器，并且存储在内存中。当要查询数据时可以先通过布隆过滤器，判定是否存在。如果布隆过滤器判定数据不存在，那就没有必要读取磁盘中的索引了。对于数据不存在的情况，数据查询就更加快速了。

* 静态数据，有序数组可以被作为索引。把数据的关键词（查询用的）抽出来，组织成有序数组，利用二分查找来快速查找数据。

# 集成学习

* **同质集成**：集成算法中的学习器相同，比如集成模型当中都是决策树。
* **异质集成**：集成算法当孩子工的个体学习器都是有不同类型的学习期组成。
* **期望目标**：<u>弱学习器有较好的准确性</u>且<u>各个学习器之间有较大差异</u>（实际情况满足较难）
* 常见两类算法：
  * **个体学习器之间强依赖，必须串行化生成每个学习器**：boosting【adaboost，GBDT】
    * 对所有训练数据进行重复使用，每次应用前对样本概率分布进行调整，达到不同训练效果。
  * 个体学习器之间**不存在强依赖**，可以**并行**生成每个学习器：bagging【random forest】
    * 不同个体学习器之间多样性容易保证
    * 每次仅使用小部分数据，训练效果不保证。

## boosting

从弱学习器出发，反复训练学习得到一系列弱分类器，然后组合弱分类器，构成一个强分类器。

**工作机制**：从初始训练集开始，得到一个基学习器，根据基学习器的表现对训练样本分布进行调整，使得序列模型前一个模型中被分错的样本，在这一轮模型训练过程中能够得到更多的关注【通常通过增加样本权重来控制】，进而得到下一个分类器。反复执行直到达到设定的基学习器数量【该数量是需要调试的超参数，通过cross validation 来进行选择】

### Adaptive boost

AdaBoost迭代算法，相同训练集训练不同的弱分类器，最终合成一个强分类器。

* **数据集相同，但需要每次训练改变数据权重值分布**：根据每次训练集中每个样本是否分类正确，及上次分类正确率来确定**每个样本的权值**。修改过权值的新数据送给下层分类器进行训练，融合每次得到的分类器作为最终的分类器。

* 算法概述：

  * 对大小为N的训练集训练得到第一个弱分类器；

  * 分错的样本和其他新数据一起构成一个新的大小为N的训练集，对这个集合的学习得到第二个弱分类器；

  * 上述两步分错的样本加上其他的新样本构成另一个新的大小为N的训练集，对这个样本的学习得到第三个弱分类器；

  * 最终经过提升的强分类器。即某个数据被分为哪一类要由各分类器权值决定。

    **每个分类器准确度足够高及分类器数量足够多时，能够提高准确度。**

* 增加权重后能够将训练集中在分类较难的数据样本上。

* 加权投票机制能够替代平均投票机制，提高分类效果。

* python实现（不指定base_estimator 默认使用决策树）

  ```
  from sklearn.ensemble import AdaboostClassifier 
  ```

  

## bagging

在原始数据集上进行采样分类，获得多种不同的样本集后来训练基学习器。

* 自助采样方法：bootstrap【有放回采样，可能出现重复采样 & 未被采样的部分】（**给定包含m的样本，有放回采样后，最终获得的样本集大致包含2/3的数据样本。**）

# 决策树Decision Tree

采用树形结构层层推理实现分类。无需任何先验条件，适用于探索知识发现。构成：**根节点：包含样本全集；内部节点：特征属性；叶节点：决策结果。**

* 根节点到每个叶节点的每条路径对应一个从数据到决策的判定流程。
* 从根节点开始，测试待分类项的特征属性，并按照其值选择输出的内部节点。当选择到达某个叶节点时，就将该叶节点存放的类别作为决策结果。

**决策树模型的学习过程包括三个步骤：特征选择（信息增益来确定）、决策树生成和决策树剪枝**。

# 随机森林Random Forest

随机森林RF(Random Forest): **多棵决策树集成算法**。基本单元为决策树，多棵树集成为森林。每棵树都是一个分类器，N棵树就会有N个分类结果，随机森林将 **所有结果中投票次数最多的作为最终输出** 。

* 生成规则：

  * 样本输入每棵树的过程中，99%不相关的树会在2分类的过程中做出完全相反的决策相互抵消，仅少数优秀分类器会做出正确预测。
  * 训练集大小n，每棵树随机且有放回的从中抽取m个作为该树的训练集，m<n 保证每棵树的训练样本均不同。【随机抽取过程可能包含重复样本】
  * 特征维度为M，指定常数m (m<<M),随机从M中选m个子集，每次分裂的时候，选取m个特征中最优的。
  * 每棵树在迭代过程中尽可能生长，不存在剪枝过程。

* 特点如下：

  * 处理高维样本且不需降维；
  * 生成过程做到无偏估计；
  * 能够评估特征在分类问题的重要性；
  * 缺省问题也能获得好结果：某几位度缺数据。
  * **多棵树集成可以避免仅仅依赖于单个树造成的误判。**
  * 比单棵树有更强的分类能力

* python 库

  ```python
  from sklearn.ensemble import RandomForestClassifier
  model = RandomForestClassifier(n_estimators=self.nTree, criterion=self.criterion, max_depth=self.maxDepth)
  model.fit(xData, xLabel)
  ```

* 重要参数说明

  * **n_estimators:** 最大弱分类器(决策树)个数，太小欠拟合，太大计算量不足
  * oob_score: 是否采用袋外样本评价好坏，默认False，袋外评价反映模型拟合后的泛化能力
  * **maxDepth**: 决策树最大深度：默认为None，决策树**最大深度不能太深**，否则最终结果会较差。常用值在**10-100**
  * **max_feature:**最大特征数，默认auto（最多考虑√N个特征），‘log2’：最多考虑‘√2’个特征
  * max_leaf_nodes: 最大叶节点数，防止过拟合，特征不多，可选None,特征多可加以限

* 分类效果相关因素

  * 任意两棵树：相关性越大，错误率越高（越相关投票结果越一致，因此尽量保证树之间的相关度越低越好）

  * 两棵树分类能力：每棵树的分类能力越强，整个森林的错误率越低。

    **PS:减少特征选择个数m**，树的相关性和分类性能降低，反之增大m，两者也增大，因此需要选择适当的特征值个数m

* 袋外错误率 oob error

  * 用于判断选取特征的数目。随机森立主要采用内部评估，在生成过程就可以建立误差的无偏估计。因生成过程中，对训练集使用了不同的bootstrape sample（随机有放回的抽取），所以对每棵树而言，**大约1/3 的训练实例没有参与第k棵树的生成，它们成为第k棵树的oob样本**。
  * 对于上述oob样本，计算方式如下：
    * 对于每个样本，计算它作为oob样本的树对它的分类情况
    * 简单多数投票作为分类结果，
    * 最后用错误分类个数占比作为oob误分率。

# 时序模型

RNN & LSTM

## 问题记录

* **时序模型一般情况不使用dropout，**因为RNN存在累乘效应，使用dropout会破坏学习过程。需要使用的话只能在RNN or LSTM之外使用。

## Markov Model

* 一阶马尔科夫假设（First order markov assumptions）：**N 时刻的观测值仅依赖于N-1时刻的观测值**
  $$
  p(x_n|x_{n-1},x_{n-2},...,x_1,x_0) = p(x_n|x_{n-1})
  $$

* 转移概率：从状态Si到Sj的概率
  $$
  a_{i,j} =p(x_n=S_j|x_{n-1}=S_i)
  $$

* 时不变性：
  $$
  p(x_n=S_j|x_{n-1}=S_i)=p(x_{n+T}=S_j|x_{n-1+T}=S_i)
  $$


### 隐马尔科夫模型HMM

统计模型，用来描述一个含有隐含未知参数的马尔科夫过程，难点在于如何从可观察的参数中确定隐含参数。

* 问题模型：假设有一个人被锁房间里很多天，但想知道外面的天气是什么。他猜测天气的唯一途径是看每天来照顾他的人有没有带伞。
  * 观察状态（observed state）={带伞、不带伞}
  * 隐含状态（hidden state） = {晴、雨}
  * 由hidden state 得到的observed state 是可观察的，需要通过倒推来确认状态
  * 能够解决的问题：已知初始化模型a = {A,B,prob},观测序列： 1）计算某个序列出现的概率；2）已知观测序列，求最可能的hidden state

# 生成模型

遇到过的生成模型包括：GAN、AutoEncoder、VAE 等。

### GPT: generative pre-Training Model

[参考](https://paperswithcode.com/method/gpt)

* A Transformer-based architecture and training procedure for NLP.
* 1st stage procedure: using unlabeled data to learn the initial parameters of network model.
* 2nd stage producre: adapt these parameters to a corresponding supervised task.
* 无标签文本语料很丰富，但可以通过无标签文本训练出一个“通用语言模型”，再使用**特定任务**的有标签语料数据进行迁移学习，GPT模型在12个任务中的9个都实现了SOTA的效果，且个别任务效果提升明显。
* 预训练使用语言模型LanguageModel的训练方式，模型使用的是transformer变体，多层transformer-decoder，

# 变邻域搜索算法VNS

**总思路：在给定的邻域序列当中，不断更新搜索每一个邻域的最优解，直到序列当中的所有邻域都被搜索过一遍之后，剩下的就是最优**

* 利用不同的动作构成的邻域结构进行交替搜索.
* 一个邻域的局部最优解不一定是另一个邻域结构的局部最优解
* 全局最优解是所有可能邻域的局部最优解。
* **领域动作**：一个函数，对当前解进行一个操作，可以得到所有解的集合。

<img src="/images/img/VDN搜索示例.png">

# 并查集

* 适用范围：找不相交的数据合并及查询问题   lcd 547/684/685

* 树形数据结构，用于处理相交的合并及查询问题，树的根节点唯一标识了一个集合，只要找到某个元素的树根，就能确定它在哪个集合里。[参考](https://zhuanlan.zhihu.com/p/93647900/)

* 主要用于解决**元素分组**问题，管理一系列**不相交的集合**，同时支持：

  * 合并Union：将两个不相交的集合合并为1个集合
  * 查询Find：查询两个元素是否在同一个集合中。

* 问题示例：若某个家族人员过于庞大，给出某个亲戚关系图后，确定任意两人是否具有亲戚关系。（x是y亲戚，y是z亲戚，则x是z亲戚

* 解决思路：**用集合的一个元素来代表集合**，通过一定规律将元素相互合并之后，构成类似于树和图的搜索结构，判断两个数之间的关系只需要判断他们是否属于同一个根节点即可。

* 路径压缩：在构成并查集的过程中，可能会出现长链结构，为了简化查询，**可以将长链的每个节点父节点都设为根节点，降低查询复杂度**

  PS: 合并过程---**尽量将简单树向复杂树上合并**

* 具体步骤：

  * 每个元素初始化为个1个集合，其根节点为自身，建一个parents = [i for i in range (n)]
  * 根据提供的元素之间的关系表格，将直接相连的两个元素进行合并（合并条件自己定义），更新上述list。
  * find 函数主要用于寻找当前位置的根元素

```python
# 并查集class
class solution:
    def find_redundant_connection(self, edges):
        # 根据给定关系建立表
        def finds(index):
            # 查找根节点
            if parents[index] != index:
                parents[index] = finds(parents[index])
            return parents[index]

        # 合并
        def union(node1, node2):
            parents[finds(node2)] = finds(node1)
        
        n = len(edges)
        parents = [i for i in range(n)]
        
        for data in edges:
            if finds(data[0]-1)!=finds(data[1]-1):
                union(data[0]-1,data[1]-1)
        else:
            return data
```

# 一致性hash算法

解决：hash函数区别对待不同配置服务器、节点数据均匀存储、节点数据活跃度不同导致访问瓶颈不同的问题。

**一致性hash与主机节点的映射关系建立**

* step1：将关键字经通用hash函数映射为32为整型hash值，这些hash值会形成一个环，最大2^32相当于0。
* step2：设集群节点为N，将hash环由小到大分成N段，每个主机节点处理hash值落在该段的数据。
* step3：对于生产环境中的配置不同的异构主机节点，需要对配置更高的节点赋予更高的权重。
* step4:  在扩容、缩容时，虽然节点数发生了变化，但只需要小幅度调整环上各个节点的位置，就不会导致大量数据迁移。

PS: 如果区分好N个环后，数字区分并不均匀，也无法通过调整权重来进行平衡数据量，此时可以加入虚拟节点来进行数据平衡。

* 在真实节点与hash环之间引入虚拟节点，用以确保某一个节点失效后，数据能够平均迁移到剩下节点当中。

**优劣**-假设总条数为M，节点数为N

|                | 传统hash                | 一致性hash                                    |
| -------------- | ----------------------- | --------------------------------------------- |
| 映射时间复杂度 | 以N为基数，取模，O(1)   | 先转为32位int-O(1); 二分法有序节点映射O(logN) |
| 数据迁移规模   | 最坏：迁移所有数据-O(M) | 各节点均匀分布：O(M/N)                        |

PS: 优点-数据迁移规模从O(M) 降低到O(M/N), 时间复杂度从O(1) 常数级上升到对数级O（logN）【对数级时间复杂度在数据量较大的情况下仍然在可接受范围内。】

# 受限波兹曼机RBM

## RBM定义

* 由一层Hidden Unit 和 一层 Visible Unit 组层的神经网络结构。通常情况下，对每一个Visible Unit与所有的Hidden Unit相连。
* **每个Unit自身都有一个权重，并且在每对Hidden Unit 和 Visible Unit之间的连接上还有一个权重。**（所有权重均为需要通过训练获得的参数）
* RBM 可针对实数信息、离散信息进行建模分析。

## RBM在推荐系统的应用

### 以用户为电影打分为例

* 对每一个用户使用单独的RBM进行建模，每个RBM都有一样的Hidden Unit数量且**仅对当前这个用户曾经打过分的数据进行建模。**（即：每个RBM需要建模的数据是不一样的，有的有三个打分数据，有的有20个）
* 如果两个用户**对同一个电影打过分**，那么针对这个电影，**两个用户对应的RBM会共享一样的权重，这样就可以联系两个独立的RBM**。
  * Key take away：<u>**共享相同电影的权重。**</u>

**具体来说**

* **对于每个RBM，每一个显单元(k维数组)都是用户对于某个电影的评价。**
  * 每个k维数组中，只有一个元素是1，其他都是0，这能够帮助用户对可能的K种输出进行建模。
* 每个RBM支队已经评过分的电影进行建模，因此无法直接对未知电影进行预测。
* 需要预测时，先拿到此电影权重，然后通过测试将K为数组那个值为1时产生最大概率，以最大概率情况的K值作为预测结果。

# 其他

* 摩尔投票法：对拼消耗，剩下最后一个是结果。 lcd229

* 点击率预测：**对某个广告将要在某个情形下展现前，系统预估其可能的点击率**，如果大概率被点击，就展示广告，否则就不展示。 同时，通过广告来完成价格评定。

  * 点击到达率=该广告实际点击次数/广告展现量  （点击100次/出现1000次）

* 漏斗算法leaky Bucket：假设服务为一个漏斗，**进水量大于出水量到一定程度，漏斗就会积水，水太多就会溢出**。

  * 实质：队列上增加一个限流器，来均匀处理数据。

* 队列算法：假设一个队列包含待处理消息，且**请求速度波动，处理速度均衡**（FIFO:队列）。**每次请求到了先判断队列是否满了，满了就丢弃，没满就存入等待**。

  * 可以加入优先级/带权重

* 令牌桶算法：有1个中间人，**在桶内按照一定速率放入一些token**，处理请求时需要拿到token才能进行，否则不处理。

  * 通过桶内token放入速率来控制流量速率，防止爆满。令牌桶在流量小的时候可以积累token，当流量大的时候可以快速处理。

* 蓄水池采样：**从N个样本种随机选择k个。N极大无法全部放入内存 or N 未知】，时间复杂度O(N)**

  原理

  * 创建长度为k的蓄水池（array）存放结果，初始化蓄水池中元素为N个样本的前k个。
  * 每次迭代过程生成一个随机数 j∈[0,N]，若j∈[0,K]，则蓄水池中的第j个元素被更新。
  * 重复上述步骤直到最后，通过一次遍历O(N) 就能保证所有N个元素，都以k/N的概率被抽样到。

* 二叉树序列化：

  * 序列化 Serialization: 将数据结构或对象转换成可以取用的格式，以待后续在当前或者其他计算机环境中恢复原先状态的过程。【Java 数据当中也有类似的】
  * 反序列化 De-serialization：序列化后数据恢复为原数据的过程。
  * **二叉树序列化：3种遍历方式已知两种就能恢复原来的二叉树。** lcd331

* 拒绝采样：针对复杂问题的随机采样方法：（lcd470：用rand7 实现rand10）

  * 思路：**若生成的随机数满足要求，那就返回该随机数，否则一直生成直到满足。**
  * lcd470：rand7*rand7 生成10个等概率的不同数即可【+—\*/均可，此处考虑两个数相乘为例子】

|      | 1      | 2       | 3       | 4       | 5       | 6       | 7       |
| ---- | ------ | ------- | ------- | ------- | ------- | ------- | ------- |
| 1    | 1-1/49 | 2-2/49  | 3-2/49  | 4-3/49  | 5-2/49  | 6-4/49  | 7-2/49  |
| 2    | 2-2/49 | 4-3/49  | 6-1/49  | 8-2/49  | 10-2/49 | 12-1/49 | 14-2/49 |
| 3    | 3-2/49 | 6-1/49  | 9-1/49  | 12-1/49 | 15-2/49 | 18-1/49 | 21-2/49 |
| 4    | 4-3/49 | 8-2/49  | 12-1/49 | 16-1/49 | 20-2/49 | 24-2/49 | 28-2/49 |
| 5    | 5-2/49 | 10-2/49 | 15-2/49 | 20-2/49 | 25-1/49 | 30-2/49 | 35-2/49 |
| 6    | 6-1/49 | 12-1/49 | 18-1/49 | 24-2/49 | 30-2/49 | 36-1/49 | 42-2/49 |
| 7    | 7-2/49 | 14-2/49 | 21-2/49 | 28-2/49 | 35-2/49 | 42-2/49 | 49-1/49 |

**题目要求rand10，则从中选10个概率相等的数即可，也就是可以模拟rand更多**

* 拜占庭将军问题
  * 点对点基本通信：存在消息丢失的不可靠信道上试图通过消息传递的方式达到两点的一致性是不可能的。
  * 问题模型：拜占庭位于如今的土耳其的伊斯坦布尔，是东罗马帝国的首都。由于当时拜占庭罗马帝国国土辽阔，为了达到防御目的，每个军队都分隔很远，**将军与将军之间只能靠信差传消息**。在战争的时候，**拜占庭军队内所有将军和副官必须达成一致的共识，决定是否有赢的机会才去攻打敌人的阵营**。但是，在**军队内有可能存有叛徒和敌军的间谍，左右将军们的决定又扰乱整体军队的秩序。在进行共识时，结果并不代表大多数人的意见。**这时候，在**已知有成员谋反的情况**下（信道不可靠），其余忠诚的将军在不受叛徒的影响下如何达成一致的协议。
  * 问题延伸：在互联网大背景下，当需要与不熟悉的对方进行价值交换活动时，如何才能防止不会被其中的恶意破坏者欺骗、迷惑从而作出错误的决策；在缺少可信任的中央节点和可信任的通道的情况下，分布在网络中的各个节点应如何达成共识 。
  * 解决方法：增加信息确认轮数 （若将军数n，叛徒m，n>=3m+1，且进行m+1轮协商）or 减少干扰噪声比例 or 消息增加签名。

* 注意力机制 attention [mechanism/model](https://blog.csdn.net/qq_40027052/article/details/78421155)：命名借鉴了人类注意力机制。
  * 人类注意力机制：视觉通过快速扫描得到全局图像，获**得需要重点关注的目标区域（注意力焦点）。抑制其他无用信息，从而获取更多关注点的细节。**
  * 深度学习的注意力机制从本质上和人类的选择性视觉注意机制类似，核心目标也是**从众多信息当中选择对当前任务更加重要的信息。**
  * Encoder-decoder框架 ：注意力机制常见框架之一。常见应用示例：翻译通过编码和解码进行。
  * Attention 模型(机器翻译常见的soft attention)：
    * 正常encoder-decoder模型无法体现“注意力”，因为每个单词在句子中成分一致，但实际使用中，会给不同的词一个权重（tom 0.3，chase 0.2,jerry 0.5) ，一定程度上增强翻译效果。
    * 注意力机制将当前固定1中间值修改为权重变化占比。示例如下

<img src="/images/img/注意力机制翻译权重示例.png">

* 特征工程
  * 模型外部的注意力机制：将原始数据、信号转化为数值向量，在数据科学中，帮助模型有效选取适当的特征，进而完成任务。

* 良好的特征工程需要特征工程师对任务内容有了解，才能更好的进行特征选取。


------

