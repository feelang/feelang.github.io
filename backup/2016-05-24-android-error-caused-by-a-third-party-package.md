---
layout: single
title: 引入三方包导致 Theme 失效
date: 2016-05-24
categories: Programming
tags:
  - Android
---

引入一个三方包之后导致 App 主题失效，定位了一个下午，做个记录。

<!-- more -->

`AndroidManifest.xml` 文件中 `application` 节点配置如下：

```java
<application
    android:allowBackup="false"
    android:icon="@mipmap/app_icon"
    android:label="@string/app_name"
    android:theme="@style/AppTheme"
    tools:replace="android:allowBackup">
```

刚开始觉得应该是 App 的 theme 被覆盖掉了，然后添加了一个 **replace**。

```xml
tools:replace="android:allowBackup, android:theme"
```

结果主题依然失效，然后把三方包中在 AndroidManifest 中注册的 `Activity` 挪到 App 的 Manifest 中，还是不行。

最后跳转 `@style/AppTheme` 时发现三方包的依赖包中也定义了一个同名的 Style，而且还是在 **values-21** 文件下，而 App 并没有定义 **values-21** 下的 Style，所以 APP 的主题就被三方包的 Style 给覆盖掉了，而 `android:replace='android:theme` 只有在属性冲突的时候起作用，我的 App 并没有提供 values-21 的 Style，因此没有冲突，无法 `replace`，于是悲剧了。

__解决方案__

0. App 的主题名字最好具有唯一性， 不要叫 `AppTheme`，容易同名。
0. App 的主题要定义完整，比如 values / values-21
