---
title: 博客功能
excerpt: Jekyll 搭建个人博客
lesson: 7
classes: wide
toc: false
---

{% raw %}

相信很多程序员选择 Jekyll 是为了搭建个人博客，虽然它远不止于此。本篇我们就来介绍 Jekyll 的博客功能。

## 博客文件约定

当一个全新的 Jekyll 项目创建完成时，默认会生成一个 `_posts` 文件夹和一篇简单的示例博客。

其中博文对应的文件遵守如下约定：

  * 文件名格式为 `[year]-[month]-[day]-[post-name].md`
  * 文件内容一般为 Markdown，不过 HTML 也可以
  * 文件必须包含 Front Matter（可以不用定义任何变量）

示例如下：  

`_posts/2021-09-26-my-post.md`
```yaml    
---
title: A blog post
---
```
    

## 访问博客文章

Jekyll 在执行构建时，针对博文会做出如下处理：

  * 将博文输出为 HTML
  * 为每篇博文创建一个 `post` 对象，属性包括日期、标题以及 url
  * 生成一个全局对象 `site.posts`，可访问所有博文

既然所有的博文都会归类于 `site.posts`，当我们需要一个页面来展示所有博文时，就可以写成如下形式：

`blog.html`

```yaml    
---
layout: default
title: Blog Page
---
<ul>
{% for post in site.posts %}
  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</ul>
```
    

博文对应的文件也支持指定布局，比如我们可以在 `_layouts` 目录下创建一个 `post.html` 的布局文件：

[minima/_layouts/post.html](https://github.com/jekyll/minima/blob/master/_layouts/post.html)

    

```html    
---
layout: default
---
<article class="post h-entry" itemscope itemtype="http://schema.org/BlogPosting">

  <header class="post-header">
    <h1 class="post-title p-name" itemprop="name headline">{{ page.title | escape }}</h1>
    <p class="post-meta">
      {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
      <time class="dt-published" datetime="{{ page.date | date_to_xmlschema }}" itemprop="datePublished">
        {{ page.date | date: date_format }}
      </time>
      {%- if page.modified_date -%}
        ~ 
        {%- assign mdate = page.modified_date | date_to_xmlschema -%}
        <time class="dt-modified" datetime="{{ mdate }}" itemprop="dateModified">
          {{ mdate | date: date_format }}
        </time>
      {%- endif -%}
      {%- if page.author -%}
        {% for author in page.author %}
          <span itemprop="author" itemscope itemtype="http://schema.org/Person">
            <span class="p-author h-card" itemprop="name">{{ author }}</span></span>
            {%- if forloop.last == false %}, {% endif -%}
        {% endfor %}
      {%- endif -%}</p>
  </header>

  <div class="post-content e-content" itemprop="articleBody">
    {{ content }}
  </div>

  <a class="u-url" href="{{ page.url | relative_url }}" hidden></a>
</article>
```
    

然后创建博文时，在 Front Matter 内指定布局：


`_posts/2021-09-26-my-post.md`

    
```yaml
---
title: A blog post
layout: post
---
```
    

这样，每次新建博文时就可以专注于内容，展示方式全部交由布局文件 `_layouts/post.html` 去处理。

除此之外，Jekyll 还支持用合集（collection）的方式来归类文章，我们下一篇见~


{% endraw %}