import unittest
from src.models.patient_referral import Referral


class TestPatientReferral(unittest.TestCase):

    def setUp(self) -> None:
        self.patient_referral = Referral()
        self.referral_dict = None

    def test_init(self):
        self.assertIsNone(self.patient_referral.referrer_name)
        self.assertIsNone(self.patient_referral.referrer_details)
        self.assertIsNone(self.patient_referral.diagnosis)
        self.assertIsNone(self.patient_referral.seizure_frequency)
        self.assertIsNone(self.patient_referral.last_seizure)

    def test_nones_to_dict(self):
        self.patient_referral.set_to_nones()
        self.referral_dict = self.patient_referral.to_dict()
        target_dict = {'Referrer name': None, 'Referrer details': None, 'Diagnosis at referral': None, 'Seizure frequency': None, 'Time since last seizure': None, 'Epilepsy-related indications': None, 'Other differential diagnostic questions': None, 'Specific paediatric indication': None, 'Other indications': None}
        self.assertEqual(self.referral_dict, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.referral_dict = self.patient_referral.to_dict()
        target_dict = {'Referrer name': "1", 'Referrer details': "1", 'Diagnosis at referral': "1", 'Seizure frequency': "1", 'Time since last seizure': "1", 'Epilepsy-related indications': "1", 'Other differential diagnostic questions': "1", 'Specific paediatric indication': "1", 'Other indications': "1"}
        self.assertEqual(self.referral_dict, target_dict)

    def set_to_ones(self):
        self.patient_referral.referrer_name = "1"
        self.patient_referral.referrer_details = "1"
        self.patient_referral.diagnosis = "1"
        self.patient_referral.seizure_frequency = "1"
        self.patient_referral.last_seizure = "1"
        self.patient_referral.epilepsy_indications = "1"
        self.patient_referral.differential_indications = "1"
        self.patient_referral.paediatric_indications = "1"
        self.patient_referral.other_indications = "1"
