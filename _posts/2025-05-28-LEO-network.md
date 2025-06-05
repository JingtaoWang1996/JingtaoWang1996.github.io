---
title: 'LEO network'
date: 2025-05-28
permalink: /posts/2025/05/LEO-network/
tags:
  - Real Work Practice
---

LEO (low-earth-orbit) network related papers 



# Measuring the Satellite Links of a LEO Network

## Back Ground & Key Idea

* Most famous LEO satellites: Starlink、Oneweb、Kuiper(亚马逊公司)、Telesat(加拿大卫星通信公司)

* **Key point: This paper focus on the satellite access network （SAN）of starlink around the world.**
  * particularly, **measure the access performance** in terms of **one-way delay** and round-trip time from **user terminal to ground station & Pop** [终端到地面站、pop点之间的连接情况及关系]
    * Both **inside-out (user terminal 2 Internet)** and outside-in(Internet 2 user terminal), and even on inactive dishes. [extend UT coverage from ref2]

* Contributions:  It reveals the unique characteristics of STARLINK SAN(satellite access network) in terms of:

  * **satellite-GS scheduling: 卫星地面站调度**
  * **media access control: 媒体访问控制**
  * **user contention：用户争用**

  并阐明了网络协议和应用面临的挑战和机遇。论文将通过公开数据集发布和会议现场演示进行补充，供研究和行业社区使用。

* The paper will be complemented by **public dataset release** and conference on-site demo.

**The inner working of these LEO networks is largely hidden and has attracted a lot of attention from the search community**

## Starlink in a Snapshot-用户连接流程

* Step1-安装User Terminal (UT) :Starlink users install their **UT with an unobstructed view of the sky.(天空没有阻挡)**
* Step2-安装完成开机之后：After power on，the user dish will determine its own location by GPS and wait fro the beacon signal(信标信号) from Starlink Satellite. 
* Step3-用户与卫星连接完成验证之后:After user authentication and authorization, the dish will receive the satellite schedule and tilt(倾斜) toward a favorable view of the sky and use its electronically steered phased array antenna（受控相控阵天线）to track the communicating satellite according to the schedule.
* Step4-通信卫星与UT的连接过程:Communicating satellite will tunnel the user traffic, potentially through other satellite via inter-satellite laser links(ISLs), to a landing GS, which will be further tunneled back to **user's home pop(GS->pop)**, where a public IPV4 address will be assigned.
  * For users opt in public IP address, the binding process is at their router.
  * **默认寻址的方式步骤见文中图1及下一个子目录**
*  Step5-用户流量到达GS网关后：Once the user traffic arrive at the GS gateway, it will subject to various authentication,authorization and accounting function(身份验证、授权、计费功能)
  * 基于用户订阅、历史记录的优先级进行排序。
  * Starlink pop structure is similar to ISP，interconnect with other ISP、ICP（Internet content provider） at IXP(internet exchange points)

## A schematic diagram of starlink SAN with the default IP addressing scheme

* 用户设备路由器：192.168.1.1 同时充当用户到SAN的网关。用SAN侧来看，用户路由器在100.64/10中还有一个唯一的
  100.a.b.c.的地址，该地址由其Dish ID分配。
* 用户设备可以通过192.168.1.100.1/dishy.starlink.com 或 34.120.255.244/my starlink.com【google地址】访问dish，dish同时充当卫星的调制解调器。
* 卫星与GS的隧道传输的流量是透明的，直到流量到达GS 网关（172.16.y.z）并进入pop点为止。pop点处，运营商级网络地址转换器会分配一个pop公共地址（xxx.pop.starlinkisp.net)
* starlink发布的用户地理位置分布http://geoip.starlinkisp.net 比POP 本身更细致?

## Paper Focus 

* Unique SAN segment of Starlink，just **between user router and GS gateway** & **closely collocated cloud VM** 【仅在用户router和GS网关之间 & 云虚拟机之前观测，避免受到流量影响】
  * with or without ISLs，so the observation is not affected by the traffic dynamics within and between POPs or remote servers.

* By carefully measuring the **one-way delay（OWD）and round-trip time（RTT） between user and GWs** and leveraging **user dish's obstruction map construction process.**
  * **Identify and infer the communicating satellite and landing GS**，which are transparent to user traffic. 【基于测量，识别用户的通信卫星及地面站之间的关系】

## Measurement Methodologies

