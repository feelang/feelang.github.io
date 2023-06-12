我们已经知道，[`@media` 规则](https://blog.csdn.net/FeeLang/article/details/127159059)用于指定特定的媒介，比如 screen, print。

本篇要介绍的特性在指定媒介的基础上更进一步，可以精确到屏幕尺寸。

这也是响应式 (responsive) 布局的基础，一个页面可以同时适配手机和平板，页面布局随浏览器尺寸的变化而变化。

首先，简单回顾一下 `@media` 用法：

```css
@media screen {
    body { font: 12px arial, sans-serif }
    #nav { display: block }
}
```

以上 CSS 样式仅仅指定了媒体类型，没有指定规格。

CSS3 增强了 `@media` 的功能，使它拥有了更加精细的控制能力。

## 特定尺寸

```css
@media screen and (max-width: 1000px) {
    #content { width: 100% }
}
```

上例代码的样式只有当 **viewport** 的宽度小于等于 1000px 时才会发生作用。

借助这一功能，我们可以轻松实现响应式设计，例如当 viewport 小于某个值时，不显示导航栏。

多个尺寸规则可以组合起来使用：

```css
@media screen and (max-width: 1000px) {
    #content { width: 100% }
}

@media screen and (max-width: 800px) {
    #nav { float: none }
}

@media screen and (max-width: 600px) {
    #content aside {
        float: none;
        display: block;
    }
}
```

上例代码中，如果 **viewport** 宽度小于 600px，所有样式都会起作用，如果 **viewport** 小于 800px 大于 600px，那么只有第一条和第二条会起作用。

与 `max-width` 相对应的，也可以指定 `min-width`。

## 特定方向

```css
@media screen and (orientation: landscape) {
    #nav { float: left }
}

@media screen and (orientation: portrait) {
    #nav { float: none }
}
```

`orientation` 用于指定屏幕方向。移动设备上很有用。

## 特定设备

这里的特定设备并非指设备品牌或类型，而是指它的物理属性。

### 宽度和高度

* `device-width`
* `device-height`
* `min-device-width`
* `max-device-width`
* `min-device-height`
* `max-device-height`

```css
@media screen and (min-device-height: 768px) and (max-device-width: 1024px) {
    /* You can apply numerous conditions separated by "and" */
}
```

### 像素比

CSS 的像素不一定等价于物理像素，理解这一点非常重要。

比如，一个物理宽度为 720px 的显示设备，浏览器可能会按照 480px 的逻辑像素来处理 CSS，**像素比**为 1.5:1，也就是说，1.5 个物流像素值对应 1 个 CSS像素值。

通过 `@media` 的 `@device-pixel-ratio` 可以指定比例：

```css
@media (device-pixel-ratio: 2) {

    body { background: url(twiceasbig.png) }

}
```

当然，还可以指定最大和最小值：

* `min-device-pixel-ratio`
* `max-device-pixel-ratio`


### 其他

指定设备分辨率：

```css
@media screen and (resolution: 326dpi) { /* */ }

@media screen and (min-resolution: 96dpi) { /* */ }
```

指定设备长宽比：

```css
@media screen and (device-aspect-ratio: 16/9) { /* */ }
```