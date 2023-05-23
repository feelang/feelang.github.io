---
title: 怎样继承一个内部类
date: 2014-05-18
classes: wide
categories: Java
---

定义一个内部类时，这个内部类会有一个隐式引用 (implicit reference) 指向外部类的实例。例如下面的代码：

```java
class WithInner {
    class Inner {}
}
```

其实，内部类Inner默认会有一个带参数的构造函数，我们通过反射来看一下。

```java
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
class WithInner {
    class Inner {
        public void getConstructors() {
            for (Constructor<?> cons : getClass().getDeclaredConstructors()) {
                StringBuilder sb = new StringBuilder();
                sb.append("constructor: ").append(cons.getName()).append("(");
                for (Class<?> param : cons.getParameterTypes()) {
                    sb.append(param.getSimpleName()).append(", ");
                }
                if (sb.charAt(sb.length() - 1) == ' ') {
                    sb.replace(sb.length() - 2, sb.length(), ")");
                } else {
                    sb.append(')');
                }
                System.out.println(sb);
            }
        }
    }
}

public class InheritInner {
    public static void main(String[] args) {
        WithInner wi = new WithInner();
        WithInner.Inner i = wi.new Inner();
        i.getConstructors();
    }
}

```

输出结果为：

<pre>
constructor: WithInner$Inner(WithInner)
</pre>

从结果可以看出参数的类型就是就是外部类 (outer class)，也就是说，构造内部类的时候，必须要给它一个外部类的引用。接下来我们让 `InheritInner` 继承 `WithInner.Inner`。

```java
class WithInner {
    class Inner {}
}
public class InheritInner extends WithInner.Inner {
    public static void main(String[] args) {
    }
}
```

无法通过编译：

<pre>
InheritInner.java:5: an enclosing instance that contains WithInner.Inner is required
public class InheritInner extends WithInner.Inner {
       ^
1 error
</pre>

报错信息提示我们 `InheritInner` 需要一个 `WithInner` 实例。

那我们给 `InheritInner` 加上我们反射出的带参数的构造函数。照样编译通不过，而且会报同样的错误。这是因为语法规定：在继承内部类的时候，在构造函数中必须要添加 enclosingClassReference.super()。

```java
class WithInner {
    class Inner {}
}


public class InheritInner extends WithInner.Inner {
    public InheritInner(WithInner wi) {
        wi.super();
    }
    public static void main(String[] args) {
        WithInner wi = new WithInner();
        InheritInner ii = new InheritInner(wi);
    }
}
```

OK，编译通过，运行也正常。但是为什么要这么做，我现在也不是很清楚。
