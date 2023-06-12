---
title: HSL颜色
permalink: /tutorials/css/advanced-colors/
---

我们已经学习过三种定义 CSS 颜色的方式——名称、RGB 以及 16 进制值。

CSS3 又带来了另一种定义颜色的方式——HSL，三个字母分别表示色相（Hue）、饱和度（Saturation）和亮度（Lightness）。

HSL 和 RGBa ("a" 表示 "alpha" 值) 适用于任何表示颜色的属性，例如 `color`,`background-color`, `border-color` 和 `box-shadow`。

## Alpha 透明值

RGBa 可以为盒元素或者文本的设置透明值。比如，下面的代码通过设置透明值，就可以让背景图透过文本显示出来：

```css
h1 {
    padding: 50px;
    background-image: url(snazzy.jpg);
    color: rgba(0,0,0,0.8);
}
```

`rgba` 比 `rgb` 多了一个 `a`，用于设置透明度，"1" 表示完全不透明，"0" 表示完全透明。所以 `rgba(0,0,0,0.8)` 表示 80% 的黑色。

`rgba` 不仅适用于文本，也适用于盒元素，还适用于阴影。总结，任何适用 `rgb` 的地方都可以使用 `rgba`。

# 色相、饱和度、亮度

Web 世界的颜色绝大部分是由**红绿蓝**组合而来，形式可以是十六进制的数值，也可以是明确的 RGB 值（或者 RGBa）。

但是这种逻辑性的颜色表达方式，不符合人们的直觉，所以 CSS3 为我们带来了 HSL。

![](https://www.2020mag.com/CMSImagesContent/2014/9/Hue-Saturation-Brightness-pic.png)

它的用法和 `rgb` 非常相似：

```css
#smut { 
    color: hsl(36, 100%, 50%);
}
```

* 色相（Hue，上例中的 "36"）- 色轮的角度值，取值范围从 0 到 360，其中 "0" 和 "360" 表示红色，"120" 表示绿色，"240" 表示蓝色
* 饱和度（Saturation，上例中的 "100%"）- 颜色饱和度，取值范围从 0% 到 100%
* 亮度（Lightness，上例中的 "50%"）- 取值范围从 0%（黑色）到 100%（白色），50% 表示正常

上例代码的 HSL 值等价于十六进制值的 `#ff9900` (`#f90`)，以及 RGB 值的 `rgb(255, 153, 0)。

## HSLa

RGB 有对应的 RGBa，HSL 也有对应的 HSLa：

```css
#rabbit { 
    background: hsla(0, 75%, 75%, 0.5);
}
```

