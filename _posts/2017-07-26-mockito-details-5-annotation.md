---
layout: single
title: Mockito 详解（五）MockitoAnnotation
date: 2017-07-26 12:35:04
categories: Programming
tags:
  - Mockito
---

MockitoAnnotations负责初始化`@Mock`、`@Spy`、`@Captor`、`@InjectMocks`等注解。

如果不用`@Mock`，我们当然可以手动创建一个mock对象：
```java
List mockedList = Mockito.mock(List.class);
```
但是相比于手动创建，使用注解可带来如下好处：

- 代码更简洁
- 避免重复创建
- 可读性好
- 验证错误更易读（因为注解默认使用field name来标记mock对象）

<!-- more -->

先来看一下用法：
```java
public class ArticleManagerTest extends SampleBaseTestCase {
  @Mock private ArticleCalculator calculator;
  @Mock private ArticleDatabase database;
  @Mock private UserProvider userProvider;

  private ArticleManager manager;

  @Before public void setup() {
    manager = new ArticleManager(userProvider, database, calculator);
  }
}

public class SampleBaseTestCase {
  @Before public void initMocks() {
    MockitoAnnotations.initMocks(this);
  }
}
```

`MockitoAnnotations`必须在执行测试方法之前（`@Before`标记）执行初始化。

```java
public class MockitoAnnotations {
  public static void initMocks(Object testClass) {
    if (testClass == null) {
      throw new MockitoException("testClass cannot be null.");
    }

    AnnotationEngine annotationEngine = new GlobalConfiguration().tryGetPluginAnnotationEngine();
    annotationEngine.process(testClass.getClass(), testClass);
  }
}
```
所有注解都由`AnnotationEngine`来处理。

寻找AnnotationEngine
---

为了保证线程安全，Mockito的configuration会保存在ThreadLocal，也就说一个线程只有一个实例。
```java
public class GlobalConfiguration implements IMockitoConfiguration, Serializable {
  private static final long serialVersionUID = -2860353062105505938L;

  // 线程安全
  private static final ThreadLocal<IMockitoConfiguration> GLOBAL_CONFIGURATION = 
        new ThreadLocal<IMockitoConfiguration>();

  // 初始化
  public GlobalConfiguration() {
    if (GLOBAL_CONFIGURATION.get() == null) {
      GLOBAL_CONFIGURATION.set(createConfig());
    }
  }

  private IMockitoConfiguration createConfig() {
    IMockitoConfiguration defaultConfiguration = new DefaultMockitoConfiguration();
    IMockitoConfiguration config = new ClassPathLoader().loadConfiguration();
    if (config != null) {
      return config;
    } else {
      return defaultConfiguration;
    }
  }

  public org.mockito.plugins.AnnotationEngine tryGetPluginAnnotationEngine() {
    IMockitoConfiguration configuration = GLOBAL_CONFIGURATION.get();
    if (configuration.getClass() == DefaultMockitoConfiguration.class) {
      return Plugins.getAnnotationEngine();
    }
    return configuration.getAnnotationEngine();
  }
}
```
`IMockitoConfiguration`的实例存储在一个static ThreadLocal变量中——`GLOBAL_CONFIGURATION`，所以在每一个线程中只有一个configuration实例，那么每次`new GlobalConfiguration`并不会多次创建实例。

`GlobalConfiguration`构造时会首先尝试通过`ClassPathLoader`来加载configuration：

