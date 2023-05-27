---
layout: single
classes: wide
author_profile: true
title: Jekyll 主题 Minimal Mistakes 使用总结
comments: true
toc: true
toc_label: '目录'
toc_sticky: true
date: 2023-05-27
---

虽然我使用 Jekyll 已经有一段时间了，但一直没注意到 **Minimal Mistakes** 这个主题的存在。

用它改版[个人技术博客](https://feelang.github.io/)后，感觉效果还不错。我打算用这个主题把[森罗社官网](https://senluoshe.com)重构一下。

所以借这篇博文用简单总结一下改版期间遇到的一些问题，留作后续参考。

## 关于 Minimal Mistakes

* [Github](https://github.com/mmistakes/minimal-mistakes)
* [Website](https://mmistakes.github.io/minimal-mistakes)

它的官网使用的便是这个主题，视觉效果还行，适合 startup 用，简单省事。

## 网页吊顶（Masthead）

* [文档](https://mmistakes.github.io/minimal-mistakes/docs/navigation)

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

---

未完待续~
