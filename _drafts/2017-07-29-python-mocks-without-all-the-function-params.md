---
layout: post
title: "Python mocks without all the function parameters"
date: 2017-07-29
---

The python [mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch) package allows you to use `patch` as a context manager or a decorator. This gets a little unwieldy if you have several functions to mock, e.g.

``` python
class TestMyFunc(unittest.TestCase):
    @mock.patch('amod.dependency_1')
    @mock.patch('amod.dependency_2')
    @mock.patch('amod.dependency_3')
    @mock.patch('amod.dependency_4')
    def test(self, mock_dependency_1, mock_dependency_2, mock_dependency_3, mock_dependency_4):
        mock_dependency_1.return_value = 0 
        mock_dependency_2.return_value = 0 
        mock_dependency_3.return_value = 0 
        mock_dependency_4.return_value = 0 
        self.assertEqual(my_func(), 0)
```

This can be particularly distracting for tests where a`mocked` function isn't relevant to 
the test yet it still has to appear in the test function parameters.

An alternative approach, which I believe aids readability of the test, is to `start` and `stop` the patcher manually, e.g.

``` python
class TestMyFunc(unittest.TestCase):

    def setUp(self):
        self.patcher_1 = mock.patch('amod.dependency_1')
        self.mock_dependency_1 = self.patcher_1.start()
        self.addCleanup(self.patcher_1.stop)

        self.patcher_2 = mock.patch('amod.dependency_2')
        self.mock_dependency_2 = self.patcher_2.start()
        self.addCleanup(self.patcher_2.stop)

        self.patcher_3 = mock.patch('amod.dependency_3')
        self.mock_dependency_3 = self.patcher_3.start()
        self.addCleanup(self.patcher_3.stop)

        self.patcher_4 = mock.patch('amod.dependency_4')
        self.mock_dependency_4 = self.patcher_4.start()
        self.addCleanup(self.patcher_4.stop)

    def test(self):
        self.mock_dependency_1.return_value = 0
        self.mock_dependency_2.return_value = 0
        self.mock_dependency_3.return_value = 0
        self.mock_dependency_4.return_value = 0
        self.assertEqual(my_func(), 0)
```

This can be improved further by extracting the duplication,

```
class PatchToAttribute(object):
    def __init__(self, target, mock_name):
        self.target = target
        self.mock_name = mock_name

    def __call__(self, setUp_func):
        def wrapped_func(test_instance):
            patcher = mock.patch(self.target)
            setattr(test_instance, self.mock_name, patcher.start())
            test_instance.addCleanup(patcher.stop)
            return setUp_func(test_instance)

        return wrapped_func


class TestMyFunc(unittest.TestCase):

    @PatchToAttribute('amod.dependency_1', 'mock_dependency_1')
    @PatchToAttribute('amod.dependency_2', 'mock_dependency_2')
    @PatchToAttribute('amod.dependency_3', 'mock_dependency_3')
    @PatchToAttribute('amod.dependency_4', 'mock_dependency_4')
    def setUp(self):
        pass

    def test(self):
        self.mock_dependency_1.return_value = 0
        self.mock_dependency_2.return_value = 0
        self.mock_dependency_3.return_value = 0
        self.mock_dependency_4.return_value = 0
        self.assertEqual(my_func(), 0)
```

We could go one step further by deriving subclasses from `PatchToAttribute` and adding
default behaviour.

The `amod.py` is shown below.

```python
def dependency_1():
    return 1

def dependency_2():
    return 2

def dependency_3():
    return 3

def dependency_4():
    return 4

def my_func():
    return dependency_1() + dependency_2() + dependency_3() + dependency_4()
```
