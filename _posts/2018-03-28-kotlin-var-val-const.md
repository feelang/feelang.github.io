---
layout: single
title: Kotlin 中 var、val、const 关键字解析
date: 2018-03-28
categories: Kotlin
---

昨天公众号后台收到一位小伙伴的留言询问，他对于 Kotlin 为何没有 Java 的 `final` 关键字感到困惑，这应该是很多初学者都会遇到的问题，所以我就写了这篇博文从更底层的角度来解析 Kotlin 声明变量时用到的三个关键字：`var`、`val` 和 `const`。

其实，Java 的 `final` 就等价于 Kotlin 的 `val`， 虽然通过 javap 反编译可以看到两者的底层实现不一样，但是从语义上讲，它们两者的确是等价的。具体原因，我们来逐一分析。

什么是属性
---
我们知道，在 Kotlin 的世界中，class 已经不再是唯一的一等公民，我们可以直接在代码文件的最顶层（top-level）声明类、函数和变量。

```kotlin
class Address {
  // class properties
  var province = "zhejiang"
  val city = "hangzhou"
}

fun prettify(address: Address): String {
  // local variable
  val district = "xihu"
  return district + ',' + address.city + ',' + address.province
}

// top-level property
val author = "liangfei"
```

上例中的 `Address` 是一个类，`prettify` 是一个函数，`author` 是一个变量，它们都是一等公民，也就是说，函数和变量可以单独存在，不会像 Java 那样依附于类。

首先，`var` 和 `val` 可分为三种类型：

* 类的属性（class property），例如上例中的 `var province = "zhejiang"`，它是 `Address` 类的一个属性；
* 顶层属性（top-level property），例如上例中的 `val author = "liangfei"`，它是文件（module）的一个属性；
* 局部变量（local variable），例如上例中的 `val district = "xihu"`，它是函数 `prettify` 的一个局部变量。

类的属性和顶层属性都是属性，所以可以统一来看待，属性本身不会存储值，也就是说它不是一个字段（field），那它的值是哪里来的呢？我们先来看一下声明一个属性的完整语法：

```kotlin
var <propertyName>[: <PropertyType>] [= <property_initializer>]
    [<getter>]
    [<setter>]
```

可以看出，一个属性的声明可以分解为五个部分：属性名、属性类型、initializer、getter、setter。

* 属性的名就是就是我们用来引用属性的方式；
* 属性的类型可以显示声明，因为 Kotlin 支持类型推导，如果类型能够从上下文推导得出，那么它也可以省略；
* initializer 是类型推导的线索之一，例如 `val author = "liangfei"`，根据 `= "liangfei"` 可以得出它是一个 `String` 类型；
* getter 也是类型推导的线索之一，所有使用属性名获取值的操作，都是通过 getter 来完成的；
* setter 用于给属性赋值。

