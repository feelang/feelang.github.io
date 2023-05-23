---
title: 合集管理
excerpt: Jekyll 合集管理
toc: false
lesson: 8
classes: wide
---

{% raw %}

上一篇我们介绍了 [Jekyll 的博客功能](https://blog.csdn.net/FeeLang/article/details/127055114)，本质上博客是一个文章的集合，集合内的文件遵循某种约定。

本篇要介绍的合集（collection）也具备这个功能，两者的不同之处在于：

  * **posts** 是相对独立的内容，有发布日期
  *  **collection** 是一类文章的合集，可以有自己的页面，但是发布日期不重要

既然合集是对内容进行分组，那它的内容一定有共同之处，比如可以是一群人，也可以是某类食谱。

合集内的内容可以展示在一个页面，也可以分开展示，而博文往往只能独立展示。

我们以本篇所属的博客专栏「Jekyll 基础教程」为例要讲解一下合集的具体用法。

首先在项目根目录下创建一个 html 文件：

_tutorial-jekyll.html_

    
```yaml
---
layout: page
title: Jekyll 教程
permalink: /tutorial/jekyll
---

{% for lesson in site.jekyll%}
    <h2>
        <a href="{{lesson.url}}">
            {{ lesson.title }}
        </a>
    </h2>
{% endfor %}
```

这个文件中用到了 `site.jekyll` 这个变量，它就是我们的合集名称，定义在 `_config.yml` 文件中：

```yaml
# Collections
collections:
  jekyll:
    output: true
    sort_by: lesson
```
    

其中

* `output: true` 表示这个合集下每个文件都会被渲染成独立的 html 文件
* `sort_by: lesson` 表示合集内容会根据 `lesson` 字段来排序

`lesson` 定义在每个合集文件的 Front Matter 中，比如：

__jekyll/liquid.md_

```yaml
---
layout: post
title: Jekyll 中文教程之「模板语言 Liquid」
lesson: ch03
---
Liquid 出自 Shopify 团队，和 Jekyll 一样，都是 Ruby 写成的。
（略）
```
    

所有的合集文件会放在一个以下划线开头的文件夹下。

我们在 `_config.yml` 中定义的合集名称叫 `jekyll`，那对应的文件就是 `_jekyll`，文件结构如下所示：

    
    ├── _jekyll
    │   ├── getting-started.md
    │   ├── installing.md
    │   └── liquid.md

合集就是这么简单，具体可以参考我用 Jekyll 搭建的个人博客
[feelang.github.io](https://github.com/feelang/feelang.github.io)。

下一篇将介绍 Jekyll 的数据文件，相当于一个小型的数据库。

{% endraw %}