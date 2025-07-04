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

* On average，there are **35-44 satellites in the field of view of a UT in any 15 seconds slot**. 

### Feature1-Impact of satellite position

**Comparing the properties of the satellites that a selected by the schedular VS available but not chosen**

#### Angle of elevation-AOE

* The position of a satellite in the sky is defined by its AOE (仰角) and azimuth with respect to the UT(相对用户定义的方位角).

  * Figure 4 中，实线表示的选定卫星的中位仰角比其他虚线表示的可被选择但未被选择的卫星高22.9◦

  * 虽然只有30%的可连接卫星的仰角在45°到90°之间，但是**the global scheduler** 还是在这个范围内选择了80%的卫星作为各个测量位置被选择的卫星。【Although only 30% of all available satellites had their AOEs in 45◦ to 90◦ range,**the global scheduler picked 80% of satellites from the range (averaged over all locations).**】

  <img src="/images/img/leo/UT最终连接卫星仰角关系图.png">

  * 根据上图，CDF值选取到0.8的话，卫星仰角需要选择到65°

#### Direction--选择朝向北边的更多

distribution of azimuth of two sets of satellites.

* 方位角被分成4个90°，**且最终选择的卫星方位角和UT的朝向强相关**
* 实验结果中除了一个在NY的因为UT在西北方向被遮挡所以选择这个方向的卫星很少，其他的都朝北方倾斜较多。
  * However，the UT was mapped to satellites【**UT被分配到其北侧的卫星的覆盖率为82%**】

#### Rationale

ref-[WRS-22 Regulation of satellites in Earth's orbit](https://www.itu.int/hub/2023/01/satellite-regulation-leo-geo-wrs/)

* The International Telecommunication Union（国际电信联盟）has imposed a mandatory geo-stationary orbit exclusion zone（地球静止轨道禁区）, which prohibits LEO satellites from transmitting to or receiving from a ground station while being in the protected part of the sky .【ITU没有设立地球禁止轨道禁区，只有一个频段的分配】
  * A satellite is a repeater in orbit, and it cannot repeat on the same frequency band that it receives on from earth. Otherwise,the satellite will interfere with itself.
* Based on satellites orbital characteristics, there are 4 types of satellites:
  * Low Earth orbit (LEO):200-2000km 
  * Medium Earth Orbit（MEO): 8000-20000
  * GeoStationary Earth (geosynchronous equatorial) orbit--AKA Clarke Orbit: fixed at 35,786 km above the equator(赤道)
  * Highly elliptical椭圆 orbit（HEO）:may reach 40,000 KM from earth in apogee (远地点)
* Satellites with high AOE can communicate with terminals in a more energy efficient way.

**几个映射关系**

* **The distance between UT and satellites increases inversely with AOE**：卫星到UT之间的距离与卫星仰角成反比
  * Radio frequency RF power decreases inversely with distance, satellites farther way need to use significantly more power to communicate with UT, satellites farther away need to use significantly more power to communicate with UT. 

### Feature2-Satellites launch dates 

**Whether the global scheduler prefers satellites from certain batches of launch dates over others **

* Averaged over all locations, the probability of picking a satellite increases with an increase of one month in the satellite’s launch date： 在基于其观测时间的所有15s间隔中，发射时间每增加一个月，选中的概率都会增加。
  * 选中概率 = %(No. of slots a satellite from a launch was picked/No. of slots a satellite from a launch was available) for all 15 second slots in our observation.

#### Rationale

* As starlink satellites are launched in batches，the difference in service time between the latest and oldest satellites can differ by years. 
  * **Starlink satellites has a service lifetime of about 5 years**, some parts of the constellation would be out of service years before others. 

### Feature3 - Sunlit-是否优先选择卫星当前时刻在太阳照射下的，以保证能量支撑

Starlink satellites are equipped with solar panels to provide power for their operations.  **Analyze whether Starlink's global scheduler has preference for sunlit satellites**

**实验方式**

* step1:For every 15s，we calculate positions of all available satellites relative to the sun using the **SkyField library**
* step2:提取所有15s的slot中至少包含一个sunlit 和 dark satellites 

**结果**

在满足step2条件的所有slot当中：

* 72.3%的情况下选择sunlit的卫星
* 只有在 **dark satellites/available satellites** >=35%时才会选择dark卫星

* **AOE of dark satellites picked by the scheduler was 25° higher than their sunlit counterparts** 

