---
layout: single
title: 用 bytecode 来看 try-catch-finally 和 return
date: 2014-10-19
Categories: Java
---

最近一直在看 Java 虚拟机规范，发现直接分析 bytecode 更能加深对 Java 语言的理解。

之前看过一篇关于 `return` 和 `finally` 执行顺序的文章，仅在 Java 的语言层面做了分析，其实我倒觉得直接看 bytecode 可能来的更清晰一点。

先看一个只有 `try-finally`，没有 `catch` 的例子。

**try - finally**

```java
public class ExceptionTest {
  public void tryFinally() {
    try {
      tryItOut();
    } finally {
      wrapItUp();
    }
  }


  // auxiliary methods
  public void tryItOut() { }

  public void wrapItUp() {}
}
```

通过 `javap -c ExceptionTest` 来查看它的字节码。

```java
public void tryFinally();
  Code:
     0: aload_0
     1: invokevirtual #2  // Method tryItOut:()V
     4: aload_0
     5: invokevirtual #3  // Method wrapItUp:()V
     8: goto          18
    11: astore_1
    12: aload_0
    13: invokevirtual #3  // Method wrapItUp:()V
    16: aload_1
    17: athrow
    18: return
  Exception table:
     from    to  target type
         0     4    11   any
```

如果没有抛出异常，那么它的执行顺序为

```
0: aload_0
1: invokevirtual #2  // Method tryItOut:()V
4: aload_0
5: invokevirtual #3  // Method wrapItUp:()V
18: return
```

如果抛出了异常，JVM 会在

```
Exception table:
   from    to  target type
       0     4    11   any
```

中进行控制跳转。如果是位于0到4字节之间的命令抛出了任何类型（any type）的异常，会跳转到11字节处继续运行。

```
11: astore_1
12: aload_0
13: invokevirtual #3
16: aload_1
17: athrow
```

astore_1会把抛出的异常对象保存到local variable数组的第二个元素。下面两行指令用来调用成员方法wrapItUp。

```
12: aload_0
13: invokevirtual #3
```

最后通过

```
16: aload_1
17: athrow
```

重新抛出异常。

通过以上分析可以得出结论：

> 在try-finally中，try块中抛出的异常会首先保存在local variable中，然后执行finally块，执行完毕后重新抛出异常。

如果我们把代码修改一下，在try块中直接return。

**try - return - finally**

```java
public void tryFinally() {
  try {
    tryItOut();
    return;
  } finally {
    wrapItUp();
  }
}
```

”反汇编“一下：

```
 0: aload_0
 1: invokevirtual #2 // Method tryItOut:()V
 4: aload_0
 5: invokevirtual #3 // Method wrapItUp:()V
 8: return
 9: astore_1
10: aload_0
11: invokevirtual #3 // Method wrapItUp:()V
14: aload_1
15: athrow
```

可以看出finally块的代码仍然被放到了return之前。
> 如果try块中有return statement，一定是finally中的代码先执行，然后return。

JVM规范是这么说的：

> Compilation of a try-finally statement is similar to that of try-catch. Pior to transferring control outside thetry statement, whether that transfer is normal or abrupt, because an exception has been thrown, thefinally clause must first be execute.
try - catch - finally

给上面的代码加一个catch块

```java
public void tryCatchFinally() {
  try {
    tryItOut();
  } catch (TestExc e) {
    handleExc(e);
  } finally {
    wrapItUp();
  }
}
```
javap一下

```java
public void tryCatchFinally();
  Code:
     0: aload_0
     1: invokevirtual #2
     4: aload_0
     5: invokevirtual #3
     8: goto          31
    11: astore_1
    12: aload_0
    13: aload_1
    14: invokevirtual #5                  
    17: aload_0
    18: invokevirtual #3
    21: goto          31
    24: astore_2
    25: aload_0
    26: invokevirtual #3
    29: aload_2
    30: athrow
    31: return
Exception table:
   from    to  target type
       0     4    11   Class TestExc
       0     4    24   any
      11    17    24   any
```

通过Exception table可以看出：

* catch监听 0 ~ 4 字节类型为TextExc的异常。
* finally为 0 ~ 4 以及 11 ~ 17 字节任何类型的异常。

也就说 catch block 本身也在 finally block 的管辖范围之内。如果catch block 中有 return statement，那么也一定是在 finally block 之后执行。
