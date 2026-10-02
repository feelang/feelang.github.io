---
title: 小程序【自律工具箱】上线图片分享功能
toc: false
classes: wide
categories: Frontend
tags:
    - 微信小程序
    - Canvas
---

> **自律工具箱**是我开发的一个小产品，主要来学习如何保持自律。

![自律工具箱小程序码](/assets/images/weapps/self-discipline-weapp.jpg)

这个小产品本来只是做给自己用的，没想到在朋友圈引起一些共鸣。

功能不多，一共四个模块：

- 50 Cognitive Biases（五十个认知偏见）
- The 7 Habits of Highly Effective People（高效能人士的七个习惯）
- Principles（原则）
- Business（商业）

其中我最满意的模块是【50 Cognitive Biases】，也是最早上线的。

因此这两天就给这个模块添加了图片分享功能，其它模块等优化好了再加。

最终效果如下：

Android | iOS
:---: | :---:
![](/assets/imgs/bias-android.jpeg) | ![](/assets/imgs/bias-ios.jpeg)

技术实现方案比较简单：

- 新增一个页面，专门用于生成图片
- 在页面中放置一个 `canvas` 元素，用于绘制文本和图片
- 当用户点击保存时，请求保存图片到相册的权限
- 当用户同意后，将 `canvas` 转化成图片，保存到相册

流程虽然简单，但背后隐藏了不少细节问题，我后面会单独写一篇博客来介绍。

除此之外，我在发布时还遇到一个问题：

> 体验版和开发版一切正常的情况下，线上版本无法保存图片。

这个问题很棘手，因为线上版本无法打日志，只能用 `wx.showModal` 展示错误信息，需要重新提交版本。

通过错误信息得知，使用保存图片这个功能需要**更新用户隐私协议**。

按照提示更改设置：

- 浏览器打开小程序管理后台
- 左侧菜单点击【设置】
- 找到【服务内容声明——用户隐私保护指引】

填写内容，更新隐私内容。

然后「保存图片到相册」的功能就可以用了。

但是当我又提交了一个版本，发布到线上之后却发现，分享又不能用了。

我分析肯定是配置的问题，于是改了一下代码，再次将错误信息通过 `wx.showModal` 展示出来。

改完之后提交发布申请，突然注意到，原来我上一个版本没有勾选「用户隐私保护指引设置——采集用户隐私」：

![小程序发版采集用户隐私](/assets/imgs/weapp-user-privacy.png)

勾选一下，发布新版本，功能一切正常。

可是当我用 iOS 测试时又发现，在生成图片的页面上，svg 格式的小图标根本无法展示，而 Android 却是正常的。

我猜测是小程序的 iOS 版本不支持将 svg 绘制到 canvas。

搜了一下，果不其然：

- [小程序 canvas   drawImage svg矢量图   真机不显示。。。希望官方后续能支持！！！](https://developers.weixin.qq.com/community/develop/doc/000cc84f42c4d88dda680b8a05b400)
- [如何把 svg 绘制到 canvas 中?](https://developers.weixin.qq.com/community/develop/doc/000282bbce0668da4bddcf72356c00)

原来 19 年就有人提出过这个问题了，看来小程序团队在两端一致性（consistency）的问题上还得努力，这跟 Google Flutter 的差距有点大。

看来没啥好办法，只好将所有的 svg 图片转化成了 jpg。

> 以下代码是 ChatGPT 帮忙生成的，我只改了文件路径的变量。

```python
# Specify the input folder containing SVG images
input_folder = '~/Source/feelang/self-discipline-toolbox-weapp/miniprogram/images/biases'

# Specify the output folder for the converted JPG images
output_folder = '~/Source/hefengcloud/hefeng-content/self-discipline/images/jpgs'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all files in the input folder
files = os.listdir(input_folder)

# Iterate over each file in the input folder
for file in files:
    # Check if the file is an SVG image
    if file.lower().endswith('.svg'):
        # Specify the input SVG file path
        svg_file = os.path.join(input_folder, file)

        # Specify the output JPG file path
        jpg_file = os.path.join(
            output_folder, os.path.splitext(file)[0] + '.jpg')

        # Convert SVG to PNG using cairosvg
        cairosvg.svg2png(url=svg_file, write_to=jpg_file)

        # Open the converted PNG image
        image = Image.open(jpg_file)

        # Convert PNG to JPG using PIL
        image.convert('RGB').save(jpg_file, 'JPEG')
```

