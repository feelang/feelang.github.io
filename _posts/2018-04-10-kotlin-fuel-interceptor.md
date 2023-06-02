---
layout: single
title: Kotlin 实战之 Fuel 的高阶函数
date: 2018-04-10 14:53:45
categories: Programming
tags:
  - Kotlin
---

[Fuel](https://github.com/kittinunf/Fuel) 是一个用 Kotlin 写的网络库，与 OkHttp 相比较，它的代码结构比较简单，但是它的巧妙之处在于充分利用了 [Kotlin 的语言特性](https://github.com/LyndonChin/kotlin-docs-zh)，所以代码看上去干净利落。

OkHttp 使用了一个 *interceptor chain* 来实现拦截器的串联调用，由于 Java 语言（ JDK ≤ 7）本身的局限性，所以实现代码比较臃肿，可读性也不友好。当然，RxJava 再加上 retrolambda 这种 backport 的出现，一定程度上了缓解了这种尴尬，但是 Kotlin 天生具备的声明式写法又使得 Java 逊色了很多。

我们知道，拦截器本质上是一个责任链模式（chain of responsibility）的实现，我们通过具体代码来学习一下 Kotlin 究竟是如何利用高阶函数实现了拦截器功能。

首先定义一个 `MutableList` 用于存储拦截器实例：

```kotlin
val requestInterceptors: 
  MutableList<((Request) -> Request) -> ((Request) -> Request)> 
   = mutableListOf()
```

> 注意，Kotlin 的类型系统明确区分了 mutable 和 immutable，默认的 List 类型是 immutable。

`requestInterceptors` 的元素类型是一个[高阶函数](https://github.com/LyndonChin/kotlin-docs-zh/blob/master/functions-and-lambdas/02_lambdas.md)：

```kotlin
((Request) -> Request) -> ((Request) -> Request)
```

作为元素类型的高阶函数，其参数也是一个高阶函数 `(Request) -> Request`， 同时，返回值也是高阶函数 `(Request) -> Request`。

然后，我们给 `requestInterceptors` 定义一个增加元素的方法：

```kotlin
fun addRequestInterceptor(
  interceptor: ((Request) -> Request) -> ((Request) -> Request)) {
    requestInterceptors += interceptor
}
```

`addRequestInterceptor` 的参数类型

```kotlin
(Request) -> Request) -> ((Request) -> Request)
```

与 `requestInterceptors` 的元素类型一致。

> 注意，这里又出现了一个 Kotlin 有而 Java 没有的语言特性：操作符重载。

我们没有调用 `requestInterceptors.add(interceptor)`，而是用了一个 `plusAssign` 的操作符 `+=`（MutableCollections.kt 中定义的操作符重载）：

```kotlin
/**
 * Adds the specified [element] to this mutable collection.
 */
@kotlin.internal.InlineOnly
public inline operator fun <T> MutableCollection<in T>.plusAssign(element: T) {
    this.add(element)
}
```

那么，此时应该定义一个拦截器的函数实例了：

```kotlin
fun <T> loggingRequestInterceptor() =
        { next: (T) -> T ->
            { t: T ->
                println(t.toString())
                next(t)
            }
        }
```

`loggingRequestInterceptor` 是一个函数，它的返回值是一个 lambda 表达式（即高阶函数）：

```kotlin
{ next: (T) -> T ->
    { t: T ->
        println(t.toString())
        next(t)
    }
}
```

1) 这个 lambda 的**参数**是 `next: (T) -> T`（参数名是 `next`，参数类型是 `(T) -> T`），**返回值**是另一个 lambda 表达式：

```kotlin
{ t: T ->
    println(t.toString())
    next(t)
}
```

2) 因为 lambda 本身是一个函数字面量（function literal），它的类型通过函数本身可以推到得出，如果我们用一个变量来引用这个 lambda 的话，变量的类型是 `(T) -> T`。

由1、2两点可知，`loggingRequestInterceptor()` 的返回值是一个 lambda 表达式，它的参数是 `(T) -> T`，返回值也是 `(T) -> T`。

这里的泛型函数略抽象，我们来看一个具体化的函数：

