---
layout: single
title: Mockito 详解（三）插桩
date: 2017-07-08
categories: Programming
tags:
  - Mockito
---

每次插桩（Stubbing）都会产生一个 Invocation，本篇从 Invocation 着手，重点分析插桩的原理。

<!-- more -->

Invocation 之间的关系如下所示：


    +----------+              +----------+
    | StubInfo |--stubbedAt-->| Location |
    +----------+              +----------+
         /|\
          |
     implements
          |  
          |  
    +--------------+                            +---------------------+
    | StubInfoImpl |-----has a----------------->| DescribedInvocation |
    +--------------+                            +---------------------+

    +---------------------+
    | DescribedInvocation |
    +---------------------+
         /|\         /|\  \ 
          |           |     \        +------------------+
          |           |       \      | InvocationOnMock | 
          |           |         \    +------------------+
          |           |           \       / 
          |           |           extends
          |        extends           \ /
          |           |        +------------+
     implements       |        | Invocation |
          |           |        +------------+
          |           |                  /|\
          |     +---------------------+   |
          |     | MatchableInvocation |   |
          |     +---------------------+   |
          |             /|\               |
          |              |                |
          |         implements           has
          |              |                |
          |              |                |
       +-------------------+              |
       | InvocationMatcher |--------------+
       +-------------------+
                  |
                  |                         +-----------------+
                  +------ has list of ----->| ArgumentMatcher |
                                            +-----------------+


`MatchableInvocation` 与 `Invocation` 的区别如下：

```java
mock.foo();   // <- invocation
verify(mock).bar();  // <- matchable invocation
```

MockHandler
---

`Invocation` 通过 `MockHandler` 进行处理：

```java
public interface MockHandler extends Serializable {
    Object handle(Invocation invocation) throws Throwable;
}
```

Mockito 提供的的 `MockHandler` 实现了如下功能：

0. 记录 Mock 对象上的方法调用以进行后续验证
0. 当 Mock 对象被插桩之后捕获 stubbing 信息
0. 返回 invocation 的插桩值

---

Invocation 表示在 Mock 方法上的一次调用，它包含两部分信息 DescribedInvocation & InvocationOnMock。

> A method call on a mock object. Contains all information and state needed for the Mockito framework to operate.

DescribedInvocation
---

`DescribedInvocation` 只是用于描述 `Invocation`。

```java
public interface DescribedInvocation {
    String toString();
    Location getLocation();
}
```

其中 `Location` 用于描述 `Invocation` 的位置：

```java
public interface Location {
    String toString();
}
```

InvocationOnMock
---

`InvocationOnMock` 用于表示 `Invocation` 和 `Mock` 之间的数据联系。

```java
public interface InvocationOnMock extends Serializable {
    Object getMock();
    Method getMethod();
    Object[] getArguments();
    <T> T getArgument(int index);
    Object callRealMethod() throws Throwable;
}
```

Invocation
---

`Invocation` 除此之外，还包含其他功能：

```java
public interface Invocation extends InvocationOnMock, DescribedInvocation {
    boolean isVerified();
    int getSequenceNumber();
    Location getLocation();
    Object[] getRawArguments();
    Class<?> getRawReturnType();
    void markVerified();
    StubInfo stubInfo();
    void markStubbed(StubInfo stubInfo);
    boolean isIgnoredForVerification();
    void ignoreForVerification();
}
```

`StubInfo` 用于描述 stubbing：

```java
public interface StubInfo {
    Location stubbedAt();
}
```

MatchableInvocation
---

`MatchableInvocation` 包含 `Invocation` 实例和 `ArgumentMatcher` 列表。它用于验证的过程（verification process）。

```java
public interface MatchableInvocation extends DescribedInvocation {
    Invocation getInvocation();
    List<ArgumentMatcher> getMatchers();
    boolean matches(Invocation candidate);
    boolean hasSimilarMethod(Invocation candidate);
    boolean hasSameMethod(Invocation candidate);
    void captureArgumentsFrom(Invocation invocation);
}
```

InvocationContainer 关系图
---

            +---------------------+                           +------------+
            | InvocationContainer |--- clear / get list of--->| Invocation |
            +---------------------+                           +------------+

Stubbing 关系图
---

          +-----------------+
          | OngoingStubbing |
          +-----------------+
                  /|\
                   |
               implements
                   |
                   |
          +-----------------+
          |   BaseStubbing  |<-----------------+
          +-----------------+                  | 
                  /|\                          |
                   |                           |
                extends                     extends 
                   |                           |
                   |                           |
       +----------------------+    +---------------------+
       | ConsecutiveStubbing  |    | OngoingStubbingImpl |
       +----------------------+    +---------------------+


