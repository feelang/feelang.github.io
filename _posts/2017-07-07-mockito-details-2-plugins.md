---
layout: post
title: Mockito 详解（二）插件机制
date: 2017-07-07
categories: test mockito
---

Mockito 通过插件形式对外提供了扩展能力，本篇主要分析其插件加载原理。

## 注册插件

插件通过 `PluginRegister` 进行注册，现在只支持四个组件，分别是：

* MockMaker
* StackTraceCleanerProvider
* InstantiatorProvider
* AnnotationEngine

`PluginRegistry` 是 package 级别的 class，其初始化的组件通过 public 级别的类 `Plugins` 对外提供：

```java
public class Plugins {
  private static final PluginRegistry registry = new PluginRegistry();

  public static StackTraceCleanerProvider getStackTraceCleanerProvider() {
    return registry.getStackTraceCleanerProvider();
  }

  public static MockMaker getMockMaker() {
    return registry.getMockMaker();
  }

  public static InstantiatorProvider getInstantiatorProvider() {
    return registry.getInstantiatorProvider();
  }

  public static AnnotationEngine getAnnotationEngine() {
    return registry.getAnnotationEngine();
  }
}
```

Mockito 提供了默认的插件。

* AnnotationEngine 
    * org.mockito.internal.configuration.InjectingAnnotationEngine
* InstantiatorProvider
    * org.mockito.internal.creation.instance.DefaultInstantiatorProvider
* MockMaker 
    * Default = org.mockito.internal.creation.bytebuddy.ByteBuddyMockMaker 
    * Inline = org.mockito.internal.creation.bytebuddy.InlineByteBuddyMockMaker
    * Android = org.mockito.android.internal.creation.AndroidByteBuddyMockMaker
* StackTraceCleanerProvider 
    * org.mockito.internal.exceptions.stacktrace.DefaultStackTraceCleanerProvider

## 加载插件

`PluginLoader` 负责加载插件。

> 需要深入了解 ClassLoader 机制。

构造
---

```java
private final PluginSwitch pluginSwitch;
private final Map<String, String> alias;

public PluginLoader(PluginSwitch pluginSwitch) {
    this.pluginSwitch = pluginSwitch;
    this.alias = new HashMap<String, String>();
}
```

* `pluginSwitch` 用于是否需要加载组件。（后面会分析）
* `alias` 表示插件别名，可以用一个简单的名字表示插件的全称（fully qualified type name）。

```java
PluginLoader withAlias(String name, String type) {
    alias.put(name, type);
    return this;
}
```

加载插件
---

```java
<T> T loadPlugin(final Class<T> pluginType, String defaultPluginClassName)
```

`loadPlugin` 方法接受两个参数，一个是插件Class，另一个是默认插件名称。

首先尝试加载 `pluginType`，如果加载成功，直接返回插件实例。

```java
T plugin = loadImpl(pluginType)
if (plugin != null) {
    return plugin;
}
```

`loadImpl` 方法的声明如下：

```java
/**
  * Equivalent to {@link java.util.ServiceLoader#load} but without requiring
  * Java 6 / Android 2.3 (Gingerbread).
  */
private <T> T loadImpl(Class<T> service)
```

**1. 首先获取 ClassLoader **

```java
ClassLoader loader = Thread.currentThread().getContextClassLoader();
if (loader == null) {
    loader = ClassLoader.getSystemClassLoader();
}
```

**2. 然后加载 mockito-extensions 下配置的资源**

```java
Enumeration<URL> resources;
try {
    resources = loader.getResources("mockito-extensions/" + service.getName());
} catch (IOException e) {
    throw new IllegalStateException("Failed to load " + service, e);
}
```

> 以 Android 平台的 Mockito 为例

`MockMaker` 插件的路径为：

```
src/main/resources/mockito-extensions/org.mockito.plugins.MockMaker
```

`MockMaker` 插件的实现类为：

```
org.mockito.android.internal.creation.AndroidByteBuddyMockMaker`
```

那么 `loader.getResources` 的返回值 `resources` 中会包含 `AndroidByteBuddyMockMaker`。

**3. 通过 PluginFinder 寻找插件的类名**

```java
String foundPluginClass = new PluginFinder(pluginSwitch).findPluginClass(Iterables.toIterable(resources))
```

> PluginFinder 的查询规则是：找到第一个不被 PluginSwitch 禁用掉的 plugin 类名。

`PluginFinder#findPluginClass` 的代码如下所示：

```java
String findPluginClass(Iterable<URL> resources) {
    for (URL resource : resources) {
        InputStream s = null;
        try {
            s = resource.openStream();
            String pluginClassName = new PluginFileReader().readPluginClass(s);
            if (pluginClassName == null) {
                //For backwards compatibility
                //If the resource does not have plugin class name we're ignoring it
                continue;
            }
            if (!pluginSwitch.isEnabled(pluginClassName)) {
                continue;
            }
            return pluginClassName;
        } catch(Exception e) {
            throw new MockitoException("Problems reading plugin implementation from: " + resource, e);
        } finally {
            IOUtil.closeQuietly(s);
        }
    }
    return null;
}
```

