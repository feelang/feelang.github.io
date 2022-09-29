---
layout: page
title: Mockito 详解（一）基本用法
date: 2017-07-06
categories: test mockito
---

Mockito 是一个用于 Java 单测的 Mock 框架，除了 JUnit 之外，它还可以用于其他单测框架（例如：TestNG）。`Mockito` 可以改变一个类或者对象的行为，能够让我们更加专注地去测试代码逻辑，省去了构造数据所花费的努力。

<!-- more -->

## 0x00 基本概念
Mock 可分为两种类型，一种是 **Class Mock**，另一种是 **Partial Mock**（Mockito 叫 **spy**）。
改变 mock 对象方法（method）的行为叫 **Stub**（插桩）。
一次 Mock 过程称为 **Mock Session**，它会记录所有的 **Stubbing**，基本包含如下三个步骤：

    +----------+      +------+      +--------+
    | Mock/Spy | ===> | Stub | ===> | Verify |
    +----------+      +------+      +--------+

## 0x01 Class Mock
Class Mock 改变了 class 的行为，所以 mock 出来的对象就完全失去了原来的行为。
如果没有对 method 进行插桩，那么 method 会返回默认值（`null`、`false`、`0`等）。

最基本的用法如下：

```java
import static org.mockito.Mockito.*;

// 利用 List.class 创建一个 mock 对象 --- mockedList
List mockedList = mock(List.class);

// 操作 mockedList
mockedList.add("one");
mockedList.clear();

// 验证
verify(mockedList).add("one");
verify(mockedList).clear();
```

## 0x02 Partial Mock（spy）

如果只是想改变一个实例（instance）的行为，我们需要使用 `spy`：

```java
List list = new LinkedList();
List spy = spy(list);

// optionally, you can stub out some methods:
when(spy.size()).thenReturn(100);

// using the spy calls *real* methods
spy.add("one");
spy.add("two");

// prints "one" - the first element of a list
System.out.println(spy.get(0));

// size() method was stubbed - 100 is printed
System.out.println(spy.size());

// optionally, you can verify
verify(spy).add("one");
verify(spy).add("two");
```

如果方法没有被插桩，那么它的行为就不会被改变。所以有些情况下，我们不能使用 `when(Object)` 进行插桩，只能使用 do 系列方法（`doReturn|Answer|Throw()`）：

```java
List list = new LinkedList();
List spy = spy(list);

// Impossible: real method is called so spy.get(0) throws IndexOutOfBoundsException 
// (the list is yet empty)
when(spy.get(0)).thenReturn("foo");

// You have to use doReturn() for stubbing
doReturn("foo").when(spy).get(0);
```

---

*Mockito 的静态方法 spy 和 mock 的区别**

`spy` 是 partial mock，所以其本质上也是 `mock`，通过源码可以得知：

```java
public static <T> T spy(T object) {
  return MOCKITO_CORE.mock((Class<T>) object.getClass(), withSettings()
    .spiedInstance(object)
    .defaultAnswer(CALLS_REAL_METHODS));
}
```

> `MOCKITO_CORE` 是 `Mockito` 的核心实现类，`spy` 和 `mock` 方法一样，都是调用了 `MOCKITO_CORE.mock`。

```java
public static <T> T mock(Class<T> classToMock) {
  return mock(classToMock, withSettings());
}

public static <T> T mock(Class<T> classToMock, MockSettings mockSettings) {
  return MOCKITO_CORE.mock(classToMock, mockSettings);
}

public static MockSettings withSettings() {
  return new MockSettingsImpl().defaultAnswer(RETURNS_DEFAULTS);
}
```

通过代码可以看出，`spy` 和 `mock` 最大的区别在于使用了不同的 `MockSettings`，`spy` 的 `MockSettings` 需要传入一个 `spiedInstance`。

`spy` 的默认 Answer 是 `CALLS_REAL_METHODS`，也就是说，如果一个方法没有被 stub，那么会执行它真实的行为。
`mock` 的默认 Answer 是 `RETURNS_DEFAULTS`，没有被 stub 的方法会返回一个默认值。

## 0x03 Stub（插桩）

仅仅 Mock 出来一个对象显然是不够的，虽然可以通过验证**方法的执行情况**来测试代码的逻辑，但是多数情况下我们还需要改变方法的返回值，这时就需要用到“插桩”。

```java
LinkedList mockedList = mock(LinkedList.class);

// stubbing
when(mockedList.get(0)).thenReturn("first");
when(mockedList.get(1)).thenThrow(new RuntimeException());

// 打印出 "first"
System.out.println(mockedList.get(0));
// 抛出异常
System.out.println(mockedList.get(1));
// 返回 null，因为 get(999) 没有被 stub
System.out.println(mockedList.get(999));
```

### Stubbing

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

**Stubbing关系图**

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
doThrow(new RuntimeException("one"))
    .doThrow(new RuntimeException("two"))
        .when(mock).someVoidMethod();
```

### Answer

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

## 0x04 Verify（验证）

Verify 用于验证 mock 行为。

Mockito 提供了两个 `verify` 方法：

```java
public static <T> T verify(T mock, VerificationMode mode) {
  return MOCKITO_CORE.verify(mock, mode);
}

