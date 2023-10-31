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
            pylint.testutils.MessageTest(
                msg_id='wrong-assert',
                args=('assertTrue(x) or assertIs(x, True)', 'assertEqual(x, True)'),
                node=assert_node,
            ),
            ignore_position=True
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
            pylint.testutils.MessageTest(
                msg_id='wrong-assert',
                args=('assertFalse(x) or assertIs(x, False)', 'assertEqual(x, False)',),
                node=assert_node,
            ),
            ignore_position=True
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
            pylint.testutils.MessageTest(
                msg_id='wrong-assert',
                args=('assertIsNone(x)', 'assertEqual(x, None)',),
                node=assert_node,
            ),
            ignore_position=True
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
            pylint.testutils.MessageTest(
                msg_id='wrong-assert',
                args=('assertIsNone(x)', 'assertEqual(x, None)'),
                node=assert_node,
            ),
            ignore_position=True
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_works_with_TestCase_subclasses(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class BaseTestCase(unittest.TestCase):
            pass

        class Tests(BaseTestCase): #@
            def test_foo():
                self.assertEqual(a, True) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id='wrong-assert',
                args=('assertTrue(x) or assertIs(x, True)', 'assertEqual(x, True)'),
                node=assert_node,
            ),
            ignore_position=True
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_ignores_non_TestCase_subclasses(self):
        class_node, assert_node = astroid.extract_node("""
        class Tests(object): #@
            def test_foo():
                self.assertEqual(a, True) #@
        """)

        with self.assertNoMessages():
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_deprecated_alias(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                self.failIfEqual(a, None) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id='deprecated-unittest-alias',
                args=('failIfEqual', 'assertNotEqual'),
                node=assert_node,
            ),
            ignore_position=True
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_isinstance(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                self.assertTrue(isinstance(a, Class)) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id='wrong-assert',
                args=('assertIsInstance(x, Class)', 'assertTrue(isinstance(x, Class))'),
                node=assert_node,
            ),
            ignore_position=True
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_isinstance_does_not_fail_with_other_expression(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                form = Form()
                self.assertTrue(form.is_valid()) #@
        """)

        with self.assertNoMessages():
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)

    def test_isnotinstance(self):
        class_node, assert_node = astroid.extract_node("""
        import unittest

        class Tests(unittest.TestCase): #@
            def test_foo():
                self.assertFalse(isinstance(a, Class)) #@
        """)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id='wrong-assert',
                args=('assertIsNotInstance(x, Class)', 'assertFalse(isinstance(x, Class))'),
                node=assert_node,
            ),
            ignore_position=True
        ):
            self.checker.visit_classdef(class_node)
            self.checker.visit_call(assert_node)
            self.checker.leave_classdef(class_node)
