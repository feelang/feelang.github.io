---
layout: post
title: SalesforceAnalytics 源码分析
date: 2017-7-22
categories: Android
---

[SalesforceAnalytics][SalesforceAnalytics] 可分为两个部分：

* Event 存储
* Event 上报

AnalyticsManager
---

AnalyticsManager 有三个属性：

key | type | comment
--- | --- | ---
storeManager | `EventStoreManager` | 在 AnalyticsManager 的构造方法中初始化，只有 getter 没有 setter
deviceAppAttributes | `DeviceAppAttribute` |
globalSequenceId | `int` | global sequence ID used by events

上面的三个属性在构造方法中进行初始化：

```java
public AnalyticsManager(String uniqueId, 
                        Context context, 
                        String encryptionKey, 
                        DeviceAppAttributes deviceAppAttributes) { 
    storeManager = new EventStoreManager(uniqueId, context, encryptionKey);
    this.deviceAppAttributes = deviceAppAttributes;
    globalSequenceId = 0;
}
```

`deviceAppAttributes` 和 `globalSequenceId` 都可以通过 set 方法赋新值。

AnalyticsManage#reset 方法可以删除 storeManager 中的所有 Events：

```java
public AnalyticsManager(String uniqueId, 
                        Context context, 
                        String encryptionKey, 
                        DeviceAppAttributes deviceAppAttributes) { 
    storeManager = new EventStoreManager(uniqueId, context, encryptionKey);
    this.deviceAppAttributes = deviceAppAttributes;
    globalSequenceId = 0;
}
```

DeviceAppAttribute
---
`DeviceAppAttribute` 包含了 App、OS、SDK、Device 的信息，它可以和 `JSONObject` 互相转换。

`DeviceAppAttribute` 的构造初始化位于应用层（SalesforceSDK 模块的 SalesforceAnalyticsManager.java 文件）。

key | meaning | value
--- | --- | ---
appVersion | App version | packageInfo.versionName
appName | App name | 通过 SalesforceSDKManager 设置
osVersion | OS version | Build.VERSION.RELEASE
osName | OS name | android
nativeAppType | App type | Native（SalesforceSDKManager）
mobileSdkVersion | Mobile SDK version | SalesforceSDKManager.SDK_VERSION
deviceModel | Device model | Build.MODEL
deviceId | Device ID
clientId | Client ID | BootConfig 提供

Encryptor
---
Encryptor 是一个工具类，其用途包括 Encryption、Decryption、Hash。

### 初始化
从 Encryptor 的初始化开始分析：

```java
Encrytor.init(getContext())
```

init 是一个静态方法，参数是一个 Context 实例。

init 方法首先检查文件系统是否支持加密：

```java
private static boolean isFileSystemEncrypted;
public static boolean init(Context ctx) {
    // Checks if file system encryption is available and active.
    DevicePolicyManager devicePolicyManager = (DevicePolicyManager) ctx.getSystemService(Service.DEVICE_POLICY_SERVICE);
    isFileSystemEncrypted = devicePolicyManager.getStorageEncryptionStatus() == DevicePolicyManager.ENCRYPTION_STATUS_ACTIVE;
    // ...
}
```

然后尝试去获取最好的加密算法：

```java
private static String bestCipherAvailable;
  
public static boolean init(Context ctx) {
  // Checks if file system encryption is available and active.
  // ...(omitted)
  // Make sure the cryptographic transformations we want to use are available.
  bestCipherAvailable = null;
  try {
    getBestCipher();
  } catch (GeneralSecurityException gex) {
    Log.e(TAG, "Security exception thrown", gex);
  }
  if (bestCipherAvailable == null) {
    return false;
  }
}
```

如果获取不到 cipher，则 init 失败，直接返回 `false`。 `getBestCipher()` 通过 `javax.crypto.Cipher` 去获取加密算法，使用 BC 作为算法提供者（Provider）。

> BC(Bouncy Castle) is a collection of APIs used in cryptography.

Encryptor 并没有把获取到的 Cipher 实例保存下来，而是仅仅保存了 Cipher 的名称 - `bestCipherAvailable`，并且提供了一个默认值 —— `PREFER_CIPHER_TRANSFORMATION`。

```java
private static final String PREFER_CIPHER_TRANSFORMATION = "AES/CBC/PKCS5Padding";
private static String bestCipherAvailable;
```

