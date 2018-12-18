# DDMP(Data—Driven Material Platform)
## 项目介绍： 
本项目是针对化学元素可以进行化学物质的查询，并且同时可以对这个化学进行物质分析和一些相关的化学运算，在此项目中我们会采用VASP进行化学物质的相关运算。并且运算后我们根据得到的数据，对数据进行数据分析。  
这次研究的主要课题是材料基因组的核心问题是通过材料数据挖掘、高通量计算与高通量实验三者的交叉融合，实现材料快速筛选与新材料理性设计，达到降低成本与缩短研发周期的高效研发模式。  
> ## 本项目：  
> * 针对材料数据库与材料计算独立运行导致数据传输效率低、出错频率高、数据分析量大的基本技术问题，利用关系数据库及NoSQL技术开发可以实现数据挖掘、快速搜索、分类管理的结构化、半结构化与非结构化结合的材料数据库  
> * 基于SOA架构与工作流技术开发材料数据库、高通量（高性能）计算、数据智能采集分析、数据存储的自动化运行平台，设计构建材料数据库（以锂电、热电材料为基础）-高通量计算一体化高效管理平台，实现数据快速传输、自动化建模、归一化的参数设置、自动化数据采集分析储存的基本模式  
> * 基于数据库-高通量计算一体化平台，开展富锂相锂离子正极材料高通量计算筛选，获得容量高、循环性能好、倍率性能好的正极材料。本项目通过材料科学与计算机技术交叉融合，建立专业化数据库并推进材料基因工程平台建设，最终实现材料快速筛选与设计  

> ## 辽宁大学计算机研究所  
> ### 硅所项目组  
> ### 辽宁大学官网：[http://www.lnu.edu.cn](http://www.lnu.edu.cn)
> ### 项目组Github：[https://github.com/wochaotiandeyingyingying/BM-Project](https://github.com/wochaotiandeyingyingying/BM-Project)  
> ### 参与成员：  
> <table>
>    <tr>
>       <td align="center">Name</td>
>       <td align="center">Title</td>
>       <td align="center">Degree</td>
>       <td align="center">Homepage</td>
>   </tr>
>    <tr>
>       <td align="center">陈廷伟</td>
>       <td align="center">Professor</td>
>       <td align="center">Doctor</td>
>       <td align="center"></td>
>   </tr>
>    <tr>
>       <td align="center">纪文迪</td>
>       <td align="center">Lecturer</td>
>       <td align="center">Doctor</td>
>       <td align="center">https://github.com/WendyLNU</td>
>   </tr>
>    <tr>
>       <td align="center">孙博</td>
>       <td align="center">Postgraduate</td>
>       <td align="center"></td>
>       <td align="center">https://github.com/wochaotiandeyingyingying</td>
>   </tr>
>    <tr>
>       <td align="center">赵纹萱</td>
>       <td align="center">Postgraduate</td>
>       <td align="center"></td>
>       <td align="center">https://github.com/MRZhaowenxuan</td>
>   </tr>
>    <tr>
>       <td align="center">宁春梅</td>
>       <td align="center">Postgraduate</td>
>       <td align="center"></td>
>       <td align="center">https://github.com/CMning</td>
>   </tr>
>    <tr>
>       <td align="center">齐传凯</td>
>       <td align="center">Postgraduate</td>
>       <td align="center"></td>
>       <td align="center">https://github.com/qcklxw</td>
>   </tr>
>   </table>		

## 项目目录： 
.
├─.idea  
│  └─inspectionProfiles  
├─bm_project   //django项目路径  
│  ├─migrations  
│  │  └─__pycache__  
│  ├─static    //静态资源  
│  │  ├─css  
│  │  │  ├─apps  
│  │  │  ├─magnific-popup  
│  │  │  ├─pages  
│  │  │  └─ui-elements  
│  │  ├─font-awesome-4.7.0  
│  │  │  ├─css  
│  │  │  ├─fonts  
│  │  │  ├─less  
│  │  │  └─scss  
│  │  ├─fonts  
│  │  ├─icons-reference  
│  │  │  └─fonts  
│  │  ├─img  
│  │  │  ├─card  
│  │  │  ├─gallery  
│  │  │  ├─search  
│  │  │  └─work  
│  │  └─js  
│  │      ├─magnific-popup  
│  │      └─popper  
│  └─__pycache__  
├─DatabaseCreate   //数据爬虫代码  
├─templates        //html页面  
└─venv  
    ├─Lib  
    │  ├─site-packages  
    │  │  └─pip-10.0.1-py3.6.egg  
    │  │      ├─EGG-INFO  
    │  │      └─pip  
    │  │          ├─_internal  
    │  │          │  ├─commands  
    │  │          │  ├─models  
    │  │          │  ├─operations  
    │  │          │  ├─req  
    │  │          │  ├─utils  
    │  │          │  └─vcs  
    │  │          └─_vendor  
    │  │              ├─cachecontrol  
    │  │              │  └─caches  
    │  │              ├─certifi  
    │  │              ├─chardet  
    │  │              │  └─cli  
    │  │              ├─colorama  
    │  │              ├─distlib  
    │  │              │  └─_backport  
    │  │              ├─html5lib  
    │  │              │  ├─filters  
    │  │              │  ├─treeadapters  
    │  │              │  ├─treebuilders  
    │  │              │  ├─treewalkers  
    │  │              │  └─_trie  
    │  │              ├─idna  
    │  │              ├─lockfile  
    │  │              ├─msgpack  
    │  │              ├─packaging  
    │  │              ├─pkg_resources  
    │  │              ├─progress  
    │  │              ├─pytoml  
    │  │              ├─requests  
    │  │              ├─urllib3  
    │  │              │  ├─contrib  
    │  │              │  │  └─_securetransport  
    │  │              │  ├─packages  
    │  │              │  │  ├─backports  
    │  │              │  │  └─ssl_match_hostname  
    │  │              │  └─util  
    │  │              └─webencodings  
    │  └─tcl8.6  
    └─Scripts  
## 项目配置： 
### 安装环境：  
* python 3  
* mongodb --数据库  
### pip3依赖：  
* django>=2.1.2 --web框架  
* djongo==1.2.30 --python操作mongodb的工具  
* pymatgen --用来分析化学材料的工具  
* xlrd  
* HTMLSession  
* json

