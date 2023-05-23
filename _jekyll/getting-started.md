---
title: 快速上手
excerpt: Jekyll 快速上手
lesson: 2
---

{% raw %}

本篇我们会通过一个最简单的 Jekyll 项目来演示如何创建一个项目，并解释这个项目的基本结构。有些细节这里可能不会深入，后续博文会逐一讲解。

## 创建并运行项目

创建一个全新的工程，执行如下命令：

    
    
    $ jekyll new learn-jekyll
    

执行完成之后，我们就成功创建了一个名为 **learn-jekyll** 的 Jekyll 项目。

进到目录下，执行如下命令：

    
    
    $ bundle exec jekyll server
    

项目进入构建阶段，成功之后，在浏览器中打开如下链接：

    
    
    http://127.0.0.1:4000/
    

一个全新的网站就构建出来了。

浏览器访问上述链接时，终端会输出一些日志，Ctrl + C 可以终止项目运行。

## 基本结构

Jekyll 也遵循「约定大于配置」的基本原则，所以上手成本极低。

在新创建的项目目录下，有两个最主要的文件夹：

  * `_posts` \- 用于存放博客文章
  * `_site` \- 用于存放项目构建完成之后所生成的静态文件，也就是说，静态网站的所有文件都会来源于此，其中 CSS 文件、JS 文件以及图片文件，会存放在该目录下的 `assets` 文件夹中。我们可以直接把该目录下的文件拿去部署

除此之外，还有一些其他文件：

  * `_config.yml` 是项目的配置文件，一些全局配置会写在这个文件内，比如 collections（后续推文会讲解），默认文件/路径，等等。总之，这里可以自定义很多东西
  * `.gitignore` 创建项目时会自动生成，不需要纳入到 CVS 的文件存放于此
  * `Gemfile` & `Gemfile.lock` 存放项目所依赖的 Ruby gems

后续我们会重点介绍 `_config.yml` 和 `Gemfile` 这两个文件，因为只有搞清楚它们才能让 Jekyll 发挥出最大的作用。

你可能已经注意到了，项目根目录下还生成了几个 Markdown 文件，Markdown 深受大家喜爱的原因是它比 html 更简洁，比富文本更易编辑。

我们在介绍 [Jekyll
的安装](https://blog.csdn.net/FeeLang/article/details/126981050)时已经提到过： Jekyll 支持
HTML 和 Markdown 两种文件格式。但静态网站所需要的文件肯定是 html 格式，所以这里的 `about.markdown` 和
`index.markdown` 在执行构建时会被转化成 html 文件，放置于 `_site` 目录下。

## 其他的约定目录

除了上面提到的几个目录，我们还可以添加其它的，Jekyll 会自动识别出它们，执行相应的处理。

  * `_data` \- 网站所需要的数据文件（相当于一个小型数据库）
  * `_drafts` \- 博客草稿，不会被构建成静态文件，也不会公开
  * `_layouts` \- 布局文件，相当于一类页面（比如博客类页面）的“父类”
  * `_includes` \- 小模块，属于 HTML 文件的一部分，可以在多个页面中复用，比如导航（navigation）、脚注（footer）等

## 常用命令

  * `bundle exec jekyll serve` \- 适用于开发阶段，构建并运行改项目，实际上是启动了一个 Jekyll 自带的 web server，利用这个命令可以生成网站所需要的静态文件，并在浏览器中直接访问
  * `jekyll build` \- 适用于部署阶段，仅仅构建出网站所需要的静态文件
  * `jekyll help` \- 查看帮助，用法 `jekyll help <command name>`

我们知道，安装完 Jekyll 之后，系统环境中就有了 `jekyll` 这个可执行的命令，它的用法很简单：

    
    
    jekyll command [argument] [option] [argument_to_option]
    
    Examples:
        jekyll new site/ --blank
        jekyll serve --config _alternative_config.yml
    

查看 `jekyll`
的所有用法可查看[官方文档](https://jekyllrb.com/docs/configuration/options/#build-command-
options)，这里罗列几个比较常用的：

  * `jekyll new PATH` \- 创建新项目
  * `jekyll new PATH --blank` \- 创建新的空项目
  * `jekyll build` 或 `jekyll b` \- 构建项目，生成可部署的 `_site` 目录
  * `jekyll serve` 或 `jekyll s` \- 构建并运行项目，会自动监听文件变化，不需要反复执行
  * `jekyll clean` \- 清除所有的构建产物
  * `jekyll new-theme` \- 创建一个新的主题脚手架
  * `jekyll doctor` \- 诊断，输出所有已经废弃的依赖包或者有问题的配置

OK，以上便是 Jekyll 的基本介绍，后续会详解每一部分的具体用法。

{% endraw %}