getBestCipher() 会在多个地方被调用，所以 Encryptor 在初始化时先获取 best cipher 的名称 —— bestCipherAvailable，后续调用 getBestCipher 时会首先尝试使用缓存起来的 bestCipherAvailable 去获取 Cipher 实例。

```java
Cipher cipher = null;
if (bestCipherAvailable != null) {
    return Cipher.getInstance(bestCipherAvailable, "BC");
}
```

如果 Cipher 实例获取失败，再尝试通过 PREFER_CIPHER_TRANSFORMATION 去获取：

```java
try {
    cipher = Cipher.getInstance(PREFER_CIPHER_TRANSFORMATION, "BC");
    if (cipher != null) {
        bestCipherAvailable = PREFER_CIPHER_TRANSFORMATION;
    }
} catch (GeneralSecurityException gex1) {
    Log.e(TAG, "Preferred combo not available", gex1);
}
```

PREFER_CIPHER_TRANSFORMATION 获取成功之后，会把它赋值给 bestCipherAvailable。

通过以上代码分析得出如下结论：

> bestCipherAvailabel 的赋值只有两种情况，要么是 "AES/CBC/PKCS5Padding"，要么是 null
> bestCipherAvailabel 作用是不是为了方便扩展？例如让用户自己指定算法。

### 加密
PREFER_CIPHER_TRANSFORMATION 指定的 AES（Advance Standard Encryption）是对称加密。
encrypt 方法除了需要传入 data 之外，还需要密钥 —— key：

```java
static byte[] encrypt(byte[] data, byte[] key)
```

参数和返回值都是 byte 数组，encrypt 可分解为如下7个步骤：

0. 调用 getBestCipher 方法获取 Cipher 实例
0. 构造密钥规格——SecretKeySpec
0. 构造初始化向量（16位）——IvParameterSpec
0. 利用 SecretKeySpec 和 IvParameterSpec 来初始化 Cipher
0. 利用 Cipher 对 data 进行加密（密文128位）
0. 拼接 IV 和 加密后的 data 到一个大数据 result
0. 返回 result

```java
final Cipher cipher = getBestCipher();
final SecretKeySpec skeySpec = new SecretKeySpec(key, cipher.getAlgorithm());
 
// Generates a unique IV per encryption.
byte[] initVector = generateInitVector();
final IvParameterSpec ivSpec = new IvParameterSpec(initVector);
cipher.init(Cipher.ENCRYPT_MODE, skeySpec, ivSpec);
byte[] meat = cipher.doFinal(data);
 
// Prepends the IV to the encoded data (first 16 bytes / 128 bits).
byte[] result = new byte[initVector.length + meat.length];
System.arraycopy(initVector, 0, result, 0, initVector.length);
System.arraycopy(meat, 0, result, initVector.length, meat.length);
return result;
```

初始化向量（initVector）是利用方法 generateInitVector 生成的：

```java
private static byte[] generateInitVector() throws NoSuchAlgorithmException, NoSuchProviderException {
    final SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
    byte[] iv = new byte[16];
    random.nextBytes(iv);
    return iv;
}
```

名词解释：

> SecureRandom

* This class provides a cryptographically strong random number generator (RNG).

> IV(Initialization Vector)

* In cryptography, an initialization vector (IV) or starting variable (SV) is a fixed-size input to a cryptographic primitive that is typically required to be random or pseudorandom.

> AES

* AES is a variant of Rijndael which has a fixed block size of 128 bits, and a key size of 128, 192, or 256 bits

Cryptor 根据参数和返回值的不同还提供了两个基于 AES-256（256 是 key 的长度）的加密方法：

一、(String data, String key) => byte[]: base64

```java
byte[] keyBytes = Base64.decode(key, Base64.DEFAULT);
byte[] dataBytes = data.getBytes(UTF8);
return Base64.encode(encrypt(dataBytes, keyBytes), Base64.DEFAULT);
```

二、(String data, String key) => String: US-ASCII

```java
byte[] bytes = encryptBytes(data, key);
return new String(bytes, "US-ASCII");
```

### 解密

decrypt 方法是 encrypt 方法的逆，它的声明如下：

```java
static byte[] decrypt(byte[] data, int offset, int length, byte[] key)
```

步骤一、首先获取 encrypt 方法中写入的 IV：

```java
// Grabs the init vector prefix (first 16 bytes / 128 bits).
byte[] initVector = new byte[16];
System.arraycopy(data, offset, initVector, 0, initVector.length);
```

