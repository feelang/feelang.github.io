---
layout: single
classes: wide
author_profile: true
title: Jekyll 默认主题 minima 使用总结
comments: true
toc: true
toc_label: '目录'
toc_sticky: true
date: 2023-06-01
---

`minima` 是 Jekyll 的默认主题，简洁大方，[https://liangfei.me](https://liangfei.me) 用的就是它。

这篇文章简单记录一下升级改版时遇到的问题。

## Remote Theme

首先在 `Gemfile` 文件添加插件依赖：

```ruby
# If you have any plugins, put them here!
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-remote-theme"
end
```

然后在 `_config.yml` 中增加两个配置：

```yaml
remote_theme: jekyll/minima
plugins:
  - jekyll-remote-theme
  - jekyll-feed
```

以上配置的意思是：利用 `jekyll-remote-theme` 这个插件获取名称为 `jekyll/minima` 的 remote theme。
* 插件仓库地址 => [jekyll-remote-theme](https://github.com/benbalter/jekyll-remote-theme)
* 主题仓库地址 => [jekyll/minima](https://github.com/jekyll/minima)

通过 `jekyll-remote-theme` 的使用文档可以得知 theme 的获取方式：

> You may also optionally specify a branch, tag, or commit to use by appending an @ and the Git ref (e.g., benbalter/retlab@v1.0.0 or benbalter/retlab@develop). 
> If you don't specify a Git ref, the HEAD ref will be used.

也就是说，`remote_theme: jekyll/minima` 会指向 `minima` 的 `master` 分支。

## 自定义 css

* 新建文件：`assets/css/style.scss`。

```sass
---
---

@import
  "minima/skins/{{ site.minima.skin | default: 'classic' }}",
  "minima/initialize";
```

## 指定布局

默认提供四种布局：

name | description
--- | ---
base | 基类
home | 首页
page | 只显示标题和内容
post | 除了标题和内容，还会显示日期（`page.date` & `page.modified_date`）和作者 `page.author`，以及评论

## 配置 GA

源码路径 `_includes/head.html`：

```html
{%- if jekyll.environment == 'production' and site.google_analytics -%}
  {%- include google-analytics.html -%}
{%- endif -%}
```

只需要在 `_config.yml` 中增加一个 `google_analytics` 的配置即可。

> 注意，只有生产环境下，GA4 才会生效。

