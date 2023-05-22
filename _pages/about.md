---
layout: page
title: 关于
permalink: /about/
---

## FeeLang

十年以上编程经验，精通多种编程语言和框架。

曾在杭州某互联网大厂做过多年前端（React）和后端（Java/SpringBoot）开发。

现自由职业。

## 联系我

<ul>
    {% for channel in site.data.channels %}
        <li>
            <a href="{{ channel.url }}">
                {{ channel.name }}
            </a>
        </li>
    {% endfor %}
</ul>
