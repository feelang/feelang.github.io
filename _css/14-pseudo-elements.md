伪元素（pseudo elements）和伪类（pseudo classes）非常相像，都是依附在选择器上使用 `selector:pseudoelement { property: value; }`。

## 首字母 & 首行

`first-letter` 作用于盒模型元素的第一个字母，`first-line` 作用于最顶部的一行。

![](https://htmldog.com/figures/firstLetterFirstLine.png)

```css
p {
    font-size: 12px;
}

p:first-letter {
    font-size: 24px;
    float: left;
}

p:first-line {
    font-weight: bold;
}
```

> CSS3 建议用两个冒号表示表示伪元素 `p::first-line`，目的是区分伪类，不过最佳实践还是用一个冒号 `p:first-line`，因为是要兼容老浏览器。

## 前后内容

`before` 和 `after` 这两个伪元素配合 `content` 属性一起使用，可以在元素前后添加内容而无需改动 HTML 代码。

`content` 的属性可以是 `open-quote`、`close-quote`，也可以是任何引号引起来的**字符串**，或者是用 `url(iamgename)` 表示的**图片**。

```css
blockquote:before {
    content: open-quote;
}

blockquote:after {
    content: close-quote;
}

li:before {
    content: "POW! ";
}

p:before {
    content: url(images/jam.jpg);
}
```

`content` 属性其实是在 HTML 代码中加了一个 box，所以我们可以给它添加样式：

```css
li:before {
    content: "POW! ";
    background: red;
    color: #fc0;
}
```