### Inside-out Measurement(UT -> GS & PoP)

* **Device**【device 可以远程，但是目前看其相关的pop都是已知的】
  * have access to a mini PC or VM behind the dish【3 dishes acquired】
    * Victoria,BC,Canada; 【Paper author owned】
    * Louisville, CO,USA;  **【associated with PoP in Denver，Google map 上看着挺远的】**
    * Ottawa,ON, Canada； **【associated with Pop in Seattle，Google map上也看得到】**
  * Through collaboration，more PC or VM is obtained,associated with the following Pops:
    * Seattle
    * Chicago
    * Dallas
    * Frankfurt,Germany
    * Lagos, Nigeria
  * For remote mini PCs or VMs, we separate access traffic and measurement traffic purposely wherever possible. 【远程设备，尽可能有意识的分离访问流量和测量流量】
  * Also get help from starlink user associated with other PoPs(eg: Sao Paulo) to **run measurement scripts at given time.**
* **Active dishes：dishes with an active subscription, we can reach any destination on the Internet.**
  * Starlink network is IPV4 and IPV6 dual stacked in terms of its PoP and backbone router ，and its dishes and provided user routers also become IPV6 capable through firmware upgrades【POP和骨干网路由器采用ipv4、ipv6双栈技术,同时通过固件升级，逐渐支持ipv6，但starlink提供的用户路由器可配置项依然很少】
    * So we also bypass Starlink provided user router wherever possible and use Open-WRT powered router with the latest firmware and configurable features.【**测量时绕过starlink提供的用户路由器，使用具有最新固件和可配置功能的OpenWRT路由器**】
  * From the user device or customer router at 192.168.1.1, we can reach its GS gateway at 100.64.0.1 (or its equivalent ipv6) in one IP hop
  * **RTT measurement tools**，such as ping and its variants can be used to determine the round-trip time between user router and its  GS gateway, r**eflecting the satellite-GS selection, MAC and user contention.**
    * **GS may process and generate ICMP messages slower than regular data traffic.** 
    * **RTT measurement still provides an envelop metric for performance analysis **
  * Well-provisioned Internet destination，such as Cloudflare(1.1.1.1)、Google(8.8.8.8) can be reached  with tools such as traceroute etc., to reveal the Pop structure and the PoP interconnection to the internet.
  * Starlink backbone address can be used to reveal the topology of starlink backbone around the world.
  * Starlink uses **MPLS(multi-protocol label switch) to route traffic to its users in its backbone**
  * Due to mis-configuration, Starlink used to **filter out return ICMP message for public IP users**, <u>even though their traffic traversed the same gateway and routers as private IP users, as verfied by outside-in measurement.</u>  【此bug已经在2023年作者提供后被修改】
  * OWD( one-way-delay) and RTT correlation, the symmetric satellite-GS selection for up and down link can be infered.
  *  **Starlink Currently uses the same satellites and GS for a bidirectional flow**
* Inactive dishes:  inactive dishes still can reach certain Starlink address for firmware updates,even some Internet address for users to access their Starlink account and resume their service through a captive portal.  【已经到期的starlink dishes还是可以联网进行激活】
  * Some meaningful research can still conduct：at link、network、transport & application layers.
  * **Inactive dishes have a lower priority than active ones with the same GS and can be forced to change to different ip**



### Outside-in Measurement (VM close -> the Starlink POP of user dish)

**Controlled Dishes**

* Use the dishes under our control to calibrate(校准) outside-in measurement. 【feasible for public ip users（公共IP地址绑定在其用户路由器上）】

  * Measurement endpoint is running on the customized，not Starlink provided 【**Starlink provided user router does not allow incoming connection establishment request to be traversed through the router, unless by pass ** 】 ---- 【**一定要用自己配置的路由器而非Starlink provided 的原因**】

  * For ipv6，Starlink allocates a /56 public block to be delegated through the user router. 

**Uncontrolled dishes**

* A more challenging task is to reach the uncontrolled dishes 
* Starlink does not allocate IP address blocks separately for public or private IP users
  * public IP users get their public IP at their router
  * private IP users get their temporary, public IP at CGNAT, both by DHCP.
* **Services such as Censys are available to list the ip that are externally reachable of all the public IPs in the starlink ip blocks.**
  * Based on this information, **correlating the measurement of controlled and uncontrolled dishes with the same Pop/GS---> infer more user-perceived performance** 