## Modeling the global scheduler

* preference：
  * newer satellites 
  * sunlit
  * located towards the North West 
  * at high angle of elevation

* Goal of this model：**predict the characteristics of the satellites allocated to server a UT in a given location and time** 



# Analysis of LEO-Satellite Fronthaul Schedulers

原文见ref7【综述类型文章-和上一篇没有区别】

## Intro

* LSNs consist of two parts: 
  * fronthaul is the connection between users and satellite constellations.
  * backhaul links the constellations to the core network.

* This paper's focuses on **the design concept for fronthaul scheduling algos**:
  * Objectives: low latency、high capacity、wide coverage、energy efficiency、fault tolerance 
  * Impact parameters：AOE、direction、launch date、sunlit status【这些参数同时对算法产生pos、neg影响，因此需要一个trade-off】
* 星间链路定义：The links within a LEO satellite constellation can either be set directly via laser or radio connection.

## Possible factors

* AOE
* SUNLIT
* exclusive zone：《无线电通信法规》第22条，因为地球静止卫星相对于地面禁止，因此，尽可能让leo在特定区域不进行连接分配。

# An In-Depth Investigation of LEO Satellite Topology Design Parameters 

## Intro

* There exists thresholds for the number of satellites per orbit and the number of orbits below which the latency performance degrades significantly.
  * When the number of satellites per orbit is below 28, there is a significant performance drop,even when the total number of orbits is increased to a very high value of 59.
  * we show that the latency
    performance is better when the angle between the traffic endpoints
    is closely aligned with the satellite orbit inclination
* Network delay between a pair of traffic endpoints depends on the alignment of satellite's orbit (inclination).

* A distinguishing feature of LEO satellites is **the presence of Inter-Satellite-Links** (compared with GEO and MEO satellites)
  * ISL: allow satellites to communicate with each other directly at the speed of light.
* Each satellite is equipped with 4 optical space laser generators and 4 laser signal receiver surface [support optical laser communication between neighboring satellites up to 80 Gbps]

* The number of orbits in a shell determines the coverage.
  * Shell: 处于同一高度、不同轨道上的卫星集合。

* inclination: equator（赤道）和卫星轨道之间的夹角-锐角
* +Grid: **The most studied topology is the +Grid topology，where each satellite connects to two adjacent satellites in the same orbit and two nearest satellites on each of its neighboring orbits.** 

## Evaluation

**Key-questions**

* what are the key parameters that influence the performance of an LEO network？
* Are there thresholds for each parameters above/below which the performance degrades significantly?
* Why does a shell with a low number of satellites outperform another shell with nearly double the number of satellites (Shell1 VS. Shell2)
* How does the difference between satellite orbit inclination and the geographical angle of the plane containing the source and destination location affect performance?



## Takeways 

* 97.6° degree orbits are sun-synchronous（太阳同步轨道）

* ISL file (Inter-Satellite Link): We **connect each satellite using the +Grid topology** and build the network for the LEO mega-constellation. Store these edges between satellites in an ISL file, which contains the network graph.

* Why does Starlink Shell 2 offer better performance than shell 1?

  * S2 offer better latency performance compared to S1,in spite of having only nearly half the number of satellites. 
  * **The satellites/orbit(20) of S1 is lower than the minimum threshold required for good performance (28)**,[satellites/orbit低于20的时候，即使卫星数量远远大于，也不会有很好的latency]

* An inclination of 55° offers the best performance. Most commercial constellations today use an orbital angle very close to this value [**STARLINK 是53°**]

  **The number of average hops changes with the inclination.**

  * When endpoint pairs have a geographic angle >70°，the average hop count gradually decrease with an increase in inclination from 45°-75°
  * When endpoint pairs have a geographic angle <40°，the average hop count gradually decrease as inclination decreases from 75°-45°

  

# SpaceX星链卫星发布星历的研究

## Intro

* 星历文件后发现该星历基本是**未来3天的预报轨道**
* 平根数研究表明星历文件的
  * 前部分是至少考虑20阶非球形引力摄动的外推轨道
  * 后部分是考虑J2项摄动的设计轨道, 星历包含协方差信息

