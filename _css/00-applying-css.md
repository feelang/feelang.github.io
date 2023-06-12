---
title: 应用方式
permalink: /tutorials/css/applying-css/
---

有三种方式可以将 CSS 作用于 HTML：
* 内联（inline）
* 内部（internal）
* 外部（outernal）

## 内联

内联的方式最简单，但也最难以维护，因为它直接通过 `style` 属性内嵌于 html 的标签之上。

例如：

```html
<p style="color: red">text</p>
```

这段代码会让段落内的文本颜色变为红色。

虽然这种写法简单粗暴，但将 CSS 文件和 HTML 文件进行隔离的方式才是最佳实践。

## 内部

```html
<!DOCTYPE html>
<html>
<head>
<title>CSS Example</title>
<style>

    p {
        color: red;
    }

    a {
        color: blue;
    }

</style>
...
```

嵌入，或者说内部样式会作用于整个页面。它位于 `head` 标签内，用 `style` 包裹起来。

## 外部

外部样式可以作用于所有网站，要用到一个额外的文件，用于存放 css 内容。

```css
p {
    color: red;
}

a {
    color: blue;
}
```

然后在 html 文件的 `<head>` 标签中定义一个 `<link>` 标签：

```html
<!DOCTYPE html>
<html>
<head>
    <title>CSS Example</title>
    <link rel="stylesheet" href="style.css">
...
```

> 注意，这里的 `style.css` 文件和当前文件夹处在同一文件夹下，否则要需要修改文件路径。

