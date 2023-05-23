---
title: 布局管理
excerpt: Jekyll 布局管理
lesson: 5
---

{% raw %}

我们知道，一个网站由多个页面组成，多个页面之间存在通用部分，比如 head、footer 或者 navigation。

这些通用部分的如果不能放在一个地方维护，任何变更都会涉及到所有文件，非常不利于维护。

Jekyll 为了解决这个问题，引入了了布局（Layout）这个概念。

## 如何使用布局

布局的用法非常简单。

首先在项目根目录下创建一个文件夹 `_layouts`，这个名称也属于 Jekyll 的约定之一。

然后在 `_layouts` 下创建一个名为 `default.html` 的 html 文件：

__layouts/default.html_

    
    
    <!DOCTYPE html>
    <html>
      <body>
        <main class="page-content" aria-label="Content">
          <div class="wrapper">
            {{ content }}
          </div>
        </main>
      </body>
    </html>
    

> 上面代码中出现了一个变量——`{{ content }}`，这里只需要注意下，后面会详细解释。

然后，我们再创建另一个文件——`page.html`，内容如下：

    
    
    ---
    layout: default
    ---
    <article class="page">
    
      <header class="page-header">
        <h1 class="page-title">{{ page.title | escape }}</h1>
      </header>
      
      <div class="page-content">
        {{ content }}
      </div>
      
    </article>
    

`page.html` 的文件顶部有一个 Front Matter，内部定义了一个变量 `layout`，值是 `default`。

`default` 指的就是 `default.html` 文件， `layout` 是变量名，用于指定当前文件的布局。

`default.html` 文件中出现的 `{{ content }}` 的作用，用一张图可能更好解释：

![content](/assets/images/jekyll/content.png)

也就是说，Jekyll 会把 `default.html` 的 `{{ content }}` 替换成 `page.html` 的文件内容（除 Front
Matter 外），并在 `_site` 目录下生成一个新的 `page.html` 文件作为最终产物。

`page.html` 和 `default.html` 本质上是一种继承关系，当然也支持多继承。

## 布局继承

`page.html` 继承自 `default.html`，`page.html` 也可拥有自己的子类。

例如，我们需要分别为 Jekyll 教程和 Flutter 教程的展示页面定义一个布局文件，就可以直接创建两个新的 HTML 文件，让它们继承
`page.html`：

![多继承](/assets/images/jekyll/inherit.png)

## 页面变量

上面 `page.html` 的代码用到了一个变量——`page.title`，这个变量并没有出现在 Front Matter 中，其实这是 Jekyll
的内置变量。

除此之外，还有许多，比如全局变量：

  * `site`
  * `page`
  * `layout`
  * `content`
  * `paginator`

有的全局变量还有自己的子变量。

我们以 `page` 为例：

  * `page.content` \- 页面内容
  * `page.title` \- 页面标题
  * `page.excerpt` \- 页面节选
  * `page.url` \- 页面 url
  * …

很多变量还可以直接在 `_config.yml` 文件中赋值，后续我们会讲到。

{% endraw %}