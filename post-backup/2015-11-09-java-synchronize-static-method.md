---
layout: single
title: 怎样在静态方法中使用 synchronized
date: 2015-11-9
categories: Programming
tags:
  - Java
---

synchronized 的实现方式
---

`synchronized` 的类型可以分为两种：

0. synchronized method
0. synchronized block

两者的实现方式是不一样的，jvm 规范中写道，编译后的 synchronized method 会有一个 **ACC_SYNCHRONIZED** 的 flag，也就是说当 jvm 的方法调用指令（the method invocation instruction）从 the run-time constant pool 中查找到这个 method 的时候，已经知道它是一个synchronized method，所以锁操作是由**方法调用**以及**返回**指令来控制的。

而 **synchronized block** 的锁是由 `monitorenter` 和 `monitorexit` 这两个指令来控制。

可以通过 javap 命令来“反汇编”一下 class 文件。

```java
public class StaticMethodTest {
    public static synchronized void staticMethod() { }
    public static void staticMethod1() {
        synchronized (StaticMethodTest.class) {
        // ...
    }
    }
    public void memberMethod() { } 
}
```

编译成 class 文件后执行
```bash
javap -verbose StaticMethodTest
```

两个静态方法的输出结果分别为
```
public static synchronized void staticMethod();
  descriptor: ()V
  flags: ACC_PUBLIC, ACC_STATIC, ACC_SYNCHRONIZED
  Code:
    stack=0, locals=0, args_size=0
       0: return
    LineNumberTable:
      line 2: 0
public static void staticMethod1();
  descriptor: ()V
  flags: ACC_PUBLIC, ACC_STATIC
  Code:
    stack=2, locals=2, args_size=0
       0: ldc           #2                  // class StaticMethodTest
       2: dup
       3: astore_0
       4: monitorenter
       5: aload_0
       6: monitorexit
       7: goto          15
      10: astore_1
      11: aload_0
      12: monitorexit
      13: aload_1
      14: athrow
      15: return
    Exception table:
       from    to  target type
           5     7    10   any
          10    13    10   any
```
其实不管静态方法还是成员方法，`synchronized` 的实现方式都是一样的，那么类和对象究竟有什么关系呢？

类和对象
---
首先要了解的就是**类究竟是怎么来的**。 

JVM 拿到编译器编译好的 class 文件后，首先会把文件载入到内存中，class 文件当然会有自己的格式，所以需要由 ClassLoader 来解析文件的内容，这个解析出来的内容会用一个 `Class` 类的实例 - Class object 来表示，这个 object 可以通过 Java 的 `ClassName.class`来获取。

也就是说，Class object 是一个 `Class` 类型的实例（instance），而对象是一个 ClassName 的 instance。Class 和 ClassName都是类型，ClassName是由 `class` 关键字定义的，而Class是内置类型。

因此成员方法的synchronized method 就等价于 synchronized (this) block，即下面两种方式是等价的。
```java
public synchronized void fun1() {
    // do something here
}
```
```java
public synchronized void fun2() {
    synchronized (this) {
    // do something here
    }
}
```
成员方法是属于 `this`，而静态方法是属于 Class Object，那么静态方法的 synchronized method 也就等价于下面这种形式的 synchronized block 了。

```java
public static synchronized void fun2() {
    synchronized (ClassName.class) {
    // do something here
    }
}
```

验证代码
---

定义了三个静态方法，分别采用不同的锁机制，并且每个方法都是一个死循环。然后再定义三个线程分别执行调用三个方法。

```java
import java.util.concurrent.*;

public class SynchronizedTest {
    private static Object lock = new Object();

    public synchronized static void fun() {
        while (true) {
            System.out.println("in fun");
            try {
                TimeUnit.MILLISECONDS.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void fun1() {
        synchronized (SynchronizedTest.class) {
            while (true) {
                System.out.println("in fun1");
                try {
                    TimeUnit.MILLISECONDS.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }


    public static void fun2() {
        synchronized (lock) {
            while (true) {
                System.out.println("in fun2");
                try {
                    TimeUnit.MILLISECONDS.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }


    public static void main(String[] args) {
        new Thread() {
            @Override
            public void run() {
                fun();
            }
        }.start();
    
    
       new Thread() {
            @Override
            public void run() {
                fun1();
            }
        }.start();


        new Thread() {
            @Override
            public void run() {
                fun2();
            }
        }.start();
    }
}

```
运行结果就是 in fun 和 in fun2 交替出现，就是没有 in fun1。 
只要运行 fun 的线程不交出锁，fun1 就无法被调用，因为他们都是共享了 Class object 的锁。
