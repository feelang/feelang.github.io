---
title: 模板语言 Liquid
excerpt: Liquid 基础语法
lesson: 3
---

{% raw %}

Liquid 出自 Shopify 团队，和 Jekyll 一样，都是 Ruby 写成的。

Liquid 是 Jekyll 内置的模板语言，有了它，我们可以在 HTML 文件中添加控制逻辑或者引用外部数据，为原本枯燥乏味的 HTML
代码增添了一丝灵动。

因为 Liquid 与 Jekyll 是「捆绑销售」，所以拿来就用，无需额外操作。

## 基础语法

    
    
    ---
    ---
    <!DOCTYPE html>
    

上述 HTML 文件顶部的两行 `---` 叫 **Front Matter** ，下一篇博文会介绍到，它的作用是告诉 Jekyll
这是一个需要预处理的文件，Jekyll 会解析文件中出现的 Liquid 代码。

Liquid 代码本身支持两种标签类型：

  * `{{ content }}` \- 输出内容到页面
  * `{% if condition == true %}` \- 控制逻辑

需要注意，逻辑控制的代码块结束之后必须要跟一个表示结束的声明（statement），例如：

`{% endif %}, {% endfor %}`

除了内容输出和逻辑控制，还可以进行变量赋值：

`{% assign myVariableName = Content of my variable; %}`

关于变量的用法，下一篇要介绍的 **Front Matter** 提供了更强大的用法，但 Liquid 变量并不会被取代，仍然有它的可用之处。

## 过滤器

过滤器（filter）的作用对象是字符串（文本）以及数组（列表），用法很简单：左边内容，右边关键词，中间用 `|` 隔开。支持链式调用。

Liquid 内置了很多过滤器，这里我们只挑几个常用的介绍一下。

### 大小写转换

  * `{{ "uppercase" | upcase }}` = UPPERCASE
  * `{{ "LOWERCASE" | downcase }}` = lowercase

### 字符串长度计算

`{{ "How long am I?" | size}}` = 14

### 文本合并

`{{ "Copyright " | append: "My Blog" }}` = Copyright My Blog

> 这里的 `append` 带了一个参数（argument）

### 日期格式化

`{{ "2021-01-01T00:00:00Z" | date_to_long_string }}` = 01 January 2021

## 条件

使用条件语句可以轻松控制页面内容的输出，为此，Liquid 提供了许多逻辑操作符：

操作符| 意义  
---|---  
==| 等于  
!=| 不等  
>| 大于  
<| 小于  
>=| 大于等于  
<=| 小于等于  
and| 与  
or| 或  
  
最常用的条件语句是 `if`，用法如下：

    
    
    {% assign title = "home" %}
    {% if title == "home" %}
      <h1>Welcome to my homepage!</h1>
    {% endif %}
    

同时也支持配套的 `elsif` 和 `else`：

    
    
    {% assign title = "home" %}
    {% if title == "home" %}
      <h1>This is the homepage</h1>
    {% elsif title == "about" %}
      <h1>This is the about page</h1>
    {% else %}
      <h1>Welcome!</h1>
    {% endif %}
    

## 循环

循环语句的语法也很简单：

`for <variable> in <list of items>`，

它让数组操作变得更加便捷。

    
    
    {% assign languages = "rust,go,python,dart,javascript" | split: "," %}
    <ul>
      {% for lang in languages %}
        <li>{{ lang }}</li>
      {% endfor %}
    </ul>
    

  * 上面代码的第一行用到了过滤器 `split`，用 `","` 把一个字符串分割成了数组，然后把数组赋值给变量 `languages`。
  * 因为有了 `for` 循环，我们可以随意更改字符串，而不用修改控制内容输出的逻辑。
  * 当然，`for` 语句里面还可以内嵌 `if` 语句。

下一篇将介绍功能十分强大的 front matter。

{% endraw %}
