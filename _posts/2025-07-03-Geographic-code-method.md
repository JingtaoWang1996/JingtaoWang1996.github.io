---
title: 'Geographic Code Method'
date: 2025-07-03
permalink: /posts/2025/07/Geographic Code Method/
tags:
  - Real Work Practice
---



关于Uber‘s H3 cell编码模型、等其他模型的相关应用介绍

# Uber‘s Intro

* Using H3 to optimizing ride pricing and dispatch 
  * 同理可以将卫星看成车、UT看成乘客
  * 基于H3可以做出一定数据的决策

## A brief history of surge

* In the beginning, the idea is :**DO not run out of cars**

  * In city scale: 可以在用车需求旺盛的时候（除夕等），将价格翻很多倍来使一部分人不去打车，尽可能保证有车提供
  * In a neighborhood(a sports/concerns event ...) scale: 对于一些特定的地区，在app上直接显示，这个地区的价格翻倍情况
    * 在驾驶员的app上能够直接看到哪些地方的价格翻倍，有local surge，为了挣钱就可以让驾驶员尽可能的靠近这些地区，便于后续的用户分配，保证有车

  * ”Driver cancel my ride again and again“
    * 基于上面的情况，如果驾驶员上线后，在向热点地区（高价格）靠近的过程中，被分配了一个非热点地区的单子，很可能就会被cancel掉，因为驾驶员希望拿到高价格地区的单子
    * surge cliffs motivates this cancellations
    * 但是实际app上画出的需求热力图不一定是真实用车需求的热力图，用车的用户可能很集中
      * 即使将整个城市的区域划分减小，但是仍然可能存在这个问题
      * 而且城市构建复杂

* 问题：boundary effect、phantom demand、scalability challenges

  * 解决方式：hexagon-一次性适配各种大小的scale

# Why hexagon

## Grids

* There are only three regular polygonal tilings **【只有三种正多边形平铺】**
  * 正三角形、正四边形、正六边形
* how to choose 
  * neighbor traversal 
    * 在随意一个cell开始，从一个cell到达另一个cell
      * 正三角：有12个neighbor 【有边、有点、有边点结合】
      * 正四边形：有8个neighbor【有边、有点】
      * 正六边形：有6个neighbor【全是边】
    * Tips1：尽可能以最简单的方式遍历所有的neighbor
    * Tips2：即使只通过边进行遍历，正六边形的扩展性也最好
  * subdivision
    * Need to be able to index as small possible the resolution【对于热点的定位越准越好，能细分的越细越好】
    * Also need efficiency
    * 正四边形：perfect subdivision
    * hexagon：Alternating CW,CCW 19.1° rotation of 7 children 1/7th the area【通过旋转后，7个hexagon能够十分近似原来的形状】
      * **同时，不同大小的hexagon能够近似任意形状的地区**
  * distortion
    * 

## hexagon的优点

**Brain storming 选择的hexagon进行划分**

* Smooth  gradients：用车需求可以在地图上平滑渐变
* Clear center of demand：**show the driver clearly where the center of demands are.**
* Dynamic neighborhoods
  * 不需要对于每个城市进行neighborhood划分，可以一次性适配各种大小
  * 不需要对各种类型的城市花费时间进行细致的城市neighborhoods划分
  * “Let the city tell us，where the demands is，where we need to send the cars“





# Some ref

* [直观感受图](https://wolf-h3-viewer.glitch.me/)
* [Uber's Intro](https://www.uber.com/en-SG/blog/h3/)
* [H3 github source](https://github.com/uber/h3?uclick_id=ee5cdcad-cb1a-4c9a-b2a6-10373f95f0d4)
* [Tiling the earth with hexagon-具体的idea](https://www.youtube.com/watch?v=ay2uwtRO3QE)










------

