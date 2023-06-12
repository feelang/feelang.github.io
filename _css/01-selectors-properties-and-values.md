---
title: HTML选择器
permalink: /tutorials/css/selectors-properties-and-values/
---

HTML 有标签（tags），而 CSS 有选择器（selectors）。

选择器是样式的名字，只能定义在在内部和外部样式表（style sheets）中。

在 [CSS 入门篇](https://blog.csdn.net/feelang/category_12029701.html)的专栏中，我们只会用到 HTML 选择器。

所谓 HTML 选择器等同于 HTML 的标签名称，它会作用于特定类型的标签。

每个选择器都有属性（properties），位于一个大括号内，属性的明明十分简单，比如 `color`、`font-weight` 或者 `background-color`。

每个属性都有一个值（value），两者用冒号隔开，不同属性用分号分割。

```css
body {
    font-size: 14px;
    color: navy;
}
```

以上代码定义了一个 HTML 选择器——`body`，它含有两个属性 `font-size` 和 `color`，值分别是 `14px` 和 `navy`。

基本上，当 `body` 作用于 HTML 文档时， `<body>` 标签间的文本（也就是整个窗口的内容）将是14像素大小，海军色。

## 长度与百分比

CSS 提供了许多属性特点单位，但也提供了很多通用单位，比如：

* `px`（用法：`font-size: 12px`）表示像素单位
* `em`（用法：`font-size: 2em`）是字体大小的单位。例如，`2em` 就表示当前字体的两倍。
* `pt`（用法：`font-size: 12pt`）表示点（point），是一个常用语印刷媒介的物理单位。
* `%`（用法：`width: 18px`）表示百分比。

其它单位还有 `pc`（活字，picas）、`cm`（厘米，centimeters）、`mm`（毫米，millimeters）和 `in`（英寸，inches），但并不常用。

当值为 0 时，不需要指明单位。例如，`border: 0` 就表示没有边框。

