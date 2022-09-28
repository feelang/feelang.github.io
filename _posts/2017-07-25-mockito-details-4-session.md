---
layout: post
title: Mockito 详解（四）MockitoSession
date: 2017-07-25 11:25:13
tags: 
 - Mockito
 - UnitTest
---

`MockitoSession`表示一次mock会话，这个会话通常是一次测试方法的执行。

<!-- more -->

在一个会话周期内，`MockitoSession`会做三件事：

0. mock初始化（initializes mocks）
0. mock使用验证（validates usage）
0. 检测插桩错误（detects incorrect stubbing）

`MockitoSession`可以帮我们省去一些原本需要手动去写的代码，并且通过一些额外的验证来驱使我们写“干净的测试”。

`MockitoSession`结束之后必须调用`finishMocking()`方法，否则下个Session开始时会抛出异常（`UnfinishedMockingSessionException`）。

Mockito提供的JUnit组件`MockitoJUnitRunner`和`MockitoRule`都使用了`MockitoSession`，所以如果我们用到了`MockitoJUnitRunner`或`MockitoRule`则不需要再使用`MockitoSession`管理会话。

如果使用了其他单测框架（例如TestNG）或者其他的JUnit Runner（Jukito、Springockito）则需要手动去集成MockitoSession。

先来看一个例子：
```java
public class ExampleTest {
    @Mock Foo foo;

    // Keeping session object in a field so that we can complete session in 'tear down' method.
    // It is recommended to hide the session object, along with 'setup' and 'tear down' methods in a base class / runner.
    // Keep in mind that you can use Mockito's JUnit runner or rule instead of MockitoSession and get the same behavior.
    MockitoSession mockito;

    @Before 
    public void setup() {
        //initialize session to start mocking
        mockito = Mockito.mockitoSession()
            .initMocks(this)
            .strictness(Strictness.STRICT_STUBS)
            .startMocking();
    }

    @After 
    public void tearDown() {
        // It is necessary to finish the session so that Mockito
        // can detect incorrect stubbing and validate Mockito usage
        // 'finishMocking()' is intended to be used in your test framework's 'tear down' method.
        mockito.finishMocking();
    }

    // test methods ...
}
```

在`@Before setup`方法中通过`startMocking`启动了一个`MockitoSession`，相应地，在`@After tearDown`方法中通过`finishMocking`结束会话。
`ExampleTest`中使用`Mock`标记了一个成员变量——`@Mock Foo foo`，`MockitoSession`自动创建foo这个mock对象。

`Mockito#mockitoSession`是一个工厂方法，每次调用都会创建一个新的`MockitoSessionBuilder`，通过这个Builder再创建一个`MockitoSession`。

> mockitoSession的方法命名不太合理，私以为newSessionBuilder更合理一些。

```java
@Incubating
public static MockitoSessionBuilder mockitoSession() {
    return new DefaultMockitoSessionBuilder();
}
```

`MockitoSessionBuilder`的定义如下：
```java
@Incubating
public interface MockitoSessionBuilder { 
    @Incubating
    MockitoSessionBuilder initMocks(Object testClassInstance);

    @Incubating
    MockitoSessionBuilder strictness(Strictness strictness);

    @Incubating
    MockitoSession startMocking() throws UnfinishedMockingSessionException;
}
```

`initMocks`方法并不会立即初始化标记了`@Mock`的成员变量，只有调用`startMocking`创建`MockitoSession`实例时才会执行初始化。

在一个线程内只允许有一个`MockitoSession`，所以开启新会话之前必须要调用`finishMocking`来结束上一次会话。但是多个线程可以允许有多个`MockitoSession`实例。

`finishMocking`定义在`MockitoSession`这个接口中：
```java
@Incubating
public interface MockitoSession {
    @Incubating
    void finishMocking();
}
```

`strictness`可以驱动开发人员写“干净的测试”，而且可以根据level来打印日志，方便调试。

```java
@Incubating
public enum Strictness {
    @Incubating
    LENIENT,

    @Incubating
    WARN,

    @Incubating
    STRICT_STUBS
}
```

`Mockito#startMocking`方法返回的`DefaultMockitoSessionBuilder`是`MockitoSessionBuilder`的默认实现：

```java
public class DefaultMockitoSessionBuilder implements MockitoSessionBuilder {
  private Object testClassInstance;
  private Strictness strictness;

  @Override
  public MockitoSessionBuilder initMocks(Object testClassInstance) {
    this.testClassInstance = testClassInstance;
    return this;
  }

  @Override
  public MockitoSessionBuilder strictness(Strictness strictness) {
    this.strictness = strictness;
    return this;
  }

  @Override
  public MockitoSession startMocking() {
    //Configure default values
    Object effectiveTest = this.testClassInstance == null ? new Object() : this.testClassInstance;
    Strictness effectiveStrictness = this.strictness == null ? Strictness.STRICT_STUBS : this.strictness;
    return new DefaultMockitoSession(effectiveTest, effectiveStrictness, new ConsoleMockitoLogger());
  }
}
```
* 当`initMocks`传入的参数为`null`时，`startMocking`会返回一个 `new Object()`
* 当`strictness`传入的参数为`null`时，默认使用`Strictness.STRICT_STUBS`

