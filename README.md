# BM-Project
## 项目介绍： 
本项目是针对化学元素可以进行化学物质的查询，并且同时可以对这个化学进行物质分析和一些相关的化学运算，在此项目中我们会采用VASP进行化学物质的相关运算。并且运算后我们根据得到的数据，对数据进行数据分析。
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
