---
layout: single
title: Jekyll 主题 Minimal Mistakes 布局（Layouts）文件源码分析
excerpt: Minimal Mistakes 提供了很多布局文件，为了更好地使用它们，这篇文章简单分析了几个比较常见的布局文件源码。 
categories: Tools
tags:
  - Jekyll
  - Minimal Mistakes
classes: wide
---

{% raw %}

Minimal Mistakes 提供了很多布局文件，为了更好地使用它们，这篇文章简单分析了几个比较常见的布局文件源码。

我们知道，Jekyll Theme 的 Layout 文件会统一放在 `_layouts` 目录下，每个 html 文件分别对应一种布局。

首先来看所有布局文件的基类 —— `_layouts/default.html`：

## default

作为所有布局文件的基类，`_layouts/default.html` 定义了生成 html 文件的基本框架。

我们从第一个标签 `<html>` 开始分析：

```html
<html lang="{{ site.locale | slice: 0,2 | default: "en" }}" class="no-js">
```

可以看出，`<html>` 标签中给 `lang` 属性赋值，取值来源于 `_config.yml` 的全局配置 `locale`。

然后是 `<head>` 标签：

```html
<head>
  {% include head.html %}
  {% include head/custom.html %}
</head>
```

其中`_includes/head.html` 做了以下几件事：

- seo
- atom feed
- viewport
- stylesheet => `/assets/css/main.css`
- fontawesome

同时也支持引入自定义 js：

```html
{% if site.head_scripts %}
  {% for script in site.head_scripts %}
    <script src="{{ script | relative_url }}"></script>
  {% endfor %}
{% endif %}
```

第二个 include 文件 `_includes/head/custom.html` 是留给我们自定义用的。

继续往下看，`<body>` 标签：

```html
{% include_cached skip-links.html %}
{% include_cached masthead.html %}
```

其中 `_includes/skip-links.html` 用于页面内快速跳转：

```html
<nav class="skip-links">
  <ul>
    <li><a href="#site-nav" class="screen-reader-shortcut">{{ site.data.ui-text[site.locale].skip_primary_nav | default: 'Skip to primary navigation' }}</a></li>
    <li><a href="#main" class="screen-reader-shortcut">{{ site.data.ui-text[site.locale].skip_content | default: 'Skip to content' }}</a></li>
    <li><a href="#footer" class="screen-reader-shortcut">{{ site.data.ui-text[site.locale].skip_footer | default: 'Skip to footer' }}</a></li>
  </ul>
</nav>
```

支持三个锚点：

- `#site-nav`
- `#main`
- `#footer`

`<body>` 标签内的第二个 include 文件 `_includes/masthead.html` 是页面吊顶，我们逐行来分析。

首先是展示网站 logo，其路径来源于全局配置 `site.logo`：

```html
{% capture logo_path %}{{ site.logo }}{% endcapture %}
```

用一个 `<a>` 标签包裹的 `<img>` 做展示：

```html
{% unless logo_path == empty %}
  <a class="site-logo" href="{{ '/' | relative_url }}"><img src="{{ logo_path | relative_url }}" alt="{{ site.masthead_title | default: site.title }}"></a>
{% endunless %}
```

logo 的右边是 `title` 和 `subtitle`，也是来自于全局配置：

```html
<a class="site-title" href="{{ '/' | relative_url }}">
  {{ site.masthead_title | default: site.title }}
  {% if site.subtitle %}<span class="site-subtitle">{{ site.subtitle }}</span>{% endif %}
</a>
```

然后是导航条：

```html
<ul class="visible-links">
  {%- for link in site.data.navigation.main -%}
    <li class="masthead__menu-item">
      <a href="{{ link.url | relative_url }}"{% if link.description %} title="{{ link.description }}"{% endif %}>{{ link.title }}</a>
    </li>
  {%- endfor -%}
</ul>
```

> 很遗憾，不支持多级导航。

接下来是搜索按钮：

```html
{% if site.search == true %}
<button class="search__toggle" type="button">
  <span class="visually-hidden">{{ site.data.ui-text[site.locale].search_label | default: "Toggle search" }}</span>
  <i class="fas fa-search"></i>
</button>
{% endif %}
```

