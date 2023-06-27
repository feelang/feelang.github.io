---
title: 【小程序】如何用 Canvas 绘制分享用的图片
classes: wide
excerpt: 
categories: fontend
tags:
  - 小程序
  - canvas
---

上一篇**【小程序】如何实现滑动翻页**中介绍了如何在小程序中实现上下滑动翻页的效果。

如果要给这个产品增加一个生成图片用于分享到朋友圈的功能，又该如何实现呢？

先来看一下最终的效果图：

<img src="/assets/imgs/bias-ios.jpeg" width="300px">

首先，新建一个页面（page），布局文件如下：

```html
<!-- pages/biases/share.wxml -->
<view class="container">
  <canvas id="myCanvas" type="2d" />
  <view class="save-btn" bind:tap="onSavePicture">
    <text>Save to Album</text>
  </view>
</view>
```

这里 `id=myCanvas` 的 `canvas` 就是我们需要绘制图片用的画布。

它的 CSS 属性如下：

```css
#myCanvas {
  margin: 40rpx 0;
  width: calc(100% - 80rpx);
  height: 80%;
  box-shadow: 2px 2px 16px 4px rgba(0, 0, 0, 0.2);
}
```

CSS 属性 |  含义
--- | ---
`margin: 40rpx 0;` | 设置元素上下的边距为40rpx（rpx是微信小程序中的响应式像素单位），左右边距为0
`width: calc(100% - 80rpx);` | 将元素的宽度设置为其父容器宽度减去80rpx
`height: 80%;` | 将元素的高度设置为其父容器高度的80%
`box-shadow: 2px 2px 16px 4px rgba(0, 0, 0, 0.2);` | 给元素应用一个阴影效果，水平偏移量为2px，垂直偏移量为2px，模糊半径为16px，扩展半径为4px，颜色为rgba(0, 0, 0, 0.2)（表示稍微透明的黑色）

