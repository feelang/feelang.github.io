在 CSS 基础教程中，我们学会了如何使用 HTML 选择器。

这一篇我们继续讲解另外两种选择器 - **class** 和 **ID**。

有了它们，我们就可以为同一种标签指定不同的样式。

CSS 的类选择器名称以 `.` 开头，ID 选择器以 `#` 开头。

所以 CSS 文件可以写成下面这样：

```css
#top {
    background-color: #ccc;
    padding: 20px
}

.intro {
    color: red;
    font-weight: bold;
}
```

在 HTML 中使用时，可以像下面这样：

```html
<div id="top">

<h1>Chocolate curry</h1>

<p class="intro">This is my recipe for making curry purely with chocolate</p>

<p class="intro">Mmm mm mmmmm</p>

</div>
```

ID 选择器和类选择器的不同之处在于，ID 作用于某个元素，而类（class）作用于某类元素。

选择器还可以只作用于特点元素，比如 `p.jam { /* whatever */ }` 将只作用于 class 为 `jam` 的 `<p>` 元素。