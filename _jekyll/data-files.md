---
title: 数据文件
excerpt: Jekyll 构建小型数据库 
lesson: 9
classes: wide
toc: false
---

{% raw %}

我们知道，动态页面可通过 API 动态获取数据，这些数据可能来自专门存储数据的数据库，也可能来自配置文件。

将数据和页面进行分离的做法，有效提高了代码的可维护性。

Jekyll 虽然只支持静态页面，但也能实现数据和页面的分离，只不过这些数据只能存储在本地。

Jekyll 称之为数据文件（Data Files），格式包括 JSON、YAML、CSV 和 TSV，支持全局访问。

下面我们通过一个例子来看一下它的具体用法。

## 创建数据文件

首先，按照 Jekyll 惯例，创建一个下划线开头的文件夹 `_data`，然后在文件夹下创建一个 yaml 文件 `skills.yml`，文件内容如下：

`_data/skills.yml`

```yaml
- name: JavaScript
  proficiency: 8

- name: CSS
  proficiency: 8

- name: React
  proficiency: 7

- name: Flutter
  proficiency: 9
```
    

## 访问数据文件

文件创建完成之后，我们就可以在 HTML 的模板文件中通过 `site.data.skills` 来获取这些数据了。

```html    
<ul>
    {% for skill in site.data.skills %}
        <li>
            {{ skill.name }}
        </li>
    {% endfor %}
</ul>
```    

可以看出，`site.data.skills` 是个数组，代表了 `skills.yml` 的文件内容。

其实，Jekyll 还支持将 `skills.yml` 中每个元素封装成不同文件，放置在 `_data` 的子文件 `skills` 下面，例如：

`_data/skill/javascript.yml`:

```yaml
name: JavaScript
proficiency: 8
```

`_data/skill/css.yml`:

```yaml
name: CSS
proficiency: 8
```
    

`_data/skill/react.yml`:

```yaml
name: React
proficiency: 7
```
    

`_data/skill/flutter.yml`:
    
```yaml
name: Flutter
proficiency: 9
```
    

然后，也是通过 `for` 循环来访问每个文件内容：

```html    
<ul>
    {% for skill_hash in site.data.skills %}
    {% assign skill = skill_hash[1] %}
        <li>
            {{ skill.name }}
        </li>
    {% endfor %}
</ul>
```
    

这样就可以在页面内输出 `skills` 的所有内容，具体代码，可异步至我用 Jekyll 搭建的个人博客
[feelang.github.io](https://github.com/feelang/feelang.github.io)。

{% endraw %}