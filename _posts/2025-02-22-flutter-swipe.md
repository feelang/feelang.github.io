---
layout: single
title: Flutter 手势交互代码的实现
categories: programming
tags:
    - Flutter
---

## 左右滑动

```dart
GestureDetector(
    onHorizontalDragEnd: (DragEndDetails details) {
        if (details.primaryVelocity != null) {
            if (details.primaryVelocity > 0) {
                // swipe to right
            } else if (details.primaryVelocity < 0) {
                // swipe to left
            }
        }
    }
)

```

解释：

- `primaryVelocity`：表示拖动结束时的水平速度（单位：像素/秒）
    - 正数： 表示用户向右滑动（速度方向向右）
    - 负数： 表示用户向左滑动（速度方向向左）
    - 零： 表示滑动速度接近零，可能只是轻触或几乎没有移动

