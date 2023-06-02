---
layout: single
title: 图解 Retrofit 之 ServiceMethod
date: 2016-07-10
categories: Programming
tags:
  - Android
---

通过 [Retrofit + RxAndroid 实践总结](http://www.liangfei.me/2016/07/06/android-retrofit-and-rxjava)，我们已经了解到了 Retrofit 的基本用法，为了知其所以然，我们以图解加源码的方式从 Service Method 入手，逐步拨开 Retrofit 的神秘面纱。

首先以官方网站的示例代码为例，看一下一个 Service Method 的组成部分：

![](/assets/imgs/service_method.png)

`ServiceMethod` 使用了 Builder 模式，先来看 `ServiceMethod.Builder` 的构造方法：

```java
public Builder(Retrofit retrofit, Method method) {
  this.retrofit = retrofit;
  this.method = method;
  this.methodAnnotations = method.getAnnotations();
  this.parameterTypes = method.getGenericParameterTypes();
  this.parameterAnnotationsArray = method.getParameterAnnotations();
}
```
构造方法接受两个参数 - `retrofit` 和 `method`，然后通过调用 `Method` 类的方法获取以下数据：

```java
final Annotation[] methodAnnotations;
final Annotation[][] parameterAnnotationsArray;
final Type[] parameterTypes;
```

`methodAnnotations` 就对应着上例中的  `@GET("users/{user}/repos"`，由 `parseMethodAnnotation` 负责解析。

method parameter 也有对应的 annotation type，由对应的 `ParameterHandler` 进行处理，例如上例中的 `@Path` 就对应着 `class Path<T> extends ParameterHandler<T>`。

一个 parameter 可以有多个 annotation，所以  `parameterAnnotationsArray` 是一个二维数组 - `Annotation[][]`。

`ServiceMethod.Builder` 最终会 `build` 出一个 `ServiceMethod` 实例，我们先来看 method annotations 的解析过程。

method annotations
---

_ServiceMethod.Builder#build_
```java
for (Annotation annotation : methodAnnotations) {
  parseMethodAnnotation(annotation);
}  
```
如下图所示，`parseMethodAnnotation` 方法根据 method annotation 的类型（蓝色框内）生成一个 request 所需要的数据（褐色框内）。

![](/assets/imgs/parse_method_annotation.png)

其中 `httpMethod` 不能为空，如果 `hasBody == false`，那么 `isMultipart` 和 `isFormEncoded` 也必须为 `false`，而且两者互斥不能同时为 `true`，否则会抛出异常。

解析完 method annotations 之后，再来解析  parameters（代码示例中的 `@Path("user") String user`）。

parameters
---

![](/assets/imgs/parse_parameter.png)

每一个 parameter annotation 类型都有对应的 `ParameterHandler`，method parameters 解析完成之后生成一个数组 - `ParameterHandler[] parameterHandlers`，这个数组在后面构建 request 的时候会用到。

解析过程中会验证 `@Path` value 的合法性，并确保 value 在 `relativeUrlParamNames`（*由 method annotations 生成*） 中。

```java
// Upper and lower characters, digits, underscores, and hyphens, starting with a character.
static final String PARAM = "[a-zA-Z][a-zA-Z0-9_-]*";
static final Pattern PARAM_URL_REGEX = Pattern.compile("\\{(" + PARAM + ")\\}");
static final Pattern PARAM_NAME_REGEX = Pattern.compile(PARAM);

private void validatePathName(int p, String name) {
  if (!PARAM_NAME_REGEX.matcher(name).matches()) {
    throw parameterError(p, "@Path parameter name must match %s. Found: %s",
        PARAM_URL_REGEX.pattern(), name);
  }
  // Verify URL replacement name is actually present in the URL path.
  if (!relativeUrlParamNames.contains(name)) {
    throw parameterError(p, "URL \"%s\" does not contain \"{\%s}\".", relativeUrl, name);
  }
}
```

`parseParameterAnnotation`  方法在解析 `Url` 类型的 parameter annotation 时会判断 parameter 类型，由于 Retrofit 本身没有依赖 Android SDK，所以无法像 `HttpUrl.class` 那样获取 `Uri.class`，但是 Retrofit 的实现很巧妙，学到了：）

```java
if (type == HttpUrl.class
    || type == String.class
    || type == URI.class
    || (type instanceof Class && "android.net.Uri".equals(((Class<?>) type).getName()))) {
  return new ParameterHandler.RelativeUrl();
} else {
  throw parameterError(p,
      "@Url must be okhttp3.HttpUrl, String, java.net.URI, or android.net.Uri type.");
}
```

method annotations 以及 parameters 都解析完成后，我们再回到 service method 的 callAdapter。

CallAdapter
---

想要了解 `CallAdapter` 的功能，我们需要先从 `Retrofit` 的 `create` 方法开始分析。

`create` 方法使用**动态代理**把 service method 的调用转发给一个 `InvocationHandler`：

```java
ServiceMethod serviceMethod = loadServiceMethod(method);
OkHttpCall okHttpCall = new OkHttpCall<>(serviceMethod, args);
return serviceMethod.callAdapter.adapt(okHttpCall);
```
由以上代码可以看出，`CallAdapter` 会把一个 `Call` 类型适配为用户定义的 service method 的 return type。

举个例子，如果我们配合 RxAndroid 使用 Retrofit，service method 的返回值类型会由 `Call` 类型变成 `Observable` 类型，这个转换其实就由 `RxJavaCallAdapterFactory` 来实现。

```java
Retrofit retrofit = new Retrofit.Builder()      
    .addCallAdapterFactory(RxJavaCallAdapterFactory.create())
    .baseUrl(BASE_URL) .build();
```

由以上代码可以看出，`RxJavaCallAdapterFactory` 是通过 `Retrofit.Builder` 的
`addCallAdapterFactory` 方法传递给 `Retrofit`，而 `create` 方法中 `adapt` 的执行者却是 `ServiceMethod`，也就是说 `ServiceMethod` 的 `CallAdapter` 是由 `Retrofit` 提供的，两者的交互关系如下图所示：  

![](/assets/imgs/retrofit_and_service_method.png)