布局和样式都非常简单，难点是用 js 代码绘制图片，由于篇幅有限，这里只分享技术要点，完整版代码可参考 => [pages/biases/share.js](https://github.com/feelang/self-discipline-toolbox-weapp/blob/main/miniprogram/pages/biases/share.js)

## 获取 canvas 实例

```javascript
const query = wx.createSelectorQuery()
query.select('#myCanvas')
  .fields({ node: true, size: true })
  .exec(res => { 
    //... 
  })
```

这段代码是微信小程序中使用 `wx.createSelectorQuery` 来选取ID为 `myCanvas` 的元素，并获取其节点信息和尺寸的示例代码。

具体解释如下：

* `const query = wx.createSelectorQuery()`： 创建一个选择器查询实例。
* `query.select('#myCanvas')`： 通过选择器 `#myCanvas` 选取ID为 `myCanvas` 的元素。
* `.fields({ node: true, size: true })`：指定要获取的字段，包括节点信息和尺寸信息。
* `.exec(res => { ... })`：执行查询操作，并在回调函数中处理查询结果。查询结果会作为参数 `res` 传递给回调函数。

然后我们可以根据实际需求，在回调函数中对获取的节点信息和尺寸进行处理，例如进行布局调整或其他操作。

其中 `res` 是一个数组，其中包含了查询结果的信息。

在执行 `query.exec()` 方法后，查询结果会作为一个数组传递给回调函数。数组的每个元素对应一个查询操作的结果，如果在 `query.select()` 中指定了多个选择器，那么数组中就会有多个元素。

每个元素都包含了指定字段的查询结果，可以通过索引来访问每个结果。例如，如果只有一个选择器查询的结果，可以通过 `res[0]` 来访问。

以上示例代码中，`res` 数组中只有一个元素，即 `res[0]`，该元素包含了 `#myCanvas` 元素的节点信息和尺寸信息。我们可以通过 `res[0].node` 来访问节点信息，通过 `res[0].width` 和 `res[0].height` 来访问宽度和高度的尺寸信息。

要注意，如果在 `query.select()` 中指定了多个选择器，那么数组中会有多个元素，每个元素对应一个选择器的查询结果。你可以根据自己的需求使用循环或条件语句来处理多个查询结果。

继续看代码，我们在 `exec` 的回调函数中，保存 canvas 和它的尺寸信息，因为后面会用到。

```javascript
const canvas = res[0].node
const width = res[0].width
const height = res[0].height
this.canvas = canvas
```

然后通过 `canvas.getContext('2d')` 来获取 2D 绘图上下文对象。这个上下文对象（通常称为 ctx）提供了一系列方法和属性，用于在 Canvas 上进行绘图和图形操作。

```javascript
const ctx = canvas.getContext('2d')
```

这里需要指出的是，`wx.createSelectorQuery()` 返回的 `size` 信息是基于**逻辑尺寸**的，而不是**物理尺寸**。

也就是说，`size` 属性表示节点的尺寸信息，但它是相对于小程序逻辑尺寸而言的，而非设备的物理尺寸。

小程序的逻辑尺寸是指开发者在编写小程序时使用的尺寸单位，通常是以 `rpx`（响应式像素）为单位。而物理尺寸则是指设备的实际像素尺寸，通常以设备的物理像素为单位（如像素）。

因此，在使用 `wx.createSelectorQuery()` 获取节点的尺寸信息时，需要根据实际场景进行适当的转换，例如根据设备的像素比 `pixelRatio` 进行逻辑尺寸到物理尺寸的转换，以便正确地进行绘制或布局操作。

注意：在使用 `size` 属性时，需要考虑到小程序的视口、屏幕方向以及可能的样式布局等因素，以确保得到准确的尺寸信息。

```javascript
const dpr = wx.getSystemInfoSync().pixelRatio
canvas.width = width * dpr
canvas.height = height * dpr
ctx.scale(dpr, dpr)
```

通过以上代码，我们首先计算出 `canvas` 的物理尺寸并赋值给 `canvas`，然后通过调用 `ctx.scale(dpr, dpr)` 修改画布的分辨率。

这样一来，我们后续的绘制可以基于逻辑像素（`rpx`）来计算尺寸。

逻辑像素和物理像素的转换关系可以用下面这个公式来计算：

```
rpx = dpr * px
```

画布准备就绪之后，就可以进行绘制了。

## 绘制矩形

绘制一个白色的矩形，并将其填充整个 Canvas 区域，用作背景色。

```javascript
ctx.fillStyle = 'white'
ctx.fillRect(0, 0, width, height)
```

## 绘制多行文本

绘制单行文本很简单，多行文本稍微复杂一些，因为 canvas 并不支持自动换行，我们只有手动换行。

首先设置基础样式：

```javascript
ctx.fillStyle = 'black'
ctx.font = 'bold 30px sans-serif'
```

然后将长文本按照指定的最大宽度进行分行处理。

我将这个功能封装成了一个小函数：

```javascript
_splitTextToLines(ctx, maxWidth, text) {
  let words = text.split(' ');
  let totalWidth = 0;
  let lineIndex = 0;
  let lineWords = [];
  const lines = [];
  words.forEach(word => {
    const wordWidth = ctx.measureText(word).width;
    totalWidth = totalWidth + wordWidth;
    if (totalWidth >= maxWidth) {
      totalWidth = 0;
      lines[lineIndex] = lineWords;
      lineIndex++;
      lineWords = [word];
    } else {
      lineWords.push(word);
    }
  });
  if (lineWords.length > 0) {
    lines[lineIndex] = lineWords;
  }
  return lines;
}
```

以上代码定义了一个名为 `_splitTextToLines` 的函数，接受三个参数：

- `ctx` 是绘图上下文对象
- `maxWidth` 是指定的最大宽度
- `text` 是待分行处理的文本。

在函数内部，首先将文本按照空格进行分割，得到一个单词数组 `words`。然后，定义了一些变量用于跟踪总宽度、行索引和当前行的单词。

接下来，通过遍历单词数组，使用 `ctx.measureText(word).width` 获取每个单词的宽度，并累加到总宽度 `totalWidth` 上。

如果累加的总宽度超过了最大宽度 `maxWidth`，则表示当前行已满，需要将当前行的单词数组 `lineWords` 添加到结果数组 `lines` 中，并重置总宽度和当前行的单词数组。

如果累加的总宽度未超过最大宽度，则将当前单词添加到当前行的单词数组 `lineWords` 中。

遍历结束后，如果当前行的单词数组 `lineWords` 不为空，则将其添加到结果数组 `lines` 中。

最后，返回包含分行结果的数组 `lines`。

这段代码的作用是将给定的文本按照最大宽度进行分行处理，确保每行的宽度不超过最大宽度，并返回分行结果。

然后我们就可以绘制返回的多行文本：

```javascript
_drawLines(ctx, lines, yOffset, canvasWidth, lineHeight) {
  let height = 0;
  lines.forEach((line, idx) => {
    let text = line.join(' ');
    let textWidth = ctx.measureText(text).width;
    height = yOffset + lineHeight * idx;
    ctx.fillText(text, parseInt((canvasWidth - textWidth) / 2), height);
  });
  return lines;
}
```

这段代码定义了一个名为 `_drawLines` 的函数，接受五个参数：

- `ctx` 是绘图上下文对象
- `lines` 是包含分行文本的数组
- `yOffset` 是垂直偏移量
- `canvasWidth` 是画布宽度
- `lineHeight` 是行高。

在函数内部，首先定义了一个变量 `height`，用于跟踪每行文本的垂直位置。

然后，通过遍历 `lines` 数组，对于每一行文本，将单词数组 `line` 使用空格连接成一个字符串 `text`。

使用 `ctx.measureText(text).width` 获取字符串 `text` 的宽度，以便进行水平居中。

计算当前行的垂直位置，使用公式 `height = yOffset + lineHeight * idx`。

最后，使用 `ctx.fillText` 在画布上绘制文本，传入文本字符串 `text`、水平位置 `parseInt((canvasWidth - textWidth) / 2)` 和垂直位置 `height`。

遍历结束后，返回分行文本的数组 `lines`。

这段代码的作用是在画布上绘制多行文本，确保每行文本居中显示，并返回分行文本的数组。

OK，我们将以上代码串接起来，就实现了绘制多行文本的功能：

```javascript
// Draw the title
ctx.fillStyle = 'black'
ctx.font = 'bold 30px sans-serif'
const titleLines = this._splitTextToLines(ctx, width - 100, title)
this._drawLines(ctx, titleLines, y, width, 35)
```

## 绘制图片

以下代码的作用是在画布上绘制一个二维码图片，并确保图片加载完成后进行绘制操作。

```javascript
let qrImg = canvas.createImage();
const qrImgSrc = `../../images/qrcode.jpg`;
const qrImgWidth = qrCodeImgSize;
const qrImgHeight = qrCodeImgSize;
qrImg.src = qrImgSrc;
qrImg.onload = () => {
  ctx.drawImage(qrImg, horizontalMargin, height - qrCodeImgSize - verticalMargin, qrImgWidth, qrImgWidth);
};
```

代码解释如下：

首先，通过 `canvas.createImage()` 创建了一个图片对象 `qrImg`。

定义了变量 `qrImgSrc` 存储二维码图片的路径。

定义了变量 `qrImgWidth` 和 `qrImgHeight` 来指定绘制的二维码图片的宽度和高度，其中 `qrCodeImgSize` 是二维码图片的大小。

将 `qrImg.src` 设置为二维码图片的路径，以加载图片。

使用 `qrImg.onload` 事件处理程序，在图片加载完成后执行绘制操作。

在 `qrImg.onload` 事件处理程序中，使用 `ctx.drawImage` 方法在画布上绘制二维码图片。参数依次为：

- 绘制的图片对象 `qrImg`
- 绘制的水平位置 `horizontalMargin`
- 绘制的垂直位置 `height - qrCodeImgSize - verticalMargin`
- 绘制的宽度 `qrImgWidth`
- 绘制的高度 `qrImgWidth`。

## 将绘制结果保存为图片

首先，保存画布内容为临时文件：

```javascript
onSavePicture() {
  let that = this
  setTimeout(() => {
    wx.canvasToTempFilePath({
      canvas: this.canvas,
      success: res => {
        const tempFilePath = res.tempFilePath
        that.shareImage(tempFilePath)
      },
      fail: res => {
        console.log(res)
      }
    })
  }, 100)
},
```

在函数内部，使用 `setTimeout` 延迟执行一段代码。这里延迟了 100 毫秒执行。

在延迟执行的代码块中，调用了微信小程序的 `wx.canvasToTempFilePath` 方法。该方法将画布内容转换为临时文件。

通过 `canvas: this.canvas` 指定要转换的画布对象。

在转换成功时，通过 `success` 回调函数获取到转换后的临时文件路径 `res.tempFilePath`。

然后调用 `that.shareImage(tempFilePath)` 将临时文件路径传递给 `shareImage` 函数进行处理。

在转换失败时，通过 `fail` 回调函数打印错误信息到控制台。

这段代码的作用是在一定延时后将当前画布内容转换为临时文件，并将临时文件路径传递给 `shareImage` 函数进行处理。

```javascript
async shareImage(url) {
  let that = this
  // 验证用户是否拥有保存到相册的权限
  wx.getSetting({
    success: res => {
      if (res.authSetting['scope.writePhotosAlbum']) {
        // 用户已授权
        that.saveImage(url);
      } else if (res.authSetting['scope.writePhotosAlbum'] !== undefined) {
        // 用户首次进入还未调起权限相关接口
        that.openSetting();
      } else {
        // 用户首次进入
        that.saveImage(url);
      }
    },
    fail: () => {
      wx.showModal({ content: '获取授权信息失败' })
    }
  })
},
```

`shareImage` 是一个异步函数，在函数内部，通过 `wx.getSetting` 方法验证用户是否拥有保存到相册的权限。

在 `getSetting` 方法的 `success` 回调函数中，根据用户的授权情况进行不同的处理。

如果用户已经授权保存到相册，即 `res.authSetting['scope.writePhotosAlbum']` 返回 `true`，则调用 `that.saveImage(url)` 方法保存图片。

如果 `res.authSetting['scope.writePhotosAlbum']` 不为 `undefined`，表示用户首次进入小程序还未调起权限相关接口，此时调用 `that.openSetting()` 方法引导用户打开权限设置页面。

如果以上两种情况都不满足，表示用户首次进入小程序，直接调用 `that.saveImage(url)` 方法保存图片。

在 `getSetting` 方法的 `fail` 回调函数中，如果获取授权信息失败，则通过 `wx.showModal` 方法显示一个模态框提示用户。

这段代码的作用是验证用户的保存到相册权限，并根据授权情况进行不同的处理。

如果权限获取成功，则将图片保存到相册：

```javascript
// 保存图片
saveImage(url) {
  let that = this;
  wx.showLoading({ title: 'Saving...' });  // 显示加载提示框
  wx.saveImageToPhotosAlbum({
    filePath: url,  // 要保存的图片路径
    success: (res) => {
      wx.hideLoading();  // 隐藏加载提示框
      wx.showToast({ icon: 'success', title: 'Saved' });  // 显示保存成功的提示
    },
    fail: (res) => {
      wx.hideLoading();  // 隐藏加载提示框
      wx.showModal({ content: `Failed: ${JSON.stringify(res)}` });  // 显示保存失败的提示，并打印错误信息
    }
  });
},
```

这段代码的作用是在保存图片到相册过程中显示加载提示框，保存成功后显示一个成功的提示，保存失败后显示一个失败的提示，并打印错误信息。

- 首先，使用 `wx.showLoading` 方法显示一个加载提示框，标题为 "Saving..."，提示用户正在保存图片。
- 然后，使用 `wx.saveImageToPhotosAlbum` 方法保存图片到相册，传入要保存的图片路径 `url`。
- 在 `success` 回调函数中，表示保存图片成功，隐藏加载提示框，并使用 `wx.showToast` 方法显示一个成功的提示，图标为 'success'，标题为 'Saved'。
- 在 `fail` 回调函数中，表示保存图片失败，隐藏加载提示框，并使用 `wx.showModal` 方法显示一个模态框，其中的内容是保存失败的提示，并将错误信息以字符串的形式进行显示。

以上就是用 Cavnas 绘制分享图片的核心代码，希望对你有所帮助。

---

* 扫码体验

![自律工具箱小程序码](https://img-blog.csdnimg.cn/14680898fc624c939d682c0d515d6538.jpeg)

* 代码仓库：[self-discipline-toolbox-weapp](https://github.com/feelang/self-discipline-toolbox-weapp/tree/main/miniprogram/pages/biases)
