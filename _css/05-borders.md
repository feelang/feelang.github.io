---
title: 边框
permalink: /tutorials/css/borders/
---

如果要给元素添加边框，一个 `border-style` 即可搞定。

它的取值有 `solid`，`dotted`，`dashed`，`double`，`groove`，`ridge`，`insect` 和 `outsect`。

![](/assets/images/css/border-style.png)

`border-width` 用于指定边框粗细，常用会用像素值。

针对元素的四个边，`border-width` 也有对应的属性：

* `border-top-width`
* `border-right-width`
* `border-bottom-width`
* `border-left-width`

`border-color` 用于指定边框颜色。

以上属性可以组合在一起使用：

```css
h2 {
    border-style: dashed;
    border-width: 3px;
    border-left-width: 10px;
    border-right-width: 10px;
    border-color: red;
}
```

