---
title: 圆角
permalink: /tutorials/css/rounded-corners/
---

圆角会让生硬的背景图变得更圆润，可以起到很好的修饰效果。

## 边框半径

`border-radius` 属性可以让盒元素的四个角变成圆角，这个属性名有点误导性，其实没有边框依然可以变圆角。

```css
#marilyn {
    background: #fff;
    width: 100px;
    height: 100px;
    border-radius: 20px;
}
```

<img src="/assets/images/css/border-radius.png" width="200"/>

有边框，也可以加圆角：

```css
#ok_a_border_then {
    border: 5px solid #8b2;
    width: 100px;
    height: 100px;
    border-radius: 5px;
}
```

## 多个值

四个角还可以分别指定：

* `border-top-left-radius`
* `border-top-right-radius`
* `border-bottom-right-radius`
* `border-bottom-left-radius`

不过，这么长的名字显得很臃肿，我们可以使用简写：

```css
#monroe {
    background: #fff;
    width: 100px;
    height: 100px;
    border-radius: 6px 12px 18px 24px;
}
```

`border-raiuds` 的四个值从左上角开始，按照顺时针方向，分别作用于左上、右上、右下、左下。

<img src="/assets/images/css/border-radius_multiple.png" width="200"/>

如果 `border-radius` 只有两个值，那么第一个值作用于左上↖和右下↘，第二只作用于右上↗和左下↙；如果是三个值，那分别作用于左上、右上和左下、右下。

## 椭圆

其实 `border-radius` 一共有 8 个值，因为每个角的半径又分为水平半径和垂直半径。

![](https://i.stack.imgur.com/FnIqF.png)

这两个值可用 `/` 分割：

```css
#nanoo {
    background: #fff;
    width: 100px;
    height: 150px;
    border-radius: 50px/100px;
    border-bottom-left-radius: 50px;
    border-bottom-right-radius: 50px;
}
```

<img src="/assets/images/css/border-radius_nanoo.png" width="200"/>