* 停泊和工作轨道卫星的星历在**前1 d的精度优于2 km**, **抬升阶段卫星星历的精度在半天不到的时间内迅速增长至数公里**
* 通过发布星历的设计轨道可以**更加精确地分析星链星座构型**, 尤其是各卫星的设计定点位置, 有助于星链卫星的识别和跟踪. 研究为星链星历的广泛应用提供有益参考, 为**星链卫星的机动检测和碰撞预警**提供依据.
* TLE数据发布方：North American Aerospace Defense Command-NORAD
* 星历数据发布方：spacex 缺少相应的明确说明给进一步使用带来了困难。

**Paper‘s Contribution**

* 星历文件名的含义、基于平根数方法初步分析了该星历采用的预报轨道模型、给出星历中对应于三个主要运行阶段的轨道精度，并利用星历数据中的理论涉及轨道明确了各星链卫星的顶点位置和星座构型参数。

## 星链卫星星历精度分析

### 发布及格式说明

Space-track是美国联合太空司令部态势感知部队运营的网站, 该网站对外部来源星历的文件命名和数据格式制定了规则, 要求卫星运营商必须按照相应的规则发布星历文件[ref9-ref6]

* 每隔8h左右更新一次，每天发布3次

* 多个压缩文件存储，压缩文件解压后发现有多个文件，每个文件对应一颗卫星：

  * 文件名称示例：对应名称见下方边表格

    **MEME_44713_STARLINK-1007_3312139_Operational_135 3879600_UNCLASSIFIED.txt** 

    | 字段名称      | 字段含义                                                     |      |      |
    | ------------- | ------------------------------------------------------------ | ---- | ---- |
    | MEME          | Mean Equator Mean Mean Equinox，verified to math J2000       |      |      |
    | 44713         | Satellite catalog-星链目录                                   |      |      |
    | Starlink-1007 | Satellite name                                               |      |      |
    | 3312139       | Start time of the ephemeris in UTC,formmated as (Day of Year, hour, and minute values) |      |      |
    | Operational   | Ephemeris includes maneuver information                      |      |      |
    | 1353879600    | Additional information provided by SpaceX, verified to match the<br/>final epoch’s GPS time in seconds, formatted as “SSSSSSSSSS” |      |      |
    | UNCLASSIFIED  | Security classification of the data                          |      |      |

* 对于每个星历文件的数据头来说：
  * 都包含：文件头和数千个数据块
  * 文件头：4行
    * 文件创建时间，时间阶段间隔
    * 起始和结束时间
    * ephemeris_source:blend（混合模型）【卫星轨道来源】
    * 采用的坐标系：UVW【相对于某个参考点或方向定义的局部坐标系】

* 数据块定义了:历元时刻和卫星状态及其协方差信息
  
  * 协方差矩阵按照下三角的方式保存，60s的时间间隔*3day = 4321个数据块
* **根据文件头可以看出：**
  
  * 星历的创建时间大部分比该星历文件的起始时间晚10-30min

### 星历的模型分析

ephemeris_source: blend

