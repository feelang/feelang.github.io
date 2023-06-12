---
title: 布局
permalink: /tutorials/css/layout/
---

现代 CSS 的布局可以说已经变得非常简单，遥想当年，人们只能用 HTML tables 来布局，可谓往事不可回首。

## 位置（Positioning）

`position` 属性用于定义一个盒元素的位置类型，它的取值包含：
* `static` - 静态位置布局，也是默认方式，浏览器会按照元素在 HTML 中出现的顺序进行布局
* `relative` - 相对位置布局，类似于 `static`，不过可以通过 `top`、`right`、`bottom` 和 `left` 来设置它相对于原点的位置
* `absolute` - 绝对位置布局，这种方式会让盒元素游摆脱正常的 HTML 流，变成完全游离的状态，可通过 `top`、`right`、`bottom` 和 `left` 来任意控制它在页面中的位置
* `fixed` - 固定位置布局，类似于 `absolute`，不过它的坐标系不是整个页面，而是浏览器窗口，所以特别适用于页面滚动的场景

### 绝对位置布局

借助 `absolute` 我们可以实现一个传统的两列式布局。

先写 HTML：

```html
<div id="navigation">
    <ul>
        <li><a href="this.html">This</a></li>
        <li><a href="that.html">That</a></li>
        <li><a href="theOther.html">The Other</a></li>
    </ul>
</div>

<div id="content">
    <h1>Ra ra banjo banjo</h1>
    <p>Welcome to the Ra ra banjo banjo page. Ra ra banjo banjo. Ra ra banjo banjo. Ra ra banjo banjo.</p>
    <p>(Ra ra banjo banjo)</p>
</div>
```

然后下面这段 CSS 代码应用上去：

```css
#navigation {
    position: absolute;
    top: 0;
    left: 0;
    width: 200px;
}

#content {
    margin-left: 200px;
}
```

一个传统的两列式布局就出现了，左边导航，右边内容。

![](images/two-columns.png)

因为左侧导航应用了 `position: aboslute` 的属性，所以就脱离了正常的 HTML 流，页面其他元素跟它也没什么关系了。

因此我们必须给 `#content` 增加一个 `margin-left` 的属性，值就是导航栏的宽度 `200px`。

按照这个思路，我们可以在右侧再增加一列导航：

```css
#navigation {
    position: absolute;
    top: 0;
    left: 0;
    width: 200px;
}

#navigation2 {
    position: absolute;
    top: 0;
    right: 0;
    width: 200px;
}

#content {
    margin: 0 200px; /* setting top and bottom margin to 0 and right and left margin to 200px */
}
```

页面变成这个样子：

![](images/three-columns.png)

`position: absolute` 能满足一些简单需求，但是它无法满足宽度值或者大小值需要动态计算的需求，因为 `position: absolute` 处理游离态，跟页面其他元素无法产生联动。

如果要在上面的示例代码中添加一个 footer，它就无能为力了。这时候需要用到 `float`。

## 浮动（Floating）

所谓浮动是指将盒元素移动到一行的左边或右边，它四周的内容会绕着它流动（flow）。

浮动通常作用于页面中的小模块，比如容器右侧的导航链接，但也可以用于大模块，比如导航列。

`float` 的取值有两个：`left` 和 `right`。

我们把上面示例代码中的 CSS 替换为如下内容：

```css
#navigation {
    float: left;
    width: 200px;
}

#navigation2 {
    float: right;
    width: 200px;
}

#content {
    margin: 0 200px;
}
```

效果是一样的。

我们还可以通过 CSS 的 `clear` 属性控制浮动对象的下一个元素是否可以绕过它：

* `clear: left` - 清楚左侧的浮动盒元素
* `clear: right` - 清楚右侧的浮动盒元素
* `clear: both` - 清楚两侧的浮动盒元素

页面内的 footer 就可以这么实现：

```html
<div id="footer">
    <p>Footer! Hoorah!</p>
</div>
```

应用下面的 CSS：

```css
#footer {
    clear: both;
}
```

这样一搞，footer 就会一直出现在所有列的底部。

![](images/footer.jpg)