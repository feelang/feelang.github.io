---
layout: single
title: 详解 Android 开发中常用的 DPI / DP / SP
date: 2015-06-23
categories: Android
---

Android的碎片化已经被喷了好多年，随着国内手机厂商的崛起，碎片化也越来越严重，根据[OpenSignal的最新调查](http://thenextweb.com/mobile/2014/08/21/18796-different-android-devices-according-opensignals-latest-fragmentation-report/)，2014年市面上有18796种不同的Android设备，作为开发者，一个无法回避的难题就是需要适配各种各样奇奇怪怪的机型。

设备机型不同必然也会导致屏幕大小和分辨率（Resolution）的不同，但是无论分辨率有多大，屏幕有多大，我们手指触控范围的大小不会发生变化，所以最优的适配方式应该是**指定大小的控件在所有的设备上的显示都一样**。

Android的官方文档对此也有明确的说明：
* When adding support for multiple screens, applications *do not work directly with resolution*; applications should be concerned *only with screen size and density*, as specified by the generalized size and density groups.

所以，适配应该与分辨率无关，只与屏幕大小和屏幕密度相关，首先来看一下什么是屏幕密度 － DPI。

DPI
---
DPI的全称是 _Dots Per Inch_，inch是一个物理单位（无论在任何设备上，其大小都是固定的），所以DPI就是指在一个inch的物理长度内有多少个dot，160DPI的屏幕就表示一个inch包含160个dot，320DPI的屏幕表示一个inch有320个Dot，所以说dot的大小是不固定的。

Android设备用DPI来表示屏幕密度(Density)，屏幕密度大就表示一个inch包含的dot比较多。那PPI是什么呢？
我们会经常看到iPad、iPhone是用PPI来表示屏幕密度，小米Pad也是用PPI来表示。

![](http://img4.tbcdn.cn/L1/461/1/ffa8ab85d4cc4d9e8b9cb379143bb83bcaf40a28)

其实对Android而言，DPI等价于PPI(Pixels-Per-Inch)，DPI最早是用于印刷行业，跟PPI还是有本质不同的，Android应该是误用了DPI这个概念。具体可以参考[PPI vs. DPI: what’s the difference?](http://99designs.com/designer-blog/2013/02/26/ppi-vs-dpi-whats-the-difference/)。

其实我们只要知道在Android设备中，DPI等价于PPI就可以了。

![](http://img2.tbcdn.cn/L1/461/1/73e824419477f8c604791f6318f8a4701c91d165)

通常我们说一个设备是多少寸时，指的是屏幕对角线(Diagonal)是多少inch，所以用对角线的像素值（px）除以对角线长度（inch），就可以计算出PPI。

![](http://img1.tbcdn.cn/L1/461/1/af31a9366de3232f78a9e48904f5b0463875ec25)

为了简化适配工作，Android根据屏幕大小（inch）和屏幕密度（DPI）对设备做了如下划分：
![](http://img1.tbcdn.cn/L1/461/1/5a7fe24f76a7f23cbdea5efa088b1188d73597f5)

DP
---
既然有那么多不同分辨率、不同尺寸的屏幕，使用px必然会导致适配困难，为了进一步简化适配工作，Android为我们提供了一个虚拟的像素单位——DP 或者 DIP (Density-Independent Pixel)，当然也可以理解为Device-Independent Pixel。为什么说是**虚拟**呢，因为它的大小不是一个物理（Phisical）值，而是由操作系统根据屏幕大小和密度动态渲染出来的。

px跟dp之间的换算关系很简单：

    px = dp * (dpi / 160)

举例来说，小米Pad的屏幕密度为326dpi，如果需要显示的图片大小为20dp，那么就需要提供一个`20 * (326 / 160) = 40`px的图片才能达到最佳显示效果，如果还要适配一个163dpi的屏幕，那么还需要再提供一个`20 * (163 / 160) = 20`px的图片。

那么一个20dp的图片，在不同设备上的显示效果如何呢？我们以iPad为例来说明。
![](http://img4.tbcdn.cn/L1/461/1/2c18879aebe47f6faa42c3f3d2e21ccc7e77d66d)

iPad2和iPad Retina的物理尺寸都是9.7inch，不同的是分辨率和PPI，一个是1024x768 / 132ppi，另一个是2048x1536 / 264ppi，

分别计算一下20dp对应多少inch

```python
ipad2 = 20 * (132 / 160) * (9.7 / (math.sqrt(1024 * 1024 + 768 * 768))) 
ipad_retina = 20 * (264 / 160) * (9.7 / (math.sqrt(2048 * 2048 + 1536 * 1536))) 
```
计算结果都是0.1250390625，这就是dp的功能，它能保证在所有的设备上显示的大小都一样。

如果只提供了一个大小为20px的图片，为了保证图片在所有设备上的物理大小都一样，高DPI的设备上系统会拉伸图片，低DPI的设备上图片会被缩小，这样既会影响UE也会影响APP的执行效率。所以我们需要为不同屏幕密度的设备提供不同的图片，他们之间的对应关系如下。
![Android 设备屏幕分级](http://img1.tbcdn.cn/L1/461/1/7d691bde9a6f414a5f93082b0312c1589289494d)

我们在用Sketch作图的时候，如果1x图片对应的是屏幕是MDPI(160dpi)，那么1.5x，2x就分别对应HDPI，XHDPI。
![](http://img4.tbcdn.cn/L1/461/1/4c46ea76d3cf05a87bdf101ac931a1d00ff730ef)

* Android vs iOS: mdpi = 1x, xhdpi = 2x, xxhdpi = 3x

SP
--

SP 全称是 Scale-independent Pixels，用于字体大小，其概念与DP是一致的，也是为了保持设备无关。因为Android用户可以根据喜好来调整字体大小，所以要使用sp来表示字体大小。
![](http://img4.tbcdn.cn/L1/461/1/ed1118ab7e089febd541bd8f1ed454e009edec24)

参考文献
---
0. http://developer.android.com/guide/practices/screens_support.html#DeclaringTabletLayouts
0. http://developer.android.com/training/multiscreen/screendensities.html
0. http://stackoverflow.com/questions/2025282/difference-between-px-dp-dip-and-sp-in-android
0. http://99designs.com/designer-blog/2013/02/26/ppi-vs-dpi-whats-the-difference
