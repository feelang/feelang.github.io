---
title: 为什么要使用内部类
classes: wide
date: 2014-04-10
categories: Java
---

我们经常会在一个类中定义一个内部类 (inner class)，这个内部类可以继承也可以实现接口，因为有一个隐式的引用 (implicit reference) 指向外部类 (outer class)，所以我们可以直接访问并操作外部类，因此可以认为内部类是外部类的一个窗口。

* An inner class provides a kind of window into the outer class.

这样问题就来了：如果我们需要一个实现了某个接口的对象，为什么不直接用一个外部类来实现那个接口呢？如果需求仅仅这么简单，当然可以这么做。

* If that's all you need, then that's how you should do it.

但是很多时候，问题不会这么简单，因为Java不支持多继承，当我们想继承多个类或者实现多个抽象类的时候，不得不借助于内部类来“继承多个类”。

* Each inner class can independently inherit from an implementation. Thus, the inner class is not limited by whether the outer class is already inheriting from an implementation.

所以可以把内部类看成解决(multiple-inheritance)的一个途径。

首先来看一个实现多个接口的例子。

```java
// Two ways that a class can implement multiple interfaces.

interface A {}
interface B {}

class X implements A, B {}

class Y implements A {
    B makeB() {
        // Anonymous inner class:
        return new B() {};
    }
}

public class MultiInterfaces {
    static void takesA(A a) {}
    static void takesB(B b) {}

    public static void main(String[] args) {
        X x = new X();
        Y y = new Y();
        takesA(x);
        takesA(y);
        takesB(x);
        takesB(y.makeB());
    }
}

```

抛开类之间has-a, is-a的关系来看，两种实现方式都可以。但是，当把接口换成抽象类或者具体类之后，就只能使用内部类了。

```java
// With concrete or abstract classes, inner
// classes are the only way to produce the effect
// of "multiple implementation inheritance."

class D {}

abstract class E {}

class Z extends D {
    E makeE() { return new E() {}; }
}

public class MultiImplementation {
    static void takesD(D d) {}
    static void takesE(E e) {}
    public static void main(String[] args) {
        Z z = new Z();
        takesD(z);
        takesE(z.makeE());
    }
}
```

当然，如果不是为了解决多重继承的问题，不一定非要使用内部类。但是内部类可以为我们提供如下便利：
* 内部类可以有多个实例 (instance)
* 每一个实例有独立的状态信息 (state information)

在一个外部类中可以有多个内部类，并且每个内部都可以实现同一个接口或者继承同一个类，但是他们的内部
实现不同。

内部类的可以“按需”创建。

内部类并不存在 **is-a** 的关系，每一个内部类都是一个独立的实体。