以上只是声明了一个属性，如果我们要赋值，它的值会存储在哪里呢？其实，编译器还会自动为属性生成一个用于存储值的字段（field），因为写代码时感知不到到它的存在，所以称为幕后字段（backing field）。具体可以参考[幕后字段](https://github.com/LyndonChin/kotlin-docs-zh/blob/master/classes-and-objects/01_properties-and-fields.md#%E5%B9%95%E5%90%8E%E5%AD%97%E6%AE%B5)，因为与本文关系不大，所以此处不做介绍。

`var` 和 `val` 所声明的属性，其最本质的区别就是：**`val` 不能有 setter**，这就达到了 Java 中 `final` 的效果。

例如，上面 Kotlin 代码中的 `Address` 类：

```kotlin
class Address {
  var province = "zhejiang"
  val city = "hangzhou"
}
```

它在 JVM 平台上的实现是下面这样的（通过 `javap` 命令查看）：

```java
public final class Address {
  public final java.lang.String getProvince();
  public final void setProvince(java.lang.String);
  public final java.lang.String getCity();
  public Address();
}
```

可以看出，针对 `var province` 属性，生成了 `getProvince()` 和 `setProvince(java.lang.String)` 两个函数。但是 `val city` 只生成了一个 `getCity()` 函数。

对于局部变量来说，`var` 或者 `val` 都无法生成 getter 或 setter，所以只会在编译阶段做检查。

看一下它的[官方定义](https://kotlinlang.org/docs/reference/properties.html)（中文版可参考[属性和字段](https://github.com/LyndonChin/kotlin-docs-zh/blob/master/classes-and-objects/01_properties-and-fields.md)）：

> Classes in Kotlin can have properties. These can be declared as mutable, using the var keyword or read-only using the val keyword.

对于类的属性来说：`var` 表示可变（mutable），`val` 表示只读（read-only）。对于顶层属性来说也是一样的。

可变和只读
---
`var` 表示可变，`val` 表示只读，而不是不可变（immutable）。我们已经知道了 `val` 属性只有 getter，但是这并不能保证它的值是不可变的。例如，下面的代码：

```kotlin
class Person {
  var name = "liangfei"
  var age = 30

  val nickname: String
    get() {
      return if (age > 30) "laoliang" else "xiaoliang"
    }

  fun grow() {
    age += 1
  }
}
```

属性 `nickname` 的值并非不可变，当调用 `grow()` 方法时，它的值会从 `"laoliang"` 变为 `"xiaoliang"`，但是无法直接给 `nickname` 赋值，也就是说，它不能位于赋值运算的左侧，只能位于右侧，这就说明了为什么它是只读（read-only），而不是不可变（immutable）。

> 其实，Kotlin 有专门的语法来定义可变和不可变的变量，后面会专门写一篇博问来分析，这里不再深入。

我们知道，Java 中可以使用 `static final` 来定义常量，这个常量会存放于全局常量区，这样编译器会针对这些变量做一些优化，例如，有三个字符串常量，他们的值是一样的，那么就可以让这个三个变量指向同一块空间。我们还知道，局部变量无法声明为 `static final`，因为局部变量会存放在栈区，它会随着调用的结束而销毁。

Kotlin 引入一个新的关键字 `const` 来定义常量，但是这个常量跟 Java 的 `static final` 是有所区别的，如果它的值无法在编译时确定，则编译不过，因此 `const` 所定义的常量叫**编译时常量**。

编译时常量
---
首先，`const` 无法定义局部变量，除了局部变量位于栈区这个原因之外，还因为局部变量的值无法在编译期间确定，因此，`const` 只能修饰属性（类属性、顶层属性）。

因为 `const` 变量的值必须在编译期间确定下来，所以它的类型只能是 `String` 或基本类型，并且不能有自定义的 getter。

所以，编译时常量需要满足如下条件：

* 顶层或者 `object` 的成员（`object` 也是 Kotlin 的一个新特性，具体可参考[对象声明](https://github.com/LyndonChin/kotlin-docs-zh/blob/master/classes-and-objects/10_objects.md#%E5%AF%B9%E8%B1%A1%E5%A3%B0%E6%98%8E)）。
* 初始化为一个 String 或者基本类型的值
* 没有自定义 getter

总结
---
最后，总结一下：

* `var`、`val` 声明的变量分为三种类型：顶层属性、类属性和局部变量；
* `var` 属性可以生成 getter 和 setter，是可变的（mutable），`val` 属性只有 getter，是只读的（read-only，注意不是 immutable）；
* 局部变量只是一个普通变量，不会有 getter 和 setter，它的 `val` 等价于 Java 的 `final`，在编译时做检查。
* `const` 只能修饰没有自定义 getter 的 `val` 属性，而且它的值必须在编译时确定。

### 参考资料
* [Why is a constant defined as a static final in Java?](https://www.quora.com/Why-is-a-constant-defined-as-a-static-final-in-Java)
* [Properties and Fields](https://kotlinlang.org/docs/reference/properties.html)
* [Kotlin中常量的探究- 技术小黑屋](https://droidyue.com/blog/2017/11/05/dive-into-kotlin-constants/)