其中 `visually-hidden` 这个 css 类比较好玩，看下源码：

```css
.visually-hidden,
.screen-reader-text,
.screen-reader-text span,
.screen-reader-shortcut {
  position: absolute !important;
  clip: rect(1px, 1px, 1px, 1px);
  height: 1px !important;
  width: 1px !important;
  border: 0 !important;
  overflow: hidden;
}

body:hover .visually-hidden a,
body:hover .visually-hidden input,
body:hover .visually-hidden button {
  display: none !important;
}
```

> 可以看出，以上 CSS 是是一种比较 tricky 的做法，应该是做 SEO 用的。

最后是自适应布局中的 `Toggle menu`：

```html
<button class="greedy-nav__toggle hidden" type="button">
  <span class="visually-hidden">{{ site.data.ui-text[site.locale].menu_label | default: "Toggle menu" }}</span>
  <div class="navicon"></div>
</button>
```

控制 `Toggle menu` 自适应布局的源码位于 `assets/js/plugins/jquery.greedy-navigation.js`。

以上便是 `_includes/masthead.html` 的源码，回到 `_layouts/default.html` 继续往下看：

**子类布局占位：**

```html
<div class="initial-content">
  {{ content }}
</div>
```

后面要分析的布局 `_includes/splash.html` , 其文件内容就是通过 `{{ content }}` 变量来占位。

**搜索：**

```html
{% if site.search == true %}
  <div class="search-content">
    {% include_cached search/search_form.html %}
  </div>
{% endif %}
```

支持三种第三方搜索插件：

- lunr
- google
- algolia

对应的 js 在 `_includes/scripts.html` 有定义。

**footer：**

```html
<div id="footer" class="page__footer">
  <footer>
    {% include footer/custom.html %}
    {% include_cached footer.html %}
  </footer>
</div>
```

其中 `_includes/footer/custom.html` 用于自定义。

`_includes/footer.html` 用于展示如下配置：

- `site.data.ui-text[site.locale].follow_label`
- `site.footer.links`
    - `link.icon`
    - `link.label`
    - `link.url`
- `site.atom_feed`
- `site.time` & `site.name || site.title` & `site.data.ui-text[site.locale].powered_by`

**scripts：**

```html
{% include scripts.html %}
```

`_includes/scripts.html` 中包含了以下内容：

1）自定义 js，默认使用 `/assets/js/main.min.js`：

```html
{% if site.footer_scripts %}
  {% for script in site.footer_scripts %}
    <script src="{{ script | relative_url }}"></script>
  {% endfor %}
{% else %}
  <script src="{{ '/assets/js/main.min.js' | relative_url }}"></script>
{% endif %}
```

2）搜索

```html
{% if site.search == true or page.layout == "search" %}
  {%- assign search_provider = site.search_provider | default: "lunr" -%}
  {%- case search_provider -%}
    {%- when "lunr" -%}
      {% include_cached search/lunr-search-scripts.html %}
    {%- when "google" -%}
      {% include_cached search/google-search-scripts.html %}
    {%- when "algolia" -%}
      {% include_cached search/algolia-search-scripts.html %}
  {%- endcase -%}
{% endif %}
```

3）埋点

```html
{% include analytics.html %}
```

4）评论

```html
{% include /comments-providers/scripts.html %}
```

5）js 脚本

```html
{% if site.after_footer_scripts %}
  {% for script in site.after_footer_scripts %}
    <script src="{{ script | relative_url }}"></script>
  {% endfor %}
{% endif %}
```

最后总结一下 `_layouts/default.html` 的代码结构：

