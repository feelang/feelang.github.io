---
title: 总结
permalink: /tutorials/css/beginner-conclusion/
---

如果把前面 5 篇教程所提到的 HTML 选择器综合起来使用，就会的到如下 CSS 文件。

可以将他们应用到一个 HTML 文件中，看一下效果。

```css
body {
    font-family: arial, helvetica, sans-serif;
    font-size: 14px;
    color: black;
    background-color: #ffc;
    margin: 20px;
    padding: 0;
}

/* This is a comment, by the way */

p {
    line-height: 21px;
}

h1 {
    color: #ffc;
    background-color: #900;
    font-size: 2em;
    margin: 0;
    margin-bottom: 7px;
    padding: 4px;
    font-style: italic;
    text-align: center;
    letter-spacing: 0.5em;
    border-bottom-style: solid;
    border-bottom-width: 0.5em;
    border-bottom-color: #c00;
}

h2 {
    color: white;
    background-color: #090;
    font-size: 1.5em;
    margin: 0;
    padding: 2px;
    padding-left: 14px;
}

h3 {
    color: #999;
    font-size: 1.25em;
}

img {
    border-style: dashed;
    border-width: 2px;
    border-color: #ccc;
}

a {
    text-decoration: none;
}

strong {
    font-style: italic;
    text-transform: uppercase;
}

li {
    color: #900;
    font-style: italic;
}

table {
    background-color: #ccc;
}
```