**4. 加载找到的插件**

```java
if (foundPluginClass != null) {
    String aliasType = alias.get(foundPluginClass);
    if (aliasType != null) {
        foundPluginClass = aliasType;
    }
    Class<?> pluginClass = loader.loadClass(foundPluginClass);
    Object plugin = pluginClass.newInstance();
    return service.cast(plugin);
}
```

0. 因为 [插件名字] 可能是简称，所以需要尝试去 `alias` 寻找 [插件名字] 的 [类名]
0. 然后利用上文获得的 `loader` 加载 [找到的插件类]
0. 创建类实例，转换类型后返回

## 插件开关

`PluginSwitch` 用于判断是否需要加载 classpath 中配置的插件。

`PluginSwitch` 本身也是一个插件，在 `PluginRegistry` 中注册：

```java
private final PluginSwitch pluginSwitch = new PluginLoader(new DefaultPluginSwitch())
    .loadPlugin(PluginSwitch.class, DefaultPluginSwitch.class.getName());
```

它的默认实现为 `DefaultPluginSwitch`：

```java
class DefaultPluginSwitch implements PluginSwitch {
  public boolean isEnabled(String pluginClassName) {
    return true;
  }
}
```

在 `PluginLoader` 的分析过程中，我们以 Android 平台的插件 `MockMaker` 为例已经稍微了解了插件的加载原理，下面再详细分析一下。

我们知道，插件通过 `PluginRegistry` 进行注册：

*PluginRegistry.java*
```java
private final MockMaker mockMaker = new PluginLoader(pluginSwitch)
            .withAlias("mock-maker-inline", "org.mockito.internal.creation.bytebuddy.InlineByteBuddyMockMaker")
            .loadPlugin(MockMaker.class, "org.mockito.internal.creation.bytebuddy.ByteBuddyMockMaker");
```

以上代码可以看出，`PluginLoader` 的构造方法需要参数 `pluginSwitch`，也就是说 `PluginLoader` 可以根据 `pluginSwitch` 是否需要加载某个 plugin。

再来看一下 `withAlias` 和 `loadPlugin` 的声明：

*withAlias@PluginLoader.java*
```java
/**
 * Adds an alias for a class name to this plugin loader. Instead of the fully qualified type name,
 * the alias can be used as a convenience name for a known plugin.
 */
PluginLoader withAlias(String name, String type)
```

针对上例，`withAlias` 的参数对应关系如下：

* name = "mock-maker-inline"
* type = "org.mockito.internal.creation.bytebuddy.InlineByteBuddyMockMaker"

也就是说，当我们遇到名字为 `mock-maker-inline` 的插件时，如果没有被 `pluginSwitch` diasable 掉，那么就去加载 `org.mockito.internal.creation.bytebuddy.InlineByteBuddyMockMaker` 这个类。

*loadPlugin@PluginLoader.java*
```java
/**
 * Scans the classpath for given pluginType. If not found, default class is used.
 */
@SuppressWarnings("unchecked")
<T> T loadPlugin(final Class<T> pluginType, String defaultPluginClassName)
```

还是针对上例，参数对应关系如下：

参数名 | 参数值
--- | ---
pluginType | MockMaker.class
defaultPluginClassName | "org.mockito.internal.creation.bytebuddy.ByteBuddyMockMaker"

直接看注释，具体原理还没有完全搞懂。

> The plugin mechanism of mockito works in a similar way as the `java.util.ServiceLoader`, however instead of
 looking in the `META-INF` directory, Mockito will look in `mockito-extensions` directory.
**The reason for that is that Android SDK strips jar from the `META-INF` directory when creating an APK.**

Mockito 加载插件的方式类似于 `ServiceLoader`，但是它是去 `mockito-extensions` 目录下寻找插件，而不是 `META-INF`。

以 Android 平台为例：

```
├── android
│   └── src
│       └── main
│           ├── java
│           │   └── org
│           │       └── mockito
│           │           └── android
│           │               └── internal
│           │                   └── creation
│           │                       ├── AndroidByteBuddyMockMaker.java
│           │                       ├── AndroidLoadingStrategy.java
│           │                       └── AndroidTempFileLocator.java
│           └── resources
│               └── mockito-extensions
│                   └── org.mockito.plugins.MockMaker
```

mockito-extensions 目录下有一个文件 `org.mockito.plugins.MockMaker`，那么 `PluginLoader` 在加载 `MockMaker` 时会首先读取 `org.mockito.plugins.MockMaker` 文件的内容（类全称或者别名）：

```
org.mockito.android.internal.creation.AndroidByteBuddyMockMaker
```

ClassLoader 把这个类加载进来之后，插件就加载完成了。