```kotlin
fun cUrlLoggingRequestInterceptor() =
        { next: (Request) -> Request ->
            { r: Request ->
                println(r.cUrlString())
                next(r)
            }
        }
```

同理，`cUrlLoggingRequestInterceptor()` 函数的参数为 `(Request) -> Request`、返回值为 `(Request) -> Request`。

拦截器都定义好了，那么应该如何调用呢？Kotlin 一行代码搞定🤟：：

```kotlin
requestInterceptors.foldRight({ r: Request -> r }) { f, acc -> f(acc) }
```

`foldRight` 是 `List` 的一个扩展函数，先来看声明：

```kotlin
/**
 * Accumulates value starting with [initial] value and applying [operation] from right to left to each element and current accumulator value.
 */
public inline fun <T, R> List<T>.foldRight(initial: R, operation: (T, acc: R) -> R): R {
    var accumulator = initial
    if (!isEmpty()) {
        val iterator = listIterator(size) // 让迭代器指向最后一个元素的末尾
        while (iterator.hasPrevious()) {
            accumulator = operation(iterator.previous(), accumulator)
        }
    }
    return accumulator
}
```

函数功能总结为一句话：从右往左，对列表中的每一个元素执行 `operation` 操作，每个操作的结果是下一次操作的入参，第一次 `operation` 的初始值是 `initial`。

回头来看拦截器列表 `requestInterceptors` 如何执行了 `foldRight`：

```kotlin
requestInterceptors.foldRight({ r: Request -> r }) { f, acc -> f(acc) }
```

参数 `inital: R` 的实参是 `{ r: Request -> r }`，一个函数字面量，没有执行任何操作，接收 `r` 返回 `r`。

参数 `operation: (T, acc: R) -> R` 可接收一个 lambda，所以它的实参 `{f, acc -> f(acc)}` 可以位于圆括号之外。`f` 的泛型是 `T`，具体类型是 

```kotlin
((Request) -> Request) -> ((Request) -> Request)
```

`acc` 的类型通过 `initial: R` 的实参 `{ r: Request -> r }` 可以推到得出——`(Request) -> Request`。

OK，语法完全没毛病，再来看语义。

    +---------------------+
    | { r: Request -> r } | ---> 初始值，命名为 *fun0*
    +---------------------+
               |
               |
              \|/    fun0 作为参数传递给 requestInterceptors 最右的 f（最后一个元素）
    +----------------------------------|------------------------f---------------------|-+
    | cUrlLoggingRequestInterceptor(): ((Request) -> Request) -> ((Request) -> Request) |
    +----------------------------------|----------------------------------------------|-+
               |
               |                  f 返回结果：
               |                  +-----------------------------+
               |                  | { r: Request ->             |
               |                  |     println(r.cUrlString()) |
               |                  |     fun0(r)                 |
               |                  | }                           |
               |                  +-----------------------------+
               |                                    命名为 *fun1*
               |  
              \|/   fun1 作为参数，传递给倒数第二个 f
    +----------------------------------|-----------------------f--------------------|-+
    | loggingRequestInterceptor(): ((Request) -> Request) -> ((Request) -> Request)   |
    +----------------------------------|--------------------------------------------|-+
               |
               |                  f 返回结果：
               |                  +-----------------------------+
               |                  | { r: Request ->             |
               |                  |     println(1.toString())   |
               |                  |     fun1(r)                 |
               |                  | }                           |
               |                  +-----------------------------+
               |                                    命名为 *fun2*
              \|/   将 fun2 解体：
    +------------------------------+
    | { r: Request ->              |
    |     println(r.toString())    |
    |     println(r.cUrlString())  | 类型为：(Request) -> request
    |     r                        |
    | }                            |
    +------------------------------+

至此，一个简单的拦截器功能就实现了，代码竟然如此简洁，感动！

参考
---
* [拆轮子系列：拆 OkHttp by Piasy](https://blog.piasy.com/2016/07/11/Understand-OkHttp/)
* [Kotlin中文文档](https://github.com/LyndonChin/kotlin-docs-zh)
