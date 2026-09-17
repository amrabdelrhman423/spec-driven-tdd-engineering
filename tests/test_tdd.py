import unittest
from core.tdd import (
    TestIntent,
    TestFailureType,
    classify_test_failure,
)

class TestTDDEngine(unittest.TestCase):
    def test_classify_assertion_failure_as_valid_red(self):
        output = """
Traceback (most recent call last):
  File "test_cart.py", line 15, in test_discount
    self.assertEqual(cart.total, 80)
AssertionError: 100 != 80
FAILED (failures=1)
"""
        res = classify_test_failure(output, exit_code=1)
        self.assertTrue(res.is_valid_red)
        self.assertEqual(res.failure_type, TestFailureType.EXPECTED_ASSERTION)
        self.assertIn("Valid RED", res.summary)

    def test_classify_syntax_error_as_infrastructure_failure(self):
        output = """
  File "cart.py", line 4
    def calculate(
                  ^
SyntaxError: unexpected EOF while parsing
"""
        res = classify_test_failure(output, exit_code=1)
        self.assertFalse(res.is_valid_red)
        self.assertEqual(res.failure_type, TestFailureType.INFRASTRUCTURE_FAILURE)
        self.assertIn("syntaxerror", res.summary.lower())

    def test_classify_import_error_as_infrastructure_failure(self):
        output = "ModuleNotFoundError: No module named 'non_existent_module'"
        res = classify_test_failure(output, exit_code=1)
        self.assertFalse(res.is_valid_red)
        self.assertEqual(res.failure_type, TestFailureType.INFRASTRUCTURE_FAILURE)

    def test_unexpected_pass_cannot_be_red(self):
        output = "Ran 1 test in 0.001s\n\nOK"
        res = classify_test_failure(output, exit_code=0)
        self.assertFalse(res.is_valid_red)
        self.assertEqual(res.failure_type, TestFailureType.UNEXPECTED_PASS)

    def test_intent_markdown(self):
        intent = TestIntent(
            requirement_id="REQ-AUTH-01",
            behavior_proven="Emits LoginSuccess upon valid credential submission",
            expected_red_reason="LoginCubit does not exist yet",
            test_file="test/login_cubit_test.dart",
            test_name="emits [LoginLoading, LoginSuccess]",
        )
        md = intent.to_markdown()
        self.assertIn("REQ-AUTH-01", md)
        self.assertIn("LoginCubit does not exist yet", md)

if __name__ == "__main__":
    unittest.main()
