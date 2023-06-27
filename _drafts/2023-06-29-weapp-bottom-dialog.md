---
title: 【小程序】如何实现从底部弹出对话框
toc: false
classes: wide
categories: Frontend
tags:
    - 微信小程序
---

{% raw %}

前面两篇两篇文章介绍了如何在小程序中实现上下滑动效果以及如何用 Canvas 绘制一张图片，这一篇作为前两篇的延续，介绍如何从底部弹出一个对话框。

相比而言，底部弹出对话框的功能比较通用，因此非常适合定义成组件（component）。

先来看一会最终实现效果：

<img src="/assets/imgs/weapp-bottom-dialog.gif" width="300px">

首先是布局文件：

```xml
<view wx:if='{{visible}}'>
  <view class='wrap {{wrapAnimate}}' style='background:rgba(0,0,0,{{bgOpacity}});'></view>
  <view catchtap='hideFrame' class='frame-wrapper {{frameAnimate}}'>
    <view catchtap='catchNone' class='frame'>
      <view class="share-btn-wrapper">
        <button class="share-btn" open-type='share'>
          <image src="../images/share.svg" />
        </button>
        <button class="share-btn" bindtap="onShareToMoments">
          <image src="../images/moments.svg" />
        </button>
      </view>
    </view>
  </view>
</view>
```

这段代码是一个包含条件渲染、点击事件和图像的小程序视图结构。根据不同的条件和用户的交互，将显示不同的视图元素，并触发相应的事件处理函数。

我们来逐行分析下：

- `<view wx:if='{{visible}}'>`：这是一个条件渲染的语法，只有当 `visible` 变量为真时，才会渲染下面的内容。
- `<view class='wrap {{wrapAnimate}}' style='background:rgba(0,0,0,{{bgOpacity}});'></view>`：这是一个空的视图元素，应用了名为 `wrap` 的类和 `wrapAnimate` 变量作为类名。还设置了背景颜色为 rgba(0,0,0,{{bgOpacity}})。`bgOpacity` 变量用于控制背景透明度。
- `<view catchtap='hideFrame' class='frame-wrapper {{frameAnimate}}'>`：这是一个视图元素，应用了名为 `frame-wrapper` 的类和 `frameAnimate` 变量作为类名。还定义了一个点击事件 `catchtap`，当被点击时会触发名为 `hideFrame` 的事件处理函数。
- `<view catchtap='catchNone' class='frame'>`：这是一个视图元素，应用了名为 `frame` 的类。同样，定义了一个点击事件 `catchtap`，当被点击时会触发名为 `catchNone` 的事件处理函数。
- `<view class="share-btn-wrapper">`：这是一个视图元素，应用了名为 `share-btn-wrapper` 的类。
- `<button class="share-btn" open-type='share'>`：这是一个按钮元素，应用了名为 `share-btn` 的类，并设置了 `open-type` 属性为 `'share'`。这意味着点击按钮时会触发微信的分享功能。
- `<image src="../images/share.svg" />`：这是一个图像元素，用于显示名为 `share.svg` 的图像文件。
- `<button class="share-btn" bindtap="onShareToMoments">`：这是一个按钮元素，应用了名为 `share-btn` 的类，并定义了一个点击事件 `bindtap`，当被点击时会触发名为 `onShareToMoments` 的事件处理函数。
- `<image src="../images/moments.svg" />`：这是一个图像元素，用于显示名为 `moments.svg` 的图像文件。

其中第一个子元素的CSS 类 `.wrap` 将创建一个占据整个屏幕的固定定位的元素，它的层叠顺序为 1，位置固定在窗口的左上角，并且宽度和高度均占满整个窗口。 用于创建遮罩层或全屏背景等效果。

```css
.wrap {
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
```

变量 `wrapAnimate` 有两个取值，分别是 `.wrapAnimate` 和 `.wrapAnimateOut`，一个控制淡入动画，一个控制淡出动画。


`.wrapAnimate` 的代码如下：

