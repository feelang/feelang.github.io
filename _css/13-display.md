HTML 元素最常用的展示方式有内联（inline）、区块（block）和不展示（none）。它们可以通过 `display` 属性来控制，对应的值分别为 `inline`、`block` 和 `none`。

## 内联

`inline` 是按照线的流向来展示元素。例如，锚点（链接）和强调（emphasis）默认就是这种展示方式。

![](https://htmldog.com/figures/displayInline.png)

例如，下面的代码会改变列表的默认展示方式，所有的列表项变成了左右排列，不再独占一行：

```css
li { display: inline }
```

## 区块

`block` 会让元素独占一行，宽度铺满父级元素。

相比内联，区块可以更精确地控制盒模型的高度、外边距和内边距。HTML的 标题和段落默认就是这种展示方式。

![](https://htmldog.com/figures/displayBlock.png)

如下代码会让导航中的 `<a>` 展示为更大的区块：

```css
#navigation a {
    display: block;
    padding: 20px 10px;
}
```

`display: inline-block` 可以实现元素的内联的情况下还可以精确控制盒模型，兼具 `inline` 和 `block` 的优势。

## 不展示

`none` 可以让一个元素不展示，特别适合需要展示/隐藏的场景。

下面的代码，用于隐藏导航的相关链接。

```css
#navigation, #related_links { display: none }
```

> 注意，`display: none` 和 `visibility: hidden` 有本质区别，`display: none` 会页面完全去掉这个元素，而 `visibility: hidden` 的元素仍然出现在页面中，也会占据位置，只不过没有显示出来。

## 表格

`table` 有些复杂，而且很少会用到。

理解 `display: table` 的最佳方式就是类比 HTML 的 `table` 元素

* `table-row` 相当于 `tr`
* `table-cell` 相当于 `td`

除此之外，还有更多表格相关的 `display` 值：

* `table-column`
* `table-row-group`
* `table-column-group`
* `table-header-group`
* `table-footer-group`
* `table-caption`

最后还有个 `inline-table`，支持内联的表格。

> 注意，尽量慎用表格，因为在一些老的浏览器上，可能会遇到稀奇古怪的问题。

## 其他显示类型

* `display: list-item` - 类似于 HTML 的 `<li>` 元素。为了显示正常，要嵌套在 `<ul>` 或 `<ol>` 元素内使用
* `display: run-in` - 展示方式取决于父级元素
* `display: flex` - flex 布局，功能十分强大，以后会讲到