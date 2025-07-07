---
title: 'LEO-orbit-prediction'
date: 2025-04-10
permalink: /posts/2025/07/LEO-orbit-prediction/
tags:
  - Theoretical
---

卫星轨道预测相关文章

* 常用方法：Batch-Least-Squares

# Research on Enhanced Orbit Prediction Techniques Utilizing Multiple Sets of Two-Line Element

## Intro

* A combination of multiple TLEs and advanced modeling techniques such as **batch least squares differential correction (最小二乘差分校正)**  and high-precision numerical propagators（高精度数值传播器） can significantly improve  TLE accuracy and reliability.
* Using **multiple TLEs** for precise orbit determination can significantly enhance the performance of orbit prediction methods, particularly compared with SGP4(常用地球物理模型之一).
* By leveraging 10-days Starlink TLEs, the accuracy of 5-day predictions can be improved by approximately twofold.
  * 使用10天的tle，5天的预测准确度可以提高两倍【**只要有历史10天的数据，那么其中5天的数据和星历准确数据对比是否就可以提高两倍？**】

* 已经发生的撞击事件：
  * 20090210的Iridium 33 和deactivated Kosmos 2251 的撞击产生了2000+太空碎片，这也是第一次公开报道的撞击事件。
  * 202103，YunHai 1-02 was struck by a space object，resulting in the loss of some functionality.
* 202303,围绕地球的发生物已经超过4.7w，7k是functionally payloads and rest 4w categorized as debris/ unclassified objects.
  * 88% of these objects occupy low-earth orbit & have diameters greater than 10cm
* Achieving accurate orbital information remains a challenge.
  * 1970s, US government has provided GP or general perturbations orbital data [Hoots, F.R.; Roehrich, R.L. Space Track Report No. 3—Models for Propagation of NORAD Element Sets](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://celestrak.org/NORAD/documentation/spacetrk.pdf)
    * These data are produced by fitting observations from US SSN using the SGP4 orbit propagator to produce **Brouwer mean element.**
  * **TLE-OD/OP**:2011，A method for determining and predicting orbits utilizing mutilple TLEs was proposed.
    * employed batch least squares differential correction and high precision numerical propagators to fit orbits using pseudo observations from several TLEs.
* Further research is necessary to effectively improve the orbit accuracy of **ascending and descending Starlink satellites using TLE-OD/OP methods**



## TLE-OD/OP methods-比SGP4有更好的精确度

* 主要方法方法：Least squares theory（最小二乘理论） 、numerical integrator （数字积分器）
* 基于上面两种方法确定一一条最合适于伪观测点（pseudo-observed data）的由multi-TLE生成的轨道
* The advanced computational technology and numerical integration algos enable consideration of complex mechanical models.[先进的计算技术和数值积分算法，能够考虑复杂的力学模型]
  * **Consequently，TLE-OD/OP provides higher orbital accuracy than SGP4(Java中orekit库使用的模型)**

### 方法概述

* TLE-OD/OP 包括计算 **three-dimensional position and velocity(速度)** vector of an object in space **using a set of observations,including positions from TLE **.
* 







## How to decide if a STARLINK satellite is ascending or descending



# Orbit Element Types



## Two-line element

* 表示卫星轨道的简化模型，常用于LEO卫星轨道分析，**多由NORAD（North American Aerospace Defense Command，北美防空司令部）生成**，用于实际的卫星跟踪和预测。
* TLE的数据更新频繁，多用于卫星的短期轨道预测

* TLE-OD(orbit determination)轨道确定:
  * 根据从不同传感器（地面站、卫星观测等）收集到的数据计算当前轨道状态。【轨道确定的目标是精确的确定卫星轨道参数】
  * 主要目的：通过多次观测和分析，提供精确的轨道状态，用于修正初始的tle数据
* TLE-OP(orbit prediction)轨道预测:
  * 根据现有TLE数据，预测未来一段时间内卫星的轨道变化【基于当前的轨道数据推算卫星未来某一时刻的位置】
  * op准确性取决于TLE的经度及所使用的预测模型
* **NORAD提供的TLE数据通常用于TLE-OP，TLE-OD的数据不会公开提供，只有特定机构或政府才会进行详细的轨道分析和修正。**

## Brouwer mean element

* 描述一个天体在受到其他天体引力干扰下的长期轨道行为的平均元素。通过对轨道各个元素（半长轴、偏心率、倾角等）进行时间平均，消除由于天体引力扰动引起的短期波动

* 是基于长期平均的轨道描述，**对短期轨道位置并不特别精确**，但能够有效描述天体再多体盈利作用下的长期轨道变化。
* 适用于 **高精度长期轨道研究** & 特别是涉及多个天体引力相互作用的情况
* Brouwer mean element最终会被转为TLE数据进行传输和存储















# Real-Time LEO Satellite Orbits Based on Batch Least-Squares Orbit Determination with Short-Term Orbit Prediction

* BLS: batch least squares
* POD: Precise Orbit Determination

## General take aways

* 与GNSS(全球导航卫星)相比，使用leo进行定位的改善优势点。
* high-sampling real-time satellite clock 在获得卫星位置实时预测中的重要作用
* 相比GNSS,leo高度更低，受到更多重力、大气的影响，导致轨道计算更复杂

* **Three steps to produce real-time LEO satellite orbits:**
  * Determine high-accuracy near-real-time LEO satellite orbits with BLS POD in the reduced-dynamic mode 
  *  Perform short-term orbit prediction,with the prediction time decided by a range of factors
  * Fit appropriate ephemeris parameters using the predicted orbits within certain time windows. 

* Based on near-real-time BLS POD and short-term orbit prediction，the accuracy of the real-time LEO satellite orbit was assessed for satellites at different altitudes.








------