```css
.wrapAnimate {
  animation: wrapAnimate 0.5s ease-in-out forwards
}

@keyframes wrapAnimate {
  0% {}

  100% {
    background: rgba(0, 0, 0, 0.35);
  }
}
```

该动画将在 0.5 秒内逐渐将元素的背景颜色变为半透明的黑色。动画结束后，元素将保持最后一个关键帧的状态。

- `animation: wrapAnimate 0.5s ease-in-out forwards;`：通过 `animation` 属性指定了动画的名称、持续时间、动画速度和结束后的状态。
  - `wrapAnimate` 是动画的名称，表示要应用的关键帧动画。
  - `0.5s` 是动画的持续时间，表示动画从开始到结束所需的时间，这里是 0.5 秒。
  - `ease-in-out` 是动画的速度曲线，表示动画在开始和结束时会缓慢变化，而在中间阶段会加速变化。
  - `forwards` 表示动画结束后元素将保持最后一个关键帧的状态。

- `@keyframes wrapAnimate { ... }`：定义了名为 `wrapAnimate` 的关键帧动画。
  - `0% {}`：表示动画的起始关键帧，这里为空，表示没有任何样式。
  - `100% { background: rgba(0, 0, 0, 0.35); }`：表示动画的结束关键帧，在动画完成时，背景颜色将变为 RGBA 值为 `rgba(0, 0, 0, 0.35)`，即半透明的黑色背景。


`.wrapAnimateOut` 的代码如下：

```css
.wrapAnimateOut {
  animation: wrapAnimateOut 0.2s ease-in-out forwards
}

@keyframes wrapAnimateOut {
  0% {
    background: rgba(0, 0, 0, 0.35);
  }

  100% {
    background: rgba(0, 0, 0, 0);
  }
}
```

该动画将在 0.2 秒内逐渐将元素的背景颜色从半透明的黑色变为完全透明，使元素逐渐消失。动画结束后，元素将保持最后一个关键帧的状态。

- `.wrapAnimateOut` 是一个类名，表示要应用的动画效果。
- `animation: wrapAnimateOut 0.2s ease-in-out forwards;`：通过 `animation` 属性指定了动画的名称、持续时间、动画速度和结束后的状态。
  - `wrapAnimateOut` 是动画的名称，表示要应用的关键帧动画。
  - `0.2s` 是动画的持续时间，表示动画从开始到结束所需的时间，这里是 0.2 秒。
  - `ease-in-out` 是动画的速度曲线，表示动画在开始和结束时会缓慢变化，而在中间阶段会加速变化。
  - `forwards` 表示动画结束后元素将保持最后一个关键帧的状态。

- `@keyframes wrapAnimateOut { ... }`：定义了名为 `wrapAnimateOut` 的关键帧动画。
  - `0% { background: rgba(0, 0, 0, 0.35); }`：表示动画的起始关键帧，在动画开始时，背景颜色为半透明的黑色。
  - `100% { background: rgba(0, 0, 0, 0); }`：表示动画的结束关键帧，在动画完成时，背景颜色将完全透明，即不可见。


第二个子元素 `<view>` 通过 CSS 类 `.frame-wrapper` 和变量 `{{frameAnimate}}` 来控制动画效果。

其中 `.frame-wrapper` 的定义如下：

```css
.frame-wrapper {
  position: fixed;
  height: 100vh;
  width: 100vw;
  z-index: 2;
  top: 50vh;
}
```

这段代码用于创建一个具有固定定位的元素，该元素的高度和宽度均占满整个视口，垂直居中定位，并位于其他具有较低 `z-index` 值的元素之上。

- `position: fixed;`：设置元素的定位方式为固定定位，这意味着元素将相对于视口固定位置，不会随滚动而移动。
- `height: 100vh;`：设置元素的高度为视口的高度，即占满整个可视区域的高度。
- `width: 100vw;`：设置元素的宽度为视口的宽度，即占满整个可视区域的宽度。
- `z-index: 2;`：设置元素的堆叠顺序，即元素在重叠时的层级顺序。具有较高 `z-index` 值的元素将显示在具有较低 `z-index` 值的元素之上。
- `top: 50vh;`：将元素的顶部边缘与视口垂直中心对齐，即垂直居中定位。


