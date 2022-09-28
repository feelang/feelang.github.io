---
layout: post
title: Retrofit + RxAndroid 实践总结
date: 2016-07-06
tags: 
 - Android
---

在接入 Retrofit + RxAndroid 之前，项目代码中主要存在如下问题：

0. 服务器 API 的定义方式不一致，有的集中定义，有的定义在业务代码中，没有分类不便于维护。
0. Request / Response / API 三者没有对应关系（Request 参数使用 Map 传递，Response 返回 JSON 数据）。
0. 每次都需要传递 `access_token` 给需要验证登录的 API。
0. Response 中错误信息的数据结构不一致，错误处理不统一。

引入 Retrofit + RxAndroid 后，以上问题都会迎刃而解。

## 定义基类

首先定义一个 `BaseResponse`，所有的 Response 都要继承自它。

### Response
```java
@Keep
public class BaseResponse {
    public static final int CODE_SUCCESS = 0;

    public String msg;
    public int code;
    @SerializedName("error_response")
    public ErrorResponse errorResponse;

    public static final class ErrorResponse {
        public String msg;
        public int code;
    }
}
```

`BaseResponse` 的主要作用是统一了错误信息的格式，同时为后面统一错误处理打好基础。

### ErrorResponseException

为了统一**请求错误**和**返回错误**，我们定义了一个继承自 `IOException` 的子类 `ErrorResponseException`：

```java
public class ErrorResponseException extends IOException {
    public ErrorResponseException() {
        super();
    }

    public ErrorResponseException(String detailMessage) {
        super(detailMessage);
    }
}
```

## 定义 Service Method

```java
public interface TradeService {
    @GET("api.tradecategories/1.0.0/get")
    Observable<Response<CategoryResponse>> tradeCategories();

    @GET("api.trade/1.0.0/get")
    Observable<Response<TradeItemResponse>> tradeDetail(@Query("tid") String tid);
}
```

其中 `CategoryResponse`、`TradeItemResponse` 全部继承自 `BaseResponse`。

泛型 `Response` 由 Retrofit 提供，定义了三个成员变量：

```java
private final okhttp3.Response rawResponse;
private final T body;
private final ResponseBody errorBody;
```

可以看出，`Response` 是对 `okhttp3.Response` 的封装，`body` 是一个 `BaseResponse` 实例。

因为 `Response` 只会根据 `code` 值判断请求是否成功，而不会判断 `body` 的内容是否出错，所以我们把 `Response` 中的错误信息称作**请求错误**，把 `body` 中的错误信息称作**返回错误**。

既然 `Response` 包含了 `BaseResponse`（即 `body`），那么我们就可以对两种错误（请求错误、返回错误）进行统一处理。

## 统一错误处理

Service Method 的返回值类型是 `Observable<Response<? extends BaseResponse>`，实际上业务方想要的是 `Observable<? extends BaseResponse>`，那么我们就定义一个 `Transformer` 来转换这两个 `Observable`。

**转换过程其实就是一个错误处理的过程**，因为我们要从 `Response` 中把 `BaseResponse` 剥离出来，如果 `Response` 或者 `BaseResponse` 中含有错误信息则意味着**转换失败**，直接抛出我们已经定义好的 `ErrorResponseException`，回调  `Subscriber` 的 `onError` 方法。

```java
public class ErrorCheckerTransformer<T extends Response<R>, R extends BaseResponse>
        implements Observable.Transformer<T, R> {

    public static final String DEFAULT_ERROR_MESSAGE = "Oh, no";

    private WeakReference<Context> contextRef;

    public ErrorCheckerTransformer(final Context context) {
        contextRef = new WeakReference<>(context);
    }

    @Override
    public Observable<R> call(Observable<T> observable) {
        return observable.map(new Func1<T, R>() {
            @Override
            public R call(T t) {
                String msg = null;
                if (!t.isSuccessful() || t.body() == null) {
                    msg = DEFAULT_ERROR_MESSAGE;
                } else if (t.body().errorResponse != null) {
                    msg = t.body().errorResponse.msg;
                    if (msg == null) {
                        msg = DEFAULT_ERROR_MESSAGE;
                    }
                } else if (t.body().code != BaseResponse.CODE_SUCCESS) {
                    msg = t.body().msg;
                    if (msg == null) {
                        msg = DEFAULT_ERROR_MESSAGE;
                    }
                }

                if (msg != null) {
                    try {
                        throw new ErrorResponseException(msg);
                    } catch (ErrorResponseException e) {
                        throw Exceptions.propagate(e);
                    }
                }

                return t.body();
            }
        });
    }
}
```

