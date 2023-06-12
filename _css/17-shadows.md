阴影可以让元素“浮起来”，盒元素和文本都适用。

## 盒阴影

`box-shadow` 属性值有一串：

```css
box-shadow: 5px 5px 3px 1px #999
```

1. 第一个值表示水平位移，正数往右，负数往左
1. 第二个值表示垂直位移，正数往下，负数往上
1. 第三个值表示模糊半径，值越小，越锐利。这个值可以省略，默认取值为 0
1. 第四个值表示延展距离，值约大，阴影越大。这个值也可以省略，默认取值为 0
1. 第五个值表示颜色。可以省略。

### 内部阴影

`box-shadow` 还可以设置内部阴影，只需要在值列表中加一个 "inset"：

```css
box-shadow: inset 0 0 7px 5px #ddd;
```

<img src="https://htmldog.com/figures/boxshadow.png" width="250">


## 文本阴影

`box-shadow` 作用于盒元素（box）。`text-shadow` 作用于文本。

```css
text-shadow: -2px 2px 2px #999;
```

1. 第一个值表示水平位移
1. 第二个值表示垂直位移
1. 第三个值表示模糊半径（可选）
1. 第三个值表示颜色（可选）

注意，`text-shadow` 没有延展距离，也没有内部阴影（"inset" 值）。