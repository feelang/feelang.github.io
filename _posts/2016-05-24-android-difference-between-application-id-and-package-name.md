---
layout: post
title: ApplicationId 与 PackageName 的区别
date: 2016-05-24 21:02:45
categories: Android
---

在 _Android Gradle Build System_ 诞生之前，**PackageName** 就是 App 的进程 id。

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.my.app"
    android:versionCode="1"
    android:versionName="1.0" >
```

此处的 package 属性有两个用途：

0. App 的进程 ID
1. `R` 的包名以及 Manifest 中 Activity 等四大组件的相对包名。

但是，Android 利用 Gradle 作为 Build System 之后就“起风了”。

<!-- more -->

```groovy
apply plugin: 'com.android.application'

android {
    compileSdkVersion 19
    buildToolsVersion "19.1"

    defaultConfig {
        applicationId "com.example.my.app"
        minSdkVersion 15
        targetSdkVersion 19
        versionCode 1
        versionName "1.0"
    }
    ...
```
`com.android.application` 插件的 `android` 这个 DSL container 中定义了一个 `applicationId`，这个 `applicationId` 取代 package name 成为 App 的进程 id。

不同的 flavor 或者 build type 可以拥有不同的 application id，也就是不同的进程 id。

```groovy
productFlavors {
    pro {
        applicationId = "com.example.my.pkg.pro"
    }
    free {
        applicationId = "com.example.my.pkg.free"
    }
}

buildTypes {
    debug {
        applicationIdSuffix ".debug"
    }
}
....
```

所以，application id 与 package name 分工明确。

0. **application id** 负责 App 的进程 ID
1. **package name** 负责 `R` 的包名以及 Manifest 中 Activity 等四大组件的相对包名

如果 build.gradle 中没有指定 `applicationId`，那么 application id 的默认值就是 `manifest` 的 `package` 属性值。

参考资料
---
* [ApplicationId versus PackageName](http://tools.android.com/tech-docs/new-build-system/applicationid-vs-packagename)
