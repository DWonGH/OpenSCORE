import unittest

from src.models.clinical_comments import ClinicalComments


class TestClinicalComments(unittest.TestCase):

    def setUp(self) -> None:
        self.clinical_comments = ClinicalComments()

    def test_init(self):
        self.assert_default()

    def test_nones_to_dict(self):
        self.clinical_comments.set_to_nones()
        self.assertIsNone(self.clinical_comments.interpreter_name)
        self.assertIsNone(self.clinical_comments.clinical_comments)

    def test_set_to_ones(self):
        self.set_to_ones()
        self.details_dict = self.clinical_comments.to_dict()
        target_dict = {
            "Interpreter name": "1",
            "Clinical comments": "1"
        }
        self.assertEqual(self.details_dict, target_dict)

    def set_to_ones(self):
        self.clinical_comments.interpreter_name = "1"
        self.clinical_comments.clinical_comments = "1"

    def assert_default(self):
        self.assertIsNone(self.clinical_comments.interpreter_name)
        self.assertIsNone(self.clinical_comments.clinical_comments)