* 对星链卫星这类低轨空间目标而言,地球的非球形引力摄动是造成其轨道根数发生变化的主要摄动力. 将星历中的卫星状态数据转换成不同阶次地球引力场下的拟平均根数[7{8], 可以初步分析外推星历采用的引力场阶次状况. 拟平均根数是密切根数扣除主要摄动力引起的短周期变化后的轨道根数, 由于它消除了短周期变化造成的相位差, 如果采用的引力场摄动阶次合适, 那么在扣除轨道半长径a的1阶和2阶短周期影响后, 平半长径除了在大气阻力摄动下稍有衰减外, 在1阶解的意义下基本保持稳定.

* 在描述卫星的运动轨道时, 通常以开普勒根数(a, e, i, Ω, !, M)为基本变量. 其中, e为偏心率、i为轨道倾角、Ω为升交点赤经、!为近地点幅角、M为平近点角. 然而, 星链卫星的轨道都是偏心率较小的近圆轨道, 继续采用开普勒根数会导致奇异性问题.

**其他结论**

* **对于工作和停泊阶段的星链星历：预测模型在约1.5天处发生突变，2023年之后会在2d时形成突变**
  * 1.5d后的星历数据是仅考虑J2项摄动的理论轨道设计。
* 抬升阶段的卫星：大部分预报时间采用理论设计模型，时间跨度2.75d
  * 抬升阶段：频繁的机动可能导致其他摄动力对轨道影响较小，因此抬升阶段直接采用理论设计模型。

### 星历的内部精度分析

* SpaceX发布的星链星历文件包含了卫星状态的协方差信息,这为判定预报轨道的精度提供了方便.
  * **通过对协方差数据进行分析，可以得到星链预报轨道的自评估精度**
* starlink卫星和火箭分离后主要有：停泊、抬升、工作3个运行阶段：
  * 停泊：350KM附近
  * 抬升：350KM-550KM
  * 工作：不同shell层的高度也不同：540-550KM
  * **停泊轨道、抬升轨道、工作轨道的3个阶段的判断方式：分析一定时间内星历数据中提供的卫星高度**
    * 维持在350KM附近：停泊阶段
    * 从350KM开始一直到560KM左右一直处于上升阶段：抬升阶段
    * 工作阶段：540-560KM，维持在一定的高度：工作阶段
* 预测精度分析：遍历某个一个卫星的星历文件，提取每个历元时刻的1、3、6协方差数据，开方得到U V W 方向的预报轨道自评估误差
  * 同一阶段星链卫星的预报经度呈现相同的变化趋势。
  * 处于停泊轨道和工作轨道上的卫星在前1d的轨道预报经度是<2km的，抬升阶段的轨道误差极大

## 发布星历的初步应用

* 星座构型是星座的基本要素，是星座覆盖特性、工作性能以及运行维持性能的决定性因素。
* 可以基于tle数据对星链星座构型进行分析
  * TLE数据+walker-σ星座 + 从卫星发射入轨和轨道面分布两方面讨论了星链星座部署情况
    * 缺少每颗卫星的定点位置及精度情况。
* 星历中含有的仅考虑J2带谐项摄动的理论设计轨道，对于研究庞大的starlink卫星非常有利。

# Optimal Gateway Placement for minimizing Intersatellite Link Usage in LEO Megaconstellation Network

用途：satellite最终入网需要gateway，如果能搞清楚gateway的分布，是否也是方案之一？

## Intro

* In addition to the gateway number，the gateway location also affect the ISL usage.
* Satellites may require different ISL hop counts and bandwidth to reach gateways at different locations. 
  * Each ISL relay is also called one hop.
* The higher user demands also require more ISL resources.
* **The ISL bandwidth is relatively smaller than the satellite-ground links.**
  * Due to the onboard limited energy and high requirements of the antenna pointing system constrain the bandwidth of  ISL. Thus, the ISL usage is expected to be minimal.
* Contribution of this paper：
  * A novel ISL usage evaluation method is proposed
  * A mixed-integer optimization model is proposed to minimize the overall ISL usage.

**Focus: The relations between gateway placement and ISL usage**

* An ISL usage metric evaluation method with lower computational cost, and solve the gateway placement problem,by minimize the ISL usage.

* considered factors include:
  * gateway number
  * the difference between ascending and descending satellites
  * ISL configuration
  * ground traffic pattern

## System model 

### Walker-δ constallation

* Formal notation： **α：Ns/Np/F**
  * α：orbit inclination
  * Ns: total satellite number
  * Np: number of orbit planes。**所有的orbit planes are evenly distributed along the equator**
    * the right ascension of ascending node(RAAN) difference between adjacent orbits is 2pi/Np
  * F：phasing factor（相位参数), 代表从一个轨道面到下一个轨道面，卫星的角度偏移量，用于确保卫星平均分布在一个orbit上不会撞上
    * res = (360°*F/Ns)
  * u：satellite phase angle(卫星相位角)，用于确定卫星在orbit plane中的位置，取值范围[-180°，180°]

* Based on the satellite flying direction and phase angle, satellites in the constellation are classified into 2 type:
  * ascending satellite (SatA): 相位角u∈[-90°，90°]从南向北飞
  * descending satellite (SatD):相位角u∈[-180°，-90° & 90°，180°]从北向南飞

## Multihop ISL path

* **The capacity at each satellite node is occupied by traffic from both its coverage regions and neighboring satellites.**
  * Since all traffic is destined to gateways, the satellites [At given moment] closer to the gateway need to carry more traffic load.
* In a multihop transmission，**each packet is relayed through mutlple ISL**, one for **each hop, occuping a larger number of redundant spectrum resources of ISL**

* **Ideally, the system capacity is proportional to the number of ISL, inversely proportional to the average of hop count** <u>**[理想情况下，系统容量与 ISL 数量成正比，与平均跳数成反比.]**</u>
  * 因此，在ISL资源有限的情况下，minimizing the hop count can effectively save the ISL usage and increase the capacity utilization efficiency
    * To minimize the usage of ISL,packet should select the minimum hop path and select the nearest gateway in terms of hop count as their destination.
