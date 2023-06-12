---
title: at规则
permalink: /tutorials/css/at-rules/
---

CSS 的 at 规则功能十分强大，有的可以引入（import）其它 CSS 文件，有的可以将 CSS 作用于特定媒体（media），有的可以加载字体（font）。

at 规则以 "@" 开头。

## 导入

`@import` 规则用法及其简单，它可以将其它 CSS 文件引入到当前文件中：

```css
@import url(morestyles.css);
```

如果 CSS 文件特别大，可以按照模块拆分成小文件，然后用 `@import` 整合到一个文件内。

> 注意，`@import` 规则必须位于文件最顶部，前面不可以出现其他 CSS 规则。

## 媒体

`@media` 用于指定特定媒体，比如打印设备：

```css
@media print {
    body {
        font-size: 10pt;
        font-family: times, serif;
    }

    #navigation {
        display: none;
    }
}
```

`@media` 规则可以后跟 `screen`, `print`, `projection`, `handheld` 以及 `all`，或者用逗号隔开的多个值：

```css
@media screen, projection {
    /* ... */
}
```

> CSS3 的 `@media` 功能更强，可以精确到屏幕尺寸。Media Queries 章节会介绍具体用法。

## 字体

`@font-face` 用于加载字体，特别适用于页面需要用到特殊字体的场景。

```css
@font-face {
    font-family: "font of all knowledge";
    src: url(fontofallknowledge.woff);
}
```

以上代码加载了名为 "fontofallknowledge.woff" 的字体文件，并通过 `font-family` 这个描述器（descriptor）将其命名为 "font of all knowledge"。

字体加载进来之后，可以像常规字体那样使用：

```css
p { 
    font-family: "font of all knowledge", arial, sans-serif; 
}
```

如果字体已经存在于本地，则无需加载，这个判断逻辑可以通过给 `src` 属性指定多个值来实现：

```css
@font-face {
    font-family: "font of all knowledge";
    src: local("font of all knowledge"), local(fontofallknowledge), url(fontofallknowledge.woff);
}
```

上面代码中 `src` 属性的取值是一个 list，`local` 用于加载本地字体，`url` 用于加载字体文件，如果 `local` 已经存在，`url` 就不会被执行。
