---
title: 'AI resource'
date: 2024-03-15
permalink: /posts/2024/03/AI-resource/
tags:
  - Real Work Practice
---

Mark Some useful AI model、community、dataset、resource here

# Hugging Face

[Official website](https://huggingface.co/): An open source data science and machine learning platform.

* login: jingtaow@buffalo.edu

  ```shell
  # create a repository from the CLI
  # if transformers or datasets is installed  
  $ pip install huggingface_hub 
  
  # Log in using a token from huggingface.co/settings/tokens
  $ huggingface-cli login
  # Create a model or dataset repo from the CLI if needed
  $ huggingface-cli repo create repo_name --type {model, dataset, space}
  
  # clone your model,dataset or space locally
  $ git lfs install 
  $ git clone https://huggingface.co/jingtaoWang/repo_name
  
  # add commit、push any file you want,including large files
  # save files via '.save_pretrained()' or move them there
  $ git add .
  $ git commit -m "commit from $user"
  $ git push 
  
  # In most cases, if your're using one of the compatible libraries,your repo will then be accessible from code. through its identifier: username/repo_name【anyone can load it with】
  tokenizer = AutoTokenizer.from_pretrained("username/repo_name")
  model = AutoModel.from_pretrained("username/repo_name")
  ```

  ## DGA-detector

  [model url](https://huggingface.co/harpomaxx/dga-detector): A DGA lexicographical(字典序) detector using 1DCNN

  * dataset：
    * normal ：alexa-top 1 millions+3161 additional normal domains
    * DGA：resource repository [Andrey Abakumov repository](https://github.com/andrewaeva/DGA)、 [John Bambenek repository](http://osint.bambenekconsulting.com/feeds/)

# 推荐系统

## 简单推荐模型

### Model1：基于流行度的推荐模型

* 最简单的流行度估计（popularity based estimation）：什么内容吸引用户，就给用户推荐什么内容。【如果能够在每个时间点上准确估计流行度，则只需按照流行度排序即可。】

* 内在假设：越有意思的东西关注度越高，越流行。【不需要过多其他信息和假设的情况下，流行度可以作为一个最简单测度。】

* 流行度估计的重要影响因素：

  * **时间**：每个应用都有一定规律，这种规律导致不同时刻的流量规律不一致。【eg：**人们更倾向于在早上或者傍晚打开新闻网站。因此任何文章投放到这两个时段都会有较高关注度，这并不表示这些文章好于其他文章，可能仅仅是由于时间的关系**】
  * **位置**：非地理位置，而是一个服务在屏幕的什么位置显示物品。【eg：类似超市货架，不同高度的物品放不同东西-较低的小孩视角(零食、玩具)；中等高度(好卖的)等】

* 流行度的衡量方式：
  $$
  流行度比值 = \frac{点击某个文章的人数M}{总用户数N}
  $$
  说明：不同分子的情况，流行度有不同的含义，后续讨论用点击率统称。

  * 点击率：点击某个文章的人数。
  * 购买率：购买某个物品的人数。

* 高级流行度估计：
  * 时间折扣：**主观经验主义的的**对于时间处理做一个定义。【9点-10点某个物品有40次点击，100次显示，那么10-11点，可以将9-10点的数据*0.5做一个经验主义判断】

### Model2：基于相似信息的推荐模型

* 相似信息推荐：**利用临近、相似的数据点来为用户做推荐**。
* 内在假设：**协同过滤-相似的用户可能会有相似的喜好、相似的物品可能会被相似的人所偏好。**【eg：用户A观看过动作电影A，用户B也看过动作电影A且还看过动作电影B，那么可以认为用户A也对动作电影B感兴趣。】
* **基于相似用户的过滤：**
  * 问题抽象：估计用户A针对一个完全没有接触过（未点击、购买、评分）等行为的物品B的偏好。
  * step1- 构建用户集合：
    * 这些用户已接触过物品B。
    * 这些用户在某方面与用户A类似。
  * step2 - 根据上述相似用户集合对物品B进行打分：
    * 首先，得到所有和A相似的用户对物品B的打分。
    * 方法1：用这些打分的平均值来预估 J 的评分。【较粗糙】
    * 方法2：对于与用户A相似度高的用户的打分赋予更高的权重，进一步修正最终的估计结果。
* 相似信息的构建：
  * 如何界定两个用户是相似的：
    * 计算两个用户对于同一个物品的"皮尔森相关度"(Pearson correlation)[偏好度是否相似]
    * 用户相关度信息有了之后，可以**设定阈值来筛选用户集合：满足一定偏好相关度的用户分数才被采用。**
* **基于相似物品的协同过滤**：上述基于用户的协同过滤也可以等价到物品上。【喜欢相同物品A的用户B和C，可以将C喜欢的其他物品D推荐给B.】

### Model3：基于内容信息的推荐模型

* 内容信息推荐系统：**用特征来表示用户、物品已经用户和物品的交互，从而将推荐问题转为监督学习。**
* 具体步骤：
  * step1：特征工程提取特征。
  * step2：构造Objective function用于评价特征向量最终的评分。
* 内容信息的各类常用特征：
  * 物品文本信息：通过<u>文本挖掘</u>的方式组成有效特征。
  * 物品类别信息(知识信息)：以新闻为例，不同类新闻可归纳为不同的属性。
  * 基于**知识图谱**进行隐含信息关联：eg-特朗普-美国总统-美国政治等。

## 基于隐变量(latent variable)的推荐模型

### 矩阵分解作为隐变量模型

* 推荐系统中最普遍的数据表达：用户和物品的交互，比如评分、点击等。对每一个用户，如果用一个向量来表达其对所有可能物品的评分，那么所有用户的向量堆积起来，就可以得到一个矩阵。这个矩阵的每一行代表一个用户，每一列代表一个物品，每一个交叉的元素代表某一个用户对于某一个商品的评分。
  * 矩阵特点：**数据稀少**。现实的系统中，一个用户不可能对所有的物品都进行评分。**实际上，一个用户仅仅对非常少的物品进行过评分，而对绝大多数物品并不会评分，甚至连评分的打算都没有。**因此，这个矩阵的绝大多数元素其实是 0（未知信息）。‘
  * 矩阵的利用：**根据有评分的用户物品交互，对还没有评分信息的物品进行预测。**根据推测补全矩阵中其他元素后，就可以根据预测的评分从大到小给用户进行推荐。

* 矩阵信息的补全：
  * 首先，假设每一个用户和每一个物品都对应一个隐向量（Latent Factor）。
  * 然后，假设矩阵的每一个元素是由所对应的用户和物品的隐向量**点积得到**。
    * 通过点积的方式进行**矩阵分解**，将特征向量计算量下降。【矩阵分解进行降维】

### 基于回归的矩阵分解

* 矩阵分解的劣势：
  * **矩阵分解的矩阵仅对用户和物品的喜好进行了“编码”，难以融合喜好之外的其他元素。**对于一个复杂的工业级推荐系统来说，有很多灵感或者直觉，都很难仅仅依赖用户和物品的喜好来捕捉到。有大量的信号，无法很好地被融合到这个矩阵分解的模式里。
  * **矩阵分解仅能通过已有训练集学习用户的隐向量和物品的隐向量，无法新增后续新的训练数据。**
    * 这种情况叫做：不能处理**“冷启动”（Cold Start）**问题，这个特点的好坏取决于具体应用，新闻场景随时在加入新数据的情况下不适合冷启动的矩阵分解情况。

* 上述两类矩阵分解劣势的解决方法：--- **基于回归的矩阵分解**
  * **首先，有一组显性用户特性和显性物品特性来表述每一个用户和物品**。这两组显式的特性解决刚才说的第一个问题，矩阵分解无法抓住更多的信号。
  * 基于回归的矩阵分解假定：用户的隐向量，其实是从用户的显式特性变换而来。同理，物品的隐向量，其实是从物品的显式特性变换而来的。而这两种变换，本质上就是两个回归模型（Regression Model）。就是说，**建立一个从显式特性到隐向量的回归模型，使得隐向量受到两方面的制约：从评分矩阵的分解得来的信息和从显式特性回归得来的信息**。这样就把这两部分信息嫁接到了一起。
    * 两部分嫁接后，”冷启动“效果会提升（加入了显性特征）。

### 分解机-Factorization Machine

**矩阵分解&基于回归的隐变量模型存在的问题**

* 矩阵分解主要解决了两个问题：
  * 从一个大矩阵降维到两个小矩阵。
  * 希望这两个小矩阵能够抓住用户和物品的相关度。
* 基于回归的矩阵分解：解决单纯的矩阵分解无法融入很多用户和物品的特性的问题。
  * 建立从显式特性到隐变量之间关系的流程，从而把更多的信号放进模型中。
  * 模型学习过程复杂，实际应用困难。

**分解机的基本原理**

* [分解机](Steffen Rendle. Factorization Machines with libFM. ACM Trans. Intell. Syst. Technol.) 是Steffen Rendle在德国康斯坦扎大学任教期间开发出来的推荐模型。
* 分解机的输入：所有的显式变量。**分解机对显式变量建模 & 显式变量的两两关系建模。**
  * 比如说有一个用户特性：用户的年龄；有一个物品特性：物品的种类。
  * 普通的回归模型/**分解机的第一步**：把用户的年龄和物品的种类直接当作特性输入到模型。
  * **分解机第二步：把这两个特性的数值进行乘积，当作一个新的特性，然后进一步处理这种两两配对的关系**。
    * PS: 原始特征进行两两配对是构建模型的一种重要的方法。
    * 两两配对的好处：对两种特性的交互信息进行建模。【eg：如果特别在意某个年龄段的用户在某种商品类别中的评分，那么，把这两个特性相乘获得两两配对的新特征，可以提高模型判断的权重。】
    * 两两配对的问题：
      * **特征空间会急速增长**：特征空间数量变成两个特征的乘积。
      * 如果单独特征中，有“类别特性”（Categorical Feature），那么在两两配对之后就会产生大量的 0，从而变成一个巨大的稀疏矩阵。
    * 两两配对问题的解决方法：**先降维，再建模**。这样就能将显式和隐式变量结合。
  * 


------

