---
layout: single
title: Jekyll 主题 Minimal Mistakes 使用总结
categories: Tools
tags:
  - Jekyll
  - Minimal Mistakes
  - Google Analytics
---

虽然我使用 Jekyll 已经有一段时间了，但一直没注意到 **Minimal Mistakes** 这个主题的存在。

用它改版[个人技术博客](https://feelang.github.io/)后，感觉效果还不错。我打算用这个主题把[森罗社官网](https://senluoshe.com)也重构一下。

用这篇博文简单总结一下改版期间遇到的一些问题，留作后续参考。

## 关于 Minimal Mistakes

* [Github](https://github.com/mmistakes/minimal-mistakes)
* [Website](https://mmistakes.github.io/minimal-mistakes)

它的官网使用的便是这个主题，视觉效果还行，适合 startup 用，简单省事。

## 网页吊顶（Masthead）

* 直接查看[文档 => docs/navigation](https://mmistakes.github.io/minimal-mistakes/docs/navigation)

在 `_data` 文件夹下新建一个 `navigation.yml` 文件即可。

## 支持中文

在 `_config.yml` 中添加一条配置：

```yaml
locale: "zh-CN"
```

拷贝[ui-text.yml](https://github.com/mmistakes/minimal-mistakes/blob/master/_data/ui-text.yml) 文件至 `_data` 目录下。

（可以删除其他不需要的语言）

我本来以为主题的 `data` 文件也是能够被复用的，事实证明并非如此，需要手动拷贝到项目中去。

## GA

老的 GA 即将线下，现在要使用 GTM。

免费开通 GTM 之后，会得到一个 `tracking_id`，然后在 `_config.yml` 文件中增加如下配置：

```yaml
analytics:
  provider               : "google-gtag"
  google:
    tracking_id          : "YOUR-TRACKING-ID"
    anonymize_ip         : false # default
```

## 评论区

> 评论区的作用是增加 customer engagement

我一直使用 Disqus，这次也不例外。

* [官网入口](https://disqus.com)
    * `Site Admin` => `Settings` => `Shortname`

然后继续在 `_config.yml` 文件中添加配置：

```yaml
comments:
  provider               : "disqus"
  disqus:
    shortname            : 'feelang-github-io'
```

## 作者信息（Author）

* 直接查看[官方文档](https://mmistakes.github.io/minimal-mistakes/docs/authors)

## Page 文件统一管理

Jekyll 官方文档的示例代码中，通常将 `Page` 文件放在根目录下，但是这么做会使得文件目录结构看起来比较乱，尤其是当页面变多之后。

比较好的办法是将这些 `Page` 文件放在一个文件夹下进行统一管理，实现步骤如下：

0. 在根目录下新建一个 `_pages` 文件夹
0. 在 `_config.yml` 文件中新增一条配置：

    ```yaml
    include:
      - _pages
    ```

这样 Page 文件就可以放到 `_pages` 文件夹中进行管理。

`include` 是 Jekyll 的一个配置命令：

> **Include**: Force inclusion of directories and/or files in the conversion. 

用法：`include: [DIR, FILE, ...]`

## 布局

这个主题提供了很多布局方式，这里只介绍几个常用的。

### splash

`splash` 适用于 landing page，它继承自 `default`。

这个主题的官网首页便是使用了这个布局。

下面简单分析下源码。

`docs/_pages/home.md` 的 **Front Matter** 定义了一个 `header` 变量：

```yaml
header:
  overlay_color: "#5e616c"
  overlay_image: /assets/images/mm-home-page-feature.jpg
  actions:
    - label: "<i class='fas fa-download'></i> Install now"
      url: "/docs/quick-start-guide/"
```

这个变量在 `_layouts/splash.html` 中会被用到：

```Liquid
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

```Liquid
{% assign video = page.header.video %}
{% include video id=video.id provider=video.provider danmaku=video.danmaku %}
```

这里进一步引用了 `_include/video` 这个模块：

```Liquid
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

```Liquid
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

### default

`_layouts/default.html` 是所有布局文件的基类，它定了 html 文件的基本框架。

通过源码可以看出，`<html>` 标签中有 `lang` 的属性：

```Liquid
<html lang="{{ site.locale | slice: 0,2 | default: "en" }}" class="no-js">
```

然后是 `<head>` 标签：

```Liquid
<head>
  {% include head.html %}
  {% include head/custom.html %}
</head>
```

`head.html` 中做了以下几件事：

- seo
- atom feed
- viewport
- stylesheet => `/assets/css/main.css`
- fontawesome

还支持自定义 js：

```Liquid
{% if site.head_scripts %}
  {% for script in site.head_scripts %}
    <script src="{{ script | relative_url }}"></script>
  {% endfor %}
{% endif %}
```

`head/custom.html` 是留给我们自定义用的。

继续看 `<body>` 标签：

```Liquid
{% include_cached skip-links.html %}
{% include_cached masthead.html %}
```

先看 `_includes/skip-links.html`：

```Liquid
<nav class="skip-links">
  <ul>
    <li><a href="#site-nav" class="screen-reader-shortcut">{{ site.data.ui-text[site.locale].skip_primary_nav | default: 'Skip to primary navigation' }}</a></li>
    <li><a href="#main" class="screen-reader-shortcut">{{ site.data.ui-text[site.locale].skip_content | default: 'Skip to content' }}</a></li>
    <li><a href="#footer" class="screen-reader-shortcut">{{ site.data.ui-text[site.locale].skip_footer | default: 'Skip to footer' }}</a></li>
  </ul>
</nav>
```

页面内快速跳转用的。

再来看 `_includes/masthead.html`，页面吊顶：

```Liquid
{% capture logo_path %}{{ site.logo }}{% endcapture %}
```

获取 `_config.yml` 中配置的 `site.logo`，并将其赋值给 `logo_path` 变量。

用一个 `<a>` 标签做展示：

```Liquid
{% unless logo_path == empty %}
  <a class="site-logo" href="{{ '/' | relative_url }}"><img src="{{ logo_path | relative_url }}" alt="{{ site.masthead_title | default: site.title }}"></a>
{% endunless %}
```

标题支持 `title` 和 `subtitle`：

```Liquid
<a class="site-title" href="{{ '/' | relative_url }}">
  {{ site.masthead_title | default: site.title }}
  {% if site.subtitle %}<span class="site-subtitle">{{ site.subtitle }}</span>{% endif %}
</a>
```

然后展示导航条：

```Liquid
<ul class="visible-links">
  {%- for link in site.data.navigation.main -%}
    <li class="masthead__menu-item">
      <a href="{{ link.url | relative_url }}"{% if link.description %} title="{{ link.description }}"{% endif %}>{{ link.title }}</a>
    </li>
  {%- endfor -%}
</ul>
```

接下来是搜索按钮：

```Liquid
{% if site.search == true %}
<button class="search__toggle" type="button">
  <span class="visually-hidden">{{ site.data.ui-text[site.locale].search_label | default: "Toggle search" }}</span>
  <i class="fas fa-search"></i>
</button>
{% endif %}
```

最后是自适应布局中的 `Toggle menu`：

```Liquid
<button class="greedy-nav__toggle hidden" type="button">
  <span class="visually-hidden">{{ site.data.ui-text[site.locale].menu_label | default: "Toggle menu" }}</span>
  <div class="navicon"></div>
</button>
```

以上便是 `_includes/masthead.html` 的源码，回到 `_layouts/default.html` 继续往下看：

子类布局占位：

```Liquid
<div class="initial-content">
  {{ content }}
</div>
```

搜索：

```Liquid
{% if site.search == true %}
  <div class="search-content">
    {% include_cached search/search_form.html %}
  </div>
{% endif %}
```

footer：

```Liquid
<div id="footer" class="page__footer">
  <footer>
    {% include footer/custom.html %}
    {% include_cached footer.html %}
  </footer>
</div>
```

最后是 scripts：

```Liquid
{% include scripts.html %}
```

`_includes/scripts.html` 中包含了以下内容：

1）自定义 js，默认使用 `/assets/js/main.min.js`：

```Liquid
{% if site.footer_scripts %}
  {% for script in site.footer_scripts %}
    <script src="{{ script | relative_url }}"></script>
  {% endfor %}
{% else %}
  <script src="{{ '/assets/js/main.min.js' | relative_url }}"></script>
{% endif %}
```

2）搜索

```Liquid
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

```Liquid
{% include analytics.html %}
```

4）评论

```Liquid
{% include /comments-providers/scripts.html %}
```

5）js 脚本

```Liquid
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

