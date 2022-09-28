---
layout: post
title: Android 中 View 炸裂特效的实现分析
date: 2015-09-30
tags: Android
---

前几天微博上被一个很优秀的 Android 开源组件刷屏了 - [ExplosionField](https://github.com/tyrantgit/ExplosionField)，效果非常酷炫，有点类似 MIUI 卸载 APP 时的动画，先来感受一下。
![](https://github.com/tyrantgit/ExplosionField/raw/master/explosionfield.gif)

ExplosionField 不但效果很拉风，代码写得也相当好，让人忍不住要拿来好好读一下。

<!-- more -->

## 创建 ExplosionField

`ExplosionField` 继承自 `View`，在 `onDraw` 方法中绘制动画特效，并且它提供了一个 `attach2Window` 方法，可以把 `ExplosionField` 最为一个子 View 添加到 Activity 上的 root view 中。

```java
public static ExplosionField attach2Window(Activity activity) {
    ViewGroup rootView = (ViewGroup) activity.findViewById(Window.ID_ANDROID_CONTENT);
    ExplosionField explosionField = new ExplosionField(activity);
    rootView.addView(explosionField, new ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
    return explosionField;
}
```
`explosionField` 的 `LayoutParams` 属性都被设置为 `MATCH_PARENT`，
这样一来，一个 view 炸裂出来的粒子可以绘制在整个 Activity 所在的区域。

> 知识点：可以用 Window.ID_ANDROID_CONTENT 来替代 android.R.id.content

### 炸裂之前的震动效果

在 View 的点击事件中，调用 `mExplosionField.explode(v)`之后，View 首先会震动，然后再炸裂。

震动效果比较简单，设定一个 [0, 1] 区间 ValueAnimator，然后在 `AnimatorUpdateListener` 的 `onAnimationUpdate` 中随机平移 x 和 y坐标，最后把 scale 和 alpha 值动态减为 0。

```java
int startDelay = 100;
ValueAnimator animator = ValueAnimator.ofFloat(0f, 1f).setDuration(150);
animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {

    Random random = new Random();

    @Override
    public void onAnimationUpdate(ValueAnimator animation) {
        view.setTranslationX((random.nextFloat() - 0.5f) * view.getWidth() * 0.05f);
        view.setTranslationY((random.nextFloat() - 0.5f) * view.getHeight() * 0.05f);

    }
});
animator.start();
view.animate().setDuration(150).setStartDelay(startDelay).scaleX(0f).scaleY(0f).alpha(0f).start();
```

### 根据 View 创建一个 bitmap

View 震动完了就开始进行最难的炸裂，并且炸裂是跟隐藏同时进行的，先来看一下炸裂的 API - `void explode(Bitmap bitmap, Rect bound, long startDelay, long duration)`：

前两个参数 bitmap 和 bound 是关键，通过 View 来创建 bitmap 的代码比较有意思。

如果 View 是一个 ImageView，并且它的 Drawable 是一个 BitmapDrawable 就可以直接获取这个 Bitmap。

```java
if (view instanceof ImageView) {
    Drawable drawable = ((ImageView) view).getDrawable();
    if (drawable != null && drawable instanceof BitmapDrawable) {
        return ((BitmapDrawable) drawable).getBitmap();
    }
}
```

如果不是一个 ImageView，可以按照如下步骤创建一个 bitmap：

0. 新建一个 Canvas
0. 根据 View 的大小创建一个空的 bitmap
0. 把空的 bitmap 设置为 Canvas 的底布
0. 把 view 绘制在 canvas上
0. 把 canvas 的 bitmap 设置成 null

当然，绘制之前要清掉 View 的焦点，因为焦点可能会改变一个 View 的 UI 状态。
一下代码中用到的 sCanvas 是一个静态变量，这样可以节省每次创建时产生的开销。

```java
view.clearFocus();
Bitmap bitmap = createBitmapSafely(view.getWidth(),
        view.getHeight(), Bitmap.Config.ARGB_8888, 1);
if (bitmap != null) {
    synchronized (sCanvas) {
        Canvas canvas = sCanvas;
        canvas.setBitmap(bitmap);
        view.draw(canvas);
        canvas.setBitmap(null);
    }
}
```

作者创建位图的办法非常巧妙，如果新建 Bitmap 时产生了 OOM，可以主动进行一次 GC - `System.gc()`，然后再次尝试创建。

这个函数的实现方式让人佩服作者的功力。

```java
public static Bitmap createBitmapSafely(int width, int height, Bitmap.Config config, int retryCount) {
    try {
        return Bitmap.createBitmap(width, height, config);
    } catch (OutOfMemoryError e) {
        e.printStackTrace();
        if (retryCount > 0) {
            System.gc();
            return createBitmapSafely(width, height, config, retryCount - 1);
        }
        return null;
    }
}
```

出了 bitmap，还有一个一个很重要的参数 bound，它的创建相对比较简单：

```java
Rect r = new Rect();
view.getGlobalVisibleRect(r);
int[] location = new int[2];
getLocationOnScreen(location);
r.offset(-location[0], -location[1]);
r.inset(-mExpandInset[0], -mExpandInset[1]);
```

首先获取 **需要炸裂的View** 的全局可视区域 - `Rect r`，然后通过 `getLocationOnScreen(location)` 获取 `ExplosionField` 在屏幕中的坐标，并根据这个坐标把 **炸裂View** 的可视区域进行平移，这样炸裂效果才会显示在 `ExplosionField` 中，最后根据 mExpandInset 值（默认为 0）扩展一下。

那创建的 bitmap 和 bound 有什么用呢？我们继续往下分析。

### 创建粒子

先来看一下炸裂成粒子这个方法的全貌：

```java
public void explode(Bitmap bitmap, Rect bound, long startDelay, long duration) {
    final ExplosionAnimator explosion = new ExplosionAnimator(this, bitmap, bound);
    explosion.addListener(new AnimatorListenerAdapter() {
        @Override
        public void onAnimationEnd(Animator animation) {
            mExplosions.remove(animation);
        }
    });
    explosion.setStartDelay(startDelay);
    explosion.setDuration(duration);
    mExplosions.add(explosion);
    explosion.start();
}
```
这里要解释一下为什么用一个容器类变量 - `mExplosions` 来保存一个 `ExplosionAnimator`。因为 activity 中多个 View 的炸裂效果可能要同时进行，所以要把每个 View 对应的炸裂动画保存起来，等动画结束的时候再删掉。

作者自定义了一个继承自 ValueAnimator 的类 - ExplosionAnimator，它主要做了两件事情，一个是创建粒子 - `generateParticle`，另一个是绘制粒子 - `draw(Canvas canvas)`。

先来看一下构造函数：

```java
public ExplosionAnimator(View container, Bitmap bitmap, Rect bound) {
    mPaint = new Paint();
    mBound = new Rect(bound);
    int partLen = 15;
    mParticles = new Particle[partLen * partLen];
    Random random = new Random(System.currentTimeMillis());
    int w = bitmap.getWidth() / (partLen + 2);
    int h = bitmap.getHeight() / (partLen + 2);
    for (int i = 0; i < partLen; i++) {
        for (int j = 0; j < partLen; j++) {
            mParticles[(i * partLen) + j] = generateParticle(bitmap.getPixel((j + 1) * w, (i + 1) * h), random);
        }
    }
    mContainer = container;
    setFloatValues(0f, END_VALUE);
    setInterpolator(DEFAULT_INTERPOLATOR);
    setDuration(DEFAULT_DURATION);
}
```

根据构造函数可以知道作者把 bitmap 分成了一个 17 x 17 的矩阵，每个元素的宽度和高度分别是 `w` 和 `h`。
```java
int w = bitmap.getWidth() / (partLen + 2);
int h = bitmap.getHeight() / (partLen + 2);
```
所有的粒子是一个 15 x 15 的矩阵，元素色值是位图对应的像素值。
```java
bitmap.getPixel((j + 1) * w, (i + 1) * h)
```
结构如下图所示，其中空心部分是粒子。

<pre>
 ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ●
 ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
</pre>

`generateParticle` 会根据一定的算法随机地生成一个粒子。这部分比较繁琐，分析略去。

其中比较巧妙的还是它的 draw 方法：

```java
public boolean draw(Canvas canvas) {
    if (!isStarted()) {
        return false;
    }
    for (Particle particle : mParticles) {
        particle.advance((float) getAnimatedValue());
        if (particle.alpha > 0f) {
            mPaint.setColor(particle.color);
            mPaint.setAlpha((int) (Color.alpha(particle.color) * particle.alpha));
            canvas.drawCircle(particle.cx, particle.cy, particle.radius, mPaint);
        }
    }
    mContainer.invalidate();
    return true;
}
```

刚开始我还一直比较困惑，既然绘制粒子是在 `ExplosionField` 的 `onDraw` 方法中进行，那肯定需要不停地刷新，结果作者并不是这么做的，实现方法又着实惊艳了一把。

首先，作者在 `ExplosionAnimator` 类中重载了 `start()` 方法，通过调用 `mContainer.invalidate(mBound)` 来刷新 将要炸裂的 View 所对应的区块。

```java
@Override
public void start() {
    super.start();
    mContainer.invalidate(mBound);
}
```

而 mContainer 即是占满了 activity 的 view - `ExplosionField`，它的 `onDraw` 方法中又会调用 `ExplosionAnimator` 的 `draw` 方法。

```java
@Override
protected void onDraw(Canvas canvas) {
    super.onDraw(canvas);
    for (ExplosionAnimator explosion : mExplosions) {
        explosion.draw(canvas);
    }
}
```

这样便形成了一个递归，两者相互调用，不停地刷新，直到所有粒子的 alpha 值变为 0，刷新就停下来了。

```java
public boolean draw(Canvas canvas) {
    if (!isStarted()) {
        return false;
    }
    for (Particle particle : mParticles) {
        particle.advance((float) getAnimatedValue());
        if (particle.alpha > 0f) {
            mPaint.setColor(particle.color);
            mPaint.setAlpha((int) (Color.alpha(particle.color) * particle.alpha));
            canvas.drawCircle(particle.cx, particle.cy, particle.radius, mPaint);
        }
    }
    mContainer.invalidate();
    return true;
}
```

### 总结

这个开源库的代码质量相当高，十分佩服作者。

----

**关于我**

* [weibo](http://weibo.com/liangfeizc)
* [github](https://www.github.com/lyndonchin)
