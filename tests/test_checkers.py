import astroid
import pylint_unittest
import pylint.testutils


class TestUniqueReturnChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint_unittest.checkers.UnittestAssertionsChecker

    def test_assertEqual_true(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                self.assertEqual(a, True) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='wrong-assert',
                args=('Use assertTrue(x) instead of assertEqual(x, True)',),
                node=assert_node,
            ),
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_assertEqual_false(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                self.assertEqual(a, False) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='wrong-assert',
                args=('Use assertFalse(x) instead of assertEqual(x, False)',),
                node=assert_node,
            ),
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_assertEqual_none(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                self.assertEqual(a, None) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='wrong-assert',
                args=('Use assertIsNone(x) instead of assertEqual(x, None)',),
                node=assert_node,
            ),
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_assertIs_none(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                self.assertIs(a, None) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.Message(
                msg_id='wrong-assert',
                args=('Use assertIsNone(x) instead of assertEqual(x, None)',),
                node=assert_node,
            ),
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)
