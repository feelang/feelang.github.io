---
title: 渐变
permalink: /tutorials/css/gradients/
---

配合 `background` 和 `background-image` 可以实现线性（linear）和辐射（radial）渐变。

## 线性渐变

`linear-gradient` 可以实现线性渐变。

```css
background: linear-gradient(yellow, red);
```

上例代码表示颜色从 "yellow" 渐变到 "red"。

![](/assets/images/css/linearGradient.png)

还可以指定渐变方向：

```css
background: linear-gradient(to right, orange, red);
```

"to right" 表示向右渐变。

```css
background: linear-gradient(to bottom right, orange, red);
```

"to bottom right" 表示向右下角渐变。

```css
background: linear-gradient(20deg, orange, red);
```

"20deg" 表示向 20 度角的方向渐变。

上例代码只指定了两个颜色，但多个颜色也没问题：

```css
background: linear-gradient(hsl(0,100%,50%),hsl(60,100%,50%),hsl(120,100%,50%),hsl(180,100%,50%),hsl(240,100%,50%),hsl(300,100%,50%));
```

![](/assets/images/css/linearGradient2.png)

## 辐射渐变

辐射渐变和线性渐变的道理是一样的，只不过它的渐变方向是从中心往四周辐射。

```css
background: radial-gradient(yellow, green);
```

![](/assets/images/css/radialGradient.png)

当然也可以指定颜色辐射的形状：

```css
background: radial-gradient(circle, yellow, green);
```

![](/assets/images/css/radialGradient2.png)


还可以指定辐射方向：

* closest-side - 最近边
* closest-corner - 最近角
* farthest-side - 最远边
* farthest-corner - 最远角

```css
background: radial-gradient(circle closest-side, yellow, green);
```

以及辐射原点：

```css
background: radial-gradient(at top left, yellow, green);
```

## Color stops

如果把渐变方向看做一条直线，那 color stops 就是上面的点，如果我们给点指定颜色，那点与点之间的区域便是渐变发生的地方。

* `linear-gradient(black 0, white 100%)` - 等价于 `gradient(black, white)`
* `radial-gradient(#06c 0, #fc0 50%, #039 100%)` - 等价于 `radial-gradient(#06c, #fc0, #039)`
* `linear-gradient(red 0%, green 33.3%, blue 66.7%, black 100%)` - 等价于 `linear-gradient(red, green, blue, black)`

可以看出，如果没有指定 color stops，那么点在线上的位置是一个等差数列。

我们打破这个「均分」，随意定义数列：

```css
background: linear-gradient(135deg, hsl(36,100%,50%) 10%, hsl(72,100%,50%) 60%, white 90%);
```

![](/assets/images/css/linearGradient3.png)

## 重复渐变

`repeating-linear-gradient` 和 `repeating-radial-gradient` 可以实现重复渐变：

```css
background: repeating-linear-gradient(white, black 15px, white 30px);
```

> 如果颜色后面不跟数值，默认取值 0，表示起点。

![](/assets/images/css/repeatingGradient.png)

```css
background: repeating-radial-gradient(black, black 15px, white 15px, white 30px);
```

![](/assets/images/css/repeatingGradient2.png)
