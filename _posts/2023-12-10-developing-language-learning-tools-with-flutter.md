---
title: Flutter 和日语
---

> Updated at 2025-10-09

我在想，**当初为什么会固执地选择 Flutter？**

- 路径依赖，我在最后一家公司上班时用 Flutter 开发过一款同时上线了 GooglePlay 和 AppStore 的 App 产品，积累了一定开发经验。
- Android 开发出身，对 Google 产品天然抱有好感（比如 Material Design）。
- 商业经验不足，高估了 App 在商业起步阶段的价值，「产品本位思想」作祟。实际上，早期更重要的是渠道。
- 被 Flutter 的营销策略所吸引，想照搬到日语业务。

那现在**为什么决定弃用 Flutter 呢？**

- 生态跟不上 iOS 的进化脚步（比如「毛玻璃」、Apple Watch）。
- Android 国内市场赚不到钱，只做 iOS 就行。
- Flutter 做的 iOS App 提审很麻烦。
- iOS 生态更繁荣、更有噱头、更有性价比。

过去两年**Flutter 帮我创造了哪些价值？**

- 开发了 Mac 桌面应用 SenluoStudio，有效支撑起社媒运营。（现在 work with Claude Code，非常高效）
- 参考 Flutter Widget of the Week 上线了「JLPT 语法讲义」系列视频，微信视频号涨粉显著。

**全面拥抱 iOS 生态，用 SwiftUI 开发 App 产品！**

---

> 以下内容写于 2023 年底。

听说很多企业正在弃用 Flutter，重回原生。

这个现象可能存在，但不会影响我继续使用 Flutter 的决心。

原因有两点：

1. 个人精力有限，无法顾及多端开发。
2. 从之前的经验来看，Flutter 足够用于应付小型应用。

除此之外，Flutter 新推出的两个 App Solution 和我目前的产品方向高度契合：

- 资讯类（日语/历史）App - [Flutter News Toolkit](https://docs.flutter.dev/resources/news-toolkit)

> 25.10.9 ⚠️　这类 App 获客极难，小团队根本不足以生产出留存用户的内容

- 学习类小游戏 - [Casual Games Toolkit](https://docs.flutter.dev/resources/games-toolkit)

> 25.10.9 ⚠️　获客难不说，设计也很难

再加上昨天冒出来的新想法：**用 Flutter 制作日语学习的 slideshow。**

> 25.10.9
>
> 这个功能已经在 SenluoStudio 实现了：JLPT 语法讲义系列。
>
> SenluoStudio 会持续更新下去，用上 Claude Code 之后，不太需要自己写代码了。

Flutter 好像成了不二之选。

这样我就可以继续磨练编程技能，还不耽误「日语学习」。

> 25.10.9
>
> 不需要再磨练编程技能，时代变了

具体要如何执行呢？

**1) 熟练掌握 Flutter 常用的 widgets 和 packages：**

- [Widget catalog](https://docs.flutter.dev/ui/widgets)
- [Flutter Widget of the Week](https://www.youtube.com/playlist?list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)
- [Flutter Favorites](https://pub.dev/packages?q=is%3Aflutter-favorite)

尤其是 [Animation and motion](https://docs.flutter.dev/ui/widgets/animation)

暂时用 Notion 来记录学习成果，等内容完善之后，整理成文本类教程。

> 25.10.9
> 
> Notion 已经弃用，改用 Obsidian。另外，单纯积累笔记没有意义，不如直接用起来，或者记到脑子里。留在笔记软件里只会成为”死“内容，还不如遇到问题去问 AI。

**2) 制作日语内容生成工具——[senluo_japanese_cms](https://github.com/feelang/senluo_japanese_cms)**

> 25.10.9
>
> 以下列出的很多功能已经上线，而且不止这些。

- [x] 假名
- [x] 文法
- [x] 单词
- [x] 汉字
- [x] 习语
- [x] 拟声拟态词
- [ ] 常用表达
- [ ] 敬语

**3) 制作日语学习 APP 并完成上线**

> 25.10.9
>
> 以后我会用 SwiftUI 开发 App

- 日语五十音
- 日语语法

