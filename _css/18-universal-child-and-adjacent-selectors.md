---
title: 更多选择器
permalink: /tutorials/css/universal-child-and-adjacent-selectors/
---

前面我们学习过 HTML 选择器，类选择器和 ID 选择器，这几种选择器配合起来使用可以让我们精确定位 HTML 元素。本篇要介绍的几个功能更加强大。

## 全局选择器

全局选择器用一个星号（`*`）来表示，它会作用于**所有元素**。全局选择器除了可以为页面设置全局样式之外，还可以配合其他选择器一起使用。

```css
* {
    margin: 0;
    padding: 0;
}

#contact * {
    display: block;
}
```

* 单独使用全局选择性相当于重置了浏览器的默认样式
* 跟在其他选择器后面使用，只会作用于该选择器的子元素

## 子选择器

大于号（`>`）用于指定一级子元素。

```html
<ul id="genus_examples">
    <li>Cats
        <ul>
            <li>Panthera</li>
            <li>Felis</li>
            <li>Neofelis</li>
        </ul>
    </li>
    <li>Apes
        <ul>
            <li>Pongo</li>
            <li>Pan</li>
            <li>Homo</li>
        </ul>
    </li>
</ul>
```

如果要给`<ul id="geneus_examples">` 的一级子元素（`<li>` 标签） "Cats" 和 "Apes" 设置样式，CSS 可以这样写：

```css
#genus_examples > li { 
    border: 1px solid red; 
}
```

其他的 `<li>` 元素不会收到影响，因为子选择器只作用于一级子元素。

如果要作用于所有子元素，可以这么写：

```css
#genus_examples  li { 
    border: 1px solid red;
}
```

## 邻接选择器

加号（`+`）表示邻接选择器，只作用于第一个邻近的节点。

```html
<h1>Clouded leopards</h1>
<p>Clouded leopards are cats that belong to the genus Neofelis.</p>
<p>There are two extant species: Neofelis nebulosa and Neofelis diardi.</p>
```

下面的 CSS 只会让第一个 `<p>` 的字体变为粗体：

```css
h1 + p { 
    font-weight: bold; 
}
```

如果要作用于所有的兄弟节点，可以使用 CSS3 新提供的兄弟选择器（`~`）：

```css
h1 ~ p { 
    font-weight: bold; 
}
```