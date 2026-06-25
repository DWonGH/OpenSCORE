import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.views.patient_referral import PatientReferralWidget


class TestPatientReferralView(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.patient_referral = PatientReferralWidget()
        self.results_dict = None

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertIsNotNone(self.patient_referral.lne_referrer_name)
        self.assertIsNotNone(self.patient_referral.lne_diagnosis)
        self.assertIsNotNone(self.patient_referral.cmb_seizure_freq)
        self.assertIsNotNone(self.patient_referral.cmb_last_seizure)
        self.assertIsNotNone(self.patient_referral.chlist_epilepsy)
        self.assertIsNotNone(self.patient_referral.chlist_other_diagnostic)
        self.assertIsNotNone(self.patient_referral.chlist_peadiatric)
        self.assertIsNotNone(self.patient_referral.chlist_other)
        target_dict = {
            'Referrer name': '',
            'Referrer details': '',
            'Diagnosis at referral': '',
            'Seizure frequency': '',
            'Time since last seizure': '',
            'Epilepsy-related indications': [],
            'Other differential diagnostic questions': [],
            'Specific paediatric indication': [],
            'Other indications': []
        }
        self.results_dict = self.patient_referral.to_dict()
        self.assertEqual(self.results_dict, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.results_dict = self.patient_referral.to_dict()
        target_dict = {
            'Referrer name': '1',
            'Referrer details': '1',
            'Diagnosis at referral': '1',
            'Seizure frequency': self.patient_referral.txt_seizure_freq[1],
            'Time since last seizure': self.patient_referral.txt_last_seizure[1],
            'Epilepsy-related indications': self.patient_referral.epilepsy_related_conditions,
            'Other differential diagnostic questions': self.patient_referral.other_differential_diagnostic_questions,
            'Specific paediatric indication': self.patient_referral.specific_paediatric_indication,
            'Other indications': self.patient_referral.other_indication
        }
        self.assertEqual(self.results_dict, target_dict)

    def set_to_ones(self):
        self.patient_referral.lne_referrer_name.setText("1")
        self.patient_referral.txe_referrer_details.setText("1")
        self.patient_referral.lne_diagnosis.setText("1")
        self.patient_referral.cmb_seizure_freq.setCurrentIndex(1)
        self.patient_referral.cmb_last_seizure.setCurrentIndex(1)
        self.set_check_list_ones(self.patient_referral.chlist_epilepsy)
        self.set_check_list_ones(self.patient_referral.chlist_other_diagnostic)
        self.set_check_list_ones(self.patient_referral.chlist_peadiatric)
        self.set_check_list_ones(self.patient_referral.chlist_other)

    def set_check_list_ones(self, chlist):
        for i in range(chlist.rowCount()):
            chlist.item(i).setCheckState(1)
