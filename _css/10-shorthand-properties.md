有些情况下，多个 CSS 属性值可以整合成一串值，每个值之间用空格分隔。

## 边距

`margin` 属性可以将 `margin-top`，`margin-right`，`margin-bottom` 和 `margin-left` 整合成一条属性：`property: top right bottom left'`。

```css
p {
    margin-top: 1px;
    margin-right: 5px;
    margin-bottom: 10px;
    margin-left: 20px;
}
```

可以整合成：

```css
p {
    margin: 1px 5px 10px 20px;
}
```

`padding` 也一样。

如果它们的属性值只有两个（比如 `padding: 1em 10em;`），那么第一个值表示**头部和底部**，第二只表示**左边和右边**。

## 边框

`border-width` 也有同样的用法。可以将 `border-width`，`border-color` 和 `border-style` 整合成一个 `border` 属性。

比如，下面这段代码：
```css
p {
    border-width: 1px;
    border-color: red;
    border-style: solid;
}
```

可以简化为：

```css
p {
    border: 1px red solid;
}
```

> 上面代码，宽度/颜色/样式的组合也可以作用于 `border-top` 和 `border-right` 等。

## 字体

字体相关的属性也可以聚合成一条：

```css
p {
    font: italic bold 12px/2 courier;
}
```

`font` 属性的四个取值分别代表 `font-style`、`font-weight`、`font-size`、`line-height` 和 `font-family`。

以上属性全部结合起来一起用：

```css
p {
    font: 14px/1.5 "Times New Roman", times, serif;
    padding: 30px 10px;
    border: 1px black solid;
    border-width: 1px 5px 5px 1px;
    border-color: red green blue yellow;
    margin: 10px 50px;
}
```