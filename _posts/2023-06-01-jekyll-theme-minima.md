---
layout: single
title: Jekyll 默认主题 minima 使用总结
categories: Tools
tags:
  - Jekyll
  - minima
  - CSS
---

`minima` 是 Jekyll 的默认主题，配置简单，风格简约。

以下内容是我在为[https://liangfei.me](https://liangfei.me)设置主题过程中的经验总结。

## 远程主题（Remote Theme）

**定义：**

> A Jekyll remote theme is a method of using a theme for your Jekyll website that is hosted on a public GitHub repository, rather than locally or as a bundled Ruby gem.

也就是说，使用「远程主题」的好处是 **免去了维护本地主题代码的麻烦**。

实现这个功能需要配置 `jekyll-remote-theme` 插件：

**⑴　首先在 `Gemfile` 文件添加 `jekyll-remote-theme` 的插件依赖**

```ruby
# If you have any plugins, put them here!
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-remote-theme"
end
```

**⑵　然后在 `_config.yml` 中增加两个配置**

```yaml
remote_theme: jekyll/minima
plugins:
  - jekyll-remote-theme
  - jekyll-feed
```

完成以上配置，我们就可以利用 `jekyll-remote-theme` 这个插件（plugin）获取名称为 `jekyll/minima` 的远程主题了。

其中：

* **插件仓库地址**：[jekyll-remote-theme](https://github.com/benbalter/jekyll-remote-theme)
* **主题仓库地址**：[jekyll/minima](https://github.com/jekyll/minima)

**那要如何指定 `remote theme` 的版本号呢？**

文档是这么写的：

> You may also optionally specify a branch, tag, or commit to use by appending an @ and the Git ref (e.g., benbalter/retlab@v1.0.0 or benbalter/retlab@develop). 
>
> If you don't specify a Git ref, the HEAD ref will be used.

也就是说，通过在主题名称后接 `@` ，我们就能够指定 `branch`、`tag` 或某个具体的 `commit`。默认会指向 `HEAD`（默认分支的最新提交）

为了保证主题的「新鲜度」，我在实际应用中指定了 `master` 分支：

```yaml
remote_theme: jekyll/minima@master
```

## 自定义 CSS

当默认主题并不能满足需求时，我们还可以通过自定义 CSS 的方式来实现个性化。

**⑴　新建文件：`assets/css/style.scss`**

```sass
---
---

@import
  "minima/skins/{{ site.minima.skin | default: 'classic' }}",
  "minima/initialize";
```

**说明**：文件顶部的两行 `---` 叫做 `Front Matter`，它表示：

- 告诉 `Jekyll` 这不是纯 SCSS 文件，而是要先经过 Liquid 渲染
- 两行 `---` 中间没写任何 YAML 内容，这里是一个空的 `Front Matter`，只起到激活 Liquid 渲染的作用

如果没有 `Front Matter`，Jekyll 会把它当成纯 SCSS 文件，不会解析成 CSS 文件。

## 指定布局（Layout）

Minima 默认提供四种布局：

- **base**: 基类
- **home**: 首页
- **page**: 只显示标题和内容
- **post**: 除了标题和内容，还会显示日期（`page.date` & `page.modified_date`）和作者 `page.author`，以及评论

## 配置 GA

源码路径 `_includes/head.html`：

```html
{%- if jekyll.environment == 'production' and site.google_analytics -%}
  {%- include google-analytics.html -%}
{%- endif -%}
```

只需要在 `_config.yml` 中增加一个 `google_analytics` 的配置即可。

> 注意，只有生产环境下，GA4 才会生效。

