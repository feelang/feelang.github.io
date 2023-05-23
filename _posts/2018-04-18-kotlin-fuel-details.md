---
layout: single
title: Kotlin 网络库 Fuel 的设计之道
date: 2018-04-18
categories: Kotlin
---

使用场景
---
一个“朴素”的 url 完全可以用一个字符串来表示（例如 `"https://www.youzan.com"`），我们可以利用 Kotlin 语言本身的特性为 `String` 类型添加一个扩展函数 `httpGet()`，然后借此发起 http 请求：

```kotlin
"https://www.youzan.com".httpGet()
```

但是，对于不是朴素字符串的对象来说，我们可以让其实现一个接口：

```kotlin
interface PathStringConvertible {
    val path: String
}
```

然后，将“计算”过后的 path 通过一个 `String` 类型提供出来，例如：

```kotlin
enum class HttpsBin(relativePath: String) : Fuel.PathStringConvertible {
    USER_AGENT("user-agent"),
    POST("post"),
    PUT("put"),
    PATCH("patch"),
    DELETE("delete");

    override val path = "https://httpbin.org/$relativePath"
}
```

但是，也会存在一种情况，所有的 url 可能会共享一个 base url，或者是其他公用参数，那么还需有一个地方来存储这些通用配置，这个地方的幕后老大就叫 `FuelManager`。

`String` 和 `PathStringConvertible` 最终也会调用到 `FuelManager`。

    +----------+
    |  String  |------------->----+
    +----------+                  |    +------+    +-------------+
                                  |--->| Fuel |--->| FuelManager |
    +-------------------------+   |    +------+    +-------------+
    |  PathStringConvertible  |->-+
    +-------------------------+


除了通过 `String` 或者 `PathStringConvertiable` 来发起请求，我们还可以直接用一个 `Request`，因此 `Fuel` 还提供了转换 `Request` 的接口：

```kotlin
interface RequestConvertible {
    val request: Request
}
```

综上来看，发起一个 http 请求可以有如下四种方式：
0. 一个字符串
0. `PathStringConvertible` 变量
0. `RequestConvertible` 变量
0. 直接使用 `Fuel` 伴生对象提供的方法

代码实现
---
### 对外提供服务的 Fuel
首先 `Fuel` 作为对外的接口提供方（类似 Facade 模式），通过一个伴生对象（companion object）提供服务（以 get 方法为例）：

```kotlin
companion object {
  @JvmStatic @JvmOverloads
  fun get(path: String, parameters: List<Pair<String, Any?>>? = null): Request =
          request(Method.GET, path, parameters)

  @JvmStatic @JvmOverloads
  fun get(convertible: PathStringConvertible, parameters: List<Pair<String, Any?>>? = null): Request =
          request(Method.GET, convertible, parameters)

  private fun request(method: Method, path: String, parameters: List<Pair<String, Any?>>? = null): Request =
          FuelManager.instance.request(method, path, parameters)

  private fun request(method: Method, convertible: PathStringConvertible, parameters: List<Pair<String, Any?>>? = null): Request =
          request(method, convertible.path, parameters)
}
```

Fuel 类通过伴生对象提供的 http 方法有 *get/post/put/patch/delete/download/upload/head*，这些方法最终会路由到 `FuleManager` 的实例（instance）。

同时，`Fule.kt` 源文件为 `String` 和 `PathStringConvertible` 定义了扩展，以支持这些 http 方法（以 get 方法为例）：

```kotlin
@JvmOverloads
fun String.httpGet(parameters: List<Pair<String, Any?>>? = null): Request = Fuel.get(this, parameters)

@JvmOverloads
fun Fuel.PathStringConvertible.httpGet(parameter: List<Pair<String, Any?>>? = null): Request = Fuel.get(this, parameter)
```