Stubbing
---

Stubbing 表示一次插桩，它的形式是 `when(x).then(y)`，用于指定 mock 的行为。

*Stubbing 的示例代码*
```java
when(mock.foo()).thenReturn(true);
```

可以通过如下代码获取 mock 对象的所有 stubbing：

```java
Mockito.mockingDetails(mock).getStubbings();
```

Stubbing 的接口规范如下：

```java
public interface Stubbing {
    Invocation getInvocation();
    boolean wasUsed();
}
```

* `getInvocation()` 返回被插桩的方法调用，例如，`mock.foo()` 就是一个 `Invocation`。
* `wasUsed()` 用于表示 stubbing 是否被使用，如果 `mock.foo()` 没有被调用，那么 `wasUsed()` 返回 false，说明存在未被使用的 stubbing，为了保持 `clarity of tests`，最好删除未被使用的 stubbing 代码。

Stubber
---

Stubber 是一个插装器。

当我们用 `doThrow()|doAnswer()|doNothing()|doReturn()` 的形式进行插桩时，可以通过 Stubber 来选择 mock 对象的方法：

*示例一*
```java
doThrow(new RuntimeException()).when(mockedList).clear();
```

*示例二*
```java
doThrow(new RuntimeException("one")).doThrow(new RuntimeException("two")).when(mock).someVoidMethod();
```

Stubber 接口定义如下：

```java
public interface Stubber {
    <T> T when(T mock);
    Stubber doThrow(Throwable... toBeThrown);
    Stubber doThrow(Class<? extends Throwable> toBeThrown);
    Stubber doThrow(Class<? extends Throwable> toBeThrown, Class<? extends Throwable>... nextToBeThrown);
    Stubber doAnswer(Answer answer);
    Stubber doNothing();
    Stubber doReturn(Object toBeReturned);
    Stubber doReturn(Object toBeReturned, Object... nextToBeReturned);
    Stubber doCallRealMethod();
}
```

可以看出，`doXXX` 方法的返回值是一个 `Stubber`，`when` 方法对 mock 对象进行处理之后再返回这个对象。

OngoingStubbing
---

```java
public interface OngoingStubbing<T> {
    OngoingStubbing<T> thenReturn(T value);
    OngoingStubbing<T> thenReturn(T value, T... values);
    OngoingStubbing<T> thenThrow(Throwable... throwables);
    OngoingStubbing<T> thenThrow(Class<? extends Throwable> throwableType);
    OngoingStubbing<T> thenThrow(Class<? extends Throwable> toBeThrown, Class<? extends Throwable>... nextToBeThrown);
    OngoingStubbing<T> thenCallRealMethod();
    OngoingStubbing<T> thenAnswer(Answer<?> answer);
    OngoingStubbing<T> then(Answer<?> answer);
    <M> M getMock();
}
```

调用 `Mockito#when` 返回一个 `OngoingStubbing`，通过 `OngoingStubbing#thenXxx` 可以改变 mock 对象的行为，从而产生一个 stubbing。

*示例代码*
```java
when(mock.someMethod(anyString())).thenReturn(10);
```

Answer
---

不管是 `Stubber` 还是 `OngoingStubbing`，除了标准返回之外，都提供了自定义返回值的方法：

* `Stubber doAnswer(Answer answer);`
* `OngoingStubbing<T> then(Answer<?> answer);`

Answer 的接口定义如下：

```java
public interface Answer<T> {
    T answer(InvocationOnMock invocation) throws Throwable;
}
```

如下代码利用 `Answer` 改变了 mock 方法的行为：

```java
when(mock.someMethod(anyString())).thenAnswer(
    new Answer() {
        public Object answer(InvocationOnMock invocation) {
            Object[] args = invocation.getArguments();
            Object mock = invocation.getMock();
            return "called with arguments: " + Arrays.toString(args);
    }
});
```

那么 `mock.someMethod("foo")` 的返回值就变成了 `called with arguments: [foo]`。

`Answer` 不接受参数，只有返回值，Mockito 还提供了其他 5 个 Answer，分别接受不同个数的参数，然后返回一个值。

* Answer1
* Answer2
* Answer3
* Answer4
* Answer5

只接受参数，没有返回值的 Answer 包括：

* VoidAnswer1
* VoidAnswer2
* VoidAnswer3
* VoidAnswer4
* VoidAnswer5

> `ValidableAnswer` 用到再分析