- html
    - head
        - include `head.html`
            - include `seo.html`
            - site.atom_feed
            - viewport
            - `/assets/css/main.css`
            - fontawesome
            - site.head_scripts
        - include `head/custom.html`
    - body
        - include_cached `skip-links.html`
            - `#site-nav`
            - `#main`
            - `#footer`
        - include_cached `masthead.html`
            - site.logo
            - site.masthead | site.title
            - site.subtitle
            - site.data.navigation.main
            - site.search
            - _Toggle menu_
        - `{{ content }}`
        - include_cached `search/search_form.html`
            - lunr
            - google
            - algolia
    - footer
        - include `footer/custom.html`
            - site.data.ui-text[site.locale].follow_label
            - site.footer.links
            - site.atom_feed
            - _copyright_
        - include_cached `footer.html`
    - include `scripts.html`
        - site.footer_scripts
        - site.search
        - include `analytics.html`
            - google
            - google-universal
            - google-gtag
            - custom
        - include `/comments-providers/scripts.html`
            - diques
            - discourse
            - facebook
            - staticman
            - staticman_v2
            - utterances
            - giscus
            - custom
        - site.after_footer_scripts


## splash

`splash` 继承自 `default` ，适用于 landing page。

Minimal Mistakes 官网首页便是使用了这个布局。

下面简单分析下源码。

主题源码的 `docs/_pages/home.md` 文件中，**[Front Matter](/tutorials/jekyll/font-matter-and-yaml)** 定义了一个 `header` 变量：

```yaml
header:
  overlay_color: "#5e616c"
  overlay_image: /assets/images/mm-home-page-feature.jpg
  actions:
    - label: "<i class='fas fa-download'></i> Install now"
      url: "/docs/quick-start-guide/"
```

这个变量在布局源码文件 `_layouts/splash.html` 中会被用到：

```html
{% if page.header.overlay_color or page.header.overlay_image or page.header.image %}
  {% include page__hero.html %}
{% elsif page.header.video.id and page.header.video.provider %}
  {% include page__hero_video.html %}
{% endif %}
```

以上代码可以看出，这里既可以展示图片，也可以展示视频。

* 展示图片的 `include` 文件是 `page_hero.html`。

它用到的参数有：

- page.header.overlay_image => overlay_img_path
- page.header.overlay_color
- page.header.overlay_filter => overlay_filter
    - gradient
    - rgba
- page.header.image_description => image_description
- page.header.show_overlay_excerpt
- page.header.cta_url
- page.header.actions
    - label
    - url
- page.header.image
- page.header.caption

展示视频的 `include` 文件是 `_includes/page__hero-video.html`：

```html
{% assign video = page.header.video %}
{% include video id=video.id provider=video.provider danmaku=video.danmaku %}
```

这里进一步引用了 `_include/video` 这个模块：

```html
{% capture video_id %}{{ include.id }}{% endcapture %}
{% capture video_provider %}{{ include.provider }}{% endcapture %}
{% capture video_danmaku %}{{ include.danmaku | default: 0 }}{% endcapture %}

{% capture video_src %}
  {% case video_provider %}
  {% when "vimeo" %}
    https://player.vimeo.com/video/{{ video_id }}?dnt=true
  {% when "youtube" %}
    https://www.youtube-nocookie.com/embed/{{ video_id }}
  {% when "google-drive" %}
    https://drive.google.com/file/d/{{ video_id }}/preview
  {% when "bilibili" %}
    https://player.bilibili.com/player.html?bvid={{ video_id }}&page=1&as_wide=1&high_quality=1&danmaku={{ video_danmaku }}
  {% endcase %}
{% endcapture %}
{% assign video_src = video_src | strip %}

<!-- Courtesy of embedresponsively.com -->
{% unless video_src == "" %}
  <div class="responsive-video-container">
    <iframe src="{{ video_src }}" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowfullscreen></iframe>
  </div>
{% endunless %}
```

代码很简单，四个视频平台：

- vimeo
- youtube
- google-drive
- bilibili

继续分析 `_layouts/splash.html` 的剩余代码：

```html
<div id="main" role="main">
  <article class="splash" itemscope itemtype="https://schema.org/CreativeWork">
    {% if page.title %}<meta itemprop="headline" content="{{ page.title | markdownify | strip_html | strip_newlines | escape_once }}">{% endif %}
    {% if page.excerpt %}<meta itemprop="description" content="{{ page.excerpt | markdownify | strip_html | strip_newlines | escape_once }}">{% endif %}
    {% if page.date %}<meta itemprop="datePublished" content="{{ page.date | date_to_xmlschema }}">{% endif %}
    {% if page.last_modified_at %}<meta itemprop="dateModified" content="{{ page.last_modified_at | date_to_xmlschema }}">{% endif %}

    <section class="page__content" itemprop="text">
      {{ content }}
    </section>
  </article>
</div>
```

