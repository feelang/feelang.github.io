---
layout: post
title: Beautiful CSS
date: 2017-08-22
categories: CSS
---

BACKGROUND
---
* _Multiple overlapping backgrounds on one element_
* _Multiple background layers stack top to bottom, in the order declared. The color layer is always at the bottom_

```css
.multi-bg {
  background-image: url(img/spades.png), url(img/hearts.png),
                    url(img/diamonds.png), url(clubs.png);
  background-position: left top, right top, left bottom, right bottom;
  background-repeat: no-repeat, no-repeat, no-repeat, no-repeat;
  background-color: pink;
}
```
⇩  short
```css
.multi-bg-shorthand {
  background: url(img/spades.png) left top no-repeat,
              url(img/hearts.png) right top no-repeat,
              url(img/diamonds.png) left bottom no-repeat,
              url(img/clubs.png) right bottom no-repeat,
              pink;
}
```
⇩  short
```css
.multi-bg-shorthand {
  background: url(img/spades.png) left top,
              url(img/hearts.png) right top,
              url(img/diamonds.png) left bottom,
              url(img/clubs.png) right bottom,
              pink;
              background-repeat: no-repeat; /* goes for all four */
}
```

TRANSFORM
---
* rotate
* scale
* move
* skew
* etc.

```css
.zan-toast {
  transform: translateY(-100%);
}
```
_`-100%`表示自身宽度的100%。_

POSITION
---
* Elements are initially positioned as `static`, meaning that block-level elements stack up vertically.
* We can give elements `relative` positioning, allowing us to nudge them around relative to their original position without altering the flow of elements around them. **Doing so also creates a new positioning context for descendant elements.**
* `Absolute` positioning allows us to give an element an exact position with regard to the nearest positioning context, which is either an ancestor with a positioning other than static, or the html element. In this model, elements are lifted out of the page flow, and put back relative to their positioning context. By default, they end up where they originally should have ended up were they static, but without affecting the surrounding elements. We can then choose to change their position, relative to the positioning context.
* `Fixed` positioning is basically the same as absolute, but the positioning context is automatically set to the **browser viewport**.

> **The very nature of absolute positioning** makes it an ideal candidate for creating things like overlays, tooltips, and dialog boxes that sit on top of other content.

> Applying absolute positioning to the comment lifts it out of the flow, but by default leaves it in the place where it would originally have ended up with a static position

NEGATIVE MARGINS
---

* [The Definitive Guide to Using Negative Margins](https://www.smashingmagazine.com/2009/07/the-definitive-guide-to-using-negative-margins/)
* Negative top and left margins move the element up and left while negative right and bottom margins make following siblings move left and up.

_more..._

* A negative margin to the left or top will pull the element in that direction, overlapping any elements next to it.
* A negative right or bottom margin will pull in any adjacent elements so that they overlap the element with the negative margin.
* On a floated element, a negative margin opposite the float direction will decrease the float area, causing adjacent elements to overlap the floated element. A negative margin in the direction of the float will pull the floated element in that direction.
* Finally, the behavior of negative margins to the sides is slightly moderated when used on a nonfloating element without a defined width. In that case, negative margins to the left and right sides both pull the element in that direction. This expands the element, potentially overlapping any adjacent elements.


FLEX BOX
---
* [Flexy Boxes](http://the-echoplex.net/flexyboxes/)
* Control [order | size | distribution | alignment]

![](/assets/imgs/flex.jpeg)

> Items inside a flex container shrink down to this size if no other sizing is in place. 

```css
.navbar ul {
  display: flex;
  /* this also implies flex-direction: row; unless told otherwise */
  flex-direction: row-reverse;
  justify-content: flex-end | justify-content | space-between | space-around
  align-items: flex-start | center | flex-end
}
```
> Flexbox calls distribution along the main axis justification, while distribution on the cross axis is called alignment.

FLEXIBLE SIZING
---
* flex-basis
* flex-grow
* flex-shrink
