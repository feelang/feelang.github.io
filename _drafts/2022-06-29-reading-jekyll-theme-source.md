---
layout: post
title: Jekyll theme
date: 2022-06-29
tags: Jekyll CSS
---

I want to build a website as to be the owned channel of content distribution.
As a software engineer, I know how to leverage computer programming to save money.
But, actually, when I started to be using the static site generator Jekyll, it turned out that I didn't have enough knowledge about CSS.
So I got some source code to read.

The first one is [minima](https://github.com/jekyll/minima).
The basic strucutre comes as following:

```
├── 404.html
├── CODE_OF_CONDUCT.md
├── Gemfile
├── History.markdown
├── LICENSE.txt
├── README.md
├── _config.yml
├── _includes
├── _layouts
├── _posts
├── _sass
├── about.md
├── assets
├── index.md
├── minima.gemspec
├── screenshot.png
└── script
```

I started to read from the `_sass` folder and keep writing notes here.

## SCSS

### [Placeholder Selectors](https://sass-lang.com/documentation/style-rules/placeholder-selectors)

```scss
/**
 * Set `margin-bottom` to maintain vertical rhythm
 */
h1, h2, h3, h4, h5, h6,
p, blockquote, pre,
ul, ol, dl, figure,
%vertical-rhythm {
  margin-bottom: $spacing-unit / 2;
}
```

```scss
/**
 * Clearfix
 */
%clearfix:after {
  content: "";
  display: table;
  clear: both;
}

/**
 * Wrapper
 */
.wrapper {
  max-width: calc(#{$content-width} - (#{$spacing-unit}));
  margin-right: auto;
  margin-left: auto;
  padding-right: $spacing-unit / 2;
  padding-left: $spacing-unit / 2;
  @extend %clearfix;
}
```

### At-rules

#### @mixin
https://sass-lang.com/documentation/at-rules/mixin

It's a SCSS at-rule, pairing with `@include`.

```scss
@mixin relative-font-size($ratio) {
  font-size: #{$ratio}rem;
}
```

#### @import
```scss
// Import pre-styling-overrides hook and style-partials.
@import
  "minima/custom-variables", // Hook to override predefined variables.
  "minima/base",             // Defines element resets.
  "minima/layout",           // Defines structure and style based on CSS selectors.
  "minima/custom-styles"     // Hook to override existing styles.
;
```

### Interpolation

https://sass-lang.com/documentation/interpolation

```scss
body {
  font: $base-font-weight #{$base-font-size}/#{$base-line-height} $base-font-family;
}
```

## CSS

### Properties

* ~~[text-size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/text-size-adjust)~~
* [font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings)
* [font-kerning](https://developer.mozilla.org/en-US/docs/Web/CSS/font-kerning)
* [overflow-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap)

### Units

#### vh & vw
https://stackoverflow.com/questions/24876368/how-do-vw-and-vh-units-work

#### rem




