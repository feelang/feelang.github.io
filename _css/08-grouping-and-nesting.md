分组和嵌套可以让代码更易于维护，无论是 HTML 代码还是 CSS 代码。

## 分组

分组的写法可以让我们同时为多个元素定义相同的属性。

例如，我们可以利用分组简化下面这段代码：

```css
h2 {
    color: red;
}

.thisOtherClass {
    color: red;
}

.yetAnotherClass {
    color: red;
}
```

分组后：

```css
h2, .thisOtherClass, .yetAnotherClass {
    color: red;
}
```

## 嵌套

一个结构良好的 CSS 文件，不会出现太多的类和 ID 选择器，因为我们可以在选择器内嵌套定义选择器：

```css
#top {
    background-color: #ccc;
    padding: 1em
}

#top h1 {
    color: #ff0;
}

#top p {
    color: red;
    font-weight: bold;
}
```

这样写可以无需指定 `<p>` 和 `<h>` 的样式，只要它们的父级元素有 `#top` 这个 ID 选择器。

```css
<div id="top">
    <h1>Chocolate curry</h1>
    <p>This is my recipe for making curry purely with chocolate</p>
    <p>Mmm mm mmmmm</p>
</div>
```

