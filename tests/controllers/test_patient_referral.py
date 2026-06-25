import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.patient_referral_controller import PatientReferralController


class TestPatientReferralController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = PatientReferralController()
        self.model = self.controller.model
        self.view = self.controller.view

    def test_init(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.view)

    def test_update_model(self):
        self.assertIsNone(self.model.referrer_name)
        self.assertIsNone(self.model.referrer_details)
        self.assertIsNone(self.model.seizure_frequency)
        self.assertIsNone(self.model.last_seizure)
        self.assertIsNone(self.model.epilepsy_indications)
        self.assertIsNone(self.model.differential_indications)
        self.assertIsNone(self.model.paediatric_indications)
        self.assertIsNone(self.model.other_indications)

        self.view.lne_referrer_name.setText("1")
        self.view.txe_referrer_details.setText("1")
        self.view.lne_diagnosis.setText("1")
        self.view.cmb_seizure_freq.setCurrentIndex(1)
        self.view.cmb_last_seizure.setCurrentIndex(1)
        self.set_check_list_ones(self.view.chlist_epilepsy)
        self.set_check_list_ones(self.view.chlist_other_diagnostic)
        self.set_check_list_ones(self.view.chlist_peadiatric)
        self.set_check_list_ones(self.view.chlist_other)

        self.controller.update_model()

        self.assertEqual(self.model.referrer_name, "1")
        self.assertEqual(self.model.referrer_details, "1")
        self.assertEqual(self.model.diagnosis, "1")
        self.assertEqual(self.model.seizure_frequency, self.view.txt_seizure_freq[1])
        self.assertEqual(self.model.last_seizure, self.view.txt_last_seizure[1])
        self.assertEqual(self.model.epilepsy_indications, self.view.epilepsy_related_conditions)
        self.assertEqual(self.model.differential_indications, self.view.other_differential_diagnostic_questions)
        self.assertEqual(self.model.paediatric_indications, self.view.specific_paediatric_indication)
        self.assertEqual(self.model.other_indications, self.view.other_indication)

    def test_update_view(self):
        self.assertEqual(self.view.lne_referrer_name.text(), '')
        self.assertEqual(self.view.txe_referrer_details.toPlainText(), '')
        self.assertEqual(self.view.lne_diagnosis.text(), '')
        self.assertEqual(self.view.cmb_seizure_freq.currentText(), '')
        self.assertEqual(self.view.cmb_last_seizure.currentText(), '')
        for i in range(self.view.chlist_epilepsy.rowCount()):
            self.assertEqual(self.view.chlist_epilepsy.item(i).checkState(), 0)
        for i in range(self.view.chlist_other_diagnostic.rowCount()):
            self.assertEqual(
                self.view.chlist_other_diagnostic.item(i).checkState(), 0)
        for i in range(self.view.chlist_peadiatric.rowCount()):
            self.assertEqual(self.view.chlist_peadiatric.item(i).checkState(), 0)
        for i in range(self.view.chlist_other.rowCount()):
            self.assertEqual(self.view.chlist_other.item(i).checkState(), 0)

        self.model.referrer_name = "1"
        self.model.referrer_details = "1"
        self.model.diagnosis = "1"
        self.model.seizure_frequency = self.view.txt_seizure_freq[1]
        self.model.last_seizure = self.view.txt_last_seizure[1]
        self.model.epilepsy_indications = self.view.epilepsy_related_conditions
        self.model.differential_indications = self.view.other_differential_diagnostic_questions
        self.model.paediatric_indications = self.view.specific_paediatric_indication
        self.model.other_indications = self.view.other_indication

        self.controller.update_view()

        self.assertEqual(self.view.lne_referrer_name.text(), '1')
        self.assertEqual(self.view.txe_referrer_details.toPlainText(), "1")
        self.assertEqual(self.view.lne_diagnosis.text(), "1")
        self.assertEqual(self.view.cmb_seizure_freq.currentText(), self.view.txt_seizure_freq[1])
        self.assertEqual(self.view.cmb_last_seizure.currentText(), self.view.txt_last_seizure[1])
        for i in range(self.view.chlist_epilepsy.rowCount()):
            self.assertEqual(self.view.chlist_epilepsy.item(i).checkState(), 2)
        for i in range(self.view.chlist_other_diagnostic.rowCount()):
            self.assertEqual(self.view.chlist_other_diagnostic.item(i).checkState(), 2)
        for i in range(self.view.chlist_peadiatric.rowCount()):
            self.assertEqual(self.view.chlist_peadiatric.item(i).checkState(), 2)
        for i in range(self.view.chlist_other.rowCount()):
            self.assertEqual(self.view.chlist_other.item(i).checkState(), 2)

    def set_check_list_ones(self, chlist):
        for i in range(chlist.rowCount()):
            chlist.item(i).setCheckState(1)
