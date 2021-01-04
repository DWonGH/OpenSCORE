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
            'Epilepsy-related indications': {
                'Clinical suspicion of epilepsy or seizure': 0,
                'Changes in seizure pattern': 0,
                'Suspicion of non-convulsive status epilepticus': 0,
                'Reconsider the initial diagnosis of epilepsy': 0,
                'Monitoring of status epilepticus': 0,
                'Classification of a patient diagnosed with epilepsy': 0,
                'Monitoring the effect of medication': 0,
                'Monitoring of seizure frequency': 0,
                'Presurgical evaluation': 0,
                'Considering stopping AED therapy': 0,
                'Drivers license or flight certificate': 0
            },
            'Other differential diagnostic questions': {
                'Psychogenic non-epileptic seizures': 0,
                'Encephalopathy': 0,
                'Loss of consciousness': 0,
                'Cerebral vascular disease': 0,
                'Disturbance of consciousness': 0,
                'Dementia': 0,
                'Paroxysmal behavioral changes': 0,
                'Other psychiatric or behavioral symptoms': 0,
                'Coma': 0,
                'Brain death': 0
            },
            'Specific paediatric indication': {
                'Genetic syndrome': 0,
                'Metabolic disorder': 0,
                'Regression': 0,
                'Developmental problems': 0
            },
            'Other indications': {
                'Follow up EEG': 0,
                'Research project': 0,
                'Assessment of prognosis': 0,
                'Other indication': 0
            }
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
            'Epilepsy-related indications': {
                'Clinical suspicion of epilepsy or seizure': 1,
                'Changes in seizure pattern': 1,
                'Suspicion of non-convulsive status epilepticus': 1,
                'Reconsider the initial diagnosis of epilepsy': 1,
                'Monitoring of status epilepticus': 1,
                'Classification of a patient diagnosed with epilepsy': 1,
                'Monitoring the effect of medication': 1,
                'Monitoring of seizure frequency': 1,
                'Presurgical evaluation': 1,
                'Considering stopping AED therapy': 1,
                'Drivers license or flight certificate': 1
            },
            'Other differential diagnostic questions': {
                'Psychogenic non-epileptic seizures': 1,
                'Encephalopathy': 1,
                'Loss of consciousness': 1,
                'Cerebral vascular disease': 1,
                'Disturbance of consciousness': 1,
                'Dementia': 1,
                'Paroxysmal behavioral changes': 1,
                'Other psychiatric or behavioral symptoms': 1,
                'Coma': 1,
                'Brain death': 1
            },
            'Specific paediatric indication': {
                'Genetic syndrome': 1,
                'Metabolic disorder': 1,
                'Regression': 1,
                'Developmental problems': 1
            },
            'Other indications': {
                'Follow up EEG': 1,
                'Research project': 1,
                'Assessment of prognosis': 1,
                'Other indication': 1
            }
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
