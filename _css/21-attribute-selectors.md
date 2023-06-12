属性选择器可以定位到拥有某个属性的元素，甚至可以精确到具体的属性值。

## 属性匹配

选择器后面跟一个大括号，大括号内是属性名：

```css
abbr[title] { 
    border-bottom: 1px dotted #ccc;
}
```

上述代码的含义是：为有 title 属性的 abbr 标签添加一条灰色的下划线。

## 属性值匹配

用法与上面类似，只不过还可以进一步指定属性值：

```css
input[type=text] { 
    width: 200px; 
}
```

上述代码只会作用于 "type" 属性值为 "text" 的 "input" 标签：`<input type="text">`。

除此之外，还可以同时指定多个属性：

```css
input[type=text][disabled] { 
    border: 1px solid #ccc;
} 
```

## 属性模糊匹配

CSS3 进一步扩展了属性选择器的用法：
- `[attribute^=something]` - 配合以 "something" 开头的属性
- `[attribute$=something]` - 配合以 "something" 结尾的属性
- `[attribute*=something]` - 配合含有 "something" 属性

举个例子，下面代码可以让外部链接（以 "http" 开头）的样式区别于内部链接：

```css
a[href^=http] {
    padding-right: 10px;
    background: url(arrow.png) right no-repeat;
}
```
