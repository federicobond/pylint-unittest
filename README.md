pylint-unittest
=============

[![Build Status](https://travis-ci.org/federicobond/pylint-unittest.svg?branch=master)](https://travis-ci.org/federicobond/pylint-unittest)
[![Latest Version](https://img.shields.io/pypi/v/pylint-unittest.svg)](https://pypi.python.org/pypi/pylint-unittest)

# About

`pylint-unittest` is a [Pylint](http://pylint.org) plugin for detecting
incorrect use of unittest assertions.

# Installation

```
pip install pylint-unittest
```

# Usage

Ensure `pylint-unittest` is installed and then execute:

```
pylint --load-plugins pylint_unittest [..other options..] <path_to_your_sources>
```

Alternatively, add `load_plugins=pylint_unittest` to your `pylintrc` file,
under the MASTER section.

# Rules

### wrong-assertion

This rule will complain if you use assertEqual with True, False or None as
arguments instead of the respective `assertTrue`, `assertFalse`, `assertIsNone`.

### deprecated-unittest-alias

This rule will complain if you use a deprecated unittest alias`. See [this](https://docs.python.org/2/library/unittest.html#deprecated-aliases)
for more information.

# License

GPL-3.0