* 本文关注的点是：**如何获得最少的hop count，而不是具体的路径选择（在hop count相同的情况下选择哪一个）**

## ISL Usage Evaluation Model

* The constellation network with ISLs can be represented by an **undirected graph** Gsat = (S, E)
  * S is the satellite node set, |S| = NS(卫星具体数量)
  *  E is the ISL set, |E| = NL.(As the mesh network topology is a 2-D torus, **NL = 2NS** 【由于网状网络拓扑结构是二维环面，因此**NL = 2NS** 】)
  * The feeder satellite set is denoted by F, F ⊆ S and |F| = NF.
* **Takes the overall traffic load on ISL as the ISL usage.**

* Each hop adds the original input traffic to an ISL, and the accumulation of input traffic along the path equals the sum of the traffic of all ISLs. 

  * 每一个卫星(hop)都会有一个自带的输入load，表示当其作为access satellite时候的load
  * **按照下图所示，在ISL上总的load就是所有黑色箭头的传输方向求和，越到后面占用的ISL越多。**

  <img src="/images/img/leo/ISL load 传输示意图.png">

* 因此，考虑到从某个access satellite的input load可能有多个destination，因此ISL的使用情况总数可以等价于：

  * 每一个卫星的load * 每一个gateway分到的每一个卫星的load的比例 * 每一个卫星到每一个satellite之间的hop count（H\_{i,m}） ==> **To evaluate ISL usage, H_{i,m}--[计算satellite2gateway之间的hop就十分重要]**

## Hop-Count Calculation Model

**We first adopt a theoretical model to calculate the hop count between two satellites**

* input：latitudes and longitudes of two satellites 
* 基于Fig10，及下面的结果，随着地面站的增加，**最多10跳从一个satellite到一个地面站**



某个时刻某个UT是否连接到某个GS

* step1: UT 25°过滤出30-50个卫星，目标GS过滤出30-50个卫星
* step2：基于文中计算出30-50个卫星每一个hop count最少的情况，过滤出最可能的路径









<img src="/images/img/leo/两个卫星之间基于ISL的hop距离计算示意图.png">

* 如上图，展示了两个卫星之间的hop计算
* 





## Other refer

* “An optimization method for the gateway station deployment in LEO satellite systems [studied the optimization of gs deployment to minimize the usage and maximize the satellite-ground link capacity for gateway in China]
  * in china 是不是就拿得到数据源了
* Y. Vasavada, R. Gopal, C. Ravishankar, G. Zakaria, and N. BenAmmar,
  “Architectures for next generation high throughput satellite systems,”
  Int. J. Satell. Commun. Netw., vol. 34, no. 4, pp. 523–546, 2016   
  * Empirical results for satellite placement 
* 



# Ref 

* ref1：[Measuring the Satellite Links of a LEO Network](https://www.ece.uvic.ca/~cai/icc24.pdf)
* ref2：[Measuring a low-earth-orbit Satellite Network](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://arxiv.org/pdf/2307.06863): Explore Starlink access、core、backbone networks initially with one Starlink user terminal associated with the Ground Station near the Seattle POP with the assistance of RIPE Atlas probes and Reddit Starlink community.
* ref3-measuring LEO from outside?:[Democratizing LEO Satellite Network Measurement](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://arxiv.org/pdf/2306.07469)
* ref4-reveal starlink scheduling internals:[Making sense of constellation](https://dl.acm.org/doi/pdf/10.1145/3624354.3630586)
* ref5-[Starlink FCC filings](https://forum.nasaspaceflight.com/index.php?topic=48981.0)
* ref6-[medium access control scheduler for UT communications](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://patentimages.storage.googleapis.com/d2/fe/83/c902a1f49fe66e/US9032075.pdf)
* ref7-[Analysis of LEO-Satellite Fronthaul Schedulers](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.net.in.tum.de/fileadmin/TUM/NET/NET-2024-09-1/NET-2024-09-1_01.pdf)
* ref8-[An In-Depth Investigation of LEO Satellite Topology Design Parameters ](https://arxiv.org/pdf/2402.08988)

* ref9-[SpaceX星链卫星发布星历的研究](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://pmo.cas.cn/xscbw/twxb/xbll/2024_65/2024_65_6/202412/P020241202575071476317.pdf)


------

