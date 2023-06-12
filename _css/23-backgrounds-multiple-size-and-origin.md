---
title: 多背景&背景原点
permalink: /tutorials/css/backgrounds-multiple-size-and-origin/
---

CSS 提供了很多处理背景的手段。

## 多背景

`background-image` 可以同时设置多个背景图片：

```css
background-image: url(this.jpg), url(that.gif), url(theother.png);
```

效果如下：

![](https://htmldog.com/guides/css/advanced/backgrounds/)

`background` 同样支持这种操作：

```css
background: url(bg.png), url(bullet.png) 0 50% no-repeat, url(arrow.png) right no-repeat;
```

以下与背景相关的属性都支持同时设定多个规则：

* `background-image`
* `background-position`
* `background-repeat`
* `background-attachment`
* `background`

## 背景大小

`background-size` 允许我们拉伸或者压缩一张背景图。

![](/assets/images/css/background-size.jpg)

它的取值包括：
* `auto` - 自适应
* 数值 - 如 `100px 50px`，表示宽为 100px，高为 50px。如果只有一个值，如 `100px`，就等价于 `100px auto`
* 百分比 - 如 `50% 25%`，表示宽度为背景区域的 50%，高度为 25%。如果只有一个值，如 `50%`，就等价于 `50% auto`
* 组合值 - `auto`、数值和百分比可以组合起来使用，比如 `80px auto`，表示宽度 80px，高度自适应，保持长宽比
* `contain` - 不超出背景区域，保持原有长宽比
* `cover` - 完全覆盖背景区域，保持原有长宽比

## 背景原点

![CSS 盒模型](images/box-model.png)

`background-origin` 用于指定在背景图在盒模型内的坐标系原点：

比如，下面这段 CSS，坐标值是 "0 0"：
```css
#burrito {
    width: 400px;
    height: 200px;
    border: 10px solid rgba(0,255,0,.5);
    padding: 20px;
    background: url(chilli.png) 0 0 no-repeat;
}
```

如果如果没指明 `background-origin`，默认值为 `padding-box`。其他取值还有 `border-box` 和 `content-box`。
