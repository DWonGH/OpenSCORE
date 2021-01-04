import unittest
from src.models.patient_details import Patient


class TestPatientDetails(unittest.TestCase):

    def setUp(self) -> None:
        self.patient_details = Patient()
        self.details_dict = None

    def test_init(self):
        self.assertIsNone(self.patient_details.name)
        self.assertIsNone(self.patient_details.id)
        self.assertIsNone(self.patient_details.dob)
        self.assertIsNone(self.patient_details.gender)
        self.assertIsNone(self.patient_details.handedness)
        self.assertIsNone(self.patient_details.address)
        self.assertIsNone(self.patient_details.medication)
        self.assertIsNone(self.patient_details.history)

    def test_nones_to_dict(self):
        self.patient_details.set_to_nones()
        self.details_dict = self.patient_details.to_dict()
        target_dict = {
            'Patient name': None,
            'Patient ID': None,
            'Patient DOB': None,
            'Patient gender': None,
            'Patient handedness': None,
            'Patient address': None,
            'Patient medication': None,
            'Patient history': None
        }
        self.assertEqual(self.details_dict, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.details_dict = self.patient_details.to_dict()
        target_dict = {
            'Patient name': "1",
            'Patient ID': "1",
            'Patient DOB': "1",
            'Patient gender': "1",
            'Patient handedness': "1",
            'Patient address': "1",
            'Patient medication': "1",
            'Patient history': "1"
        }
        self.assertEqual(self.details_dict, target_dict)

    def set_to_ones(self):
        self.patient_details.name = "1"
        self.patient_details.id = "1"
        self.patient_details.dob = "1"
        self.patient_details.gender = "1"
        self.patient_details.handedness = "1"
        self.patient_details.address = "1"
        self.patient_details.medication = "1"
        self.patient_details.history = "1"
