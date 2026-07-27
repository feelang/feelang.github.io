---
layout: single
title: 写 Gradle 插件的一点经验
date: 2016-09-14 17:40:06
categories: Programming
tags:
  - Gradle
---

本着简单易用的原则，参考[android-resource-remover][android-resource-remover] 写了一个删除无用资源的 Gradle 插件 - [clean-unused-resources-gradle-plugin](https://github.com/YouzanMobile/clean-unused-resources-gradle-plugin)，结果微博发出来不到10分钟，[陈启超][chen-qi-chao]就告诉我 AS2.0+ 已经提供了[此功能](http://stackoverflow.com/questions/6373482/remove-all-unused-resources-from-an-android-project)。天哪，为了纪念这个短命无用的轮子，只好写篇博客，把造轮子的过程记录下来，也算对别人有点用处。

<!-- more -->

[官方文档][writing-custom-plugins]说了，自定义 Gradle 插件有三种方式：

0. Build script
1. `buildSrc` project
2. Standalone project

但是，AS 不完美支持第三种方式，我们用 AS 的爸爸 [IntelliJ IDEA CE](https://www.google.co.jp/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwiD0qrLho7PAhVO4GMKHYqWDd4QFggeMAA&url=https%3A%2F%2Fwww.jetbrains.com%2Fidea%2Fdownload%2F&usg=AFQjCNFTvvWm6f-CgwkzJvE5OINbz0s-Mg) 就好了。

首先 New 一个基于 Gradle 的 Groovy 工程：

![new a groovy project](http://upload-images.jianshu.io/upload_images/620698-b0fe160f1a0de293.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

修改一下自动生成的 build.gradle 文件，把 `repositories` 和 `dependencies` 替换掉，其他保持不变。

```groovy
repositories {
  jcenter()
}

dependencies {
  compile gradleApi()
  testCompile group: 'junit', name: 'junit', version: '4.11'
}
```

然后创建 `src` 和 `resources` 目录（以 [clean-unused-resources-gradle-plugin][clean-unused-resources-gradle-plugin] 为例）：


![project structure](http://upload-images.jianshu.io/upload_images/620698-1d195dc7d9796835.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`resources/META-INF/gradle-plusings/` 是必不可少，否则别人无法使用你的插件，目录下的 `*.properties` 文件名就是插件的名字，别人`apply` 的时候会用到：

```groovy
apply plugin: 'com.youzan.mobile.cleaner'
```

文件内容是把  `implementation-class` 指向你插件类的全名。

```
implementation-class=com.youzan.mobile.CleanerPlugin
```

`CleanerPlugin.groovy` 实现了接口`Plugin<Project>`，而 `org.gradle.api.Plugin` 就是由 `compile gradleApi()` 提供，我们在 build.gradle 的 `dependencies` 中已经添加过了。

准备就绪，开始写插件。

首先，实现 `apply` 方法：

```groovy
class CleanerPlugin implements Plugin<Project> {
  @Override
  void apply(Project project) {
    // 创建一个 extension
    project.extensions.create('resourceCleaner', CleanerExtension);
    // 修改 lint report 路径
    project.afterEvaluate {
      project.android.lintOptions.xmlOutput = new File(project.buildDir, "lintResult.xml");
    }
    // 创建 task
    project.tasks.create('cleanResource', CleanTask)
  }
}
```

第一步通过 `project.extensions.create` 创建一个 `extension`：

*CleanerExtension.groovy*
```groovy
class CleanerExtension {
  Iterable<String> excludedFiles
}
```

这个 `extension` 用于别人向你的插件传递参数，例如：

```groovy
resourceCleaner {
  excludedFiles = [
    'string_pos.xml',
    'string_car.xml',
  ]
}
```
第二步修改 lint report 的路径：

```groovy
project.afterEvaluate {
  project.android.lintOptions.xmlOutput = new File(project.buildDir, "lintResult.xml");
}
```
这里用到了 Android Gradle Plugin 的 DSL，所以 IDEA 无法动态提示，没关系，我们直接去翻[文档](http://google.github.io/android-gradle-dsl/current/)，里面有详解的解释：

![Android Plugin DSL References](http://upload-images.jianshu.io/upload_images/620698-eabe9b5c18386134.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

配置参数（CleanerExtension）和文件参数（lintOptions.xmlOutput）都准备好了。

第三步，主角上场，创建一个 `task`：

```groovy
class CleanTask extends DefaultTask {
  CleanTask() {
    super()
    dependsOn "lint"
  }

  @TaskAction
  def clean() {
    def lintResult = project.android.lintOptions.xmlOutput
    def excludedFiles = project.resourceCleaner.excludedFiles
    Cleaner.clean(lintResult, excludedFiles)
  }
}
```
`CleanTask` 继承自 `DefaultTask`，因为 CleanTask 的输入是 lint report，所以在构造方法中通过调用 `dependsOn "lint"` 让自己依赖于 lint 这个 `task`。

`CleanTask` 就好像 1984 里面的猪，只负责发号施令，安排工作，真正干活的“人”是 `Cleaner`：

```groovy
class Cleaner {
    def static clean(File report, Iterable<String> excludedFiles) {
        def issues = new XmlSlurper().parse(report)
        issues.'*'.findAll {
            it.name() == 'issue' && it.@id == 'UnusedResources'
        }.each {
            def file = new File(it.location.@file.text())
            if (file.name in excludedFiles) return;
            def line = it.location.@line
            def column = it.location.@column

            if ((line == '' && column == '') || column == '1') {
                println "deleting " + file.path
                file.delete()
            } else {
                def m = it.@message =~ $/`R.(\w+).([^`]+)`/$
                if (!m) return;

                def type = m.group(1)
                def entryName = m.group(2);

                def parsed = new XmlSlurper().parse(file)
                parsed.'**'.findAll {
                    it.@name == entryName && it.name().contains(type)
                }*.replaceNode {}

                XmlUtil.serialize(parsed, new FileWriter(file))
            }
        }
    }
}
```

一个简单的独立工程的 Gradle Plugin 就这么写完了，是不是非常简单，先不要高兴，还有最后一步 - 发布到 jCenter。

继续修改 `build.gralde`。

添加 bintray 插件。

```groovy
plugins {
    id "com.jfrog.bintray" version "1.4"
}

Properties properties = new Properties();
properties.load(project.rootProject.file('local.properties').newDataInputStream())

bintray {
    user = properties.getProperty("bintray.user")
    key = properties.getProperty("bintray.apikey")
    publications = ['mavenJava']
    pkg {
        repo = 'maven'
        name = 'cleaner-gradle-plugin'
        desc = 'a gradle plugin to clean unused resources detected by Lint'
        websiteUrl = 'https://github.com/YouzanMobile/clean-resource-gradle-plugin'
        issueTrackerUrl = 'https://github.com/YouzanMobile/clean-resource-gradle-plugin/issues'
        vcsUrl ='https://github.com/YouzanMobile/clean-resource-gradle-plugin'
        publicDownloadNumbers = true
        licenses = ['MIT']
    }
}

```

maven-publish 插件：

```groovy
apply plugin: 'maven-publish'

// custom tasks for creating source/javadoc jars
task sourcesJar(type: Jar, dependsOn: classes) {
    classifier = 'sources'
    from sourceSets.main.allSource
}

task javadocJar(type: Jar, dependsOn: javadoc) {
    classifier = 'javadoc'
    from javadoc.destinationDir
}

// add javadoc/source jar tasks as artifacts
artifacts {
    archives sourcesJar, javadocJar
}

publishing {
    publications {
        mavenJava(MavenPublication) {
            from components.java
            artifact sourcesJar
            artifact javadocJar
            groupId 'com.youzan.mobile'
            artifactId 'cleaner-gradle-plugin'
            version versionName
        }
    }
}
```

OK，大功告成，演出结束，下面是致谢：

* [NuwaGradle](https://github.com/jasonross/NuwaGradle)
* [陈启超_V](http://weibo.com/chenqichao2016)
* [Gradle User Guide](https://docs.gradle.org/current/userguide/userguide.html)

[android-resource-remover]: https://github.com/KeepSafe/android-resource-remover
[writing-custom-plugins]: https://docs.gradle.org/current/userguide/custom_plugins.html
[chen-qi-chao]: http://weibo.com/u/2491729875?topnav=1&wvr=6&topsug=1&is_all=1
[clean-unused-resources-gradle-plugin]: https://github.com/YouzanMobile/clean-unused-resources-gradle-plugin
