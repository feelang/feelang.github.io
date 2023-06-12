---
title: 背景图
permalink: /tutorials/css/background-images/
---

我们知道，html 有一个 `<img>` 标签，可以用来展示图片，提高页面的丰富度。

CSS 的背景图片也有这个功能，但用法却截然不同。

```css
body {
    background: white url(https://res.cloudinary.com/hefengcloud-com/image/upload/v1661790942/westlake/ping-hu-qiu-yue_g0brov.png) no-repeat top right;
}
```

上一篇我们介绍了属性的简写，这里的 `background` 也是简写，它可以拆解成：

* `background-color` - 背景颜色
* `background-image` - 图片路径
* `background-repeat` - 图片的重复方式，取值包含：
    * `repeat`
    * `repeat-y`
    * `repeat-x`
    * `no-repeat`
* `background-position` - 取值比较灵活，可以是 `top`，`center`，`bottom`，`left`，也可以是长度值或者百分比，或者任何有意义的组合，比如 `top right`。

已上属性是最常用的，也是最基本的，除此之外还有其他更高级的用法：

* `background-attachment`
* `background-clip`
* `background-origin`
* `background-size`


> `background` 属性可应用于绝大部分 HTML 元素，除了最常用的 `<body>`，还可以用于列表元素，甚至搜索框内展示图标也可以借此实现。
