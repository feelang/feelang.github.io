---
title: 变换
permalink: /tutorials/css/transformations/
---

本篇要介绍的属性是 `transform`，它可以将 CSS 的盒子变换成另外的形状。

我们知道，CSS 的盒子是方形的，从几何变换的角度来看，`transform` 要做的是改变盒子在 x 轴和 y 轴上的坐标。

它提供了四种变换方式：
* `rotate` - 旋转
* `skew` - 倾斜
* `scale` - 缩放
* `translat` - 平移

![](/assets/images/css/transform.png)

## 旋转

```css
.note {
    width: 300px;
    height: 300px;
    background: hsl(36,100%,50%);
    transform: rotate(-10deg);
}
```

`transform: rotate(-10deg)` 会将 `.note` 作用的盒子（box）逆时针旋转 10 度。

## 倾斜

```css
transform: skew(20deg,10deg);
```

`skew` 有两个参数，分表表示 x 坐标和 y 坐标上的变形角度。

当然，也可以只指定一个参数，例如 `skew(20deg)`，它等价于 `skew(20deg,0)`。

## 缩放

改变宽度值或高度值也可以实现盒子的缩放，但要让盒子的内容也跟着缩放，就只能用 `scale` 来做。

```css
transform: scale(2);
```

`scale(2)` 表示盒子会在 x 轴和 y 轴上放大 2 倍。参数小于 1 表示缩小，比如 `scale(0.5)`。

当然也可以分开指定 x 轴和 y 轴上的缩放比例：

```css
transform: scale(1,2);
```

x 轴上不变，y 轴上放大两倍。

## 平移

`translate` 可以实现盒子的平移。

```css
transform: translate(100px,200px);
```

上例代码会让盒子在 x 轴上平移 100px，y 轴上平移 200px。

> 以上所有变换函数，都可以针对 x 轴和 y 轴分别操作：
> * `skewX`
> * `skewY`
> * `scaleX`
> * `scaleY`
> * `translateX`
> * `translateY`

## 组合变换

以上变换可以组合起来使用：

```css
transform: rotate(-10deg) scale(2);
```

> 以上变换会按照值的定义顺序进行，先逆时针旋转 10 读，再放大 2 倍。

除了以上方式，CSS 还提供了矩阵变换：

```css
transform: matrix(2,-0.35,0.35,2,0,0);
```

> 理解矩阵变换需要一定的数学知识。

## 原点

以上变换都是围绕盒子的中心位置进行的。`transform-origin` 可以改变变换的坐标原点。

![](/assets/images/css/transform-origin.png)

`transforma-origin` 的取值可以坐标值：

```css
transform-origin: 0 0;
```

也可以是语义字符串：`center`, `top`, `right`, `bottom`, `left`，还可以是百分比。

---

以上变换都是基于二位坐标系，`transform` 还支持三维坐标系变换：

* `translate3d`
* `scale3d`
* `matrix3d`