CSS Transitions 让我们不写一行 JavaScript 代码也能实现过渡动画。

举一个最简单的例子：

```css
a:link {
    color: hsl(36,50%,50%);
}
a:hover {
    color: hsl(36,100%,50%);
}
```

当鼠标悬浮于某个链接时，它的颜色会从 `hsl(36,50%,50%)` 瞬间变化为 `hsl(36,100%,50%)`。 这个变化因为没有过渡，会显得特别生硬。

有了 `transition` 属性，我们便可以实现一个非常平滑的过渡效果，它也是一个简写属性，取值由以下部分构成：

* `transition-property` - 目标属性
* `transition-duration` - 过渡时长
* `transition-timing-function` - 缓动函数：匀速、加速以及减速。
* `transtion-delay` - 动画触发的等待时长

我们把上面的 CSS 稍作修改：

```css
a:link {
    transition: all .5s linear 0;
    color: hsl(36,50%,50%);
}
a:hover {
    color: hsl(36,100%,50%);
}
```

动画效果就有了，当鼠标悬浮在链接上时，颜色会发生渐变，非常平滑。

这里的 `transition` 表示所有的属性在半秒内完成线性过渡，没有延迟。

> 注意，这么多渐变属性中，只有 `transition-duration` 是必需的，其它都有默认值：
> * `transition-property: all;`
> * `transition-timing-function: ease;`
> * `transition-delay: 0;`
>
> 所以最简单的渐变可以写成 `transition: .5s.`。

## 特定属性

虽然 "all" 可以让渐变作用于所有属性，但我们仍然可以指定某个属性，例如 `transition: color .5s ease 0` 将只作用于颜色属性。

也可以同时指定多个属性，中间用逗号隔开：

```css
a:link {
    transition: .5s;
    transition-property: color, font-size;
}
```

还可以同时指定多条渐变规则：

```css
a:link {
    transition: color .5s, font-size 2s;
}
```

## 缓动

`transition-timing-function` 类似于数学表达式 `velocity = func(time)`，它会根据时间来改变动画速度，一般称作「差值函数」。

它的变化是一个三次贝塞尔曲线，取值有 `ease` 和 `linear` 两类。
* `ease` 表示先加速后减速。可拆分成 `ease-in` 和 `ease-out`。
* `linear` 表示匀速。

> [cubic-bezier.com](https://cubic-bezier.com/) 很好了演示了这两种动画。