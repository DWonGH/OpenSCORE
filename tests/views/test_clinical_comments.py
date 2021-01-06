import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.views.clinical_comments import ClinicalCommentsWidget


class TestClinicalCommentsWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.clinical_comments = ClinicalCommentsWidget()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertIsNotNone(self.clinical_comments.txe_interpreter_name)
        self.assertIsNotNone(self.clinical_comments.txe_clinical_comments)
        target_dict = {
            "Interpreter name": '',
            "Clinical comments": ''
        }
        results_dict = self.clinical_comments.to_dict()
        self.assertEqual(results_dict, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.results_dict = self.clinical_comments.to_dict()
        target_dict = {
            "Interpreter name": "1",
            "Clinical comments": "1"
        }
        self.assertEqual(self.results_dict, target_dict)

    def set_to_ones(self):
        self.clinical_comments.txe_interpreter_name.setText("1")
        self.clinical_comments.txe_clinical_comments.setText("1")
