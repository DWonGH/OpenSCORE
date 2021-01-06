import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.patient_details_controller import PatientDetailsController


class TestPatientDetailsController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = PatientDetailsController()
        self.model = self.controller.model
        self.view = self.controller.view

    def test_init(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.view)

    def test_update_model(self):
        self.assertIsNone(self.model.name)
        self.assertIsNone(self.model.id)
        self.assertIsNone(self.model.dob)
        self.assertIsNone(self.model.handedness)
        self.assertIsNone(self.model.address)
        self.assertIsNone(self.model.medication)
        self.assertIsNone(self.model.history)

        self.view.lne_name.setText("1")
        self.view.lne_id.setText("1")
        self.view.lne_dob.setText("1")
        self.view.cmb_handedness.setCurrentIndex(1)
        self.view.txe_address.setText("1")
        self.view.txe_medication.setText("1")
        self.view.txe_history.setText("1")
        
        self.controller.update_model()

        self.assertEqual(self.model.name, "1")
        self.assertEqual(self.model.id, "1")
        self.assertEqual(self.model.dob, "1")
        self.assertEqual(self.model.handedness, self.view.txt_handedness[1])
        self.assertEqual(self.model.address, "1")
        self.assertEqual(self.model.medication, "1")
        self.assertEqual(self.model.history, "1")

    def test_update_view(self):
        self.assertEqual(self.view.lne_name.text(), '')
        self.assertEqual(self.view.lne_id.text(), '')
        self.assertEqual(self.view.lne_dob.text(), '')
        self.assertEqual(self.view.cmb_handedness.currentText(), '')
        self.assertEqual(self.view.txe_address.toPlainText(), '')
        self.assertEqual(self.view.txe_history.toPlainText(), '')

        self.model.name = "1"
        self.model.id = "1"
        self.model.dob = "1"
        self.model.handedness = "Right"
        self.model.address = "1"
        self.model.medication = "1"
        self.model.history = "1"

        self.controller.update_view()

        self.assertEqual(self.view.lne_name.text(), '1')
        self.assertEqual(self.view.lne_id.text(), '1')
        self.assertEqual(self.view.lne_dob.text(), '1')
        self.assertEqual(self.view.cmb_handedness.currentText(), 'Right')
        self.assertEqual(self.view.txe_address.toPlainText(), '1')
        self.assertEqual(self.view.txe_history.toPlainText(), '1')


