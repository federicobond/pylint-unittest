"""Models."""
from astroid.nodes import ClassDef, FunctionDef, Expr, Const, Attribute, Name

from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import check_messages
from pylint.checkers import BaseChecker

from pylint_unittest.__pkginfo__ import BASE_ID
from pylint_unittest.utils import node_is_subclass


MESSAGES = {
    'W%d01' % BASE_ID: ("%s",
                        'wrong-assert',
                        ""),
}

MESSAGE_ASSERTEQUAL_TRUE = 'Use assertTrue(x) instead of assertEqual(x, True)'
MESSAGE_ASSERTEQUAL_FALSE = 'Use assertFalse(x) instead of assertEqual(x, False)'
MESSAGE_ASSERTEQUAL_NONE = 'Use assertIsNone(x) instead of assertEqual(x, None)'


def is_self_assert(node):
    return (
        isinstance(node, Attribute) and
        isinstance(node.expr, Name) and
        node.expr.name == 'self' and
        node.attrname in ('assertEqual', 'assertIs')
    )


class UnittestAssertionsChecker(BaseChecker):
    """Unittest assertions checker."""
    __implements__ = IAstroidChecker

    name = 'unittest-assertions-checker'
    msgs = MESSAGES

    def __init__(self, linter=None):
        super(UnittestAssertionsChecker, self).__init__(linter)    
        self._is_testcase = False

    def visit_classdef(self, node):
        if node_is_subclass(node, 'unittest.case.TestCase', '.TestCase'):
            self._is_testcase = True

    def leave_classdef(self, node):
        self._is_testcase = False

    @check_messages('wrong-assert')
    def visit_call(self, node):
        if not self._is_testcase:
            return

        if is_self_assert(node.func):
            for arg in node.args[:2]:
                if not isinstance(arg, Const):
                    continue
                if arg.value is True:
                    self.add_message('wrong-assert', args=(MESSAGE_ASSERTEQUAL_TRUE,), node=node)
                elif arg.value is False:
                    self.add_message('wrong-assert', args=(MESSAGE_ASSERTEQUAL_FALSE,), node=node)
                elif arg.value is None:
                    self.add_message('wrong-assert', args=(MESSAGE_ASSERTEQUAL_NONE,), node=node)
