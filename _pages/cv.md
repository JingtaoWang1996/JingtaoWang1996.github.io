---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* 01/2020-09/2018  M.S. The state University of NewYork, University at Buffalo
* 09/2014-06/2018  B.S. Chongqing University of Posts and Telecommunications

Work experience
======
* 06/2020-now: Research & Development Engineer
  * CETC Cyber Security Research Instituion

Project experiences （Selected）
======
* **06/2025-now: Starlink network info analysis**
   * Research background information related to starlink and collect Key Infrastructure of Starlink (Pop,Gateway,satellite tle,ephemeris data).
   * Minimize possible UT connected satellites to 30-55 by setting Angle of Elevation(AOE) to 25°[with reliable proof]
   * Currently working on the link line from UT to backbone network.
* **08/2024-03/2025: Different DNS server discovery and server service area estimation**
   * DNS forwarder,indirect server,open recursive server discovery using controlled authority server & designed DNS requests.
   * DNS recursive server serve area estimation with localized domain and non-recursive cache probing. [Considering multi-cache case, improving the accuracy]
   * Authority server affect area estimation by active subdomain ip location. [old method for new question!!!]
* **Backend development based on Springboot by project**
   * 10/2022-03/2023: Learn springboot and get started with basic development work by BC project.
   * 11/2023-03/2024: Mainly responsible for backend development and detailed communication and modification among all parties by CYD project.
* **06/2022-09/2022: Malicious Domain Detection: DGA data & Collected open source threat info based**
   * Pre-collected 8 type of malicious domain & ip with total 223w+ data nums.
   * Pre-processed DGA model training data: normal domains(10% alexa top 1million---10w) & 8 type of different dga domains(1w each).
     * 5 selected domain features：length、entropy、n-gram in normal domains、n-gram in dga domains、diff in previous two n-gram.
     * Benchmark: with random selected 36000 test data, Logistic regression can obtain 88.6% accuracy.
     * Ensemble model Based: Using voting classifier with Logistic Regression、RF、Naive Bayes can imporve the accuracy up to 93% with same test data.
   * Modularize the above datas & models and successfully deploy them to multiple projects.
* **02/2022-04/2022: Anomaly Detection: BGP data based**
   * Collect real attack events (Nimda/Slammer/CodeRed) time sequential update message data from RIPE.
   * Data preprocess and select 7 features (Based on attack relevance) as the model input. 
   * By testing, LSTM can gain 93.7% accuracy with both 3k of normal and anomaly sequential data.
* **10/2020-now: DNS domain verify system**
   * Develope a 100k/minute/server-level domain query modual by asynchronous multiprocess method.
   * Assigned maintenance related works.
   * Gain Develop/Performance optimization/Batch deployment/maintenance experience on Linux Server.
* **02/2019-01/2020: Nonparametric QCD for High-dimensional Sequential Data  （M.S thesis）**
   * Propose Generative Model (GAN & VAE) based nonparametric QCD algorithms to deal with high-dimensional sequential data QCD problem. 
   * Best QCD peformance on 10D Gaussian/KDD/SWAT datasets compared with some popular QCD alogrithms. 
* **03/2018-05/2018: BPNN based Transformer Fault Detection （B.S thesis）**
   * Establish BPNN a transformer fault detection model with IEC three ratio processed transformer gas data.
   * Optimize BPNN model with GA & PSO algorithms and gain the optimal detection accuracy: 95%± 2%.
  
  
<!-- Skills
======
* Skill 1
* Skill 2
  * Sub-skill 2.1
  * Sub-skill 2.2
  * Sub-skill 2.3
* Skill 3

Publications
======
  <ul>{% for post in site.publications %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Talks
======
  <ul>{% for post in site.talks %}
    {% include archive-single-talk-cv.html %}
  {% endfor %}</ul>
  
Teaching
======
  <ul>{% for post in site.teaching %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Service and leadership
======
* Currently signed in to 43 different slack teams
 -->
