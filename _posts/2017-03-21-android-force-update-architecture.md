---
layout: single
title: Android 强升逻辑和实现
date: 2017-03-21
categories: android
---

“强制升级”会中断用户操作，阻碍正常使用，看似是一个不光彩的行为，但是智者千虑必有一失，我们无法保证 App 的正确性，在某些紧急情况下，强制升级还是非常必要的，而且接入的时间越早越好。

有赞微商城 App 早期版本只提供了一个更新提示的对话框，并不会强制用户去升级。随着后端网关升级，一些老的服务需要下线，但是新版本到达率并不理想，继续维护老接口带来一定成本，而且新功能也无法触及用户。 

产品设计
---

为了提升版本到达率，我们重新梳理了强制升级的逻辑。

![](/assets/imgs/force_update_flow.png)

升级过程中首先要保证 apk 的**下载成功率**，下载完成之后要及时弹出安装页面，为了防止下载失败，也要提供**市场下载**的选项，这样一定程度上也能保证升级之后渠道的一致性。

* 更新对话框需要展示标题、内容和动作按钮。

![](/assets/imgs/recommend_update.jpeg)

![](/assets/imgs/force_update.png)

* 状态栏下载通知需要展示应用名字和描述。

![](/assets/imgs/update_notification.png)

构造参数
---

业务方需要提供的参数：
```java
public class AppUpdater {
  public static class Builder {
    private Context context;

    private String url;         // apk 下载链接
    private String title;       // 更新对话框 title
    private String content;     // 更新内容
    private boolean force;      // 是否强制更新

    private String app;         // app 名字
    private String description; // app 描述
  }

  private AppUpdater(final Builder builder) {
    this.builder = builder;
  }

  public void update() {
    Intent intent = new Intent(builder.context, DownloadActivity.class);
    intent.putExtra(DownloadActivity.EXTRA_STRING_APP_NAME,  builder.app);
    intent.putExtra(DownloadActivity.EXTRA_STRING_URL, builder.url);
    intent.putExtra(DownloadActivity.EXTRA_STRING_TITLE, builder.title);
    intent.putExtra(DownloadActivity.EXTRA_STRING_CONTENT, builder.content);
    intent.putExtra(DownloadActivity.EXTRA_STRING_DESCRIPTION,  builder.description);
    intent.putExtra(DownloadActivity.EXTRA_BOOLEAN_FORCE, builder.force);
    builder.context.startActivity(intent);
  }
```

使用 DownloadManager 下载 apk
---
为了提高下载成功率，我们使用了系统 Service - [DownloadManager][DownloadManager]，因为是独立进程，不会增加 App 占用的系统开销，但是某些 ROM 上禁用了此服务，不过没关系，我们可以引导用户去应用市场或者直接跳转到浏览器去下载。

```java
private void downloadApk() {
 if (TextUtils.isEmpty(downloadUrl)) return;

 // check dir
 File path = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
 if (!path.exists() && !path.mkdirs()) {
   Toast.makeText(this, String.format(getString(R.string.app_updater_dir_not_found),
           path.getPath()), Toast.LENGTH_SHORT).show();
   return;
 }

 /** construct request */
 final DownloadManager.Request request = new DownloadManager.Request(Uri.parse(downloadUrl));
 request.setAllowedNetworkTypes(DownloadManager.Request.NETWORK_MOBILE
         | DownloadManager.Request.NETWORK_WIFI);
 request.setAllowedOverRoaming(false);

 request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS,
         appName + ".apk");


 if (!TextUtils.isEmpty(appName)) {
   request.setTitle(appName);
 }

 if (!TextUtils.isEmpty(description)) {
   request.setDescription(description);
 } else {
   request.setDescription(downloadUrl);
 }

 /** start downloading */
 downloadId = downloadManager.enqueue(request);
 setStatus(STATUS_DOWNLOADING);
}
```

注册监听下载完成的 Receiver
---
我们通过一个全局的 Receiver 来接收下载完成的广播，这样即使 App 进程被杀死，依然可以弹出安装界面。

```xml
<receiver
    android:name=".DownloadReceiver"
    android:enabled="true"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.DOWNLOAD_COMPLETE"/>
    </intent-filter>
</receiver>
```

接收到广播之后，弹出安装界面。
```java
private void installApk(final Context context, final Uri uri) {
    Intent intent = new Intent(Intent.ACTION_VIEW);
    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

    Uri apkUri = uri;
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
        apkUri = FileProvider.getUriForFile(context, context.getPackageName() + ".provider",
                new File(uri.getPath()));
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION
                | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
    }
    intent.setDataAndType(apkUri, "application/vnd.android.package-archive");
    context.startActivity(intent);
}
```

> 注意此处有坑，在 SDK >= 24 的系统中，Intent 不允许携带 `file://` 格式的数据，只能通过 `provider` 的形式共享数据。

所以我们还需要注册一个 `FileProvider`。

```xml
<provider
    android:name="android.support.v4.content.FileProvider"
    android:authorities="${applicationId}.provider"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/provider_paths"/>
</provider>
```

`${applicationId}$` 是 `AndroidManifest.xml` 中的占位符，gradle 会进行替换。

```xml
android:authorities="${applicationId}.provider"
```

对应 Java 代码：

```java
FileProvider.getUriForFile(context, context.getPackageName() + ".provider", new File(uri.getPath()))
```

注意：Java 代码中 `getPackageName()` 的返回值是 `ApplicationId`。

> [package name 和 application id 的区别](http://blog.csdn.net/feelang/article/details/51493501)

* 完整版代码：https://github.com/LyndonChin/ZanAppUpdater

[DownloadManager]:https://developer.android.com/reference/android/app/DownloadManager.html
