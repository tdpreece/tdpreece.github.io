---
layout: post
title: "Webpack example"
date: 2016-09-27
---


## Getting started
First, I followed Webpack's getting [started tutorial](http://webpack.github.io/docs/tutorials/getting-started/).

I created a new npm project and installed webpack
```bash
npm init
npm install --save-dev webpack
```

I then created two Javascript files to demonstrate how to use Javascript that is defined in another module.

```Javascript
// content.js
module.exports = "It works from content.js.";
```

```Javascript
// entry.js
document.write(require("./content.js"));
```

I then compiled this into a bundle file by running,
```bash
./node_modules/webpack/bin/webpack.js ./entry.js bundle.js
```

I tested the bundle.js file by referencing it in an html file and viewing this
file in my browser.

```html
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <script type="text/javascript" src="bundle.js" charset="utf-8"></script>
  </body>
</html>
```

Viewing index.html in a browser simple displays `It works from content.js.`.

## Webpack with Backbone

I wanted to create a simple project using [Backbone.js](http://backbonejs.org/) so I installed backbone along with jQuery and Underscore.

```bash
npm install --save-dev backbone
npm install --save-dev jquery
npm install --save-dev underscore
```

I created a new node project and created directory name `src` for my src files to live in and a directory called `www`, which would contain the files that could be deployed to a web server.  These directories would end up looking like the following.

```bash
> $ tree src/ www/
src/
├── index.html
├── index.js
├── MainView.html
└── MainView.js
www/
├── bundle.js
└── index.html
```

I copied the same `index.html` file from the simple example above into the `src` directory.  As you can see the `index.html` doesn't have to do a lot, just refernce the bundle.js.

I created an index.js file, which would act as an entry to my application, and a Bacbone.js view.
```javascript
// index.js
var $ = require('jquery');
var MainView = require('./MainView');

mainView = new MainView();
$('body').append(mainView.render().el);
```

```javascript
// MainView.js
var Backbone = require('backbone');
var _ = require('underscore');

module.exports = Backbone.View.extend({

  tagName: "div",

  template: require('./MainView.html'),

  events: {
  },

  initialize: function() {
  },

  render: function() {
	this.$el.html(
        this.template({ 'msg': 'This is the Main View' }));
	return this;
  }

});
```

```html
// MainView.html
<h1>{{ msg }}</h1>
```

As I wanted to keep the template file in a separate file I needed to install a
loader

```bash
npm install --save-dev mustache-loader
```

and configure it's use in the webpack.config.js,

```javascript
// webpack.config.js
...
    module: {
        loaders: [{
            test: /\.html$/,
            loader: 'mustache',
        },],
    },
...
```

I also added some config to the webpack.config.js to help it resolve paths, know the entry to my app and where I'd like my bundle.js file saved to,
```javascript
// webpack.config.js
...
    context: __dirname + '/src',
    entry: "./index",
    output: {
        path: __dirname + '/www',
        filename: "bundle.js"
    },
...
```
The final step was to copy the index.html file from `src/` to `www/` as part of the build.  The easiest way for me to do this (without addding new dependencies was to add a script to do this in the package.json.
```javascript
// package.json 
...
  "scripts": {
    "build": "node ./node_modules/webpack/bin/webpack.js && cp ./src/index.html ./www/"
...
```

I built the bundle via the command,
```bash
npm run build
```
Then opened the `www/index.html` file in a browser and could see "This is the Main View".

## Next steps 
Other useful things that Webpack can do:
 * [automatically add vendor prefixes for css](https://www.npmjs.com/package/autoprefixer)(e.g. -webkit-full-screen),
 * [add a source map](https://webpack.github.io/docs/configuration.html#output-devtoolmodulefilenametemplate) 
 * https://webpack.github.io/docs/list-of-plugins.html

