import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.clinical_comments_controller import ClinicalCommentsController


class TestClinicalCommentsController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = ClinicalCommentsController()
        self.model = self.controller.model
        self.view = self.controller.view

    def test_init(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.view)

    def test_update_model(self):
        self.assertIsNone(self.model.interpreter_name)
        self.assertIsNone(self.model.clinical_comments)
        self.controller.update_model()
        self.assertEqual(self.model.interpreter_name, '')
        self.assertEqual(self.model.clinical_comments, '')
        self.view.txe_interpreter_name.setText("1")
        self.view.txe_clinical_comments.setText("1")
        self.controller.update_model()
        self.assertEqual(self.model.interpreter_name, "1")
        self.assertEqual(self.model.clinical_comments, "1")

    def test_update_view(self):
        self.assertEqual(self.view.txe_interpreter_name.text(), '')
        self.assertEqual(self.view.txe_clinical_comments.toPlainText(), '')
        self.model.interpreter_name = "1"
        self.model.clinical_comments = "1"
        self.controller.update_view()
        self.assertEqual(self.view.txe_interpreter_name.text(), "1")
        self.assertEqual(self.view.txe_clinical_comments.toPlainText(), "1")