除了获取错误信息 msg 之外，我们还可以根据 code 值来判断是否需要唤起登录：

```java
public void tryLogin(final int responseCode) {
    final Context context = contextRef.get();
    if (context == null) return;

    if (responseCode == CODE_TOKEN_INVALID || responseCode == CODE_TOKEN_INVALID_PY
            || responseCode == CODE_TOKEN_EMPTY) {
        LocalBroadcastManager.getInstance(context)
                .sendBroadcast(new Intent(INTENT_ACTION_LOGIN));
    }
}
```

## 创建 Service Method

不同的 Service Method 可能对应着不同的网关，因此我们需要定义一个工厂为不同的网关生产 Service Method。

```java
public class ServiceFactory {
    public static final String OLD_BASE_URL = "https://liangfeizc.com/gw/oauthentry/";
    public static final String NEW_BASE_URL = "https://liangfei.me/api/oauthentry/";

    private static final OkHttpClient sClient = new OkHttpClient.Builder()
            .addInterceptor(new Interceptor() {
                @Override
                public Response intercept(Chain chain) throws IOException {
                    Request request = chain.request();
                    HttpUrl url = request.url().newBuilder()
                            .addQueryParameter("access_token", UserInfo.getAccessToken())
                            .build();
                    request = request.newBuilder().url(url).build();
                    return chain.proceed(request);
                }
            })
            .build();

    public static <T> T createOldService(Class<T> serviceClazz) {
        return createOauthService(OLD_BASE_URL, serviceClazz);
    }

    public static <T> T createNewService(Class<T> serviceClazz) {
        return createOauthService(NEW_BASE_URL, serviceClazz);
    }

    public static <T> T createOauthService(String baseUrl, Class<T> serviceClazz) {
        Retrofit retrofit = new Retrofit.Builder()
                .client(sClient)
                .baseUrl(baseUrl)
                .addConverterFactory(GsonConverterFactory.create())
                .addCallAdapterFactory(RxJavaCallAdapterFactory.create())
                .build();

        return retrofit.create(serviceClazz);
    }
}

```

因为这两个网关都要求登录后才能访问，因此我们通过 `OkHttpClient#addInterceptor` 拦截 `Request` 之后加上了参数 `access_token`。

## 线程模型

大多数情况下，我们都会在 io 线程发起 request，在主线程处理 response，所以我们定义了一个默认的线程模型：

```java
public class SchedulerTransformer<T> implements Observable.Transformer<T, T> {
    @Override
    public Observable<T> call(Observable<T> observable) {
        return observable
                .subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread());
    }

    public static <T> SchedulerTransformer<T> create() {
        return new SchedulerTransformer<>();
    }
}
```

为了方便使用，我们又定义了一个 `SchedulerTransformer` 和 `ErrorCheckerTransformer` 的合体 `RemoteTransformer`：

```java
public class RemoteTransformer<R extends BaseResponse>
        implements Observable.Transformer<Response<R>, R> {

    private Context mContext;

    public RemoteTransformer(final Context context) {
        mContext = context;
    }

    @Override
    public Observable<R> call(Observable<Response<R>> observable) {
        return observable
                .compose(new SchedulerTransformer<Response<R>>())
                .compose(new ErrorCheckerTransformer<Response<R>, R>(mContext));
    }
}
```

## Subscriber
为了进一步统一错误消息的展示方式，我们又对 `Subscriber` 进行了一层封装。

### BaseSubscriber

```java
public abstract class BaseSubscriber<T> extends Subscriber<T> {
    private WeakReference<Context> contextRef;

    public BaseSubscriber(Context context) {
        contextRef = new WeakReference<>(context);
    }

    protected Context getContext() {
        return contextRef == null ? null : contextRef.get();
    }

    @Override
    public void onError(Throwable e) {
        final Context context = contextRef.get();
        if (context == null) return;

        if (e != null && e instanceof ErrorResponseException) {
            ErrorResponseException exception = (ErrorResponseException) e;
            onError(exception);
        } else {
            // 统一处理由 App 引发的错误
            ErrorResponseException exception = new ErrorResponseException(
                    context.getString(R.string.zan_remote_request_failed),
                    CODE_NETWORK_UNCONNECTED);
            onError(exception);
        }
    }

    public abstract void onError(ErrorResponseException e);

    @Override
    public void onCompleted() {

    }
}
```