`DefaultMockitoSession#startMocking`创建了一个`MockitoSession`的默认实现——`DefaultMockitoSession`，我们先来看构造方法：

```java
private final Object testClassInstance;
private final UniversalTestListener listener;

public DefaultMockitoSession(Object testClassInstance, Strictness strictness, MockitoLogger logger) {
    this.testClassInstance = testClassInstance;
    listener = new UniversalTestListener(strictness, logger);
    try {
        //So that the listener can capture mock creation events
        Mockito.framework().addListener(listener);
    } catch (RedundantListenerException e) {
        Reporter.unfinishedMockingSession();
    }
    MockitoAnnotations.initMocks(testClassInstance);
}
```
构造方法内使用`Strictness`和`MockitoLogger`实例创建了一个 `UniversalTestListener`，它会监听一次mock会话中的事件：

* onMockCreated
* testFinished

然后在`testFinished`事件中，根据`Strictness`打印日志（借助`MockitoLogger`）。

```java
switch (currentStrictness) {
    case WARN: emitWarnings(logger, event, createdMocks); break;
    case STRICT_STUBS: reportUnusedStubs(event, createdMocks); break;
    case LENIENT: break;
    default: throw new IllegalStateException("Unknown strictness: " + currentStrictness);
}
```

`MockitoLogger`是`Logger`的接口规范：
```java
public interface MockitoLogger {
    void log(Object what);
}
```
`ConsoleMockitoLogger`就是将log打印至`System.out`：
```java
public class ConsoleMockitoLogger implements MockitoLogger {
    public void log(Object what) {
        System.out.println(what);
    }
}
```

那么`UniversalTestListener`是如何监听mock的创建呢？

再回到DefaultMockitoSession的构造方法：
```java
Mockito.framework().addListener(listener);
```

`Mockito#framework`也是一个工厂方法：
```java
@Incubating
public static MockitoFramework framework() {
    return new DefaultMockitoFramework();
}
```

`MockitoFramework`用于管理Mockito框架的配置以及其生命周期的回调。

```java
@Incubating
public interface MockitoFramework {
    @Incubating
    MockitoFramework addListener(MockitoListener listener) throws RedundantListenerException;

    @Incubating
    MockitoFramework removeListener(MockitoListener listener);
}
```

`MockitoFramework`支持的Listner类型是`MockitoListener`，而且同一类型的Listener只能add一次，否则会抛出`RedundantListenerException`。


`DefaultMockitoFramework`是`MockitoFramework`的默认实现：
```java
public class DefaultMockitoFramework implements MockitoFramework {
    public MockitoFramework addListener(MockitoListener listener) {
        Checks.checkNotNull(listener, "listener");
        mockingProgress().addListener(listener);
        return this;
    }

    public MockitoFramework removeListener(MockitoListener listener) {
        Checks.checkNotNull(listener, "listener");
        mockingProgress().removeListener(listener);
        return this;
    }
}
```

`addListener`和`removeListener`必须在同一个线程内才会生效，因为`MockingProgress`是`ThreadLocal`：

```java
public class ThreadSafeMockingProgress {

    private static final ThreadLocal<MockingProgress> MOCKING_PROGRESS_PROVIDER = 
        new ThreadLocal<MockingProgress>() { 
            @Override 
            protected MockingProgress initialValue() {
                return new MockingProgressImpl();
        }
    };

    private ThreadSafeMockingProgress() {
    }

    public final static MockingProgress mockingProgress() {
        return MOCKING_PROGRESS_PROVIDER.get();
    }
}
```
`DefaultMockitoSession`的`finishMocking`方法会调用`removeListener`：
```java
public void finishMocking() {
    //Cleaning up the state, we no longer need the listener hooked up
    //The listener implements MockCreationListener and at this point
    //we no longer need to listen on mock creation events. We are wrapping up the session
    Mockito.framework().removeListener(listener);

    //Emit test finished event so that validation such as strict stubbing can take place
    listener.testFinished(new TestFinishedEvent() {
        public Throwable getFailure() {
            return null;
        }
        public Object getTestClassInstance() {
            return testClassInstance;
        }
        public String getTestMethodName() {
            return null;
        }
    });

    //Finally, validate user's misuse of Mockito framework.
    Mockito.validateMockitoUsage();
}
```
`Mockito.validateMockitoUsage()`也是通过`MockingProgress`来实现。

`MockingProgress`顾名思义，表示一次mock过程，实现略复杂，暂且按下不表，后面再分析。

最后再回到`DefaultMockitoSession`的构造方法：
```java
MockitoAnnotations.initMocks(testClassInstance);
```

至此则真相大白了，原来`@Mock`标记的成员变量是由`MockitoAnnotations`来初始化，欲知后事如何，且看下回分析。