步骤二、然后获取密文——meat：

```java
// Grabs the encrypted body after the init vector prefix.
int meatLen = length - initVector.length;
int meatOffset = offset + initVector.length;
byte[] meat = new byte[meatLen];
System.arraycopy(data, meatOffset, meat, 0, meatLen);
```

步骤三、获取 SecretKeySpec 和 IvParameterSpec 来初始化 Cipher（与 encrypt 相反，init 的 mode 是 Cipher.DECRYPT_MODE）：

```java
final Cipher cipher = getBestCipher();
final SecretKeySpec skeySpec = new SecretKeySpec(key, cipher.getAlgorithm());
final IvParameterSpec ivSpec = new IvParameterSpec(initVector);
cipher.init(Cipher.DECRYPT_MODE, skeySpec, ivSpec);
```

步骤四、cipher 开始对密文——meat 进行解密处理：

```java
byte[] padded = cipher.doFinal(meat, 0, meatLen);
byte[] result = padded;
```

PREFER_CIPHER_TRANSFORMATION 定义的 Cipher 名称是 AES/CBC/PKCS5Padding，里面有一个 padding，应该是用于填充 block size。
那么 block size 是什么呢，可以再看一次 AES 的定义：

> AES is a variant of Rijndael which has a fixed block size of 128 bits, and a key size of 128, 192, or 256 bits

也就是说，block size 是 AES 的长度（128bit/16byte），如果密文长度不足 128 位，需要根据 PKCS5Padding 来填充剩余的位数：

> PKCS5Padding is interpreted as a synonym for PKCS7Padding in the cipher specification. It is simply a historical artifact, and rather than change it Sun decided to simply pretend the PKCS5Padding means the same as PKCS7Padding when applied to block ciphers with a blocksize greater than 8 bytes.

因此，解密之后的数据需要去掉填充值：

```java
byte paddingValue = padded[padded.length - 1];
if (0 <= paddingValue) {
    if (paddingValue < (byte) 16) {
        byte compare = padded[padded.length - paddingValue];
        if (compare == paddingValue) {
            result = new byte[padded.length - paddingValue];
            System.arraycopy(padded, 0, result, 0, result.length);
        }
    }
}
```

最后、返回 result。
Crypto 基于上面的 decrypt 算法还提供了另外两个解密方法：
一、(byte[] data, String key) => String

```java
byte[] keyBytes = Base64.decode(key, Base64.DEFAULT);
byte[] dataBytes = Base64.decode(data, Base64.DEFAULT);
 
// Decrypts with AES-256.
byte[] decryptedData = decrypt(dataBytes, 0, dataBytes.length, keyBytes);
return new String(decryptedData, 0, decryptedData.length, UTF8);
```

二、（String data, String key) => String

```java
return decrypt(data.getBytes(), key);
```

### 哈希

Hashing 用于验证数据的完整性（Integrity），并且算法不可逆。常见的哈希算法有：SHA1、SHA2(SHA256)、SHA3、MD5。

Cryptor 使用了 HMAC SHA-256：

> In cryptography, a Keyed-hash Message Authentication code (HMAC) is a specific type of Message Authentication Code (MAC) involving a cryptographic hash function and a secret cryptographic key.

使用 HMAC 还需要提供一个密钥 —— secret cryptographic key。

```java
static String hash(String data, String key) {
```

**步骤一**、把 String 类型的 data 和 key 转换成 UTF8 编码的 byte 数组：
```java
byte [] keyBytes = key.getBytes(UTF8);
byte [] dataBytes = data.getBytes(UTF8);
```

**步骤二**、获取 MAC（Message Authentication Code） 实例：
```java
Mac sha = Mac.getInstance(MAC_TRANSFORMATION, "BC");
```

**步骤三**、使用 SecreteKeySpec 初始化 MAC 实例（sha）：
```java
SecretKeySpec keySpec = new SecretKeySpec(keyBytes, sha.getAlgorithm());
sha.init(keySpec);
```

**步骤四**、计算哈希值：
```java
byte [] sig = sha.doFinal(dataBytes);
```

**步骤五**、将哈希值（byte 数据）进行 Base64 编码变转换成字符串：
```java
Base64.encodeToString(sig, Base64.NO_WRAP);
```

android.util.Base64 提供了以下几种编解码 flag

