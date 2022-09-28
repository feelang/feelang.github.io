---
layout: post
title: Android 单元测试
date: 2016-01-28 11:24:30
tags: 
  - Android
  - UnitTest
---

Android Studio 和 Android Gradle Plugin 可以让我们脱离 `android.jar` 直接在 development machine 上执行单元测试。

> Unit tests run on a local JVM on your development machine

<!-- more -->

Gradle 插件会编译 `src/test/java` 的代码，运行时会用到一个修改过的 `android.jar`（去掉了所有的 `final` 修饰符），这样就可以利用多态引入 **mocking libraries**。

```groovy
dependencies {
  testCompile 'junit:junit:4.12'
  testCompile "org.mockito:mockito-core:1.9.5"
}
```

命令行
---

```groovy
./gradlew test --continue
```

等价于

```groovy
./gradlew testDebug testRelease --continue
```

其中 `--continue` 表示即使某个 case 失败了，也会继续执行剩下的 case。

Flavors & Build type
---

遵守规范

* src/main/java/Foo.java -> src/test/java/FooTest.java
* src/debug/java/Foo.java -> src/testDebug/java/FooTest.java
* src/myFlavor/java/Foo.java -> src/testMyFlavor/java/FooTest.java

"Method ... not mocked."
---

今天遇到的就是这个问题：

<pre>
java.lang.RuntimeException: Method isEmpty in android.text.TextUtils not mocked.
</pre>

加了 mock 依赖后还是搞不定：

```groovy
testCompile "org.mockito:mockito-core:1.9.5
```

修改配置，让 mock 方法返回默认值还是不行：

```groovy
android {
  testOptions { 
    unitTests.returnDefaultValues = true
  } 
}
```
结果却是：

> We are aware that the default behavior is problematic when using classes like Log or TextUtils and will evaluate possible solutions in future releases.

总结
---

* `android.jar` 是被 mock 过的，所以有些 Android API 返回值可能会不是预期值。
* JUnit 本身是针对 java 代码的单测，所以尽量不要用于使用了 Android API 的方法。
* Android Gradle 插件提供的 mocked android.jar 跟我刚开始工作时做过的测试框架原理类似。

