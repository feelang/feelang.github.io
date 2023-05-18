---
layout: post
title: Gulp 和 Webpack 有什么区别？
date: 2022-10-14
categories: frontend
---

我在深入学习 Sass 时了解到 Gulp 是一个 task runner，随即产生一个疑问：Webpack 是什么呢，它和 Gulp 的区别是什么？

简单来说，Webpack 是一个模块打包器（module bundler），而 Gulp 是一个任务执行器（task runner），两者有本质区别，功能也没有冲突，可以一起使用。只不过 Webpack 功能过于强大，很多开发者逐渐用 Webpack 替代了 Gulp。


## Gulp

Gulp 是一个流式构建工具（streaming build system），可以自动化执行多个任务。也就是说，我们可以把一些重复性、确定性的任务交给 gulp 去做。

这些任务包括压缩 CSS 或 JS 代码，转义 SASS 或者 LESS 文件，将 SVG 图标转换为字体文件，监听文件变化，等等。

有了 Gulp，这些任务就能被自动化掉。

## Webpack

Webpack 是一个 js 的模块打包工具（module bundler），它可以将模块以及模块的依赖整合成静态产物（static assets）。

既然如此，Webpack 完全可以和 Gulp 配合使用。

但是，随着 js 生态的发展，module bundler 和 task runner 之间的界限越来越模糊，而 Webpack 基于插件（plugin）功能实现了高度可扩展性，很快，开源社区就为 webpack 实现了任务管理（task management）的功能，这个原本不属于它功能范畴的新特性。

随着 Webpack 生态的日益繁荣，Gulp 便慢慢淡出了人们的视野。

简单来说，Webpack 的作用对象是带依赖的模块，而 PNG 文件，Sass 或 CSS 脚本，以及其它图片和媒体文件都是「模块」的具体形式，所以 Webpack 可以将他们整合成内聚的静态产物用于部署。


## 参考文章
* https://buddy.works/tutorials/gulp-js-and-webpack-which-one-to-use-and-when
* https://forestry.io/blog/gulp-and-webpack-best-of-both-worlds/
* https://www.keycdn.com/blog/gulp-vs-grunt