flag | meaning
--- | ---
CRLF | Encoder flag bit to indicate lines should be terminated with a CRLF pair instead of just an LF. Has no effect if NO_WRAP is specified as well.
NO_WRAP	| Encoder flag bit to omit all line terminators (i.e., the output will be on one long line).
NO_PADDING | Encoder flag bit to omit the padding '=' characters at the end of the output (if any).
URL_SAFE | Encoder/decoder flag bit to indicate using the "URL and filename safe" variant of Base64 (see RFC 3548 section 4) where - and _ are used in place of + and *. DEFAULT	Encoder/Decoder flag, RFC 2045
NO_CLOSE | Flag to pass to Base64OutputStream to indicate that it should not close the output stream it is wrapping when it itself is closed.

判断是否是 Base64 编码可通过如下代码：

```java
public static boolean isBase64Encoded(String key) {
    try {
        Base64.decode(key, Base64.DEFAULT);
        return true;
    } catch (IllegalArgumentException e) {
        return false;
    }
}
```

EventStoreManager
---

EventStoreManager 用于将 Event 数据加密后存储在文件系统。它有如下存储规则：

* 每一个 Event 对应一个 File
* File 的 rootDir 是 context.getFilesDir()
* File Name 的规则是 EventID + filenameSuffix
    * EventID 通过 UUID.randomUUID() 来生成（by InstrumentationEventBuilder#buildEvent）
    * filenameSuffix 时构造时传入
* Event 存入 File 之前需要加密（Encryptor）
* 从 File 读取 Event 之后需要解密（Encryptor）
* File 最大数是 1000（maxEvents = 1000）

### 初始化
因为 Cryptor 是基于 AES-256 进行加解密，因此构造时需要传入 encryptionKey。

```java
public EventStoreManager(String filenameSuffix, Context context, String encryptionKey) {
  this.filenameSuffix = filenameSuffix;
  this.context = context;
  this.encryptionKey = encryptionKey;
  fileFilter = new EventFileFilter(filenameSuffix);
  rootDir = context.getFilesDir();
}
```

### 更改 encryptionKey

encryptionKey 之后可以更改，但是更改之后所有的 Event File 都需要重新加密存储。

```java
public void changeEncryptionKey(String oldKey, String newKey) {
    final List<InstrumentationEvent> storedEvents = fetchAllEvents();
    deleteAllEvents();
    encryptionKey = newKey;
    storeEvents(storedEvents);
}
```

### 存储 Event
```java
public void storeEvent(InstrumentationEvent event) {
    if (event == null || TextUtils.isEmpty(event.toJson().toString())) {
        Log.d(TAG, "Invalid event");
        return;
    }
    if (!shouldStoreEvent()) {
        return;
    }
    final String filename = event.getEventId() + filenameSuffix;
    FileOutputStream outputStream;
    try {
        outputStream = context.openFileOutput(filename, Context.MODE_PRIVATE);
        outputStream.write(encrypt(event.toJson().toString()).getBytes());
        outputStream.close();
    } catch (Exception e) {
        Log.e(TAG, "Exception occurred while saving event to filesystem", e);
    }
}
```

### 获取 Event
```java
private InstrumentationEvent fetchEvent(File file) {
    if (file == null || !file.exists()) {
        Log.e(TAG, "File does not exist");
        return null;
    }
    InstrumentationEvent event = null;
    String eventString = null;
    final StringBuilder json = new StringBuilder();
    try {
        final BufferedReader br = new BufferedReader(new FileReader(file));
        String line;
        while ((line = br.readLine()) != null) {
            json.append(line).append('\n');
        }
        br.close();
        eventString = decrypt(json.toString());
    } catch (Exception ex) {
        Log.e(TAG, "Exception occurred while attempting to read file contents", ex);
    }
    if (!TextUtils.isEmpty(eventString)) {
        try {
            final JSONObject jsonObject = new JSONObject(eventString);
            event = new InstrumentationEvent(jsonObject);
        } catch (JSONException e) {
            Log.e(TAG, "Exception occurred while attempting to convert to JSON", e);
        }
    }
    return event;
}
```
 
