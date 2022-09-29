---
layout: post
title: RichEditor 源码解析
date: 2016-01-27 10:09:06
categories: Android
---

`RichEditor` 是一个继承自 `WebView` 的自定义 view。

<!--more-->

基本功能
---
枚举类型 `Type` 定了它所支持的排版格式：

```java
public enum Type {
  BOLD,
  ITALIC,
  SUBSCRIPT,
  SUPERSCRIPT,
  STRIKETHROUGH,
  UNDERLINE,
  H1,
  H2,
  H3,
  H4,
  H5,
  H6
}
```

首先在构造函数中加载一个 html 文件。

```java
private static final String SETUP_HTML = "file:///android_asset/editor.html"

public RichEditor(Context context, AttributeSet attrs, int defStyleAttr) {
  super(context, attrs, defStyleAttr);
  setVerticalScrollBarEnabled(false);
  setHorizontalScrollBarEnabled(false);
  getSettings().setJavaScriptEnabled(true);
  setWebChromeClient(new WebChromeClient());
  setWebViewClient(createWebviewClient());

  // 加载 html 文件
  loadUrl(SETUP_HTML);

  applyAttributes(context, attrs);
}
```

其中 html 文件 - `editor.html` 加载了两个 css 文件 - `normalize.css` & `style.css`，一个 js 文件 - `rich_editor.js`。

`body` 中插入了一个 `contentEditable="true"` 的 `div`。

```html
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="user-scalable=no">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" type="text/css" href="normalize.css">
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div id="editor" contentEditable="true"></div>
    <script type="text/javascript" src="rich_editor.js"></script>
  </body>
</html>
```

`rich_editor.js` 中定义了很多排版功能的 API，`RichEditor` 类似 proxy，对外提供了 Java API。

```java
public void setEditorFontColor(int color) {
  String hex = convertHexColorString(color);
  exec("javascript:RE.setBaseTextColor('" + hex + "');");
}
```

其中 `exec` 用于执行 js 代码。

```java
protected void exec(final String trigger) {
  if (isReady) {
    load(trigger);
  } else {
    postDelayed(new Runnable() {
      @Override public void run() {
        exec(trigger);
      }, 100);
    }
  }
}
```

只有当 `rich_editor.html` 加载完成后 `isReady` 才会被置为 `true`。

```java
protected class EditorWebViewClient extends WebViewClient {
  @Override public void onPageFinished(WebView view, String url) {
    isReady = url.equalsIgnoreCase(SETUP_HTML);
    if (mLoadListener != null) {
      mLoadListener.onAfterInitialLoad(isReady);
    }
  }
  // other methods
}
```

构造函数在加载 `editor.html` 之前已经设置了一个 `EditorWebViewClient` 的实例。

```java
public RichEditor(Context context, AttributeSet attrs, int defStyleAttr) {
  // other statements
  setWebViewClient(createWebviewClient());
  loadUrl(SETUP_HTML)
  // other statements
}

protected EditorWebViewClient createWebviewClient() {
  return new EditorWebViewClient();
}
```

当 `editor.html` 加载完成，`isReady` 被设为 `true` 之后，`exec` 方法就可以调用 `load(trigger)` 执行 js 了。

```java
private void load(String trigger) {
  if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
    evaluateJavascript(trigger, null);
  } else {
    loadUrl(trigger);
  }
}
```

`evaluateJavascript` 以及 `loadUrl` 都是 `Webview` 提供的方法。

`evaluateJavascript` 是从 API 19 开始引入的，可以异步执行 js 代码。*Asynchronously evaluates JavaScript in the context of the currently displayed page.*

SCHEME
---

RichEditor 提供了两个 Scheme 负责回调 java 代码。

```java
private static final String CALLBACK_SCHEME = "re-callback://";
private static final String STATE_SCHEME = "re-state://";
```

然后在 `EditorWebViewClient` 中重写了 `shouldOverrideUrlLoading` 方法：

```java
protected class EditorWebViewClient extends WebViewClient {
  @Override
  public void onPageFinished(WebView view, String url) {
    isReady = url.equalsIgnoreCase(SETUP_HTML);
    if (mLoadListener != null) {
      mLoadListener.onAfterInitialLoad(isReady);
    }
  }

  @Override
  public boolean shouldOverrideUrlLoading(WebView view, String url) {
    String decode;
    try {
      decode = URLDecoder.decode(url, "UTF-8");
    } catch (UnsupportedEncodingException e) {
      // No handling
      return false;
    }

    if (TextUtils.indexOf(url, CALLBACK_SCHEME) == 0) {
      callback(decode);
      return true;
    } else if (TextUtils.indexOf(url, STATE_SCHEME) == 0) {
      stateCheck(decode);
      return true;
    }

    return super.shouldOverrideUrlLoading(view, url);
  }
}
```

如果 url 符合 CALLBACK 的 scheme，就会执行 `callback` 方法：

```java
private void callback(String text) {
  mContents = text.replaceFirst(CALLBACK_SCHEME, "");
  if (mTextChangeListener != null) {
    mTextChangeListener.onTextChange(mContents);
  }
}
```

如果 url 符合 STATE 的 scheme，就会执行 `stateCheck` 方法：

```java
private void stateCheck(String text) {
  String state = text.replaceFirst(STATE_SCHEME, "").toUpperCase(Locale.ENGLISH);
  List<Type> types = new ArrayList<>();
  for (Type type : Type.values()) {
    if (TextUtils.indexOf(state, type.name()) != -1) {
      types.add(type);
    }
  }

  if (mDecorationStateListener != null) {
    mDecorationStateListener.onStateChangeListener(state, types);
  }
}
```

通过以下两个 set 方法可以设置回调。

```java
public void setOnDecorationChangeListener(OnDecorationStateListener listener) {
  mDecorationStateListener = listener;
}

public void setOnInitialLoadListener(AfterInitialLoadListener listener) {
  mLoadListener = listener;
}
```

总结
---

编辑器的核心功能由 js 实现，RichEditor 封装了 js 的功能，为上层提供了 java 接口。

参考
---

* https://github.com/wasabeef/richeditor-android