## Measurement Result and Analysis 

### UT-Sat-GS Performance 

**UT-Sat-GS：User Terminal ->Satellite->Ground Station**

* UT-Sat-GS performance is of most concern for most Starlink users, as reflected on Reddit、Facebook、X。

  * **By comparing such performance with different satellite density at different latitudes、user population、weather condition，one can also figure out the dominating factors**

    * larger dish may achieve a high throughput（吞吐量） but latency is determined by service tiers(延迟取决于服务层级).

  * results：User perceived performance (RTT) by ping in about 15ms intervals to its GW is actually heavily influenced by their local setup.

    **基于Fig2和3的数据，可以在Fig4的CDF中明显看出** ：ping 时间小于横轴的概率，越往左且越快到达1表示ping的时间越少 

    * 除了West Indian Ocean to Lagos 的ping时长大概率超过100ms，其他的用户到Pop点的ping时长大概率在100ms以内【符合starlink官网公布的网络性能数据】

    

  ​       

* Starlink router Gen-2 (later 2023 Gen-3 Starlink-router has the Ethernet ports returned) removed the built in ports，which makes the wifi signal strength limitied 【**This paper’s measurement use the Ethernet connection to dishes not wifi 】**

*  **【dishes带有遮挡的情况大概率会影响实验，因此选择的dishes都是放置在房顶无遮挡的地方】**：More critically, many users do not have a clear view of the sky, and even slight obstructions at the place where Starlink often picks satellites to communicate with can considerably affect the performance (eg: the one with in NYC)