### ToastSubscriber

以 Toast 形式展示错误消息。

```java
public abstract class ToastSubscriber<T> extends BaseSubscriber<T> {
    public ToastSubscriber(Context context) {
        super(context);
    }

    @Override
    public void onError(Throwable e) {
        final Context context = getContext();
        if (context == null) return;
        Toast.makeText(context, Errors.detailsOf(e), Toast.LENGTH_SHORT).show();
    }
}
```

### DialogSubscriber

以 Dialog 形式展示错误消息。

```java
public abstract class DialogSubscriber<T> extends BaseSubscriber<T> {

    public DialogSubscriber(Context context) {
        super(context);
    }

    @CallSuper
    @Override
    public void onError(Throwable e) {
        DialogUtil.showDialog(getContext(), e.getMessage(), "OK", true);
    }
}
```

## 统一 loading 动画

每一次网络请求（Remote Request）都会触发一次 loading，而我们希望一个页面（Activity / Fragment）中重叠的多个请求只显示一次 loading 动画（可能是一个 ProgressBar）。
我们可以把请求队列看成一个栈，请求开始意味着入栈，请求完毕意味着出栈，为了简化代码，具体实现没必要使用 `Stack` 变量。 

因为基本上所有的请求都在页面中发起，所以我们在 BaseActivity 中展示 loading 动画：
```java
public abstract class BaseActivity {
    // progress bar
    private int progressCount;
    private View progressView;

    public void showProgressBar() {
        if (++progressCount == 1) {
            progressView = LayoutInflater.from(this).inflate(R.layout.progressbar_layout, null);
            ViewGroup rootView = (ViewGroup) getWindow().getDecorView();
            FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(
                    FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT);
            params.gravity = Gravity.CENTER;
            rootView.addView(progressView, params);
        }
    }

    public void hideProgressBar() {
        if (progressCount > 0 && --progressCount == 0) {
            ViewGroup rootView = (ViewGroup) getWindow().getDecorView();
            rootView.removeView(progressView);
        }
    }
}
```

为了方便 RxJava 使用，再定义一个方法来创建 `RemoteTransformer`：
```java
/**
 * Observable.compose(applyLoading()).
 *
 * @param <T> subclass of {@link BaseResponse}
 * @return the composer of error checker and scheduler.
 */
public <T extends BaseResponse> RemoteTransformer<T> applyLoading() {
    return new RemoteTransformer<T>(this) {
        @Override
        public Observable<T> call(Observable<Response<T>> observable) {
            return super.call(observable).compose(BaseActivity.this.<T>applyProgressBar());
        }
    };
}

public <T> Observable.Transformer<T, T> applyProgressBar() {
    return new Observable.Transformer<T, T>() {
        @Override
        public Observable<T> call(Observable<T> observable) {
            return observable.doOnSubscribe(new Action0() {
                @Override
                public void call() {
                    showProgressBar();
                }
            }).doOnCompleted(new Action0() {
                @Override
                public void call() {
                    hideProgressBar();
                }
            }).doOnError(new Action1<Throwable>() {
                @Override
                public void call(Throwable throwable) {
                    hideProgressBar();
                }
            });
        }
    };
}
```

除了网络请求，loading 可能会用于其他异步操作，因此单独定义了一个 `applyProgressBar` 方法。

`BaseFragment` 直接调用 `BaseActivity` 的方法就可以了：

```java
public class BaseFragament {
    protected void showProgressBar() {
        BaseActivity activity = (BaseActivity) getActivity();
        if (activity != null) {
            activity.showProgressBar();
        }
    }

    protected void hideProgressBar() {
        BaseActivity activity = (BaseActivity) getActivity();
        if (activity != null) {
            activity.hideProgressBar();
        }
    }

    protected <T> Observable.Transformer<T, T> applyProgressBar() {
        return ((BaseActivity) getActivity()).applyProgressBar();
    }

    public <T extends BaseResponse> RemoteTransformer<T> applyLoading() {
        return ((BaseActivity) getActivity()).applyLoading();
    }
}
```

