import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.views.patient_details import PatientDetailsWidget


class TestPatientDetailsView(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.patient_details = PatientDetailsWidget()
        self.details_dict = None

    def test_init(self):
        self.assertIsNotNone(self.patient_details.lne_name)
        self.assertIsNotNone(self.patient_details.lne_id)
        self.assertIsNotNone(self.patient_details.lne_dob)
        self.assertIsNotNone(self.patient_details.cmb_gender)
        self.assertIsNotNone(self.patient_details.cmb_handedness)
        self.assertIsNotNone(self.patient_details.txe_address)
        self.assertIsNotNone(self.patient_details.txe_medication)
        self.assertIsNotNone(self.patient_details.txe_history)
        target_dict = {
            'Patient name': '',
            'Patient ID': '',
            'Patient DOB': '',
            'Patient gender': '',
            'Patient handedness': '',
            'Patient address': '',
            'Patient medication': '',
            'Patient history': ''
        }
        self.details_dict = self.patient_details.to_dict()
        self.assertEqual(self.details_dict, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.details_dict = self.patient_details.to_dict()
        target_dict = {
            'Patient name': "1",
            'Patient ID': "1",
            'Patient DOB': "1",
            'Patient gender': self.patient_details.txt_gender[1],
            'Patient handedness': self.patient_details.txt_handedness[1],
            'Patient address': "1",
            'Patient medication': "1",
            'Patient history': "1"
        }
        self.assertEqual(self.details_dict, target_dict)

    def set_to_ones(self):
        self.patient_details.lne_name.setText("1")
        self.patient_details.lne_id.setText("1")
        self.patient_details.lne_dob.setText("1")
        self.patient_details.cmb_gender.setCurrentIndex(1)
        self.patient_details.cmb_handedness.setCurrentIndex(1)
        self.patient_details.txe_address.setText("1")
        self.patient_details.txe_medication.setText("1")
        self.patient_details.txe_history.setText("1")