EventStoreManager 获取 rootDir 文件夹下 Event File 的方式比较巧妙：
```java
private List<File> getAllFiles() {
    final List<File> files = new ArrayList<File>();
    final File[] listOfFiles = rootDir.listFiles();
    for (final File file : listOfFiles) {
        if (file != null && fileFilter.accept(rootDir, file.getName())) {
            files.add(file);
        }
    }
    return files;
}
  
private static class EventFileFilter implements FilenameFilter {
    private String fileSuffix;
    public EventFileFilter(String fileSuffix) {
        this.fileSuffix = fileSuffix;
    }
 
    @Override
    public boolean accept(File dir, String filename) {
        return filename != null && filename.endsWith(fileSuffix);
    }
}
```

InstrumentationEvent
---
InstrumentationEvent 表示一个埋点事件，其包含如下字段：

InstrumentEvent 也可以和 JSONObject 互相转换。

### InstrumentationEventBuilder

InstrumentationEvent 属性比较多，通过 InstrumentationEventBuilder 可方便地构造 InstrumentationEvent。

buildEvent 需要从 AnalyticsManager 处获取属性值，所以 InstrumentationEvent 的构造需要传入 AnalyticsManager 实例。
```java
private InstrumentationEventBuilder(AnalyticsManager analyticsManager, Context context) {
    this.analyticsManager = analyticsManager;
    this.context = context;
}
```

build 过程中首先通过 UUID 生成 eventId：
```java
final String eventId = UUID.randomUUID().toString();
```

如果发现必填的字段没有值，会直接抛出异常 - EventBuilderException。 

sequenceId 每次加一：
```java
int sequenceId = analyticsManager.getGlobalSequenceId() + 1;
analyticsManager.setGlobalSequenceId(sequenceId);
```

EventBuilderHelper 位于上层（SalesforceSDK 模块），用于应用层代码的埋点。它提供了同步和异步两种方式：

```java
// 同步
static void createAndStoreEventSync(final String name, final UserAccount userAccount,
                                    final String className, final JSONObject attributes)
// 异步
static void createAndStoreEvent(final String name, final UserAccount userAccount,
                                final String className, final JSONObject attributes)
```

异步埋点通过一个后台线程来执行：
```java
private static final ExecutorService threadPool = Executors.newFixedThreadPool(2);
```

createAndStoreEvent 方法内部的实现如下：
```java
threadPool.execute(new Runnable() {
    @Override
    public void run() {
        createAndStore(name, userAccount, className, attributes);
    }
});
```

不管是同步还是异步，最终都要通过 createAndStore 实现埋点，而 createAndStore 会通过 InstrumentationEventBuilder 来构造一个 Event，然后通过 EventStoreManager 保存到文件中。

createAndStore 的 create 需要提供如下参数：

属性 | 值
--- | ---
name | 参数传入
startTime | `System.currentTimeMillis()`
page | `{ "context": className（参数传入）}`
schemaType | `SchemaType.LightningInteraction`
eventType | `EventType.system`

store 通过如下调用链保存到文件：

> SalesforceAnalyticsManager ==> AnalyticsManager ==> EventStoreManager#storeEvent

## Publisher
AnalyticsManager 负责存储 Event，Publisher 负责上报 Event。

### AnalyticsPublisher
Publisher 和 Transformer 一一对应，他们的映射关系存储在 SalesforceAnalyticsManager 的成员变量 `remotes` 中：

```java
public class SalesforceAnalyticsManager {
  private Map<Class<? extends Transform>, Class<? extends AnalyticsPublisher>> remotes;
}
```

SalesforceAnalyticsManager 是 AnalyticsManager 的应用层，上层代码的埋点都要使用 SalesforceAnalyticsManager：

![](/assets/imgs/arc.png)

上报埋点数据必须要用到 networking，而 networking 属于 SalesforceSDKCore 模块，因此 Publisher 也要属于 SalesforceSDKCore 模块。

Publisher 的接口定义如下：

```java
public interface AnalyticsPublisher {
  boolean publish(JSONArray events);
}
```

### AILTNPublisher

`AnalyticsPublisher` 负责上报 events，但是 events 需要首先转换成一个 JSONArray。SalesforceSDKCore 模块提供了一个具体的实现：

```java
public class AILTNPublisher implements AnalyticsPublisher
```

`AILTNPublisher` 对应着 `AILTNTransformer`，它的 publish 方法会构造出 `JSONArray`：

```javascript
{
  "logLines": [
    {
      "code": "ailtn",
      "data": {
        "schemaType": "",
        "payload": {
        }
      }
    },
    {
      "code": "ailtn",
      "data": {
        "schemaType": "",
        "payload": {
        }
      }
    }
  ]
}
```