## 如何使用

我们以获取 Category 为例来说明如何利用 Retrofit 和 RxAndroid 来改写现有模块。

### 1. 定义 CategoryResponse
`CategoryResponse` 必须继承自 `BaseResponse`，里面包含了错误信息的数据结构。

```java
@Keep
public class CategoryResponse extends BaseResponse {
    public Response response;

    @Keep
    public static final class Response {
        public List<Category> categories;
    }
}
```

其中 `Category` 是具体的实体类型。

### 2. 定义 Service Method
```java
public interface TradeService {
    @GET("api.tradecategories/1.0.0/get")
    Observable<Response<CategoryResponse>> tradeCategories();
```

**注意点**

* `TradeService` 必须是一个 `interface`，而且不能继承其他 `interface`。
* `tradeCategories` 的返回值必须是  `Observable<Response<? extends BaseResponse>>` 类型。

### 3. 利用 ServiceFactory 创建一个 TradeService 实例

在适当的时机（`Activity#onCreate`、`Fragment#onViewCreated` 等）根据网关类型通过 `ServiceFactory` 创建一个 `TradeService` 实例。

```java
mTradeService = ServiceFactory.createNewService(TradeService.class)
```

### 4. TradeService 获取数据
```java
mTradeService.tradeCategories()
        .compose(new RemoteTransformer<CategoryResponse>(getContext()))
        .compose(applyLoading())
        .map(new Func1<CategoryResponse, List<Category>>() {
            @Override
            public List<Category> call(CategoryResponse response) {
                return response.response.categories;
            }
        })
        .flatMap(new Func1<List<Category>, Observable<Category>>() {
            @Override
            public Observable<Category> call(List<Category> categories) {
                return Observable.from(categories);
            }
        })
        .subscribe(new ToastSubscriber<Category>(getActivity) {
            @Override
            public void onNext(Category category) {
                // business related code
            }
        });
```

注意：`RemoteTransformer` 包含了**线程分配**和**错误处理**两部分功能，所以调用方只需要关心正确的数据就可以了。

## 测试

### NetworkBehavior - 网络环境模拟

```java
private void givenNetworkFailurePercentIs(int failurePercent) {
    mNetworkBehavior.setDelay(0, TimeUnit.MILLISECONDS);
    mNetworkBehavior.setVariancePercent(0);
    mNetworkBehavior.setFailurePercent(failurePercent);
}
```

### TestSubscriber - 带断言的 Subscriber

```java
private TestSubscriber<Response<CategoryResponse>> mTestSubscriberCategory = TestSubscriber.create()
subscriber.assertError(RuntimeException.class);
subscriber.assertNotCompleted();
```

### MockRetrofit - 为 Retrofit 添加 Mock 数据（NetworkBehavior 等）

```java
@Before
public void setUp() {
    Retrofit retrofit = new Retrofit.Builder()
            .addConverterFactory(GsonConverterFactory.create())
            .addCallAdapterFactory(RxJavaCallAdapterFactory.create())
            .baseUrl(ServiceFactory.CARMEN_BASE_URL)
            .build();

    MockRetrofit mockRetrofit = new MockRetrofit.Builder(retrofit)
            .networkBehavior(mNetworkBehavior)
            .build();
}
```

### BehaviorDelegate - Retrofit Service 的代理，用于产生 Mock 数据

```java
BehaviorDelegate<TradesService> delegate = mockRetrofit.create(TradesService.class);
mTradesServiceMock = new TradesServiceMock(delegate);
```

```java
public class TradesServiceMock implements TradesService {
    private final BehaviorDelegate<TradesService> mDelegate;

    public TradesServiceMock(BehaviorDelegate<TradesService> delegate) {
        mDelegate = delegate;
    }

    @Override
    public Observable<Response<CategoryResponse>> tradeCategories() {
        return mDelegate.returningResponse("{\"error_response\": \"my god\"}").tradeCategories();
    }
}
```

总结
---

通过以上实践可以看出，Retrofit + RxAndroid 大大改善了代码的可维护性。

0. 以 API 为中心，Request、Response、Method 一一对应，开发效率飙升
0. 告别 Callback Hell，以同步方式写异步代码，让代码结构更清晰，更易于维护
0. 基于事件，各种 Operator，四两拨千斤，尽情发挥你的想象力。
