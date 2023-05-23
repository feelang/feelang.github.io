---
title: 安装
excerpt: Jekyll 安装步骤
lesson: 1
---

{% raw %}

## Jekyll 简介

Jekyll 是一个静态网站生成器（static site generator），它是 [Github
Pages](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-
jekyll) 推荐的建站工具，支持 Markdown 和 HTML 两种文件类型，其中 HTML 使用了 **Liquid** 模板语言。

所谓模板语言，是一种文本处理工具，它可以让我们更高效地生成 HTML 文件，Spring 框架的 `thymeleaf`、Django 自有的
template language 等等，都属于此类，它们的语法大同小异，用法相差无几，Jekyll 之所以使用 Liquid，估计是因为它们都由 Ruby
写成。

Ruby 是一个比较老的语言，当年有个 Web 框架叫 Ruby on Rails
着实火了一阵，不过最近几年几乎看不到身影了，说明人气已经大不如前，不过这并不会影响到 Jekyll 的易用性，因为 Jekyll 本身是一个
[Gem](https://rubygems.org/gems/jekyll)，类似于 Nodejs 的 package，安装使用非常简单，即使完全不懂
Ruby 也照样搞的定。

## 安装依赖包

  * [`Ruby`](https://www.ruby-lang.org/en/downloads/)（版本不能低于 2.4.0，可通过 `ruby -v` 查看安装情况）
  * [`RubyGems`](https://rubygems.org/pages/download)（通过 `gem -v` 查看安装情况）
  * [`GCC`](https://gcc.gnu.org/install/)（通过 `gcc -v` 或者 `g++ -v` 查看安装情况）
  * [`Make`](https://www.gnu.org/software/make/)（通过 `make -v` 查看安装情况）

在 Mac 和 Linux 系统，这些依赖包的安装都非常简单，这里不再赘述，Windows
也不复杂，[官方文档](https://jekyllrb.com/docs/installation/#requirements)都有详细的步骤，照着做就可以了。

等以上依赖包都安装完成之后，就可以安装 Jekyll 了。

## 安装 Jekyll

一行命令即可搞定，非常简单：

    
    
    gem install jekyll bunder
    

等待安装完成，检查一下：

    
    
    jekyll -v
    

没有问题，恭喜安装成功。

是不是非常简单？

下一篇将介绍如何利用 Jekyll 快速创建一个网站。

{% endraw %}