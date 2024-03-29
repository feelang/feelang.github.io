---
layout: single
title: 「译」精通Kotlin标准函数：run、with、let、also和apply
date: 2018-03-31
categories: Programming
tags:
  - Kotlin
---

> 原文地址：https://medium.com/@elye.project/mastering-kotlin-standard-functions-run-with-let-also-and-apply-9cd334b0ef84

一些 Kotlin 的[标准函数](https://github.com/JetBrains/kotlin/blob/master/libraries/stdlib/src/kotlin/util/Standard.kt)非常相似，以至于我们都无法确定要使用哪一个。这里我会介绍一种简单的方式来区分他们的不同点以及如何选择使用。

## 作用域函数

接下来聚焦的函数有：`run`、`with`、`T.run`、`T.let`、`T.also` 以及 `T.apply`。我称他们为**作用域函数**（scoping functions），因为它们为调用方函数提供了一个内部作用域。

最能够体现作用域的是 `run` 函数：

```kotlin
fun test() {
    var mode = "I am sad"

    run {
        val mood = "I am happy"
        println(mood) // I am happy
    }

    println(mood) // I am sad
}
```

基于此，在 `test` 函数内部，你可以拥有一个单独的区域，在这个作用域内，`mood` 在打印之前被重新定义成了 `I am happy`，并且它完全被包裹（enclosed）在 `run` 的区域内。

这个作用域函数本身看起来并不会非常有用。但是除了拥有单独的区域之外，它还有另一个优势：它有返回值，即区域内的最后一个对象。

因此，下面的代码会变得整洁，我们把 `show()` 函数应用到两个 view 之上，但是并不需要调用两次。

```kotlin
run {
    if (firstTimeView) introView else normalView
}.show()
```

> 这里演示所用，其实还可以简化为 `(if (firstTimeView) introView else normalView).show()`。

## 作用域函数三大特性

为了让作用域函数更有意思，可将其行为分类为三大特性。我会使用这些特性来区分彼此。

### 一、正常 vs. 扩展函数

如果我们看一下 `with` 和 `T.run`，会发现它们的确非常相似。下面的代码做了同样的事情。

```kotlin
with(webview.settings) {
    javaScriptEnabled = true
    databaseEnabled = true
}

// similarly

webview.settings.run {
    javaScriptEnabled = true
    databaseEnabled = true
}
```

但是，它们的不同点在于，一个是正常函数（即 `with`），另一个是扩展函数（即 `T.run`）。

假设 `webview.settings` 可能为空，那么代码就会变成下面的样子：

```kotlin
// Yack!
with(webview.settings) {
    this?.javaScriptEnabled = true
    this?.databaseEnabled = true
}

// Nice
webview.settings?.run {
    javaScriptEnabled = true
    databaseEnabled = true
}
```

在这个案例中，`T.run` 的扩展函数明显要好一些，因为我们可以在使用前就做好了空检查。

### 二、this vs. it 参数
如果我们看一下 `T.run` 和 `T.let`，会发现两个函数是相似的，只有一点不同：它们接收参数的方式。下面代码展示了用两个函数实现同样的逻辑：

```kotlin
stringVariable?.run {
    println("The length of this String is $length")
}

// Similarly

stringVariable?.let {
    println("The length of this String is ${it.length}")
}
```

如果检查一下 `T.run` 的函数签名就会发现 `T.run` 只是一个调用 `block: T.()` 的扩展函数。因此在它的作用域内，`T` 可以被引用为 `this`。实际编程中，`this` 大部分情况下都可以被省略。因此，在上面的例子中，我们可以在 `println` 的声明语句中使用 `$length` 而不是 `${this.length}`。我把它称之为：**this 作为参数**进行传递。

但是，对于 `T.let` 函数，你会发现 `T.let` 把它自己传入了函数 `block: (T)`。因此它被当做一个 lambda 参数来传递。在作用域函数内它可以被引用为 `it`。所以我称之为：**it 作为参数**进行传递。

从上面可以看出，`T.run` 好像比 `T.let` 高级，因为它更隐式一些，但是 `T.let` 函数会有些一些微妙的优势：

* `T.let` 可以更清楚地区分所得变量和外部类的函数/成员。
* `this` 不能被省略的情况下，例如用作一个函数参数，`it` 比 `this` 更短更清晰。
* `T.let` 允许用更好的命名来表示转换过的所用变量（the converted used variable），也就是说，你可以把 `it` 转换为其他名字：

    ```kotlin
    stringVariable?.let {
        nonNullString ->
        println("The non null string is $nonNullString")
    }
    ```

### 三、返回 this vs. 其他类型

现在，我们看一下 `T.let` 和 `T.also`，如果我们看一下函数作用域内部的话，会发现两者是一样的：

```kotlin
stringVariable?.let {
    println("The length of this String is ${it.length}")
}

// Exactly the same as below

stringVariable?.also {
    println("The length of this String is ${it.length}")
}
```

但是，它们微妙的区别之处在于返回了什么。`T.let` 返回了一个不同类型的值，但是 `T.also` 返回了 `T` 自身，也就是 `this`。

简单的示例如下：

```kotlin
val original = "abc"

// Evolve the value and send to the next chain
original.let {
    println("The original String is $it") // "abc"
    it.reversed() // evolve it as parameter to send to next let
}.let {
    println("The reverse String is $it") // "cba"
    it.length // can be evolve to other type
}.let {
    println("The length of the String is $it") // 3
}

// Wrong
// Same value is sent in the chain (printed answer is wrong)
original.also {
    println("The original String is $it") // "abc"
    it.reversed() // even if we evolve it, it is useless
}.also {
    println("The reverse String is ${it}") // "abc"
    it.length // even if we evolve it, it is useless
}.also {
    println("The length of the String is ${it}") // "abc"
}

// Corrected for also (i.e. manipulate as original string
// Same value is sent in the chain
original.also {
    println("The original String is $it") // "abc"
}.also {
    println("The reverse String is ${it.reversed()}") // "cba"
}.also {
    println("The length of the String is ${it.length}") // 3
}
```

上面的 `T.also` 貌似没什么意义，因为我们可以轻松把它们组合进一个单一的函数块内。仔细想一下，它们会有如下优势：

* 它可以为相同的对象提供清晰的处理流程，可以使用粒度更小的函数式部分。
* 它可以在被使用之前做灵活的自处理（self manipulation），可以创建一个链式构造器操作。

如果两者结合链式来使用，一个进化自己，一个持有自己，就会变得非常强大，例如：

```kotlin
// Normal approach
fun makeDir(path: String): File {
    val result = File(path)
    result.mkdirs()
    return result
}

// Improved approach
fun makeDir(path: String) = path.let{ File(it) }.also{ it.mkdirs() }
```

## 回顾一下所有的特性

通过这三个特性，我们可以清楚地知道每个函数的行为。让我们举例说明一下上面没有提到的 `T.apply` 函数，它的 3 个特性如下所述：

* 它是一个扩展函数
* 它把 `this` 作为参数
* 它返回了 `this`（它自己）

```kotlin
// Normal approach
fun createIntent(intentData: String, intentAction: String): Intent {
    val intent = Intent()
    intent.action = intentAction
    intent.data = Uri.parse(intentData)
    return intent
}

// Improved approach, chaining
fun createIntent(intentData: String, intentAction: String) = 
    Intent().apply { action = intentAction }
            .apply { data = Uri.parse(intentData) }
```

或者我们也可以把一个非链式的对象创建过程变得可链式（chain-able）：

```kotlin
// Normal approach
fun createIntent(intentData: String, intentAction: String): Intent {
    val intent = Intent()
    intent.action = intentAction
    intent.data = Uri.parse(intentData)
    return intent
}

// Improved approach, chaining
fun createIntent(intentData: String, intentAction: String) = 
    Intent().apply { action = intentAction }
            .apply { data = Uri.parse(intentData) }
```

## 函数选择

现在思路变清晰了，根据这三大特性，我们可以对函数进行分类。基于此可以构建一个决策树来帮助我们根据需要来选择使用哪一个函数。

![](/assets/imgs/function-selection.png)

希望上面的决策树能够更清晰地阐述这些函数，同时也能简化你的决策，使你能够得当地使用这些函数。
