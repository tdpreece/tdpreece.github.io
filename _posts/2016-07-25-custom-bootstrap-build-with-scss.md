---
layout: post
title: "Custom bootstrap build with SCSS"
date: 2016-07-25
---

The following describes how I went about customising bootstrap using
SCSS.
I tried to do this with as few dependencies as possible so that I could
focus on the subject.  In production I'd use [Gulp](http://gulpjs.com/)
to automate the build process.

## Prerequisites
* Node

## Setting up
I created a new directory for this project then crated a new node 
project by running a the following command and hitting Enter when 
presented with questions.


```bash
mkdir custom_bootstrap_build_with_scsss
cd custom_bootstrap_build_with_scsss
npm init
```

I Installed node-sass, which compiles .scss files to css.

```bash
npm install --save node-sass
```

I then installed [Bower](https://bower.io/) a package manager for 
front-end components.

```bash
npm install --save bower
```

I created a bower.json file by running the following command and hitting
Enter when presented with questions.

```bash
./node_modules/bower/bin/bower init
```

I used Bower to install Bootstrap.
```bash
./node_modules/bower/bin/bower install --save bootstrap-sass
```

## Building the css from scss

I created a scss dir for my site,

```bash
mkdir scss
```

and added a file to hold my site's scss.

```scss
// ./scss/site.scss
@import "bootstrap";
@import "bootstrap/theme";
```

I built the the css using node-sass.

```bash
mkdir css
./node_modules/node-sass/bin/node-sass --include-path ./bower_components/bootstrap-sass/assets/stylesheets -o css scss/
```

This produced a ./css/site.css file, which could then be referenced in the HTML files for my site.

## Customizing Bootstrap

Bootstrap can be customized by setting variables, which will take 
precedence over Bootstrap's defaults.  A list of these variables can be 
found in `./bower_components/bootstrap-sass/assets/stylesheets/bootstrap/_variables.scss`

I wanted to change the colour of the primary buttons so I needed to 
specify a new colour for the $btn-primary-bg variable.

I created a [partial SCSS file](http://sass-lang.com/guide##topic-4) to 
store my variables.


```scss
// ./scss/_variables.scss
$btn-primary-bg: ##ff2828;
```

I then imported the _variables.scss in site.scss


```scss
// ./scss/site.scss
@import "variables";
@import "bootstrap";
@import "bootstrap/theme";
```

`variables` has to be included before bootstrap because of the way bootstrap allows
you to override variables.  In `./bower_components/bootstrap-sass/assets/stylesheets/bootstrap/_variables.scss`
you'll notice that variable definitions are followed by [`!default`](http://sass-lang.com/documentation/file.SASS_REFERENCE.html##variable_defaults_), 
which means that the variable is only assigned if it hasn't already been
assigned.

```scss
// ./bower_components/bootstrap-sass/assets/stylesheets/bootstrap/_variables.scss
$btn-primary-color:              ##fff !default;
$btn-primary-bg:                 $brand-primary !default;
$btn-primary-border:             darken($btn-primary-bg, 5%) !default;`
 
```


I then re-built the site css file and opened it up to check that my 
changes had been applied.

```scss
// ./css/site.css
...
.btn-primary {
  color: ##fff;
  background-color: ##ff2828;
  border-color: ##ff0f0f; }
...
```

## References
[Creating a Custom Bootstrap Build With SCSS - Trey Hunner](https://www.codementor.io/development-process/tutorial/create-custom-bootstrap-build-with-scss)

