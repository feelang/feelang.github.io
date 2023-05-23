---
layout: single
title: Sass 和 Less 的用法和比较
date: 2018-1-25
categories: CSS
---

[Sass](http://sass-lang.com/) 和 [Less](http://lesscss.org/) 是两种 CSS 预处理器，扩展了 CSS 语法，目的都是为了让 CSS 更容易维护。

## Sass
Sass 有两种语法，最常用是的 `SCSS`（Sassy CSS），是 CSS3 的超集。另一个语法是 SASS（老的，缩进语法，类 Python）。

Sass 的预处理器工具是 sass：

```bash
# 单个文件
sass input.sass output.css

# 监控
sass --watch input.sass output.css

# 监控目录
sass --watch app/sass:public/stylesheets
```

Sass 扩展了 css 的特性：

* 变量
* 嵌套
* 混合（mixin）
* 继承

### 变量

```SCSS
$font-stack:        Helvetica, sans-serif;
$primary-color:     #333;

body {
    font: 100% $font-stack;
    color: $primary-color;
}
```

### 嵌套

```SCSS
nav {
    ul {
        margin: 0;
        padding: 0;
        list-style: none;
    }

    li { display: inline-block; }

    a {
        display: block;
        padding: 6px 12px;
        text-decoration: none;
    }
}
```

### 局部（Partials）

局部 Sass 文件不会被翻译成 css 文件，命名规范是下划线开头——`_partial.scss`，可以用 `@import` 导入。

> css 也可以模块化

### 导入

CSS 也有 import，但是会带来 HTTP 请求开销。Sass 的 `@import` 只是合并文件，不会发请求。

```SCSS
// _reset.cscc
html,
body,
ul,
ol {
    margin: 0;
    padding: 0;
}
```

```SCSS
// base.scss

@import 'reset';

body {
    font: 100% Helvetica, sans-serif;
    background-color: #efefef;
}
```

### 混合（Mixin）

> Mixins are a way of including ("mixing in") a bunch of properties from one rule-set into another rule-set.

Mixin 特别适用于处理 vendor prefiex。

```SCSS
@mixin border-radius($radius) {
    -webkit-border-radius: $radius;
       -moz-border-radius: $radius;
        -ms-border-radius: $radius;
            border-radius: $radius;
}

.box { @include border-radius(10px); }
```
### 扩展/继承

`@extend` 可以为 CSS 的属性 “提取公因式”，这个“公因式”叫占位类（placeholder class）。

如果占位类没有并用到就不会输出到 CSS 文件。

```SCSS
// This CSS won't print because %equal-height is never extended.
$equal-heights {
    display: flex;
    flex-wrap: wrap;
}

// This CSS will print because $message-shared is extended
$message-shared {
    border: 1px solid #ccc;
    padding: 10px;
    color: #333;
}

.message {
    @extend $message-shared;
}

.success {
    @extend $message-shared;
    border-color: green;
}

.error {
    @extend $message-shared;
    border-color: red;
}

.warning {
    @extend $message-shared;
    border-color: yellow;
}
```

处理后的 CSS 文件如下：

```CSS
.message, .success, .error, .warning {
    border: 1px solid #cccccc;
    padding: 10px;
    color: #333;
}

.success {
    border-color: green;
}

.error {
    border-color: red;
}

.warning {
    border-color: yellow;
}
```

### 操作符

支持数学运算。

```SCSS
.container { width: 100%; }

article[role="main"] {
    float: left;
    width: 600px / 960px * 100%;
}

aside[role="complementary"] {
    float: right;
    width: 300px / 960px * 100%;
}
```

处理过后的 CSS 如下：

```CSS
.container {
    width: 100%;
}

article[role="main"] {
    float: left;
    width: 62.5%;
}

aside[role="complementary"] {
    float: right;
    width: 31.25%;
}
```

## Less

相比于 Sass，Less 的预处理支持压缩。

```bash
lessc --clean-css styles.less styles.min.css
```

Less 还可以直接用在 Node 环境：

```javascript
var less = require('less');

less.render('.class { width: (1 + 1) }'), function (e, output) {
    console.log(output.css);
});
```

打印结果：

```CSS
.class {
    width: 2;
}
```

Less 还支持传入配置：

```javascript
var less = require('less');
less.render('.class { width: (1 + 1) }',
    {
        paths: ['.', './lib'],  // Specify search paths for @import directives
        filename: 'style.less', // Specify a filename, for better error messages
    },
    function(e, output) {
        console.log(output.css);
    });
```

还可以直接用于端侧，不推荐用于生产环境，有性能开销。

```html
<!-- set options before less.js script -->
<link rel="stylesheet/less" type="text/css" href="styles.less" />

<script>
  less = {
    env: "development",
    async: false,
    fileAsync: false,
    poll: 1000,
    functions: {},
    dumpLineNumbers: "comments",
    relativeUrls: false,
    rootpath: ":/a.com/"
  };
</script>

<script src="less.js"></script>
```

## tips
下面代码中的 `&` 表示父选择器：

```Less
.clearfix {
    display: block;
    zoom: 1;

    $:after {
        content: " ";
        display: block;
        font-size: 0;
        height: 0;
        clear: both;
        visiblity: hidden;
    }
}
```
