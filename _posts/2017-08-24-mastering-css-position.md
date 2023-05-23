---
layout: single
title: 精通 CSS 之 position
date: 2017-08-24 08:42:17
categories: CSS
---

HTML的“正常”布局称为 __document flow__，在这种 normal flow 下，元素按照从左到右（`inline block`）、从上到下（`block`）进行排列。

`position` 则打破了 normal flow。

我们把元素的父节点（ancestor）称为 __containing block__。

`position`有五个取值：

- `static`
- `absolute`
- `fixed`
- `relative`
- `sticky`

同时有四个属性依附于`position`，它们表示距离边界（edge of contaning block）的 offset，因为我们称之为 __offset properties__。

- `top`
- `bottom`
- `right`
- `left`

## static

`static` 是默认值，标记了 `position: static` 的元素依然会遵守 __document flow__，因此 __offset properties__ 不起作用。

例如，下面的 `top`、`left` 毫无作用。

```css
div.dlg {
  position: static;
  top: 20px;
  left: 10px;
}
```

## absolute

`absolute` 是相对于它的 __containing block__，但是 __containing block__ 必须有 `position` 修饰，**并且 `position` 的取值不能是 `static`**，兜底的 __contaning block__ 是`body`。

`absolute` 会让元素脱离 __document flow__，并且不会保留它原本在 __normal flow__ 里的 gap。

## fixed

`fixed` 与 `absolute` 非常类似，不过它的 __containing block__ 是 __view port__，也就是说，`absolute` 的元素会固定在可见区域的某个位置，无论页面如何滚动，它的位置不会改变。

## relative

`relative`的“相对”是相对于 __normal flow__，__offset properties__ 作用于它原本在 __normal flow__ 下的位置。

`relative` 并没有脱离 __document flow__，只会在原有位置的基础上有了 __offset__，因此它会在原本的位置上留下 gap。

## sticky

`sticky` 表示在滑动之后将元素固定于某个位置，它的 __containing block__ 必须用 `overflow: scroll` 来修饰。

```css
#scrollbox {
  overflow: scroll; 
  width: 15em; 
  height: 18em;
}

#scrollbox h2 {
  position: sticky; 
  top: 2em; 
  bottom: auto;
  left: auto; 
  right: auto;
}
```

**参照資料**

* [CSS Layout - The position Property](https://www.w3schools.com/css/css_positioning.asp)
* O'REILLY - Positioning in CSS 
