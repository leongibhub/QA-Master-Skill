import ast
import unittest
from qa_master.api_codegen import generate_pytest, validate_scenarios
GOOD={"method":"GET","path":"/health","expected_statuses":[200],"approved":True}
class ApiCodegenTests(unittest.TestCase):
    def test_valid(self):
        ast.parse(generate_pytest([GOOD]))
    def test_requires_execution_approval(self):
        self.assertIn("QA_EXECUTION_APPROVED",generate_pytest([GOOD]))
    def test_requires_target(self):
        self.assertIn("QA_TARGET_URL",generate_pytest([GOOD]))
    def test_requires_mutation_approval(self):
        self.assertIn("QA_MUTATION_APPROVED",generate_pytest([dict(GOOD,method="POST",allow_mutation=True)]))
    def test_missing_cases(self):
        with self.assertRaises(ValueError):generate_pytest([])
    def test_case_unapproved(self):
        with self.assertRaises(ValueError):generate_pytest([dict(GOOD,approved=False)])
    def test_no_expected_status(self):
        with self.assertRaises(ValueError):generate_pytest([dict(GOOD,expected_statuses=[])])
    def test_str_status(self):
        with self.assertRaises(ValueError):generate_pytest([dict(GOOD,expected_statuses=["200"])])
    def test_unresolved_parameters(self):
        with self.assertRaises(ValueError):generate_pytest([dict(GOOD,path="/users/{id}")])
    def test_path_traversal(self):
        with self.assertRaises(ValueError):generate_pytest([dict(GOOD,path="/../admin")])
    def test_absolute_url(self):
        with self.assertRaises(ValueError):generate_pytest([dict(GOOD,path="https://example.com/api")])
    def test_mutation_disallowed(self):
        with self.assertRaises(ValueError):generate_pytest([dict(GOOD,method="DELETE")])
    def test_explicit_mutation(self):
        ast.parse(generate_pytest([dict(GOOD,method="POST",allow_mutation=True,json_body={"a":1})]))
    def test_body_validation(self):
        with self.assertRaises(ValueError):validate_scenarios([dict(GOOD,json_body="bad")])
    def test_json_oracle(self):
        self.assertIn("response.json()",generate_pytest([dict(GOOD,expected_json={"ok":True})]))
    def test_multiple_cases(self):
        self.assertEqual(len(validate_scenarios([GOOD,dict(GOOD,path="/ready")])),2)