### 幕后老大 FuleManager
FuleManager 利用[伴生对象](https://github.com/LyndonChin/kotlin-docs-zh/blob/master/classes-and-objects/10_objects.md#伴生对象)实现了单例模式：

```kotlin
companion object {
  //manager
  var instance by readWriteLazy { FuelManager() }
}
```

同时利用[代理属性](https://github.com/LyndonChin/kotlin-docs-zh/blob/master/classes-and-objects/12_delegated-properties.md)实现了单例的懒加载。

`readWriteLazy` 是一个函数，它的返回值是一个 `ReadWriteProperty`，代码比较容易，具体可见 [Delegates.kt](https://github.com/kittinunf/Fuel/blob/master/fuel/src/main/kotlin/com/github/kittinunf/fuel/util/Delegates.kt#L8)。

也就是说，当我们第一次访问 `FuelManager` 时，一个具体的实例会被创建出来，这个实例担负了存储公用配置和发起请求的重任，首先来看它的属性：

```kotlin
var client: Client
var proxy: Proxy?
var basePath: String?

var baseHeaders: Map<String, String>?
var baseParams: List<Pair<String, Any?>>

var keystore: KeyStore?
var socketFactory: SSLSocketFactory

var hostnameVerifier: HostnameVerifier
```

`Client` 是一个接口，通过它我们可以自定义 http 引擎。

```kotlin
interface Client {
  fun executeRequest(request: Request): Response
}
```

    +---------+     +--------+     +----------+
    | Request | ==> | Client | ==> | Response |
    +---------+     +--------+     +----------+
                         |
                        \|/                   +--------------------+
                  +------------+              | HttpURLConnection  |
                  | HttpClient | --based on-- +--------------------+
                  +------------+              | HttpsURLConnection |
                                              +--------------------+


Fuel 默认提供的 Http 引擎是 `HttpClient`，它是基于 HttpURLConnection 的实现。

`basePath`、`baseHeaders` 和 `baseParams` 存储了请求的公用配置，我们可以通过 `FuleManager.instance` 为其赋值：

```kotlin
FuelManager.instance.apply {
  basePath = "http://httpbin.org"
  baseHeaders = mapOf("Device" to "Android")
  baseParams = listOf("key" to "value")
}
```

`keystore` 用于构建 `socketFactory`，再加上 `hostnameVerifier`，它们用于 https 请求，在 `HttpClient` 中有用到：

```kotlin
private fun establishConnection(request: Request): URLConnection {
  val urlConnection = if (proxy != null) request.url.openConnection(proxy) else request.url.openConnection()
  return if (request.url.protocol == "https") {
    val conn = urlConnection as HttpsURLConnection
    conn.apply {
      sslSocketFactory = request.socketFactory // socketFactory
      hostnameVerifier = request.hostnameVerifier // hostnameVerifier
    }
  } else {
    urlConnection as HttpURLConnection
  }
}
```

*如果要深入了解 HTTPS 证书，可参考 「[HTTPS 精读之 TLS 证书校验](https://zhuanlan.zhihu.com/p/30655259)」。*

FuelManager 在发起请求时会用这些参数构建一个 `Request`。

```kotlin
fun request(method: Method, path: String, param: List<Pair<String, Any?>>? = null): Request {
  val request = request(Encoding(
        httpMethod = method,
        urlString = path,
        baseUrlString = basePath,
        parameters = if (param == null) baseParams else baseParams + param
  ).request)

  request.client = client
  request.headers += baseHeaders.orEmpty()
  request.socketFactory = socketFactory
  request.hostnameVerifier = hostnameVerifier
  request.executor = createExecutor()
  request.callbackExecutor = callbackExecutor
  request.requestInterceptor = requestInterceptors.foldRight({ r: Request -> r }) { f, acc -> f(acc) }
  request.responseInterceptor = responseInterceptors.foldRight({ _: Request, res: Response -> res }) { f, acc -> f(acc) }
  return request
}
```

关于 `requestInterceptor` 和 `responseInterceptor`，原理与 OkHttp 实现的拦截器一致，只不过这里利用了 Kotlin 的高阶函数，代码实现非常简单，具体细节可参考 「[Kotlin实战之Fuel的高阶函数](http://liangfei.me/2018/04/10/kotlin-fuel-interceptor/)」。

跟其他网络库一样，一次完整的请求，必然包含两个实体—— `Request` & `Response`，先来看 `Request`。

### 请求实体 Request
```kotlin
class Request(
  val method: Method,
  val path: String,
  val url: URL,
  var type: Type = Type.REQUEST,
  val headers: MutableMap<String, String> = mutableMapOf(),
  val parameters: List<Pair<String, Any?>> = listOf(),
  var name: String = "",
  val names: MutableList<String> = mutableListOf(),
  val mediaTypes: MutableList<String> = mutableListOf(),
  var timeoutInMillisecond: Int = 15000,
  var timeoutReadInMillisecond: Int = timeoutInMillisecond) : Fuel.RequestConvertible
```

它支持三种类型的请求：

```kotlin
enum class Type {
  REQUEST,
  DOWNLOAD,
  UPLOAD
}
```

针对每个类型都有对应的任务（task）：

```kotlin
//underlying task request
internal val taskRequest: TaskRequest by lazy {
  when (type) {
    Type.DOWNLOAD -> DownloadTaskRequest(this)
    Type.UPLOAD -> UploadTaskRequest(this)
    else -> TaskRequest(this)
  }
}
```

涉及到上传下载的 `DownloadTaskRequest` 和 `UploadTaskRequest` 都继承自 `TaskRequest`，它们会处理文件和流相关的东西，关于此可参考 IO 哥写的 [一些「流与管道」的小事](https://zhuanlan.zhihu.com/p/35518932) 以及 [OK, IO](https://zhuanlan.zhihu.com/p/35807478)。

`FuelManager` 在构造 `Request` 时用到了一个类——`Encoding`：

```kotlin
class Encoding(
  val httpMethod: Method,
  val urlString: String,
  val requestType: Request.Type = Request.Type.REQUEST,
  val baseUrlString: String? = null,
  val parameters: List<Pair<String, Any?>>? = null) : Fuel.RequestConvertible
```

`Encoding` 也是继承自 `Fuel.RequestConvertible`，它完成了对 `Request` 参数的组装编码，并产生了一个 `Request`。

`Encoding` 组装 query parameter 的方式可以说赏心悦目，贴出来欣赏一下：

```kotlin
private fun queryFromParameters(params: List<Pair<String, Any?>>?): String = params.orEmpty()
  .filterNot { it.second == null }
  .map { (key, value) ->  URLEncoder.encode(key, "UTF-8") to URLEncoder.encode("$value", "UTF-8") }
  .joinToString("&") { (key, value) -> "$key=$value" }
```

### 请求返回结果 Response
```kotlin
class Response(
  val url: URL,
  val statusCode: Int = -1,
  val responseMessage: String = "",
  val headers: Map<String, List<String>> = emptyMap(),
  val contentLength: Long = 0L,
  val dataStream: InputStream = ByteArrayInputStream(ByteArray(0))
```

由 `Response` 的属性可以看出，它所携带的仍然是一个流（Stream），我们先看 `Response` 是如何与 `Request` 串联起来的。

`Deserializable.kt` 文件为 `Request` 定了名称为 `response` 的扩展函数：

```kotlin
private fun <T : Any, U : Deserializable<T>> Request.response(
  deserializable: U,
  success: (Request, Response, T) -> Unit,
  failure: (Request, Response, FuelError) -> Unit): Request {

    val asyncRequest = AsyncTaskRequest(taskRequest)

    asyncRequest.successCallback = { response ->
      val deliverable = Result.of { deserializable.deserialize(response) }
      callback {
        deliverable.fold({
          success(this, response, it)
        }, {
          failure(this, response, FuelError(it))
        })
      }
    }

    asyncRequest.failureCallback = { error, response ->
      callback {
        failure(this, response, error)
      }
    }

    submit(asyncRequest)
    return this
}
```

扩展函数 `response` 的参数中，`deserializable` 负责反序列化操作，`success` 和 `failure` 用于处理请求结果。

Fuel 提供了两个 `Deserializable` 的实现：`StringDeserializer` 以及 `ByteArrayDeserializer`，它们用于反序列化 response 的 stream。

### 异步请求
`Deserializable.kt` 为 `Request` 定义的扩展函数 `response` 在执行异步操作时用到了一个 `AsnycTaskRequest`，其实它本身并不提供异步实现，而是交由一个 `ExecutorService` 去执行，而这个 `ExecutorService` 恰由 `FuelManager` 定义，并在构造 `Request` 时传入给它。

FuleManager.kt
```kotlin
//background executor
var executor: ExecutorService by readWriteLazy {
  Executors.newCachedThreadPool { command ->
    Thread(command).also { thread ->
      thread.priority = Thread.NORM_PRIORITY
      thread.isDaemon = true
    }
  }
}
```

`AsyncTaskRequest` 和 `UploadTaskRequest`、`DownloadTaskRequest` 一样，都是继承自 `TaskRequest`，只不过它多了两个异步调用的回调：

```kotlin
var successCallback: ((Response) -> Unit)? = null
var failureCallback: ((FuelError, Response) -> Unit)? = null
```

## 请求图例
至此，请求、回复，异步调用，对外接口都了解过了，一个基本的网络库框架已经成型。

             +------------------------+
             | https://www.youzan.com |
             +------------------------+
                         |
                         |
                        \|/
                      +------+
                      | Fuel |
                      +------+
                         |
                         |
                        \|/
                  +-------------+
                  | FuelManager |
                  +-------------+
                         |
                         |
                        \|/
    +---------+      +--------+      +----------+
    | Request | ===> | Client | ===> | Response |
    +---------+      +--------+      +----------+

虽然Fuel 的复杂度不可与 OkHttp 相提并论，但是依赖 Kotlin 语言本身的灵活性，它的代码却比 OkHttp 要简洁的多，特别是关于高阶函数和扩展函数的运用，极大地提升了代码的可读性。

## 参考资料

* [原文链接](http://liangfei.me/2018/04/18/kotlin-fuel-details/)
* [一些「流与管道」的小事](https://zhuanlan.zhihu.com/p/35518932)
* [OK，IO](https://zhuanlan.zhihu.com/p/35807478)
* [HTTPS 精读之 TLS 证书校验](https://zhuanlan.zhihu.com/p/30655259)
* [Kotlin 官方中文教程](https://github.com/LyndonChin/kotlin-docs-zh)
* [Kotlin实战之Fuel的高阶函数](http://liangfei.me/2018/04/10/kotlin-fuel-interceptor/)
