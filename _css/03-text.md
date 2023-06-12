有许多属性可以控制文本的大小和形状。

## font-family

`font-family` 表示字体，常见的西文字体有 Times New Roman，Arial 和 Verdana。

我们可以同时指定多个字体，比如 `font-family: arial, helvetica, serif`。

浏览器会按照字体定义的顺序去系统中做匹配，如果匹配不上会使用默认字体。

如果字体内包含空格，可以用引号包裹起来：`font-family: "Times New Roman"`。

## font-size

`font-size` 用于指定文本大小。

当然可以通过 `font-size` 修改 `<p>` 标签的字体大小来表示标题，但最好用专用的标题标签（如 `<h1>`，`<h2>`）。

## font-weight

`font-weight` 用于指定文本粗细。常见用法是 `font-weight: bold` 或者 `font-weight: normal`，不过也有其他值，比如 `bolder`，`lighter`，`100`，`200`，`300`，`400`（等价于 `normal`），`500`，`600`，`700`（等价于 `bold`），`800` 或 `900`。

> 注意，一些老的浏览器并不支持除 `bold` 和 `normal` 以外的值。

## font-style

`font-style` 用于指定是否斜体。`font-style: italic` 或者 `font-style: normal`。

## text-decoration

`text-decoration` 用于指定文本线条。

* `text-decoration: underline` - 下划线
* `text-decoration: overline` - 上划线
* `text-decoration: line-through` - 中划线

这个属性通常用来修饰链接，当然也可以指定没有线条：`text-decoration: none`。

## text-transform

`text-transform` 用于改变大小写。

* `text-transform: capitalize` - 首字母大写
* `text-transform: uppercase` - 全部大写
* `text-transform: lowercase` - 全部小写
* `text-transform: none` - 未指定

以上属性可以配合起来一起使用：

```css
body {
    font-family: arial, helvetica, sans-serif;
    font-size: 14px;
}

h1 {
    font-size: 2em;
}

h2 {
    font-size: 1.5em;
}

a {
    text-decoration: none;
}

strong {
    font-style: italic;
    text-transform: uppercase;
}
```

## 文本间距

![](https://htmldog.com/figures/spacingOutText.gif)

`letter-spacing` 和 `word-spacing` 分表表示字母间距和字间距。取值可以是数值或者 `normal`。

`line-height` 用于指定行高，但不会改变字体大小。如果取值为数值，表示几倍于字体大小，除此之外，还可以指定长度值、百分比或者 `normal`。

`text-align` 用于指定文本在元素内的对齐方式，取值有 `left`，`right`，`center` 和 `justify`。

`text-indent` 用于指定缩进，取值为长度或百分比。常用语印刷媒介，Web 这样的数字媒介很少用到。

```css
p {
    letter-spacing: 0.5em;
    word-spacing: 2em;
    line-height: 1.5;
    text-align: center;
}
```