其中 `payload` 属性装载的是经过 AILTNTransfromer#tranform 之后的 event 数据（一个 JSONArray）。
 
数组组装完成之后会发往服务端（REST API 是 `/services/data/v39.0/connect/proxy/app-analytics-logging`）。

**第一步**、因为 SalesforceSDK 支持多用户，所以我们要先获取当前用户的 RestClient：

```java
// RestClient allows you to send authenticated HTTP requests to a force.com server.
final RestClient restClient = SalesforceSDKManager.getInstance().getClientManager().peekRestClient();
```

**第二步**、首先用之前组装的 logLines 构造一个 `RequestBody`（Media Type 是 `application/json; charset=utf-8`）：

```java
RequestBody.create(RestRequest.MEDIA_TYPE_JSON, body.toString())
```

**第三步**、用 gzip 进行压缩：

```java
gzipCompressedBody(RequestBody.create(RestRequest.MEDIA_TYPE_JSON, body.toString()))
```

`gzipCompressBody` 的实现方式如下：

```java
private RequestBody gzipCompressedBody(final RequestBody body) {
    return new RequestBody() {
        @Override
        public MediaType contentType() { return body.contentType(); }
 
        @Override
        public long contentLength() {
            return -1; // We don't know the compressed length in advance!
        }
 
        @Override
        public void writeTo(BufferedSink sink) throws IOException {
            final BufferedSink gzipSink = Okio.buffer(new GzipSink(sink));
            body.writeTo(gzipSink);
            gzipSink.close();
        }
    };
}
```

_类似 Decorator 模式，把未压缩的 RequestBody 数据压缩之后返回一个新的 RequestBody。_

_注意：contentLength() 方法的返回值是 -1，因为压缩之后的长度在 gzipCompressBody 创建的 RequestBody 中来不及计算。_

**第四步**、计算 Content-Length：

```java
private RequestBody setContentLength(final RequestBody requestBody) throws IOException {
    final Buffer buffer = new Buffer();
    requestBody.writeTo(buffer);
    return new RequestBody() {
        @Override
        public MediaType contentType() {
            return requestBody.contentType();
        }
 
        @Override
        public long contentLength() {
            return buffer.size();
        }
 
        @Override
        public void writeTo(BufferedSink sink) throws IOException {
            sink.write(buffer.snapshot());
        }
    };
}
```

当然也可以通过 Interceptor 压缩并计算长度：

```java
class GzipRequestInterceptor implements Interceptor {
    @Override
    public Response intercept(Chain chain) throws IOException {
        Request originalRequest = chain.request();
        if (originalRequest.body() == null || originalRequest.header("Content-Encoding") != null) {
            return chain.proceed(originalRequest);
        }
 
        Request compressedRequest = originalRequest.newBuilder()
            .header("Content-Encoding", "gzip")
            .method(originalRequest.method(), setContentLength(gzip(originalRequest.body())))
            .build();
        return chain.proceed(compressedRequest);
  }
}
```

**第五步**、构造 HTTP HEADER 参数：

```java
final Map<String, String> requestHeaders = new HashMap<>();
requestHeaders.put(CONTENT_ENCODING, GZIP);
requestHeaders.put(CONTENT_LENGTH, Long.toString(requestBody.contentLength()));
```

**第六步**、构造 RestRequest 发送请求：

```java
final RestRequest restRequest = new RestRequest(
        RestRequest.RestMethod.POST, apiPath, requestBody, requestHeaders);
restResponse = restClient.sendSync(restRequest);
```


### AnalyticsPublisherService

AnalyticsPublisherService 继承自 `IntentService`，在 `onHandleIntent` 方法中通过调用 SalesforceAnalyticsManager#publishAllEvents 方法把埋点数据发往服务端。

```java
/**
 * Handles the publish action in the provided background thread.
 */
private void handleActionPublish() {
    final UserAccount userAccount = UserAccountManager.getInstance().getCurrentUser();
    if (userAccount != null) {
        final SalesforceAnalyticsManager analyticsManager = SalesforceAnalyticsManager.getInstance(userAccount);
        analyticsManager.publishAllEvents();
    }
}
```

