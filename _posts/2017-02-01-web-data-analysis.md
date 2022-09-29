---
layout: post
title: 架构笔记之数据分析
date: 2017-02-01
categories: data
---

蚂蚁积分是一个数据产品，这个简单的积分体现的是**风控**和**信用**，分数越高表明放贷的风险越小、履约的概率越大，而积分背后的风控体系和信用体系都是来自数据的采集和分析，所以数据是最重要的。

<!-- more -->

数据来源
---
* **UGC**（*对这些数据的分析和掌握可以提供更好的服务*）
* **日志**（*可以得到系统的情况*）

数据分析类型
---
* 数据分析的**实时与否**
  * **实时分析任务**（金融、电子商务）
  * **离线分析任务**（数据挖掘搜、索引擎索引计算、推荐内容计算、机器学习）
* 分析的**数据类型**不同
  * **流式数据处理**（*数据整体价值*）
    * 负载、QPS、网络 Traffic、磁盘 IO
    * 交易下单笔数、交易总金额、PV、UV
    * 用户行为分析
  * **批量数据处理**

日志收集
---
* **inofity 机制**（*解决了日志收集的效率问题*）
  监控文件系统的变化，及时通知应用程序进行相关事件处理。响应性的处理机制，避免了频繁的文件轮询任务，提高了任务的处理效率。

* **ActiveMQ**（*解决了日志数据分发的问题*)
  ActiveMQ-CPP 是 CMS（C++ Messaging Service）的一种实现，是一个能够与 ActiveMQ（支持 JMS 的 Java MOM）进行通信的 C++ 客户端库，能够与 ActiveMQ 高效和便捷地进行通信。

* **架构和存储**
  数据需要经过 inotify 客户端，经由 ActiveMQ 进行转发，通过 Storm 进行实时处理，在存储到 MySQL、HDFS、Hbase 或者 Memcache 这些存储系统当中，最后在进行深度分析或者实时展现。

  ![日志收集和分析系统架构](http://upload-images.jianshu.io/upload_images/620698-119c11e12169cd7e.png)

  * **Storm** - 实时分布式流处理系统（数据流切割、集群容错、任务调度），类似 Hadoop 提供的大数据解决方案，但是它处理的对象是**没有终点的数据流**，而非 Hadoop 的 MapReduce 那样的**批处理系统**。
  * **Hadoop**（海量数据持久化存储和分析方案）
    * **HDFS**（Hadoop Distributed File System）保存**非实时海量数据**，然后通过 MapReduce 或者 HiveSQL 进行数据分析与挖掘。
    * **Hbase**（列存储系统、天生支持数据表的自动分区）保存实时展现内容。
    * **关系型数据库**（例 MySQL）存储可控量级的数据（PV信息、系统 load 平均值等）。关系型数据库复杂的条件查询与多表关联的能力是 Hbase 这类列存储数据库所不具备的。
    * **高效缓存系统**（例 Memcache，内存电信号寻址）用于实时性和系统 TPS（Transaction Per Second）能力要求非常高的场景（活动交易量的实时统计）

  * **Chukwa**
    基于 Hadoop 开发的数据采集与分析框架。

离线数据分析
---
* Hadoop
  * **HDFS**
    ![](https://hadoop.apache.org/docs/r1.2.1/images/hdfsarchitecture.gif)
  * **MapReduce**（处理海量数据的并行编程模型和计算框架）
    ![](http://upload-images.jianshu.io/upload_images/620698-862e495ff97953e7.png)
  * **Hive**
    Hive 是基于 Hadoop 的一个**数据仓库**工具，可以讲 HDFS 存储的结构化的数据文件映射为一张数据库表，提供完整的 SQL 查询功能，还可以将 SQL 语句转换成 MapReduce 任务进行运行。
    ![](http://upload-images.jianshu.io/upload_images/620698-f5a1fcc0e1d9f341.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

流式数据分析
---
* **Storm**
  * Topology 原语执行的是实时处理任务，不同于 MapReduce 执行的是批处理任务。
  * 实习分析、在线机器学习、持续计算、分布式 RPC、ETL 等
  * 特点
    * 编程模型简单（Topology 原语）
    * 高容错性和高可靠性
    * 高效（ZeroMQ 作为底层消息队列）
    * 多语言支持
    * 可扩展性（方便地支持集群扩展）

  ![](http://upload-images.jianshu.io/upload_images/620698-8ea1b43dc2421b8d.png)

数据同步
---
数据分析过程：从在线的 OLTP（OnLine Transaction Processing、传统的关系型数据的主要应用）库中，以及日志系统当中，提取和清洗所需要到的数据到 OLAP（OnLine Analytical Processing、数据仓库系统的主要应用） 系统，如构建在 Hadoop 上的 Hive 平台，然后在OLAP 系统上进行多维度复杂的数据分析和汇总操作，利用这些数据构建数据报表，提供前端展现。

* **离线数据同步**
  * Sqoop
  * DataX
* **实时数据同步**
  * ActiveMQ
    ![](http://upload-images.jianshu.io/upload_images/620698-74b47f6dd1ba3d8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  * MySQL 的 Binary log

数据报表
---
* 数据可视化
* highcharts （js 报表工具）

参考资料
---
0. 《大型分布式网站架构设计与实践》
0. http://tech.youzan.com/you-zan-big-data-practice/
0. https://github.com/alibaba/DataX/wiki/DataX-Introduction