// times(1) 是 VerificationMode 的默认值
public static <T> T verify(T mock) {
  return MOCKITO_CORE.verify(mock, times(1));
}
```

验证模式如下所示：

### times
```java
verify(mock, times(2)).someMethod("some arg");
```

### never
```java
verify(mock, never()).someMethod();
```

### atLeastOnce
```java
verify(mock, atLeastOnce()).someMethod("some arg");
```

### atLeast
```java
verify(mock, atLeast(3)).someMethod("some arg");
```

### atMost
```java
verify(mock, atMost(3)).someMethod("some arg");
```

### calls
```java
inOrder.verify(mock, calls(2)).someMethod( "some arg" );
```

### only
```java
verify(mock, only()).someMethod();
//above is a shorthand for following 2 lines of code:
verify(mock).someMethod();
verifyNoMoreInvocations(mock);
```

### timeout
```java
//passes when someMethod() is called within given time span
verify(mock, timeout(100)).someMethod();
//above is an alias to:
verify(mock, timeout(100).times(1)).someMethod();

//passes as soon as someMethod() has been called 2 times before the given timeout
verify(mock, timeout(100).times(2)).someMethod();

//equivalent: this also passes as soon as someMethod() has been called 2 times before the given timeout
verify(mock, timeout(100).atLeast(2)).someMethod();

//verifies someMethod() within given time span using given verification mode
//useful only if you have your own custom verification modes.
verify(mock, new Timeout(100, yourOwnVerificationMode)).someMethod();
```

### after
```java
//passes after 100ms, if someMethod() has only been called once at that time.
verify(mock, after(100)).someMethod();
//above is an alias to:
verify(mock, after(100).times(1)).someMethod();

//passes if someMethod() is called *exactly* 2 times after the given timespan
verify(mock, after(100).times(2)).someMethod();

//passes if someMethod() has not been called after the given timespan
verify(mock, after(100).never()).someMethod();

//verifies someMethod() after a given time span using given verification mode
//useful only if you have your own custom verification modes.
verify(mock, new After(100, yourOwnVerificationMode)).someMethod();
```

## 0x05 ArgumentMatcher

插桩时除了指定特定的参数，还可以使用通配符 —— `ArgumentMatcher`。

```java
class ListOfTwoElements implements ArgumentMatcher<List> {
  public boolean matches(List list) {
    return list.size() == 2;
  }

  public String toString() {
    //printed in verification errors
    return "[list of 2 elements]";
  }
}

List mock = mock(List.class);

when(mock.addAll(argThat(new ListOfTwoElements))).thenReturn(true);

mock.addAll(Arrays.asList("one", "two"));

verify(mock).addAll(argThat(new ListOfTwoElements()));
```

`ArgumentMatchers` 负责生产 `ArgumentMatcher`：

```java
public class ArgumentMatchers {
  public static <T> T any();
  public static <T> T any(Class<T> type);
  public static <T> T isA(Class<T> type);
  public static boolean anyBoolean();
  public static byte anyByte();
  public static char anyChar();
  public static int anyInt();
  public static long anyLong();
  public static float anyFloat();
  public static double anyDouble();
  public static short anyShort();
  public static String anyString();

  public static <T> List<T> anyList();
  public static <T> List<T> anyListOf(Class<T> clazz);
  public static <T> Set<T> anySet();
  public static <T> Set<T> anySetOf(Class<T> clazz);
  public static <K, V> Map<K, V> anyMap();
  public static <K, V> Map<K, V> anyMapOf(Class<K> keyClazz, Class<V> valueClazz);
  public static <T> Collection<T> anyCollection();
  public static <T> Collection<T> anyCollectionOf(Class<T> clazz);
  public static <T> Iterable<T> anyIterable();
  public static <T> Iterable<T> anyIterableOf(Class<T> clazz);

  public static boolean eq(boolean value);
  public static byte eq(byte value);
  public static char eq(char value);
  public static double eq(double value);
  public static float eq(float value);
  public static int eq(int value);
  public static long eq(long value);
  public static short eq(short value);
  public static <T> T eq(T value);
  public static <T> T refEq(T value, String... excludeFields);
  public static <T> T same(T value)

  public static <T> T isNull();
  public static <T> T isNull(Class<T> clazz);
  public static <T> T notNull();
  public static <T> T notNull(Class<T> clazz);
  public static <T> T isNotNull();
  public static <T> T isNotNull(Class<T> clazz);
  public static <T> T nullable(Class<T> clazz);

  // String argument matcher
  public static String contains(String substring);
  public static String matches(String regex);
  public static String matches(Pattern pattern);
  public static String endsWith(String suffix);
  public static String startsWith(String prefix);

  // Custom argument matcher
  public static <T> T argThat(ArgumentMatcher<T> matcher);
  public static char charThat(ArgumentMatcher<Character> matcher);
  public static boolean booleanThat(ArgumentMatcher<Boolean> matcher);
  public static byte byteThat(ArgumentMatcher<Byte> matcher);
  public static short shortThat(ArgumentMatcher<Short> matcher);
  public static int intThat(ArgumentMatcher<Integer> matcher);
  public static long longThat(ArgumentMatcher<Long> matcher);
  public static float floatThat(ArgumentMatcher<Float> matcher);
  public static double doubleThat(ArgumentMatcher<Double> matcher);
}
```