因为 SalesforceSDK 支持多用户，所以调用 `publishAllEvents` 之前先要获取当前用户（userAccount）的 SalesforceAnalyticsManager。 `publishAllEvents` 最终还是要调回 AnalyticsPublisher 的 publish 方法。不过，它会遍历 remotes，把原始的 Event 列表通过 Transformer 进行格式转换，然后调用对应 Publisher 的 publish 方法。

_SalesforceAnalyticsManager.java_
```java
private Map<Class<? extends Transform>, Class<? extends AnalyticsPublisher>> remotes;
```

因为 remotes 的 key 和 value 都是 Class 类型，所以要通过反射来实例化它们：

```java
Transform transformer = null;
try {
    transformer = transformClass.newInstance();
} catch (Exception e) {
    Log.e(TAG, "Exception thrown while instantiating class", e);
}
  
AnalyticsPublisher networkPublisher = null;
try {
    networkPublisher = remotes.get(transformClass).newInstance();
} catch (Exception e) {
    Log.e(TAG, "Exception thrown while instantiating class", e);
}
```

遍历完成，所有的 publisher 都请求成功之后，删除所有的 events：

```java
if (success) {
    eventStoreManager.deleteEvents(eventsIds);
}
```

AnalyticsPublisherService 提供一个静态方法用于启动 Service：

```java
public static void startActionPublish(Context context) {
    final Intent intent = new Intent(context, AnalyticsPublisherService.class);
    intent.setAction(ACTION_PUBLISH);
    context.startService(intent);
}
```

那么，何时启动 Service 呢？SalesforceAnalyticsManager 在初始化时会创建一个「定时任务」，这个定时任务会每隔一段时间去启动一次 AnalyticsPublisherService：

```java
private static final int DEFAULT_PUBLISH_FREQUENCY_IN_HOURS = 8;
private static ScheduledFuture createPublishHandler() {
    final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
    final Runnable publishRunnable = new Runnable() {
        @Override
        public void run() {
            AnalyticsPublisherService.startActionPublish(
                    SalesforceSDKManager.getInstance().getAppContext());
        }
    };
    return scheduler.scheduleAtFixedRate(publishRunnable, 0, sPublishFrequencyInHours,
            TimeUnit.HOURS);
}
```
返回值用一个静态成员变量 —— sScheduler 保存。 默认间隔时间是8个小时，当然也可以由用户指定。

```java
// Adds a handler for publishing if not already active.
if (!sPublishHandlerActive) {
    sScheduler = createPublishHandler();
    sPublishHandlerActive = true;
}
```

`sPublishHandlerActivity` 也是一个静态变量，用于标记定时任务有没有启动。 因为 sScheduler 是一个静态变量，所以所有的用户（UserAccount）会共享一个定时任务
如果用户改变了定时任务的执行周期，需要通过过 sScheduler 结束掉当前的任务，然后重新启动一个新任务

多用户管理
---
SalesforceAnalyticsManager 通过一个 map 来管理多用户实例：

```java
private static Map<String, SalesforceAnalyticsManager> INSTANCES;
public static synchronized SalesforceAnalyticsManager getInstance(UserAccount account,
                                                                  String communityId) {
  // 無関係なスースコードを省略
  String uniqueId = account.getUserId();
  if (UserAccount.INTERNAL_COMMUNITY_ID.equals(communityId)) {
      communityId = null;
  }
 
  if (!TextUtils.isEmpty(communityId)) {
      uniqueId = uniqueId + communityId;
  }
 
  SalesforceAnalyticsManager instance;
  if (INSTANCES == null) {
      INSTANCES = new HashMap<>();
      instance = new SalesforceAnalyticsManager(account, communityId);
      INSTANCES.put(uniqueId, instance);
  } else {
      instance = INSTANCES.get(uniqueId);
  }
 
  if (instance == null) {
      instance = new SalesforceAnalyticsManager(account, communityId);
      INSTANCES.put(uniqueId, instance);
  }
}
```

Transform
---
Transform 会把一个通用的 Event 转换成特定的目标格式。

例如把 `InstrumentationEvent` 转换成 `JSONObject`：
```java
public interface Transform {
  public JSONObject transform(InstrumentationEvent event);
}
```

SalesforceAnalytics 定义了一个把 Event 转换成 AILTN 格式的 AILTNTransformer。

*不知道 AILTN 是什么，网上也没找到资料。*


[SalesforceAnalytics]: https://github.com/forcedotcom/SalesforceMobileSDK-Android/tree/master/libs/SalesforceAnalytics