变量 `frameAnimte` 的取值也是两个：`frameAnimate` 和 `frameAnimateOut`，分别用于控制淡入和淡出动画：

```javascript
.frameAnimate {
  animation: frameAnimate 0.5s ease forwards;
}

@keyframes frameAnimate {
  0% {}

  100% {
    opacity: 1;
    top: 0vh;
  }
}

.frameAnimateOut {
  animation: frameAnimateOut 0.2s ease forwards;
}

@keyframes frameAnimateOut {
  0% {
    opacity: 1;
    top: 0vh;
  }

  100% {
    opacity: 0;
    top: 100vh;
  }
}
```

以上代码定义了两个动画：

- `.frameAnimate` 动画将元素的不透明度设为 1，并使其从顶部进入视口，
- `.frameAnimateOut` 动画将元素的不透明度设为 0，并使其从当前位置向视口底部移出。

```css
.frame {
  background: #fff;
  position: absolute;
  bottom: 0;
  width: 88.2vw;
  padding: 5.9vw 5.9vw 0;
  border-top-left-radius: 20rpx;
  border-top-right-radius: 20rpx;
  z-index: 3;
}
```

`.frame` 定义了一个底部弹出框或浮动窗口的样式，具有白色背景、圆角边框和一定的宽度。该元素的位置会相对于其最近的定位父元素进行定位，并且位于其他元素的上方，z-index 值为 3。

<img src="/assets/imgs/weapp-bottom-dlg-frame.jpeg" width="300px">

其代码含义如下：

- `background: #fff;`：指定了元素的背景颜色为白色（#fff）。
- `position: absolute;`：将元素的定位方式设置为绝对定位，相对于其最近的非静态定位父元素定位。
- `bottom: 0;`：将元素的底部边缘与父元素的底部边缘对齐。
- `width: 88.2vw;`：将元素的宽度设置为视口宽度的 88.2%。
- `padding: 5.9vw 5.9vw 0;`：设置元素的内边距，上方为视口宽度的 5.9%，左右方向为视口宽度的 5.9%，下方为 0。
- `border-top-left-radius: 20rpx;`：设置元素的左上角边框半径为 20 像素。
- `border-top-right-radius: 20rpx;`：设置元素的右上角边框半径为 20 像素。
- `z-index: 3;`：指定元素的堆叠顺序，具有更高的 z-index 值的元素将覆盖具有较低 z-index 值的元素。

通过以上代码可以看出，决定动画框架的一共有三个 `<view>`，其所对应的 css 分别是：

- `wrap`
- `frame-wrapper`
    - `frame`

它们三者的布局关系，可以用一张图来表示：

![](/assets/imgs/weapp-bottom-animation.png)

布局和展示关系定义好之后，最后我们来看下对应的 js 代码：

0. 展示

    ```javascript
    showFrame() {
        this.setData({ 
            visible: true, 
            wrapAnimate: 'wrapAnimate', 
            frameAnimate: 'frameAnimate' 
        });
    }
    ```

0. 隐藏

    ```javascript
    hideFrame(e) {
        let that = this
        this.setData({ wrapAnimate: 'wrapAnimateOut', frameAnimate: 'frameAnimateOut' });
        setTimeout(() => {
            that.setData({ visible: false })
        }, 200);
    }
    ```

用法很简单：

```xml
<share-dialog id="bottomFrame" bindsharetomoments="onShareToMoments"></share-dialog>
```

其中 `bindsharetomoments` 的代码定义在组件的 js 文件中：

```javascript
onShareToMoments(e) {
    this.hideFrame()
    this.triggerEvent('sharetomoments')
}
```

以上就是如何实现从底部弹出对话框的全部代码，希望对你有所帮助。

---

扫码体验： ![](/assets/images/weapps/self-discipline-weapp.jpg)

代码仓库：[self-discipline-toolbox-weapp](https://github.com/feelang/self-discipline-toolbox-weapp/tree/main/miniprogram/pages/biases)

{% endraw %}