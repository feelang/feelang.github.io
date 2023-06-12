---
title: 颜色
permalink: /tutorials/css/colors/
---

CSS 的颜色值有三种定义方法：
* 颜色名称
* RGB
* 16进制编码

例如，下面的 5 中方式都表示红色：

* `red`
* `rgb(255, 0, 0)`
* `rgb(100%, 0%, 0%)`
* `#ff0000`
* `#f00`

CSS 内置了一些颜色名称，比如 `aqua`，`black`，`blue`，`fuchsia`，`gray`，`green`，`lime`，`maroon`，`navy`，`olive`，`purpule`，`red`，`silver`，`teal`，`white`，`yellow` 以及 `transparent`。

> 注意，除了 `white` 和 `black`，其他颜色在网站设计中并不常用，每个一个设计精美的网站一般会定义自己的颜色组合。

RGB 有三个取值范围为 [0, 255] 的值，其中 0 表示最小值，255 表示最大值。这三个值也可以用百分比来表示。

16进制编码是一个用 16 进制表示的数值。它以 `#` 开头，支持六位和三位：
* 三位值有等价的六位值，例如 `#ff0000` 等于 `#f00`，`#cc9966` 等于 `#c96`
* 三位值更简洁一些，三个数值分别代表 RGB
* 六位精度更高，比如 `#fc3846` 就无法用三位值来表达

> CSS3 还支持 HSL 颜色，后面高阶教程中会详细讲解

## 颜色和背景色

颜色有两种，`color` 和 `background-color`。

例如，一个黄底蓝字的 `<h1>` 标题：

```css
h1 {
    color: yellow;
    background-color: blue;
}
```

这个颜色可能有些刺眼，我们可以用 16 进制色值稍作调整：

```css
body {
    font-size: 14px;
    color: navy;
}

h1 {
    color: #ffc;
    background-color: #009;
}
```

`color` 和 `background-color` 可作用于大部分 HTML 元素，如果作用于 `body` 之上，会修改页面内的所有颜色。