---
title: Front Matter & YAML
excerpt: Jekyll 文件的基本组成
lesson: 4
---
{% raw %}

在上一篇[Jekyll教程——快速上手](/tutorials/jekyll/getting-started/)中我们提到过 Front Matter，说它功能很强大，那它究竟强在哪呢？这篇我们来解密一下。

## Front Matter 是什么

首先，我们来搞清楚 Front Matter 的定义。

Front Matter 翻译成中文是「前页（指扉页、版权页、目次等）」，它是位于 HTML/Markdown 文件的顶部，遵循 YAML 语法的一块区域。

在 Front Matter 内，我们可以像下面这样定义变量：

    
```yaml
---
# the title that will appear in the HTML head tag
title: Home
---
``` 

YAML 类似 JSON，是另一种可序列化的文件格式。

上例代码中的 `title: home` 是 YAML 定义变量的方式：左边是 key，右边是 value，中间用逗号隔开。

value 可以是任意类型，整形、浮点数、字符串、布尔都可以。

那这个变量怎么用呢？

上一篇介绍 Liquid 语法时我们提到过，Jekyll 处理 Liquid 代码的前提条件是 HTML/Markdown 文件头部带有 Front
Matter，所以 Front Matter 和 Liquid 本来就是“天生一对”。

Front Matter 中定义的变量，可以给 Liquid 用：

```html 
<head>
{% if page.title %}
  <title>Jekyll Tutorial | {{ page.title }}</title>
{% else %}
  <title>Jekyll Tutorial</title>
{% endif %}
  <link rel="stylesheet" href="css/style.css">
</head>
```
    

## YAML 基本语法

通过上面的示例可以看出，Front Matter 等于是在 HTML/Markdown 文件中专门开辟了一块用来写 YAML 的地方。

这种将页面逻辑和数据部分进行分离的方式，有效提高了代码的可维护性。

其中，YAML 变量支持的数据结构如下：

### 数组

数组有两种写法，一种是垂直（vertical），另一种是内联（inline）。

```yaml

# vertical
languges_vertical:
  - Rust
  - Go
  - Python
  - Dart 
  - JavaScript

# inline
languages_inline: [Rust, Go, Python, Dart, JavaScript]

```
    

然后，这些数据可以直接拿给 Liquid 用：

```yaml   
<!-- Display on page -->
{% for lang in page.languages_vertical %}
  {{ lang }}
{% endfor %}
```
    
### 对象

上例中的数组元素都是字符串类型，无法表达一些比较复杂的数据结构，比如产品列表、人员列表。

这个时候就需要用到 YAML 对象了。

```yaml
languges:
  - name: Rust
    website: https://www.rust-lang.org/
  - name: Go
    website: https://www.rust-lang.org/
  - name: Python
    website: https://www.python.org/
  - name: Dart 
    website: https://dart.dev/
  - name: JavaScript
    website: https://www.javascript.com/
```
    

用法跟上面一样，直接在 Liquid 代码中访问变量 `langauges`：

```html
<div class="lang-grid">
{% for lang in page.languages %}
  <div class="lang">
    <a href="{{ lang.website }}">{{ lang.name }}</a>
  </div>
{% endfor %}
</div>
```

## 多行文本

定义变量时，我们经常会遇到文本过长的情况，最简单的方式是用引号包起来，但这么写不太美观，而且换行还得用转义字符。

还好，YAML 有专门的语法来定义长文本。

  * 如果不需要换行，可以用折叠形式（folded style）：
    
        Kea: >-  
      The kea is the worldâ€™s only alpine parrot and native to New Zealand, 
      with high intelligence and curiosity - which also extends to its eating habits.
    

  * 如果需要换行，可以用字面行式（literal style）：
    
        kakapo: |-  
      The kakapo is another parrot native to New Zealand  
      Unlike the kea, it is a nocturnal, flightless herbivore, and the heaviestÂ parrot in the world.  
      Unfortunately, these traits have led to it being critically endangered.  
    

使用字面行式时，有两点需要注意一下：

0. 需要换行时，要在行尾加两个空格
0. html 文件中的 front matter，使用多行文本前需要 markdownify 一下：`{{ multiline_text | markdownify }}`，否则文本会被折叠，不会输出多行。

多于 YAML 的多行语法，可移步至 [YAML Multiline](https://yaml-multiline.info/)。

下一篇将介绍页面布局。

{% endraw %}