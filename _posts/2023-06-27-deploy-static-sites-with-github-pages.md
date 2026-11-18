---
title: 用 GitHub Pages 部署 Jekyll 站点：从建仓到绑定域名
---

我用 GitHub Pages 部署过五个静态网站，从个人博客到公司官网都有。网页在发布前就生成好了，访客打开网站时，托管服务直接提供这些文件，所以不必自己租服务器。下面以这个博客为例，讲讲怎样从建仓走到绑定自己的域名。

## 建仓并预览站点

我用个人账号 `feelang` 建了一个名为 `feelang.github.io` 的仓库。做个人或组织的主页时，仓库名用对应的用户名或组织名加上 `.github.io`。

静态网站生成器会把文章和模板合成网页。我用的是 Jekyll，写文章时只需要准备 Markdown，布局和样式可以留给模板。Hugo、Hexo、Eleventy、Gatsby、VuePress、Pelican 和 MkDocs 也能用来做静态站点，可以按熟悉的语言和站点用途选。

把空仓库克隆到本地，进入仓库目录。在准备好 Ruby 并装好 Jekyll 和 Bundler 后，生成初始站点并打开预览：

```bash
jekyll new .
bundle exec jekyll serve
```

浏览器打开 `http://127.0.0.1:4000`，先确认首页能显示。如果遇到环境或依赖问题，可以对照 [Jekyll 快速入门](https://jekyllrb.com/docs/) 排查。

## 推送代码并部署

```bash
git add .
git commit -m "Create Jekyll site"
git push
```

回到仓库的 **Settings → Pages**，在 **Build and deployment** 下把发布来源设为 **GitHub Actions**。用建议的 Jekyll 工作流配置发布，再到仓库的 **Actions** 页签查看构建和部署结果。

部署成功后，先用默认地址 `feelang.github.io` 验证。以后更新文章，把改动提交并推送即可。具体设置可参照 [GitHub Pages 发布来源说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

## 绑定自己的域名

当时我用 `feelang.xyz` 做示例。先在 Pages 的 **Custom domain** 填好域名，再到域名服务商的控制台调整 DNS。以[阿里云 DNS](https://dns.console.aliyun.com/)为例，`www` 子域名可用 `CNAME` 指向 `feelang.github.io`；根域名用服务商支持的 `ALIAS`、`ANAME` 或按 GitHub 的说明配置 `A` 记录。这里的 CNAME 是 DNS 别名，访问者的地址栏仍然可以显示自己的域名。

等解析生效，在 Pages 里开启 **Enforce HTTPS**，再用自定义域名打开网站确认。记录类型和核验步骤见 [GitHub Pages 自定义域名说明](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)。

写这篇文章时，我用 GitHub Pages 部署过这些站点：

| 域名 | 当时的用途 |
| --- | --- |
| [feelang.xyz](https://feelang.xyz) | 个人技术网站 |
| [liangfei.me](https://liangfei.me) | 个人网站 |
| [senluoshe.com](https://senluoshe.com) | 内容社区 |
| [everjapan.com](https://everjapan.com) | 内容社区 |
| [hefengcloud.com](https://hefengcloud.com) | 公司官网 |

