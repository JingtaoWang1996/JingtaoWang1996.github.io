---
title: 'Offensive Reconnaissance'
date: 2025-05-26
permalink: /posts/2025/05/Offensive-Reconnaissance/
tags:
  - Real Work Practice
---

Offensive Reconnaissance-进攻侦察相关文献阅读笔记



# The Silent Art of Reconnaissance：The Other Side of the Hill 

**Paper Target:** 

* explores different kind of reconnaissance techniques that are used by an attacker or hacker to collect information regarding the target. 
* Further determines which recon technique gathers the most information about the target while keeping its identity hidden. 

## Reconnaissance BG

* Originated in 1800-1810 from French language means "Act of Surveying"
* Virtually every network attack preceded by network reconnaissance.
* The process of reconnaissance,revolve around one simple idea **"Information Gathering"**

### Type of Reconnaissance 

**Passive Reconnaissance**

* No direct contact of any sort between the target and attacker.
* Many times the information is all available online target website, such as DNS & WHOIS, which gives out handy information for drafting a sketch and then keeps fill in the blanks by using other open-source tools.
* In short: Start with target's DNS and whois record,then further dig other possible information such as mail records.etc. -> Social Engineering and online publications to further decide what kind of attack tools to use.

**Active Reconnaissance**

* Most common reason is anonymity(匿名)
* **Start with tools that send packets to learn the target system.**
  * **traceroute** : <u>Know the address of routers and firewall that protected the target hosts.</u>
    * Possible Infos: **Gateway、Each hops、TimeTaken**
  * **Port Scanning** ：nmap、zmap、masscan etc.,
  * **DNS Scanning**
  * **Footprinting **: nmap

## Reconnaissance Tools

| Passive Reconnaissance        | Active Reconnaissnce |
| ----------------------------- | -------------------- |
| Centeralops.net               | Kali Linux           |
| Dnsstuff.com                  | zmap                 |
| Who.is                        | nmap                 |
| Mxtoolbox.com                 | masscan              |
| Web.archive.org               | dnsrecon             |
| Wayback.archive-it.org        | dnsenum              |
| Google Operator Search Engine | dnsmap               |









# Ref

* [The Silent Art of Reconnaissance: The Other Side of the hill](https://www.researchgate.net/profile/Usman-Dar-4/publication/341494652_The_Silent_Art_of_Reconnaissance_The_Other_Side_of_the_Hill/links/5ec42898299bf1c09acbd8ba/The-Silent-Art-of-Reconnaissance-The-Other-Side-of-the-Hill.pdf)






------

