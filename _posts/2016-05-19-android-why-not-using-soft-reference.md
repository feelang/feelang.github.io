---
layout: post
title: SoftReference 为什么被 Android “放弃”
date: 2016-05-19
categories: Android
---

JDK 中除了默认的 Strong Reference 之外，还有三个其他的 Reference：

* WeakReference
* SoftReference
* PhantomReference

他们都是为了更高效地利用 Heap。

<!-- more -->

WeakReference
---
如果一个变量的 Reference 只剩下 `WeakReference`，那么 GC 会毫不留情地把这个变量回收掉。也就是说，`WeakReference` 没有能力能够让这个变量可以在内存中再飞一会。

Android 开发者应该都了解 `WeakReference` 的用法，一个比较典型的应用场景是 `Handler` ，为了避免 Memory Leak，我们会定义一个内部静态类，然后以 `WeakReference` 的形式引用 `Activity`，这样一来，队列中的 `Message` （可能会排队很长时间）就不会干扰到 GC 回收 `Activity`。

```java
public class MainActivity extends Activity {
    private static final int MSG_ID = 0x00;

    public void testSafeHandler() {
        SafeHandler handler = new SafeHandler(this);
        handler.sendEmptyMessage(MSG_ID);
    }

    public static class SafeHandler extends Handler {
        private WeakReference<Activity> mActivityRef;
        public SafeHandler(Activity activity) {
            mActivityRef = new WeakReference<>(activity);
        }

        public void handleMessage(Message msg) {
            switch (msg.what) {
                case MSG_ID:
                    Activity activity = mActivityRef.get();
                    if (activity != null) {
                        activity.finish();
                    }
            }
        }
    }
}
```

SoftReference
---

从 [SoftReference 的官方定义][oracle-softreference] 来看，只有当内存告急（即将 OOM）时，才会对只剩下 Soft Reference 的变量进行回收，因此 SoftReference 比较适合用来做 Cache：

> Soft references are most often used to implement memory-sensitive caches.

但是 [SoftReference 的 Android 版本][android-softreference] 对此**持不同意见**：

> In practice, soft references are inefficient for caching.

因为 SoftReference 无法提供足够的信息可以让 runtime 很轻松地决定 clear 它还是 keep 它。举个例子，如果有 10 个 SoftReference 变量，并且他们所引用的变量都没有了 Strong Reference，那么 runtime 就懵逼了，因为它不知道该 clear 哪几个或者 keep 哪几个。更要命的是，runtime 不知道应该是 clear 掉 SoftReference 还是增大 Heap。

所以 Android 放弃了 `SoftReference`，推荐使用 `android.util.LruCache` 做 Cache 管理，至少 `LruCache` 可以根据变量的**使用频次**来决定是否应该 clear 掉它，这样就比单纯使用 `SoftReference` 多了一个决策条件 - 使用频次。

[oracle-softreference]:https://docs.oracle.com/javase/7/docs/api/java/lang/ref/SoftReference.html
[android-softreference]:https://developer.android.com/reference/java/lang/ref/SoftReference.html
