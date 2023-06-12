伪类（pseudo classes）要和选择器捆绑使用，用于表示某种状态（state）或关系（relation）。

它的形式如下，选择器后面跟了一个冒号和伪类：

```
selector:pseudo_class {
    property: value;
}
```

## 链接

`:link` 表示未访问过的链接，`:visited` 表示访问过的链接。

下面的代码根据链接是否访问过来指定不同颜色：

```css
a:link {
    color: blue;
}

a:visited {
    color: purple;
}
```

## 动态伪类

动态伪类用于动态改变选择器的属性值。

* `:active` - 激活状态，比如用户链接被点击
* `:hover` - 悬浮状态，比如光标划过一个链接
* `:focus` - 获取焦点状态，比如选中，或者等待键盘输入

> `focus` 常用于**表单元素**，但也会用于**链接**，因为有的用户可能不用鼠标，而是使用键盘配合 tag 来切换焦点。

```css
a:active {
    color: red;
}

a:hover {
    text-decoration: none;
    color: blue;
    background-color: yellow;
}

input:focus, textarea:focus {
    background: #eee;
}
```

## 第一个子节点

`:first-child` 用于精确指定第一个子节点。

```html
<body>
    <p>I’m the body’s first paragraph child. I rule. Obey me.</p>
    <p>I resent you.</p>
...
```

如果我们只想改变第一个 `<p>` 标签的样式，就可以像下面这样定义 CSS：

```css
p:first-child {
    font-weight: bold;
    font-size: 40px;
}
```

> CSS3 提供了更多的伪类，比如 `last-child`，`target` 以及 `first-of-type` 等等。