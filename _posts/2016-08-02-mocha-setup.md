---
layout: post
title: "Setting up Mocha JavaScript test framework"
date: 2016-08-02
---
# Setting up Mocha JavaScript test framework

The following describes how I went about setting up [Mocha](https://mochajs.org/)
for testing some simple Javascript.  I tried to do this with as few dependencies
as possible so I could focus on Mocha's role.  In production I'd also be 
using the [Webpack](karma test runner) (to ease working with multiple 
Javascript modules), [Karma](https://karma-runner.github.io) (test runner)
and [Gulp](http://gulpjs.com/) (to automate Tasks).

## Installing Mocha
I created a new directory for this project then crated a new node project by
running a the following command and hitting Enter when presented with questions.

```bash
npm init
```

I then installed Mocha and [Chai](http://chaijs.com/) an assertion library.  Mocha
doesn't come with an assertion library.

```bash
npm install --save-dev mocha
npm install --save-dev chai
```

## A simple test

I created a simple test file using the example in [Mocha's documentation](https://mochajs.org/#getting-started) as a guide.

```javascript
/* 
 * simple_test.js
 */

var assert = require('chai').assert;

describe('mySum', function () {
    it('Should return sum of two integers', function () {
        assert.equal(4, mySum(2, 2));
    });
});

function mySum(x, y) {
    return x + y;
}
```

I ran the tests in the terminal,

```
./node_modules/mocha/bin/mocha simple_test.js
```

![alt text](http://tdpreece.github.io/assets/img/mocha_setup/mocha_simple_test_run.png "Simple test run results")

## Running tests in a browser

I wanted to be able to test interactions that involved the DOM so I had to run tests in the browser.

I first installed jQuery for convenience.

```
npm install --save-dev jquery
```

Then I created an html file that contained some setup for Mocha and a fixture for my tests (this was based
on the [example in Mocha's documentation](https://mochajs.org/#browser-specific-methods)).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Mocha Tests</title>
  <link href="./node_modules/mocha/mocha.css" rel="stylesheet" />
</head>
<body>
  <div id="mocha"></div>
  <div id="fixture"></div>

  <script src="./node_modules/jquery/dist/jquery.js" ></script>
  <script src="./node_modules/mocha/mocha.js"></script>
  <script src="./node_modules/chai/chai.js"></script>

  <script>mocha.setup('bdd')</script>
  <script src="in_browser_test.js"></script>
  <script>
    mocha.run();
  </script>
</body>
</html>
```

I created a new Javascript test file that interacted with the DOM.

```javascript
/* 
 * in_browser_test.js
 */

describe('Adds my name', function () {
    before(function () {
       this.$fixture = $('<div id="fixture"></div>');
    });
    
    beforeEach(function () {
        $( '#fixtures' ).empty();
    });

    afterEach(function () {
        $( '#fixtures' ).empty();
    });

    it('Should add my name', function () {
        addsName(this.$fixture, 'Tim');
        chai.expect(this.$fixture.html()).to.equal('Tim');
    });
});

function addsName(el, aname) {
    el.html(aname);
}
```

I ran the tests by opening the html file in a browser.

![alt text](http://tdpreece.github.io/assets/img/mocha_setup/mocha_tests_in_browser.png "In browser run results")

## Running tests with PhantomJS

I wanted to be able to run these tests quickly from the command line without the need
to start up a full web browser so I installed [PhantomJS](http://phantomjs.org/) (a headless browser).

I ran the following command to install a PhantomJS runner for Mocha along with PhantomJS and other dependencies.

```bash
npm install --save-dev mocha-phantomjs
```

I then made a copy of the in_browser_test.html named phantom_test_runner.html and made the
following changes,

```html
   <script>mocha.setup('bdd')</script>
   <script src="in_browser_test.js"></script>
   <script>
-    mocha.run();
+    if (window.mochaPhantomJS) { mochaPhantom.run(); }
+    else { mocha.run(); }
   </script>
```

I could then run the tests using PhantomJS from the command line,

```bash
./node_modules/mocha-phantomjs/bin/mocha-phantomjs phantom_test_runner.html
```

![alt text](http://tdpreece.github.io/assets/img/mocha_setup/mocha_phantomjs_run.png "Phantom run results")

