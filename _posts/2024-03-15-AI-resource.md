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


------