* **【在同一个服务区域的用户越多，对user performance的影响也越大】**：User performance is also dominated by the competing users in the same service cell （eg: Pops such as Perth with few active users have the lowest UT-to-GW(GS gatway) RTT）
  * Starlink also limits new customers in certain cells，until most recently with more satellites launched and so capacity，or puts them at lower priority to maintain a reasonable performance for high-priority users.
  * Measurement to capture capacity changes over time, [some data](https://zenodo.org/records/10020034)
    * This dataset conclude the data from **2023-09-13 to 2023-09-17**
    * Work is continued by: [LENS](https://github.com/clarkzjw/LENS)
* 【会对user performance产生影响的因素】: location、satellite & user density、weather condition(obstruction)

**Starlink re-configures satellite-GS selection every 15s**

#### Satellite-GS selection

* Comparing UT-Sat-GS performance around the world, **A distinct feature emerges despite the location、satellite & user density、weather condition **
  * The minimum RTT jumps in a step-wise manner in certain intervals。Upon close inspection and investigation，i**t corresponds to the satellite-GS reconfiguration interval every 15s**, as mentioned in [Starlink FCC filings-ref5] and a patent granted to Starlink [ref6]【最小RTT会在特定时间间隔内逐步跃变，最终发现是在satellite 和 GS的调整间隔15s，这个15s在starlink FCC filing 和 patent 中都有提到】
    * Such min-RTT changes，often in 10,20 or even 50 ms，are way above the change of propagation delay of visible satellites(远高于卫星传播的延迟变化)，but indeed caused by the changing GS associated with the satellites and the need to tunnel back to the home POP.
  * **Globally synchronized at 57,12,27,42 seconds off each minutes (discovered by other researchers too )**
    * 间隔是15s

### Inter-Sat Link(ISL) Performance

* ISL provide Internet access to users who are faraway from GSs.【In the middle of an ocean】
* This paper measured the SAN performance of a starlink user in the middle of the Indian Ocean，5000+ KM away from the nearest GS.
  * a Rwanda Ip associated with the Lagos PoP.
  * **Compare with the ping time of land case, the ISL case has larger delay(CDF达到1需要的延迟更大).**
    * The ISL performance has been greatly improved from May2Aug，likely due to more satellites becoming available.
    * **Currently, Starlink ISL always routers toward user's  home PoP first,regardless of its destination**
      * eg: the **packet from the Lagos user to a Perth user** arrives at Lagos first, and then London->NYC->Denver->LA->Sydney->Perth 【为什么要绕一圈？？？】
      * The ipv4 packets have to be tunneled back to Lagos to be NAT’ed
      * **With public IPV6 address，packet can go towards the destination directly.**

### GS-Sat-GS performance

CG---(Community Gateway )

* **September 2023, Starlink also opened the first community gateway 【! 1st community gateway in Dutch Harbor, Alaska 】**
* CG- Community Gateway
  * a mini GS with a local distribution network.
  * Unlink individual user dishes for each household, the CG aggregates and distributes user traffic through the mini GS. 【与单个用户使用的天线不同，CG通过mini GS聚合和分配流量】

# Measuring a low-earth-orbit Satellite Network 

**上一篇的previous work **



# Making Sense of Constellations

 --- subtitle：Methodologies for Understanding Starlink‘s scheduling algorithms

* Use high-frequency and high-fidelity(高保真) measurements to uncover evidence of hierarchical traffic controllers in Starlink 
  * **A global controller which allocates satellites to UT**
  * **An on-satellite controller that schedules transmission for user flows**
* We then devise a novel approach for identifying how satellites are allocated to UT.  **【探测如何将卫星分配给UT的方法】**
  * Using data gathered with this approach，we measure the characteristics of the global controller and identify the factors that influence the allocation of satellites to UT.
  * Finally use this data to build a model which approximates Starlink‘s global scheduler.
    * **Model is able to predict the characteristics of the satellite allocated to a UT at a specific location  and time** with reasonably high accuracy and at a rate significantly higher than the baseline.
* Knowledge of algorithms responsible for **determining which satellites route traffic from specific UT location**
*  This paper: Uncover the scheduling algos used by SAN by Analyzing data from high-frequency measurements from **4 Starlink terminal（Deployed both in US and EU）** to servers co-located at their corresponding Pop

## Back Ground

### Starlink routes traffic from UT2GS in two step

* Step1: **A global network cntroller** allocates a satellite to each user terminal based on a variety of factors： Load（载荷）、Geospatial conditions（地理空间条件）、Satellite charge（卫星电荷） etc.,
  * **These allocations are made every 15s，globally**
* Step2：A local on-satellite controller schedules flows from the UT assigned to it.
  * The hierarchical traffic engineering mechanisms，commonly deployed in terrestrial WAN. 

### Contributions

* 1st to uncover hierarchical(分层的) controllers and the characteristics of traffic engineering in starlink。
  * ms级粒度能够确保找到流量中的特征（abrupt latency changes）
  * By co-locating our destination server at the Starlink PoP，minimize the influence of terrestrial latency on our measurement. 【将目标服务器与starlink的pop **共置-co-locating**】
  * Novel **methodology for identifying the satellite currently serving a given terminal** allows us to obtain ground-truth regarding the traffic engineering decisions made by Starlink.

* **Uncover the characteristics and performance of Starlink’s global scheduler【The algorithms responsible for allocating satellites to specific UT】**

### Starlink Key component and connection

* **<u>step1: UT connect to satellite >25° （only one satellite at a time ）</u>**
* **<u>step2: satellite forward traffic from UT 2 Ground Station</u>**
* **<u>step3: Ground Station received traffic and send it through【wired】 links to Starlink‘s PoP</u>**
* **<u>step4: Pop is a terrestrial server with wired connectivity to GS, and connect to the Internet backbone</u>**
* **<u>step5: From pop, the traffic is routed to destination on the Internet.</u>** 

#### UT 

* UT can connect to any satellite at angle of elevation higher tha**n <u>25°s</u>.** While tens of satellites satisfy the angle of elevation constraints. a terminal can connect to only one satellites at a time.
* Terminals forward user traffic to the satellite assigned to them.
  * **<u>Internals of the algorithms that maps UT to satellites are currently known only to the operators of the starlink network.</u>**
    * **In this paper, Empirically demonstrate characteristics of this algo and build its approximation.**

#### Satellites

* A starlink satellites connects to multiple UT at a time. They **allocate radio frames** to UT mapped to them to exchange data. 
  * This paper find the evidence that this allocation is determined by **a local on-satellite controller.**
    * This on-satellite controller's description:  **Medium access control scheduler**
    * This controller considers factors such as: User priority、current load、also the per-terminal flow **when forwarding traffic from UT to Ground Station**

#### Ground stations and Pops

* Ground Station received traffic from satellites and then it through wired links to Starlink Pop.
* Ground Station can communicates with satellites at an angle > 25 °
* Pop is a terrestrial server with wired connectivity to GS
* Pop are connected to the Internet backbone
* From POP, traffic is routed to destination on the Internet. 

## Evidence of Traffic Engineering

### Experiment Setup

* Perform measurement using 4 starlink UT: Western Europe、Northeast US、MiddleWest US、NorthWest US.

* Router configuration ：Operated in bridge mode and **connected them to** a dedicated Raspberry Pi.

  * These pi were the source of the measurement.
  * This approach prevents the complexities which arise from using wireless router.
  * The destination of the measurements **were servers co-located at the Starlink PoPs assigned to the regions of our UT.**

  * 在UT侧的router配置成桥接模式，同时将router连接到一个树莓派；探测的终点在POP点分配给这这个UT的server上。

* Measurements:

  * 测量目标：round-trip times(RTT) and packets loss rate **【从router连接的树莓派到pop点的server】**
  * 探测包发送：【下面这两个数据的选择是为了保证能够获得可靠和未定的SAN数据】
    * iRTT：1 packet / 20ms
    * iPerf3: 以上行连接50%的带宽发送探测数据包
    * 更高的频率和带宽带来的数据稳定度变化极大。

## Observation1-starlink relies on a global controller for satellite2UT scheduling

* Figure2：RTT by Time 可以看出每一格(15s)：**图2的间隔正好是12s、27s、42s、57s** 能够看出较大的切换

  <img src="/images/img/leo/RTT探测结果证明.png">

* 能够确认的确是出现了global change的原因：

  * 测试的两个端点（UT router的树莓派和Pop的server）消除了地面网络的原因-有线连接
  * These effects were observed,simultaneously from all 4 vantage point (UT)
  * These effects were noticed even when UT were running well under capacity.

* [FCC filing from space X](https://pdfhost.io/v/BnYWSR~wq_Starlink_Services_LLC_
  Application_for_ETC_Designation) describes a global scheduler for periodically allocating terminals to satellites 

  * **Page9: Each satellites currently has 2 Ka band parabolic antennas 【抛物面天线】that form connections back 2 the internet backbone.** 
  * Page9:These **antennas connect to ground station sites** deployed across the country that directly **connect via fiber to SpaceX's PoP** 【地面站和pop点通过光纤直连】

### 天线的作用

* Ka：卫星上两个Ka 频段的抛物面天线用于连接地面站，地面站通过光纤连接到pop点，再到主干网。 [ref](FCC filing form of space X )
* Ku:  SpaceX also provides customers with their **own phased-array terminal** to be deployed at their service location to **connect directly to the satellite’s Ku- band RF beam** assigned to the user's service area.

### Starlink Handover Info from FCC filing 

* **Page7** of [FCC filing from space X](https://pdfhost.io/v/BnYWSR~wq_Starlink_Services_LLC_
  Application_for_ETC_Designation) ：Beacuse the Starlink satellites are constantly moving, the network plans these connections on 15s intervals, continuously re-generating and publish a schedule of connections to the satellites fleet and handing off connections between satellites. 
* To accomplish these frequent hand-off, Starlink uses **advanced phased-array technology** for both the satellites and the customer Starlink Kit, which allows **for nearly instantaneous hand-offs** between different satellites **with no mechanical transitions.** 
  * Phased-array technologies encourage efficient spectrum sharing(频谱共享) by allowing both the satellite and user antennas to adjust the direction where the steer their RF beams purely by adjusting the signal of individual antenna elements that make up the combined phased-array.
* Both the UT and the satellite phased-array are made up of hundreds of antenna elements, controlled by proprietary digital beamforming chips that SpaceX has designed for dynamic hand-offs**[space X 专为动态切换涉及的专有数字波束成形芯片控制].** The ability to **control hand-offs in software with millisecond** precision allows SpaceX to turn the constant motion of the constellation into a key advantage for the Starlink network. These micro-adjustments enhance Starlink’s reliability and enables more efficient management of capacity in real time.
  * 软件控制切换

## Observation2- Starlink use an on-satellite controller for scheduling terminal flows

**The second peculiar characteristic of the latency measurements from our user terminals
is that within the fifteen-second time interval, latency measurements the user terminal frequently form parallel bands that are a few milliseconds apart.【在十五秒的时间间隔内，用户终端的延迟测量经常形成相隔几毫秒的平行带。】**

* These bands reflect evidence that radio frames（无线电帧） are allocated to user terminals by an on-satellite controller in a somewhat round-robin fashion (某种循环方式分配个UT).

## Obtaining Satellite Allocations

**SAN uses a global scheduler to assign satellites to user terminals every 15s **

* The starlink mobile app **no longer identifies the satellites that a UT is connected to.**

* **Leverages Starlink's obstruction maps to identify the satellite allocated  to a specific UT** 
  * 将 Starlink 卫星的公开位置与每个终端的障碍物地图中记录的连接卫星的观测结果关联起来。【输入：障碍图-Obstruction maps、UT到卫星的连接情况、卫星轨道】

**输入数据**

* Obstruction maps-[可能的数据来源1](https://github.com/clarkzjw/LENS)：
  * 123px * 123px 2D images
  * mark the trajectory of satellites recently served the user terminal 【最近为用户终端提供服务的卫星轨迹】
  * These images are used to create a 3D map made available to users via Starlink mobile APP.
    * 3D map is meant to help users identify the quality of the location of their UT.  突出显示UT到any satellites meant to serve the terminal
    * Obstruction map使用grpc工具获取

* Satellite Position：TLE format
  * CelesTrak：These files only indicate satellite position every 6 hours， use SGP4 satellite propagation algorithm to calculate satellite positions，relative to a UT location for a specific point in time. 【以UT为观测点，计算所有的卫星位置】

* GRPC 2D obstruction map获取更多参数
  * Identifying satellite parameters from obstruction map is crucial for identifying the connected satellites.
    * 将2D的obstruction map 和 3D的 starlink app map对其后会发现：
      * 2d obstruction map 是一个 以 62*62 为中心的极坐标图
      * **极坐标图的半径代表仰角，范围从 25 到 90**
      * **𝜃：在极坐标中表示方位角azimuth，𝜃=0表示正北方**
    * since the obstruction map is a square which contains a polar plot, we also need to get the boundaries of the polar plot within this square.
      * We accomplish this by keeping the terminal online for 2 consecutive days. The terminal will establish connections with satellites from practically all the regions of the sky within the field of view. 
        * This will result in essentially fully coloring the polar plot region in the gRPC map **【Figure3的e图】**，Since the gRPC map does not reset.

## Starlink‘s global scheduler

The starlink network uses a global scheduler to allocate UT to individual satellites every 15s. 【The scheduling algo is not publicly known.】

* Analyze characteristics of satellites that were allocated to our UT with the goal of reverse engineering the algorithm of the global scheduler

* On average，there are 35-44 satellites in the field of view of a UT in any 15 seconds slot. 

### Comparing the properties of the satellites that a selected by the schedular VS available but not chosen

#### Angle of elevation-AOE

* The position of a satellite in the sky is defined by its AOE (仰角) and azimuth with respect to the UT(相对用户定义的方位角).

  * Figure 4 中，实线表示的选定卫星的中位仰角比其他虚线表示的可被选择但未被选择的卫星高22.9◦

  * 虽然只有30%的可连接卫星的仰角在45°到90°之间，但是**the global scheduler** 还是在这个范围内选择了80%的卫星作为各个测量位置被选择的卫星。【Although only 30% of all available satellites had their AOEs in 45◦ to 90◦ range,**the global scheduler picked 80% of satellites from the range (averaged over all locations).**】

  <img src="/images/img/leo/UT最终连接卫星仰角关系图.png">

  * 根据上图，CDF值选取到0.8的话，卫星仰角需要选择到65°

* 

#### Direction







# Ref 

* ref1：[Measuring the Satellite Links of a LEO Network](https://www.ece.uvic.ca/~cai/icc24.pdf)
* ref2：[Measuring a low-earth-orbit Satellite Network](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://arxiv.org/pdf/2307.06863): Explore Starlink access、core、backbone networks initially with one Starlink user terminal associated with the Ground Station near the Seattle POP with the assistance of RIPE Atlas probes and Reddit Starlink community.
* ref3-measuring LEO from outside?:[Democratizing LEO Satellite Network Measurement](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://arxiv.org/pdf/2306.07469)
* ref4-reveal starlink scheduling internals:[Making sense of constellation](https://dl.acm.org/doi/pdf/10.1145/3624354.3630586)
* ref5-[Starlink FCC filings](https://forum.nasaspaceflight.com/index.php?topic=48981.0)
* ref6-[medium access control scheduler for UT communications](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://patentimages.storage.googleapis.com/d2/fe/83/c902a1f49fe66e/US9032075.pdf)




------

