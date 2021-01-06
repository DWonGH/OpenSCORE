import json
import os
import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.main_window_controller import MainWindowController


class TestMainWindowController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = MainWindowController()
        self.patient_details = self.controller.patient_details_controller
        self.patient_referral = self.controller.patient_referral_controller
        self.recording_conditions = self.controller.recording_conditions_controller
        self.diagnostic_significance = self.controller.diagnostic_significance_controller
        self.clinical_comments = self.controller.clinical_comments_controller

    def test_init(self):
        self.assertIsNotNone(self.controller.model)
        self.assertIsNotNone(self.controller.view)
        self.assert_model_is_default()
        self.assert_view_is_default()

    def test_report_is_loaded(self):
        self.assert_model_is_default()
        self.assert_view_is_default()

    def test_update_from_open(self):
        self.assert_model_is_default()
        self.assert_view_is_default()
        test_report = os.path.join(os.getcwd(), 'data', 'test_report.json')
        self.controller.model.open_report(test_report)
        self.controller.update_view_from_model()
        with open(test_report, 'r') as f:
            test_report_dict = json.load(f)
        self.assertEqual(self.controller.model.report.to_dict(), test_report_dict)
        self.assertEqual(self.controller.recording_conditions_controller.view.lne_edf_location.text(), self.controller.model.edf_file_path)
        self.assertEqual(self.controller.view.toolbar.lbl_current_eeg_name.text(), self.controller.model.edf_file_path)

    def test_update_model_from_view(self):
        self.assert_model_is_default()
        self.assert_view_is_default()
        self.set_view_to_ones()
        self.assert_view_is_ones()
        self.controller.update_model_from_view()
        self.assert_view_is_ones()
        self.assert_model_is_ones()

    def test_update_view_from_model(self):
        self.assert_view_is_default()
        self.assert_model_is_default()
        self.set_model_to_ones()
        self.assert_model_is_ones()
        self.controller.update_view_from_model()
        self.assert_model_is_ones()
        self.assert_view_is_ones()

    def assert_model_is_default(self):
        self.assertIsNone(self.controller.model.report.patient_details.name)
        self.assertIsNone(self.controller.model.report.patient_details.id)
        self.assertIsNone(self.controller.model.report.patient_details.dob)
        self.assertIsNone(self.controller.model.report.patient_details.handedness)
        self.assertIsNone(self.controller.model.report.patient_details.address)
        self.assertIsNone(self.controller.model.report.patient_details.medication)
        self.assertIsNone(self.controller.model.report.patient_details.history)

        self.assertIsNone(self.controller.model.report.patient_referral.referrer_name)
        self.assertIsNone(self.controller.model.report.patient_referral.referrer_details)
        self.assertIsNone(self.controller.model.report.patient_referral.seizure_frequency)
        self.assertIsNone(self.controller.model.report.patient_referral.last_seizure)
        self.assertIsNone(self.controller.model.report.patient_referral.epilepsy_indications)
        self.assertIsNone(self.controller.model.report.patient_referral.differential_indications)
        self.assertIsNone(self.controller.model.report.patient_referral.paediatric_indications)
        self.assertIsNone(self.controller.model.report.patient_referral.other_indications)

        self.assertIsNone(self.controller.model.report.recording_conditions.study_id)
        self.assertIsNone(self.controller.model.report.recording_conditions.study_date)
        self.assertIsNone(self.controller.model.report.recording_conditions.recording_duration)
        self.assertIsNone(self.controller.model.report.recording_conditions.technologist_name)
        self.assertIsNone(self.controller.model.report.recording_conditions.physician_name)
        self.assertIsNone(self.controller.model.report.recording_conditions.sensor_group)
        self.assertIsNone(self.controller.model.report.recording_conditions.recording_type)
        self.assertIsNone(self.controller.model.report.recording_conditions.alertness)
        self.assertIsNone(self.controller.model.report.recording_conditions.cooperation)
        self.assertIsNone(self.controller.model.report.recording_conditions.age)
        self.assertIsNone(self.controller.model.report.recording_conditions.latest_meal)
        self.assertIsNone(self.controller.model.report.recording_conditions.skull_defect)
        self.assertIsNone(self.controller.model.report.recording_conditions.brain_surgery)
        self.assertIsNone(self.controller.model.report.recording_conditions.tech_description)
        self.assertIsNone(self.controller.model.report.recording_conditions.edf_location)

        # TODO: Clinical comments + diagnostic significance

    def set_model_to_ones(self):
        # Set some test data in the model
        self.controller.model.report.patient_details.name = "1"
        self.controller.model.report.patient_details.id = "1"
        self.controller.model.report.patient_details.dob = "1"
        self.controller.model.report.patient_details.handedness = "Right"
        self.controller.model.report.patient_details.address = "1"
        self.controller.model.report.patient_details.medication = "1"
        self.controller.model.report.patient_details.history = "1"

        self.controller.model.report.patient_referral.referrer_name = "1"
        self.controller.model.report.patient_referral.referrer_details = "1"
        self.controller.model.report.patient_referral.diagnosis = "1"
        self.controller.model.report.patient_referral.seizure_frequency = self.patient_referral.view.txt_seizure_freq[1]
        self.controller.model.report.patient_referral.last_seizure = self.patient_referral.view.txt_last_seizure[1]
        self.controller.model.report.patient_referral.epilepsy_indications = {
            'Changes in seizure pattern': 1,
            'Classification of a patient diagnosed with epilepsy': 1,
            'Clinical suspicion of epilepsy or seizure': 1,
            'Considering stopping AED therapy': 1,
            'Drivers license or flight certificate': 1,
            'Monitoring of seizure frequency': 1,
            'Monitoring of status epilepticus': 1,
            'Monitoring the effect of medication': 1,
            'Presurgical evaluation': 1,
            'Reconsider the initial diagnosis of epilepsy': 1,
            'Suspicion of non-convulsive status epilepticus': 1
        }
        self.controller.model.report.patient_referral.differential_indications = {
            'Brain death': 1,
            'Cerebral vascular disease': 1,
            'Coma': 1,
            'Dementia': 1,
            'Disturbance of consciousness': 1,
            'Encephalopathy': 1,
            'Loss of consciousness': 1,
            'Other psychiatric or behavioral symptoms': 1,
            'Paroxysmal behavioral changes': 1,
            'Psychogenic non-epileptic seizures': 1
        }
        self.controller.model.report.patient_referral.paediatric_indications = {
            'Developmental problems': 1,
            'Genetic syndrome': 1,
            'Metabolic disorder': 1,
            'Regression': 1
        }
        self.controller.model.report.patient_referral.other_indications = {
            'Assessment of prognosis': 1,
            'Follow up EEG': 1,
            'Other indication': 1,
            'Research project': 1
        }

        self.controller.model.report.recording_conditions.study_id = "1"
        self.controller.model.report.recording_conditions.study_date = "1"
        self.controller.model.report.recording_conditions.recording_duration = "1.00"
        self.controller.model.report.recording_conditions.technologist_name = "1"
        self.controller.model.report.recording_conditions.physician_name = "1"
        self.controller.model.report.recording_conditions.sensor_group = \
        self.recording_conditions.view.txt_sensor_group[1]
        self.controller.model.report.recording_conditions.recording_type = \
        self.recording_conditions.view.txt_recording_type[1]
        self.controller.model.report.recording_conditions.alertness = self.recording_conditions.view.txt_alertness[1]
        self.controller.model.report.recording_conditions.cooperation = self.recording_conditions.view.txt_cooperation[
            1]
        self.controller.model.report.recording_conditions.age = "1"
        self.controller.model.report.recording_conditions.latest_meal = "1"
        self.controller.model.report.recording_conditions.skull_defect = \
        self.recording_conditions.view.txt_skull_defect[1]
        self.controller.model.report.recording_conditions.brain_surgery = \
        self.recording_conditions.view.txt_brain_surgery[1]
        self.controller.model.report.recording_conditions.tech_description = "1"
        self.controller.model.report.recording_conditions.edf_location = "1"

        self.controller.model.report.diagnostic_significance.diagnosis = "Abnormal recording"
        self.controller.model.report.diagnostic_significance.abnormal_specification = [
                "Psychogenic non-epileptic seizures (PNES)",
                "Other non-epileptic clinical episode",
                "Focal dysfunction of the central nervous system",
                "Diffuse dysfunction of the central nervous system",
                "Coma",
                "Brain death",
                "EEG abnormality of uncertain clinical significance"
            ]

        # TODO: Clinical comments

    def assert_model_is_ones(self):
        self.assertEqual(self.controller.model.report.patient_details.name, "1")
        self.assertEqual(self.controller.model.report.patient_details.id, "1")
        self.assertEqual(self.controller.model.report.patient_details.dob, "1")
        self.assertEqual(self.controller.model.report.patient_details.handedness, self.patient_details.view.txt_handedness[1])
        self.assertEqual(self.controller.model.report.patient_details.address, "1")
        self.assertEqual(self.controller.model.report.patient_details.medication, "1")
        self.assertEqual(self.controller.model.report.patient_details.history, "1")

        self.assertEqual(self.controller.model.report.patient_referral.referrer_name, "1")
        self.assertEqual(self.controller.model.report.patient_referral.referrer_details, "1")
        self.assertEqual(self.controller.model.report.patient_referral.diagnosis, "1")
        self.assertEqual(self.controller.model.report.patient_referral.seizure_frequency, self.patient_referral.view.txt_seizure_freq[1])
        self.assertEqual(self.controller.model.report.patient_referral.last_seizure, self.patient_referral.view.txt_last_seizure[1])
        self.assertEqual(
            self.controller.model.report.patient_referral.epilepsy_indications,
            {
                'Changes in seizure pattern': 1,
                'Classification of a patient diagnosed with epilepsy': 1,
                'Clinical suspicion of epilepsy or seizure': 1,
                'Considering stopping AED therapy': 1,
                'Drivers license or flight certificate': 1,
                'Monitoring of seizure frequency': 1,
                'Monitoring of status epilepticus': 1,
                'Monitoring the effect of medication': 1,
                'Presurgical evaluation': 1,
                'Reconsider the initial diagnosis of epilepsy': 1,
                'Suspicion of non-convulsive status epilepticus': 1
            }
        )
        self.assertEqual(
            self.controller.model.report.patient_referral.differential_indications,
            {
                'Brain death': 1,
                'Cerebral vascular disease': 1,
                'Coma': 1,
                'Dementia': 1,
                'Disturbance of consciousness': 1,
                'Encephalopathy': 1,
                'Loss of consciousness': 1,
                'Other psychiatric or behavioral symptoms': 1,
                'Paroxysmal behavioral changes': 1,
                'Psychogenic non-epileptic seizures': 1
            }
        )
        self.assertEqual(
            self.controller.model.report.patient_referral.paediatric_indications,
            {
                'Developmental problems': 1,
                'Genetic syndrome': 1,
                'Metabolic disorder': 1,
                'Regression': 1
            }
        )
        self.assertEqual(
            self.controller.model.report.patient_referral.other_indications,
            {
                'Assessment of prognosis': 1,
                'Follow up EEG': 1,
                'Other indication': 1,
                'Research project': 1
            }
        )
        self.assertEqual(self.controller.model.report.recording_conditions.study_id, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.study_date, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.recording_duration, "1.00")
        self.assertEqual(self.controller.model.report.recording_conditions.technologist_name, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.physician_name, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.sensor_group,
                         self.recording_conditions.view.txt_sensor_group[1])
        self.assertEqual(self.controller.model.report.recording_conditions.recording_type,
                         self.recording_conditions.view.txt_recording_type[1])
        self.assertEqual(self.controller.model.report.recording_conditions.alertness,
                         self.recording_conditions.view.txt_alertness[1])
        self.assertEqual(self.controller.model.report.recording_conditions.cooperation,
                         self.recording_conditions.view.txt_cooperation[1])
        self.assertEqual(self.controller.model.report.recording_conditions.age, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.latest_meal, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.skull_defect,
                         self.recording_conditions.view.txt_skull_defect[1])
        self.assertEqual(self.controller.model.report.recording_conditions.brain_surgery,
                         self.recording_conditions.view.txt_brain_surgery[1])
        self.assertEqual(self.controller.model.report.recording_conditions.tech_description, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.edf_location, "1")

        # TODO: Clinical comments + diagnostic significance

    def assert_view_is_default(self):
        self.assertEqual(self.controller.view.toolbar.lbl_current_eeg_name.text(), '')

        self.assertEqual(self.patient_details.view.lne_name.text(), '')
        self.assertEqual(self.patient_details.view.lne_id.text(), '')
        self.assertEqual(self.patient_details.view.lne_dob.text(), '')
        self.assertEqual(self.patient_details.view.cmb_handedness.currentText(), '')
        self.assertEqual(self.patient_details.view.txe_address.toPlainText(), '')
        self.assertEqual(self.patient_details.view.txe_history.toPlainText(), '')

        self.assertEqual(self.patient_referral.view.lne_referrer_name.text(), '')
        self.assertEqual(self.patient_referral.view.txe_referrer_details.toPlainText(), '')
        self.assertEqual(self.patient_referral.view.lne_diagnosis.text(), '')
        self.assertEqual(self.patient_referral.view.cmb_seizure_freq.currentText(), '')
        self.assertEqual(self.patient_referral.view.cmb_last_seizure.currentText(), '')
        for i in range(self.patient_referral.view.chlist_epilepsy.rowCount()):
            self.assertEqual(self.patient_referral.view.chlist_epilepsy.item(i).checkState(), 0)
        for i in range(self.patient_referral.view.chlist_other_diagnostic.rowCount()):
            self.assertEqual(
                self.patient_referral.view.chlist_other_diagnostic.item(i).checkState(), 0)
        for i in range(self.patient_referral.view.chlist_peadiatric.rowCount()):
            self.assertEqual(self.patient_referral.view.chlist_peadiatric.item(i).checkState(), 0)
        for i in range(self.patient_referral.view.chlist_other.rowCount()):
            self.assertEqual(self.patient_referral.view.chlist_other.item(i).checkState(), 0)

        self.assertEqual(self.recording_conditions.view.lne_study_id.text(), '')
        self.assertEqual(self.recording_conditions.view.lne_study_date.text(), '')
        self.assertEqual(self.recording_conditions.view.spb_duration.text(), ' ')
        self.assertEqual(self.recording_conditions.view.lne_technologist.text(), '')
        self.assertEqual(self.recording_conditions.view.lne_physician.text(), '')
        self.assertEqual(self.recording_conditions.view.cmb_sensor_group.currentText(), '')
        self.assertEqual(self.recording_conditions.view.cmb_recording_type.currentText(), '')
        self.assertEqual(self.recording_conditions.view.cmb_alertness.currentText(), '')
        self.assertEqual(self.recording_conditions.view.cmb_cooperation.currentText(), '')
        self.assertEqual(self.recording_conditions.view.spb_age.text(), ' ')
        self.assertEqual(self.recording_conditions.view.lne_latest_meal.text(), '')
        self.assertEqual(self.recording_conditions.view.cmb_skull_defect.currentText(), '')
        self.assertEqual(self.recording_conditions.view.cmb_brain_surgery.currentText(), '')
        self.assertEqual(self.recording_conditions.view.txe_tech_description.toPlainText(), '')
        self.assertEqual(self.recording_conditions.view.lne_edf_location.text(), '')

        self.assertFalse(self.diagnostic_significance.view.rbt_normal.isChecked())
        self.assertFalse(self.diagnostic_significance.view.rbt_no_definite.isChecked())
        self.assertFalse(self.diagnostic_significance.view.rbt_abnormal.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_pnes.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_pnes.isEnabled())
        self.assertFalse(self.diagnostic_significance.view.chbx_other_nonepileptic.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_other_nonepileptic.isEnabled())
        self.assertFalse(self.diagnostic_significance.view.chbx_focal_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_focal_dysfunction.isEnabled())
        self.assertFalse(self.diagnostic_significance.view.chbx_diffuse_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_diffuse_dysfunction.isEnabled())
        self.assertFalse(self.diagnostic_significance.view.chbx_coma.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_coma.isEnabled())
        self.assertFalse(self.diagnostic_significance.view.chbx_brain_death.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_brain_death.isEnabled())
        self.assertFalse(self.diagnostic_significance.view.chbx_uncertain.isChecked())
        self.assertFalse(self.diagnostic_significance.view.chbx_uncertain.isEnabled())

        # TODO: clinical comments

    def set_view_to_ones(self):
        self.patient_details.view.lne_name.setText("1")
        self.patient_details.view.lne_id.setText("1")
        self.patient_details.view.lne_dob.setText("1")
        self.patient_details.view.cmb_handedness.setCurrentIndex(1)
        self.patient_details.view.txe_address.setText("1")
        self.patient_details.view.txe_medication.setText("1")
        self.patient_details.view.txe_history.setText("1")

        self.patient_referral.view.lne_referrer_name.setText("1")
        self.patient_referral.view.txe_referrer_details.setText("1")
        self.patient_referral.view.lne_diagnosis.setText("1")
        self.patient_referral.view.cmb_seizure_freq.setCurrentIndex(1)
        self.patient_referral.view.cmb_last_seizure.setCurrentIndex(1)
        self.set_check_list_ones(self.patient_referral.view.chlist_epilepsy)
        self.set_check_list_ones(self.patient_referral.view.chlist_other_diagnostic)
        self.set_check_list_ones(self.patient_referral.view.chlist_peadiatric)
        self.set_check_list_ones(self.patient_referral.view.chlist_other)

        self.recording_conditions.view.lne_study_id.setText("1")
        self.recording_conditions.view.lne_study_date.setText("1")
        self.recording_conditions.view.spb_duration.setValue(1)
        self.recording_conditions.view.lne_technologist.setText("1")
        self.recording_conditions.view.lne_physician.setText("1")
        self.recording_conditions.view.cmb_sensor_group.setCurrentIndex(1)
        self.recording_conditions.view.cmb_recording_type.setCurrentIndex(1)
        self.recording_conditions.view.cmb_alertness.setCurrentIndex(1)
        self.recording_conditions.view.cmb_cooperation.setCurrentIndex(1)
        self.recording_conditions.view.spb_age.setValue(1)
        self.recording_conditions.view.lne_latest_meal.setText("1")
        self.recording_conditions.view.cmb_skull_defect.setCurrentIndex(1)
        self.recording_conditions.view.cmb_brain_surgery.setCurrentIndex(1)
        self.recording_conditions.view.txe_tech_description.setText("1")
        self.recording_conditions.view.lne_edf_location.setText("1")

        self.diagnostic_significance.view.rbt_abnormal.setChecked(True)
        self.diagnostic_significance.view.chbx_pnes.setChecked(True)
        self.diagnostic_significance.view.chbx_other_nonepileptic.setChecked(True)
        self.diagnostic_significance.view.chbx_focal_dysfunction.setChecked(True)
        self.diagnostic_significance.view.chbx_diffuse_dysfunction.setChecked(True)
        self.diagnostic_significance.view.chbx_coma.setChecked(True)
        self.diagnostic_significance.view.chbx_brain_death.setChecked(True)
        self.diagnostic_significance.view.chbx_uncertain.setChecked(True)

        #TODO: Clinical comments

    def assert_view_is_ones(self):
        # Test that the UI has updated correctly
        self.assertEqual(self.patient_details.view.lne_name.text(), '1')
        self.assertEqual(self.patient_details.view.lne_id.text(), '1')
        self.assertEqual(self.patient_details.view.lne_dob.text(), '1')
        self.assertEqual(self.patient_details.view.cmb_handedness.currentText(), 'Right')
        self.assertEqual(self.patient_details.view.txe_address.toPlainText(), '1')
        self.assertEqual(self.patient_details.view.txe_history.toPlainText(), '1')

        self.assertEqual(self.patient_referral.view.lne_referrer_name.text(), '1')
        self.assertEqual(self.patient_referral.view.txe_referrer_details.toPlainText(), "1")
        self.assertEqual(self.patient_referral.view.lne_diagnosis.text(), "1")
        self.assertEqual(self.patient_referral.view.cmb_seizure_freq.currentText(),
                         self.patient_referral.view.txt_seizure_freq[1])
        self.assertEqual(self.patient_referral.view.cmb_last_seizure.currentText(),
                         self.patient_referral.view.txt_last_seizure[1])
        for i in range(self.patient_referral.view.chlist_epilepsy.rowCount()):
            self.assertEqual(self.patient_referral.view.chlist_epilepsy.item(i).checkState(), 1)
        for i in range(self.patient_referral.view.chlist_other_diagnostic.rowCount()):
            self.assertEqual(self.patient_referral.view.chlist_other_diagnostic.item(i).checkState(), 1)
        for i in range(self.patient_referral.view.chlist_peadiatric.rowCount()):
            self.assertEqual(self.patient_referral.view.chlist_peadiatric.item(i).checkState(), 1)
        for i in range(self.patient_referral.view.chlist_other.rowCount()):
            self.assertEqual(self.patient_referral.view.chlist_other.item(i).checkState(), 1)

        self.assertEqual(self.recording_conditions.view.lne_study_id.text(), "1")
        self.assertEqual(self.recording_conditions.view.lne_study_date.text(), "1")
        self.assertEqual(self.recording_conditions.view.spb_duration.text(), "1.00")
        self.assertEqual(self.recording_conditions.view.lne_technologist.text(), "1")
        self.assertEqual(self.recording_conditions.view.lne_physician.text(), "1")
        self.assertEqual(self.recording_conditions.view.cmb_sensor_group.currentText(),
                         self.recording_conditions.view.txt_sensor_group[1])
        self.assertEqual(self.recording_conditions.view.cmb_recording_type.currentText(),
                         self.recording_conditions.view.txt_recording_type[1])
        self.assertEqual(self.recording_conditions.view.cmb_alertness.currentText(),
                         self.recording_conditions.view.txt_alertness[1])
        self.assertEqual(self.recording_conditions.view.cmb_cooperation.currentText(),
                         self.recording_conditions.view.txt_cooperation[1])
        self.assertEqual(self.recording_conditions.view.spb_age.text(), "1")
        self.assertEqual(self.recording_conditions.view.lne_latest_meal.text(), "1")
        self.assertEqual(self.recording_conditions.view.cmb_skull_defect.currentText(),
                         self.recording_conditions.view.txt_skull_defect[1])
        self.assertEqual(self.recording_conditions.view.cmb_brain_surgery.currentText(),
                         self.recording_conditions.view.txt_brain_surgery[1])
        self.assertEqual(self.recording_conditions.view.txe_tech_description.toPlainText(), "1")
        self.assertEqual(self.recording_conditions.view.lne_edf_location.text(), "1")

        self.assertFalse(self.diagnostic_significance.view.rbt_normal.isChecked())
        self.assertFalse(self.diagnostic_significance.view.rbt_no_definite.isChecked())
        self.assertTrue(self.diagnostic_significance.view.rbt_abnormal.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_pnes.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_pnes.isEnabled())
        self.assertTrue(self.diagnostic_significance.view.chbx_other_nonepileptic.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_other_nonepileptic.isEnabled())
        self.assertTrue(self.diagnostic_significance.view.chbx_focal_dysfunction.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_focal_dysfunction.isEnabled())
        self.assertTrue(self.diagnostic_significance.view.chbx_diffuse_dysfunction.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_diffuse_dysfunction.isEnabled())
        self.assertTrue(self.diagnostic_significance.view.chbx_coma.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_coma.isEnabled())
        self.assertTrue(self.diagnostic_significance.view.chbx_brain_death.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_brain_death.isEnabled())
        self.assertTrue(self.diagnostic_significance.view.chbx_uncertain.isChecked())
        self.assertTrue(self.diagnostic_significance.view.chbx_uncertain.isEnabled())

        # TODO: Clinical comments

    def set_check_list_ones(self, chlist):
        for i in range(chlist.rowCount()):
            chlist.item(i).setCheckState(1)