"""pylint_unittest module."""
from __future__ import absolute_import

from .checkers import UnittestAssertionsChecker


def register(linter):
    linter.register_checker(UnittestAssertionsChecker(linter))