```java
public class ClassPathLoader {
  public static final String MOCKITO_CONFIGURATION_CLASS_NAME = "org.mockito.configuration.MockitoConfiguration";
  public IMockitoConfiguration loadConfiguration() {
    // try-catch is omitted.
    Class<?> configClass = Class.forName(MOCKITO_CONFIGURATION_CLASS_NAME);
    return (IMockitoConfiguration) configClass.newInstance();
  }
}
```
> `MockitoConfiguration`是一个插件，关于插件的加载方式可参考[Mockito 详解（二）插件机制](http://www.liangfei.me/2017/07/07/mockito-details-2-plugins/#加载插件)。

如果加载不到类`MockitoConfiguration`，说明没有配置插件，那么就退而求其次，使用默认值——`DefaultMockitoConfiguration`，它内部配置的 `AnnotationEngine`是`InjectingAnnotationEngine`。

`AnnotationEngine`找到了，开始分析如何处理annotation。

处理Annotation
---
`AnnotationEngine`的接口规范如下：
```java
public interface AnnotationEngine {
  void process(Class<?> clazz, Object testInstance);
}
```

每个`Annotation`所对应的`AnnotationEngine`如下表所示：

Annotation | AnnotationEngine
--- | ---
@Mock & @Captor | IndependentAnnotationEngine
@Spy | SpyAnnotationEngine
@InjectMocks | InjectingAnnotationEngine

因为注解会作用到单个变量（Field）上，根据注解初始化变量的工作由`FieldAnnotationProcessor`完成：
```java
public interface FieldAnnotationProcessor<A extends Annotation> {
  Object process(A annotation, Field field);
}
```
`process`的返回值`Object`就是根据注解创建的对象。

### IndependentAnnotationEngine(@Mock & @Captor)

`@Mock`可以指定创建mock所需要的变量：

```java
@Target({FIELD, PARAMETER})
@Retention(RUNTIME)
@Documented
public @interface Mock {
  Answers answer() default Answers.RETURNS_DEFAULTS;
  String name() default "";
  Class<?>[] extraInterfaces() default {};
  boolean serializable() default false;
}
```

`MockAnnotationProcessor`会首先读取`Mock`的参数，然后构建一个`mockSettings`，最后通过调用`Mockito#mock`创建一个mock对象。

```java
public class MockAnnotationProcessor implements FieldAnnotationProcessor<Mock> {
  public Object process(Mock annotation, Field field) {
    MockSettings mockSettings = Mockito.withSettings();

    if (annotation.extraInterfaces().length > 0) { // never null
      mockSettings.extraInterfaces(annotation.extraInterfaces());
    }

    // 默认使用field name
    if ("".equals(annotation.name())) {
      mockSettings.name(field.getName());
    } else {
      mockSettings.name(annotation.name());
    }

    if (annotation.serializable()) {
      mockSettings.serializable();
    }

    mockSettings.defaultAnswer(annotation.answer());
    return Mockito.mock(field.getType(), mockSettings);
  }
}
```

`Captor`的原理是一样的，它会创建一个`ArgumentCaptor`。

```java
public class CaptorAnnotationProcessor implements FieldAnnotationProcessor<Captor> {
    public Object process(Captor annotation, Field field) {
        Class<?> type = field.getType();
        if (!ArgumentCaptor.class.isAssignableFrom(type)) {
            // exception message is omitted
            throw new MockitoException("");
        }
        Class<?> cls = new GenericMaster().getGenericType(field);
        return ArgumentCaptor.forClass(cls);
    }
}
```
通过代码可以看出，`@Captor`标记的变量必须是`ArgumentCaptor`类型。

`IndependentAnnotationEngine`会初始化一个Annotation Class到FieldAnnotationProcessor的映射：

```java
// 成员变量，省略了new
private final Map<Class<? extends Annotation>, FieldAnnotationProcessor<?>> annotationProcessorMap;

// 构造方法，注册了两个annotation processor
public IndependentAnnotationEngine() {
  registerAnnotationProcessor(Mock.class, new MockAnnotationProcessor());
  registerAnnotationProcessor(Captor.class, new CaptorAnnotationProcessor());
}
```

`MockitoAnnotations#initMocks`方法直接调用了`AnnotationEngine#process`：
```java
annotationEngine.process(testClass.getClass(), testClass);
```
`IndependentAnnotationEngine#process`的实现如下所示：

```java
public void process(Class<?> clazz, Object testInstance) {
  Field[] fields = clazz.getDeclaredFields();
  for (Field field : fields) {
    boolean alreadyAssigned = false;
    for(Annotation annotation : field.getAnnotations()) {
      Object mock = createMockFor(annotation, field);
      if (mock != null) {
        throwIfAlreadyAssigned(field, alreadyAssigned);
        alreadyAssigned = true;
        try {
          setField(testInstance, field,mock);
        } catch (Exception e) {
          throw new MockitoException("Problems setting field " + field.getName() + " annotated with "
                    + annotation, e);
        }
      }
    }
  }
}
```
0. 首先遍历所有的`field`，获取该`field`的annotations
0. 然后根据annotation类型创建mock对象

  ```java
  private Object createMockFor(Annotation annotation, Field field) {
    return forAnnotation(annotation).process(annotation, field);
  }

  private <A extends Annotation> FieldAnnotationProcessor<A> forAnnotation(A annotation) {
    if (annotationProcessorMap.containsKey(annotation.annotationType())) {
      return (FieldAnnotationProcessor<A>) annotationProcessorMap.get(annotation.annotationType());
    }
    return new FieldAnnotationProcessor<A>() {
      public Object process(A annotation, Field field) {
        return null;
      }
    };
  }
  ```

0. `setField`会把新创建的mock对象——`Object mock`通过反射赋值给`testInstance`的成员变量。

  ```java
  public class FieldSetter {
    private FieldSetter() {
    }
    public static void setField(Object target, Field field, Object value) {
      AccessibilityChanger changer = new AccessibilityChanger();
      changer.enableAccess(field);
      try {
        field.set(target, value);
      } catch (IllegalAccessException e) {
          throw new RuntimeException("msg omitted");
      } catch (IllegalArgumentException e) {
          throw new RuntimeException("msg omitted");
      }
      changer.safelyDisableAccess(field);
    }
  }
  ```

总结
---

* `MockitoAnnotations`只是负责初始化`testInstance`内用`Annotation`标记的`Field`。
* `Field`通过`Mockito#mock`完成初始化。
* `MockitoSession`除了借助`MockitoAnnotations`完成`Field`初始化之外，还会监控整个mock progress
