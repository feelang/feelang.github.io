---
layout: single
title: 诡异的问题 NoClassDefFoundError
date: 2016-07-20 21:33:33
categories: Programming
tags:
  - Android
---

今天又遇到一个比较难搞的问题，记一下流水账。

APP 中引用了一个二方包，编译成功，结果运行时报错 - `NoClassDefFoundError`。

<!-- more -->

## try #1 - multiDexKeepProguard
首先确认是不是由于类没有被放到 main dex 中导致了这个问题。打开文件 `build/intermediates/multi-dex/debug/maindexlist.txt`，查找类名，发现文件中包含了我们要找的类。

不放心，说不定是 Multidex 的bug，手动把这个“丢失”的类放进 main dex。

*build.gralde*
```groovy
android {
  defaultConfig {
    multiDexEnabled = true
    multiDexKeepProguard file('multidex.pro')
  }  
}
```

*multidex.pro*
```proguard
-keep public the-full-name-of-the-missing-class { *; }
```

编译运行，问题依然，并没有什么卵用。

既然不是 main dex 问题，那我们先来确认一下问题是否由 MultiDex 引起。

## try #2 - 关掉 Multidex
关掉 multidex 然后打一个 release 包。

> 由于方法数受限，关掉 Multidex 之后打不出 Debug 包，但是混淆过后方法数减少很多，可以顺利打出 Release 包。

*build.gradle*
```groovy
defaultConfig {
  multiDexEnabled true
}
```

编译运行，依然出错，可以确定不是 Multidex 的锅。

## try #3 - 传递依赖

把依赖由只依赖 aar 改为传递依赖。

~~`compile 'me.liangfei.android:weird-1.0.0@aar'`~~ 
`compile 'me.liangfei.android:weird-1.0.0'`

结果却发现 `weird.aar` 引用了一个**服务端已经删除但是有本地缓存**的包，也就是说 `weird.aar` 引用了一个并不存在的包，所以改为传递依赖之后，gradle 无法获取这个并不存在的包。

由此推断出，`weird.aar` 肯定不是一个“正确”的包，估计上面的问题也是由此引发（待确认）。


## 总结

### 打包
* 本地打包不可信
* 必须要通过 CI 发包

### ClassNotFoundException vs NoClassDefFoundError

* `ClassNotFoundException` 一般是 `ClassLoader` 无法找到类导致的，例如 `Class.forName("your-class")`。
* `NoClassDefFoundError` 一般是属于 **Link Error**，主要是由于打包之后缺失文件导致的，例如 `new` 一个对象。