这部分代码只是给 `article` 元素中添加了四个 `meta`：

Page Variable | Item Property
--- | ---
page.title | headline
page.excerpt | description
page.date | datePublished
page.last_modified_at | dateModified

对页面视觉没有作用，应该只是为了 SEO。

`_includes/splash.html` 本身的代码比较简单，我们再回过头去看使用了这个布局的文件 `docs/_pages/home.md`。

Front Matter 中除了 `header` 变量，还有一个 `feature_row` 数组：

```yaml
feature_row:
  - image_path: /assets/images/mm-customizable-feature.png
    alt: "customizable"
    title: "Super customizable"
    excerpt: "Everything from the menus, sidebars, comments, and more can be configured or set with YAML Front Matter."
    url: "/docs/configuration/"
    btn_class: "btn--primary"
    btn_label: "Learn more"
```

可以看出，数组元素的属性挺多的，我们来看下它是如何被展示的。

在 `docs/_pages/home.md` 文件的末尾通过如下代码引入了 `_includes/feature_row` 文件：

```html
{% include feature_row %}
```

我们来分析一下 `_includes/feature_row` 的源码：

```html
{% if include.id %}
  {% assign feature_row = page[include.id] %}
{% else %}
  {% assign feature_row = page.feature_row %}
{% endif %}
```

第一个 `assign` 没看懂，问了一下 ChatGPT，回答如下：

```
In Jekyll, the code `{% assign feature_row = page[include.id] %}` is using the html templating language to assign a value to the `feature_row` variable.

Let's break down the code:

- `{% assign ... %}` is a html tag used for variable assignment.
- `feature_row` is the name of the variable being assigned.
- `page` is a special object in Jekyll that represents the current page being processed.
- `[include.id]` is accessing a value from the `page` object using square brackets and `include.id`.

In this case, `include.id` is likely a variable or parameter that holds a specific identifier or key. By using `page[include.id]`, the code is retrieving a value associated with that identifier from the `page` object and assigning it to the `feature_row` variable.

The purpose and usage of the `feature_row` variable depend on the specific context and how it is used later in the Jekyll template or layout.
```

也就是说，`page` 实际上是 Javascript 的一个 Object，`page[include.id]` 的意思是：取 `page` 对象中属性名为 `include.id` 的那个变量。

进一步说，我们可以在 `docs/_pages/home.md` 文件中定义一个名称为 `features` 的数组，然后通过如下代码传参给 `_includes/feature_row`：

```html
{% include feature_row id="features" %}
```

继续分析 `_includes/feature_row` 源码。

通过遍历 `feature_row`，获取数组元素 `f`：

```html
{% for f in feature_row %}
```

在 for 循环体内，依次展示每个元素的属性：

1）`image_path`

```html
{% if f.image_path %}
  <div class="archive__item-teaser">
    <img src="{{ f.image_path | relative_url }}"
         alt="{% if f.alt %}{{ f.alt }}{% endif %}">
    {% if f.image_caption %}
      <span class="archive__item-caption">{{ f.image_caption | markdownify | remove: "<p>" | remove: "</p>" }}</span>
    {% endif %}
  </div>
{% endif %}
```

2）`title`

```html
{% if f.title %}
  <h2 class="archive__item-title">{{ f.title }}</h2>
{% endif %}
```

3）`excerpt`

```html
{% if f.excerpt %}
  <div class="archive__item-excerpt">
    {{ f.excerpt | markdownify }}
  </div>
{% endif %}
```

4）`url`

```html
{% if f.url %}
  <p><a href="{{ f.url | relative_url }}" class="btn {{ f.btn_class }}">{{ f.btn_label | default: site.data.ui-text[site.locale].more_label | default: "Learn More" }}</a></p>
{% endif %}
```

以上便是 `_includes/feature_row` 的源码，至此，`_layouts/splash.html` 也分析完了。


{% endraw %}
