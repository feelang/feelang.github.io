---
layout: single
title: Anko 的设计之道
date: 2018-05-17
categories: Kotlin Android
---

[Anko](https://github.com/kotlin/anko) 是一个完全基于 Kotlin 设计的 Android 三方库，名字来自于 Android Kotlin 这两个单词的前两个字母。Anko 试图建立一套新的 Android 开发范式， 虽然不会成为主流，但是它的设计思想值得我们借鉴。

## 新的 UI 体系

先看一下 Anko 用于构建 UI 的几个关键类：

    +--------------+
    | ViewManaager |
    +-------.------+
           /|\
            |
    +---------------+
    |  AnkoContext  |<--------------+
    +-------.-------+               |
           /|\                      |
            |                       |
    +-----------------+   +-----------------------+
    | AnkoContextImpl |   | DelegatingAnkoContext |
    +-------.---------+   +-----------------------+
           /|\
            |
    +---------------------+
    | ReusableContextImpl |
    +---------------------+

这里需要强调的是，`AnkoContext` 继承自 `ViewManager`，而不是 `android.content.Context`。刚开始读源码时，总会觉得 `AnkoContext` 的命名有点反直觉，但是，就像文章一开始所说的——“Anko 试图建立一套新的 Android 开发范式” ——其实 `AnkoContext` 和 `android.content.Context` 之间是并列关系。

就像 Android 需要基于 `Context` 来创建一个 `View` 一样，Anko 创建 UI 组件也需要基于 `AnkoContext`。

既然 `AnkoContext` 与 `android.content.Context` 是并列关系，那么大部分为 `android.content.Context` 定义扩展的地方也定义了 `AnkoContext` 的扩展。例如 `Dimensions.kt` 文件：

```kotlin
fun Context.dip(value: Int): Int = (value * resources.displayMetrics.density).toInt()
inline fun AnkoContext<*>.dip(value: Int): Int = ctx.dip(value)
inline fun View.dip(value: Int): Int = context.dip(value)
inline fun Fragment.dip(value: Int): Int = activity.dip(value)
```

Anko 的 UI 组件用一个接口 `AnkoComponent` 来表示，接口内提供了一个模板方法 `createView`：

```kotlin
interface AnkoComponent<in T> {
    fun createView(ui: AnkoContext<T>): View
}
```

可以看出，`AnkoComponent` 的类型参数（type parameter）是一个逆变的声明处变型（declaration-site variance），模板方法 `createView` 的作用是基于 `AnkoContext<T>` 实例创建一个 `View`。

`AnkoContext` 继承自 `ViewManager`，也是一个接口，它“内藏”了 Android 的 `android.content.Context` 实例，同时还定义了一个类型为 `T` 的属性 `owner` 用于表示 `AnkoContext` 的拥有者。`AnkoContext` 没有对类型参数 `T` 加以限定，任何类型都可以。

```kotlin
interface AnkoContext<out T> : ViewManager {
  val ctx: Context
  val owner: T
  val view: View

  override fun updateViewLayout(view: View, params: ViewGroup.LayoutParams) {
    throw UnsupportedOperationException()
  }

  override fun removeView(view: View) {
    throw UnsupportedOperationException()
  }

  companion object {
    fun create(ctx: Context, setContentView: Boolean = false): AnkoContext<Context>
          = AnkoContextImpl(ctx, ctx, setContentView)

    fun createReusable(ctx: Context, setContentView: Boolean = false): AnkoContext<Context>
          = ReusableAnkoContext(ctx, ctx, setContentView)

    fun <T> create(ctx: Context, owner: T, setContentView: Boolean = false): AnkoContext<T>
          = AnkoContextImpl(ctx, owner, setContentView)

    fun <T> createReusable(ctx: Context, owner: T, setContentView: Boolean = false): AnkoContext<T>
          = ReusableAnkoContext(ctx, owner, setContentView)

    fun <T: ViewGroup> createDelegate(owner: T): AnkoContext<T> = DelegatingAnkoContext(owner)
  }
}
```

`AnkoContext` 还通过伴生对象（companion object）提供了五个工厂方法，它们生产出来的对象都是 `AnkoContext` 的子类，上面的类关系图已经展示出了它们之间的关系。

`AnkoContextImpl` 是 `AnkoContext` 接口的具体实现，覆写了 `ViewManager#addView` 方法：

```kotlin
override fun addView(view: View?, params: ViewGroup.LayoutParams?) {
  if (view == null) return

  if (myView != null) {
    alreadyHasView()
  }

  this.myView = view

  if (setContentView) {
    doAddView(ctx, view)
  }
}
```

我们来分析一下 `addView` 的具体实现：

参数 `view: View?` 是一个可空类型，但是 `AnkoContext` 的属性 `view: View` 是一个非可空类型，所以 `AnkoContextImpl` 重新定义了一个属性 `var myView: View?` 用于存储参数 `view: View?`：

```kotlin
private var myView: View? = null

override val view: View
  get() = myView ?: throw IllegalStateException("View was not set previously")
```

`AnkoContextImpl` 的构造方法多了一个属性参数 `setContentView: Boolean`，它表示是否要把 `addView` 的参数 `view` 设置为属性 `ctx: Context` 的 content view：

```kotlin
private fun doAddView(context: Context, view: View) {
  when (context) {
    is Activity -> context.setContentView(view)
    is ContextWrapper -> doAddView(context.baseContext, view)
    else -> throw IllegalStateException("Context is not an Activity, can't set content view")
  }
}
```

`ReusableAnkoContext` 继承自 `AnkoContextImpl`，两者唯一的不同点在于 `ReusableAnkoContext` 的 `alreadHasView` 是一个空实现，而 `AnkoContextImpl` 会抛出一个异常，它不支持 view 复用。

`DelegatingAnkoContext` 是 `AnkoContext` 的另一个实现：

```kotlin
internal class DelegatingAnkoContext<T: ViewGroup>(override val owner: T): AnkoContext<T> {
  override val ctx: Context = owner.context
  override val view: View = owner

  override fun addView(view: View?, params: ViewGroup.LayoutParams?) {
    if (view == null) return

    if (params == null) {
      owner.addView(view)
    } else {
      owner.addView(view, params)
    }
  }
}
```

`DelegatingAnkoContext` 的类型参数指定了 upper bound —— `<T: ViewGroup>`，也就是说 `DelegatingAnkoContext` 的 `owner` 必须是 `ViewGroup` 或者它的子类。

关于 `DelegatingAnkoContext` 名字中的 `Delegating` 应该是为了表达属性 `view: View` 代理了（delegating）`owner: T`：

```kotlin
override val view: View = owner
```

再来回看一下这几个类的继承关系：

* `AnkoContext` 继承自 `ViewManager`
* `AnkoContextImpl` 和 `DelegatingAnkoContext` 实现了 `AnkoContext`
* `ReusableContextImpl` 继承自 `AnkoContextImpl`。

```
+--------------+
| ViewManaager |
+-------.------+
       /|\
        |
+---------------+
|  AnkoContext  |<--------------+
+-------.-------+               |
       /|\                      |
        |                       |
+-----------------+   +-----------------------+
| AnkoContextImpl |   | DelegatingAnkoContext |
+-------.---------+   +-----------------------+
       /|\
        |
+---------------------+
| ReusableContextImpl |
+---------------------+
```


## 基于 DSL 实现 UI 布局

DSL 可以用于取代手写 XML 布局，其优势如下：
* 类型安全：编译阶段就能够发现类型错误，而且不会出现 NPE
* 代码复用：可封装 View 的创建逻辑
* 性能提升：节省了 inflate 的运行开销

先来看一段代码：

```kotlin
verticalLayout {
    padding = dip(32)

    imageView(android.R.drawable.ic_menu_manage).lparams {
        margin = dip(16)
        gravity = Gravity.CENTER
    }

    val name = editText {
        hintResource = R.string.name
    }
    val password = editText {
        hintResource = R.string.password
        inputType = TYPE_CLASS_TEXT or TYPE_TEXT_VARIATION_PASSWORD
    }

    button("Log in") {
        onClick {
            ui.owner.tryLogin(ui, name.text, password.text)
        }
    }

    myRichView()
}.applyRecursively(customStyle)
```

在 Anko 新的 UI 体系中，`AnkoComponent` 表示一个 UI 组件，模板方法 `createView` 返回 `View` 实例，上面的代码即可作为 `createView` 的函数内容，返回值是一个 vertical 的 `LinearLayout`。

加上 `AnkoComponent` 把上面的代码补全：

```kotlin
class MainActivityUi : AnkoComponent<MainActivity> {
  private val customStyle = { v: Any ->
    when (v) {
      is Button -> v.textSize = 26f
      is EditText -> v.textSize = 24f
    }
  }
  override fun createView(ui: AnkoContext<MainActivity>) = with(ui) {
    relativeLayout {
      // ...
    }.applyRecursively(customStyle)
  }
}
```

我们来分析一下 `relativeLayout` 如何成为 `ui: AnkoContext<MainActivity>` 的 content view。

首先，`relativeLayout` 是 `ViewManager` 的扩展函数，返回值是一个 `LinearLayout`：

```kotlin
inline fun ViewManager.verticalLayout(theme: Int = 0, init: (@AnkoViewDslMarker _LinearLayout).() -> Unit): LinearLayout {
  return ankoView(`$$Anko$Factories$CustomViews`.VERTICAL_LAYOUT_FACTORY, theme, init)
}
```

然后，它会调用 `ViewManager` 的另一个扩展函数——`ankoView`：

```kotlin
inline fun <T : View> ViewManager.ankoView(factory: (ctx: Context) -> T, theme: Int, init: T.() -> Unit): T {
  val ctx = AnkoInternals.wrapContextIfNeeded(AnkoInternals.getContext(this), theme)
  val view = factory(ctx)
  view.init()
  AnkoInternals.addView(this, view)
  return view
}
```

`ankoView` 会调用 `AnkoInternals#addView`：

```kotlin
fun <T : View> addView(manager: ViewManager, view: T) = when (manager) {
  is ViewGroup -> manager.addView(view)
  is AnkoContext<*> -> manager.addView(view, null)
  else -> throw AnkoException("$manager is the wrong parent")
}
```

也就是说，`verticalLayout` 函数会把它所创建的 `LinearLayout` 作为 child view 添加到接收者（receiver）中，这里是 `ViewManager`。

再回到 `AnkoComponent` 的 `createView`：

```kotlin
override fun createView(ui: AnkoContext<MainActivity>) = with(ui) {
  verticalLayout {
    // ...
  }
}
```

`with(ui)` 会把 `ui: AnkoContext<MainActivity>` 作为第二个参数（用大括号表示的高阶函数）的 receiver，也就是说 高阶函数内的 `this` 会指向变量 `ui`。这样的话，`AnkoInternals.addView(this, view)` 会调用到 `AnkoContext` 的 `addView` 方法，具体如何处理取决于接口 `AnkoContext` 的具体实现。

下面举例来展示它们的用法。

### 自定义 View

```kotlin
class RichView : LinearLayout {
  private lateinit var image: ImageView
  private lateinit var text: TextView

  private fun init() = AnkoContext.createDelegate(this).apply {
    gravity = CENTER
    padding = dip(24)

    image = imageView(imageResource = R.drawable.kotlin) {
      onClick { startAnimation() }

      padding = dip(8)
      layoutParams = LinearLayout.LayoutParams(dip(48), dip(48))
    }

    text = textView("Anko Rich view") {
      textSize = 19f
    }

    startAnimation()
  }

  // ...
}
```

`AnkoContext.createDelegate` 创建了一个 `DelegatingAnkoContext`，它的 owner 和 view 都是 `this`，也就说扩展函数 `image`、`text` 所创建的 view 都会作为 child view 添加给 `this`。

### Activity 的 content view

```kotlin
class MainActivity : AppCompatActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    val adapter = ProverbAdapter(this, proverbs)
    MainActivityUI(adapter).setContentView(this)
  }
}

class MainActivityUI(private val adapter: ProverbAdapter) : AnkoComponent<MainActivity> {
  override fun createView(ui: AnkoContext<MainActivity>) = with(ui) {
    relativeLayout {
      recyclerView {
        layoutManager = LinearLayoutManager(context, LinearLayoutManager.VERTICAL, false).apply {
          adapter = this@MainActivityUI.adapter
        }
      }.lparams(width = matchParent, height = matchParent)
    }.apply {
      layoutParams = FrameLayout.LayoutParams(matchParent, matchParent).apply {
        padding = dip(16)
      }
    }
  }
}
```

`MainActivityUI` 是 `AnkoComponent<MainActivity>` 的子类，类型实参 `<MainActivity>` 表示 `AnkoContext` 的 `owner` 的类型。

创建完 `MainActivityUI` 的实例之后，用法就变得非常简单，直接调用它的扩展函数 `setContentView`：

```kotlin
MainActivityUI(adapter).setContentView(this)
```

`setContentView` 会创建一个 `AnkoContextImpl` 类型的实例，然后把这个实例作为参数调用 `createView`。

```
fun <T : Activity> AnkoComponent<T>.setContentView(activity: T): View =
    createView(AnkoContextImpl(activity, activity, true))
```

### RecyclerView.ViewHolder

首先用 `AnkoComponent` 定义 item 的 UI 组件。

```kotlin
class ProverbComponent(val ui: AnkoContext<ProverbAdapter>) : AnkoComponent<ProverbAdapter> {
  lateinit var category: TextView
  lateinit var title: TextView

  fun createView() = createView(ui)

  override fun createView(ui: AnkoContext<ProverbAdapter>) = with (ui) {
    linearLayout {
      category = textView {
        textColor = Color.RED
      }

      textView {
        text = ": "
      }

      title = textView {
        textColor = Color.BLUE
      }
    }
  }
}
```

然后用 `ViewHolder` 来 hold 这个组件。

```kotlin
class ViewHolder(val ankoComponent: ProverbComponent) : RecyclerView.ViewHolder(ankoComponent.createView())
```

创建组件所使用的 `AnkoContext` 是 `ReusableAnkoContext`。

```kotlin
class ProverbAdapter(context: Context, private val items: List<Proverb>) : RecyclerView.Adapter<ViewHolder>() {
  private val ankoContext: AnkoContext<ProverbAdapter> = AnkoContext.createReusable(context, this)

  override fun onBindViewHolder(holder: ViewHolder, position: Int) {
    holder.ankoComponent.category.text = items[position].category
    holder.ankoComponent.title.text = items[position].phrase
  }

  override fun getItemCount(): Int {
    return items.size
  }

  override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
    return ViewHolder(ProverbComponent(ankoContext))
  }
}
```

## 总结

Anko 这种基于 DSL 的布局方式可以算得上是一股清流，虽然在执行效率上面有所提升，但是从开发效率和分工协作的角度来看，DSL 算不上是一种高效的方式。

我们都知道，用 Sketch 画 UI 肯定比手写代码的方式效率高，无论是 Android 还是 iOS，UI 的布局方式都在朝着“拖拽”的方向演进，比如 `ConstraintLayout`、`AutoLayout`，设计稿直接转换为 XML 布局文件也已经指日可待。除此之外，逻辑代码和布局代码混在一起的方式也不便于代码维护。

UI 布局只是 Anko 的功能之一，有时间了再分析一下 Anko Coroutines 的实现。
