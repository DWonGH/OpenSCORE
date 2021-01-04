import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.main_window_controller import MainWindowController


class TestMainWindowController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = MainWindowController()

    def test_init(self):
        self.assertIsNotNone(self.controller.model)
        self.assertIsNotNone(self.controller.view)

    def test_update_model_from_view(self):

        # Test that the model is default / blank
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

        # Fill out the UI form with some test data
        self.controller.view.patient_details.lne_name.setText("1")
        self.controller.view.patient_details.lne_id.setText("1")
        self.controller.view.patient_details.lne_dob.setText("1")
        self.controller.view.patient_details.cmb_handedness.setCurrentIndex(1)
        self.controller.view.patient_details.txe_address.setText("1")
        self.controller.view.patient_details.txe_medication.setText("1")
        self.controller.view.patient_details.txe_history.setText("1")

        self.controller.view.patient_referral.lne_referrer_name.setText("1")
        self.controller.view.patient_referral.txe_referrer_details.setText("1")
        self.controller.view.patient_referral.lne_diagnosis.setText("1")
        self.controller.view.patient_referral.cmb_seizure_freq.setCurrentIndex(1)
        self.controller.view.patient_referral.cmb_last_seizure.setCurrentIndex(1)
        self.set_check_list_ones(self.controller.view.patient_referral.chlist_epilepsy)
        self.set_check_list_ones(self.controller.view.patient_referral.chlist_other_diagnostic)
        self.set_check_list_ones(self.controller.view.patient_referral.chlist_peadiatric)
        self.set_check_list_ones(self.controller.view.patient_referral.chlist_other)

        self.controller.view.recording_conditions.lne_study_id.setText("1")
        self.controller.view.recording_conditions.lne_study_date.setText("1")
        self.controller.view.recording_conditions.spb_duration.setValue(1)
        self.controller.view.recording_conditions.lne_technologist.setText("1")
        self.controller.view.recording_conditions.lne_physician.setText("1")
        self.controller.view.recording_conditions.cmb_sensor_group.setCurrentIndex(1)
        self.controller.view.recording_conditions.cmb_recording_type.setCurrentIndex(1)
        self.controller.view.recording_conditions.cmb_alertness.setCurrentIndex(1)
        self.controller.view.recording_conditions.cmb_cooperation.setCurrentIndex(1)
        self.controller.view.recording_conditions.spb_age.setValue(1)
        self.controller.view.recording_conditions.lne_latest_meal.setText("1")
        self.controller.view.recording_conditions.cmb_skull_defect.setCurrentIndex(1)
        self.controller.view.recording_conditions.cmb_brain_surgery.setCurrentIndex(1)
        self.controller.view.recording_conditions.txe_tech_description.setText("1")

        # Update the model using the views data
        self.controller.update_model_from_view()

        # Test that the model has updated correctly
        self.assertEqual(self.controller.model.report.patient_details.name, "1")
        self.assertEqual(self.controller.model.report.patient_details.id, "1")
        self.assertEqual(self.controller.model.report.patient_details.dob, "1")
        self.assertEqual(self.controller.model.report.patient_details.handedness, self.controller.view.patient_details.txt_handedness[1])
        self.assertEqual(self.controller.model.report.patient_details.address, "1")
        self.assertEqual(self.controller.model.report.patient_details.medication, "1")
        self.assertEqual(self.controller.model.report.patient_details.history, "1")

        self.assertEqual(self.controller.model.report.patient_referral.referrer_name, "1")
        self.assertEqual(self.controller.model.report.patient_referral.referrer_details, "1")
        self.assertEqual(self.controller.model.report.patient_referral.diagnosis, "1")
        self.assertEqual(self.controller.model.report.patient_referral.seizure_frequency, self.controller.view.patient_referral.txt_seizure_freq[1])
        self.assertEqual(self.controller.model.report.patient_referral.last_seizure, self.controller.view.patient_referral.txt_last_seizure[1])
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
        self.assertEqual(self.controller.model.report.recording_conditions.sensor_group, self.controller.view.recording_conditions.txt_sensor_group[1])
        self.assertEqual(self.controller.model.report.recording_conditions.recording_type, self.controller.view.recording_conditions.txt_recording_type[1])
        self.assertEqual(self.controller.model.report.recording_conditions.alertness, self.controller.view.recording_conditions.txt_alertness[1])
        self.assertEqual(self.controller.model.report.recording_conditions.cooperation, self.controller.view.recording_conditions.txt_cooperation[1])
        self.assertEqual(self.controller.model.report.recording_conditions.age, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.latest_meal, "1")
        self.assertEqual(self.controller.model.report.recording_conditions.skull_defect, self.controller.view.recording_conditions.txt_skull_defect[1])
        self.assertEqual(self.controller.model.report.recording_conditions.brain_surgery, self.controller.view.recording_conditions.txt_brain_surgery[1])
        self.assertEqual(self.controller.model.report.recording_conditions.tech_description, "1")

    def test_update_view_from_model(self):

        # Check UI is default / blank
        self.assertEqual(self.controller.view.patient_details.lne_name.text(), '')
        self.assertEqual(self.controller.view.patient_details.lne_id.text(), '')
        self.assertEqual(self.controller.view.patient_details.lne_dob.text(), '')
        self.assertEqual(self.controller.view.patient_details.cmb_handedness.currentText(), '')
        self.assertEqual(self.controller.view.patient_details.txe_address.toPlainText(), '')
        self.assertEqual(self.controller.view.patient_details.txe_history.toPlainText(), '')

        self.assertEqual(self.controller.view.patient_referral.lne_referrer_name.text(), '')
        self.assertEqual(self.controller.view.patient_referral.txe_referrer_details.toPlainText(), '')
        self.assertEqual(self.controller.view.patient_referral.lne_diagnosis.text(), '')
        self.assertEqual(self.controller.view.patient_referral.cmb_seizure_freq.currentText(), '')
        self.assertEqual(self.controller.view.patient_referral.cmb_last_seizure.currentText(), '')
        for i in range(self.controller.view.patient_referral.chlist_epilepsy.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_epilepsy.item(i).checkState(), 0)
        for i in range(self.controller.view.patient_referral.chlist_other_diagnostic.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_other_diagnostic.item(i).checkState(), 0)
        for i in range(self.controller.view.patient_referral.chlist_peadiatric.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_peadiatric.item(i).checkState(), 0)
        for i in range(self.controller.view.patient_referral.chlist_other.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_other.item(i).checkState(), 0)

        self.assertEqual(self.controller.view.recording_conditions.lne_study_id.text(), '')
        self.assertEqual(self.controller.view.recording_conditions.lne_study_date.text(), '')
        self.assertEqual(self.controller.view.recording_conditions.spb_duration.text(), ' ')
        self.assertEqual(self.controller.view.recording_conditions.lne_technologist.text(), '')
        self.assertEqual(self.controller.view.recording_conditions.lne_physician.text(), '')
        self.assertEqual(self.controller.view.recording_conditions.cmb_sensor_group.currentText(), '')
        self.assertEqual(self.controller.view.recording_conditions.cmb_recording_type.currentText(), '')
        self.assertEqual(self.controller.view.recording_conditions.cmb_alertness.currentText(), '')
        self.assertEqual(self.controller.view.recording_conditions.cmb_cooperation.currentText(), '')
        self.assertEqual(self.controller.view.recording_conditions.spb_age.text(), ' ')
        self.assertEqual(self.controller.view.recording_conditions.lne_latest_meal.text(), '')
        self.assertEqual(self.controller.view.recording_conditions.cmb_skull_defect.currentText(), '')
        self.assertEqual(self.controller.view.recording_conditions.cmb_brain_surgery.currentText(), '')
        self.assertEqual(self.controller.view.recording_conditions.txe_tech_description.toPlainText(), '')
        self.assertEqual(self.controller.view.recording_conditions.lne_edf_location.text(), '')

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
        self.controller.model.report.patient_referral.seizure_frequency = self.controller.view.patient_referral.txt_seizure_freq[1]
        self.controller.model.report.patient_referral.last_seizure = self.controller.view.patient_referral.txt_last_seizure[1]
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
        self.controller.model.report.recording_conditions.sensor_group = self.controller.view.recording_conditions.txt_sensor_group[1]
        self.controller.model.report.recording_conditions.recording_type = self.controller.view.recording_conditions.txt_recording_type[1]
        self.controller.model.report.recording_conditions.alertness = self.controller.view.recording_conditions.txt_alertness[1]
        self.controller.model.report.recording_conditions.cooperation = self.controller.view.recording_conditions.txt_cooperation[1]
        self.controller.model.report.recording_conditions.age = "1"
        self.controller.model.report.recording_conditions.latest_meal = "1"
        self.controller.model.report.recording_conditions.skull_defect = self.controller.view.recording_conditions.txt_skull_defect[1]
        self.controller.model.report.recording_conditions.brain_surgery = self.controller.view.recording_conditions.txt_brain_surgery[1]
        self.controller.model.report.recording_conditions.tech_description = "1"
        self.controller.model.report.recording_conditions.edf_location = "1"

        # Update the view using the models data
        self.controller.update_view_from_model()

        # Test that the UI has updated correctly
        self.assertEqual(self.controller.view.patient_details.lne_name.text(), '1')
        self.assertEqual(self.controller.view.patient_details.lne_id.text(), '1')
        self.assertEqual(self.controller.view.patient_details.lne_dob.text(), '1')
        self.assertEqual(self.controller.view.patient_details.cmb_handedness.currentText(), 'Right')
        self.assertEqual(self.controller.view.patient_details.txe_address.toPlainText(), '1')
        self.assertEqual(self.controller.view.patient_details.txe_history.toPlainText(), '1')

        self.assertEqual(self.controller.view.patient_referral.lne_referrer_name.text(), '1')
        self.assertEqual(self.controller.view.patient_referral.txe_referrer_details.toPlainText(), "1")
        self.assertEqual(self.controller.view.patient_referral.lne_diagnosis.text(), "1")
        self.assertEqual(self.controller.view.patient_referral.cmb_seizure_freq.currentText(), self.controller.view.patient_referral.txt_seizure_freq[1])
        self.assertEqual(self.controller.view.patient_referral.cmb_last_seizure.currentText(), self.controller.view.patient_referral.txt_last_seizure[1])
        for i in range(self.controller.view.patient_referral.chlist_epilepsy.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_epilepsy.item(i).checkState(), 1)
        for i in range(self.controller.view.patient_referral.chlist_other_diagnostic.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_other_diagnostic.item(i).checkState(), 1)
        for i in range(self.controller.view.patient_referral.chlist_peadiatric.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_peadiatric.item(i).checkState(), 1)
        for i in range(self.controller.view.patient_referral.chlist_other.rowCount()):
            self.assertEqual(self.controller.view.patient_referral.chlist_other.item(i).checkState(), 1)

        self.assertEqual(self.controller.view.recording_conditions.lne_study_id.text(), "1")
        self.assertEqual(self.controller.view.recording_conditions.lne_study_date.text(), "1")
        self.assertEqual(self.controller.view.recording_conditions.spb_duration.text(), "1.00")
        self.assertEqual(self.controller.view.recording_conditions.lne_technologist.text(), "1")
        self.assertEqual(self.controller.view.recording_conditions.lne_physician.text(), "1")
        self.assertEqual(self.controller.view.recording_conditions.cmb_sensor_group.currentText(), self.controller.view.recording_conditions.txt_sensor_group[1])
        self.assertEqual(self.controller.view.recording_conditions.cmb_recording_type.currentText(), self.controller.view.recording_conditions.txt_recording_type[1])
        self.assertEqual(self.controller.view.recording_conditions.cmb_alertness.currentText(), self.controller.view.recording_conditions.txt_alertness[1])
        self.assertEqual(self.controller.view.recording_conditions.cmb_cooperation.currentText(), self.controller.view.recording_conditions.txt_cooperation[1])
        self.assertEqual(self.controller.view.recording_conditions.spb_age.text(), "1")
        self.assertEqual(self.controller.view.recording_conditions.lne_latest_meal.text(), "1")
        self.assertEqual(self.controller.view.recording_conditions.cmb_skull_defect.currentText(), self.controller.view.recording_conditions.txt_skull_defect[1])
        self.assertEqual(self.controller.view.recording_conditions.cmb_brain_surgery.currentText(), self.controller.view.recording_conditions.txt_brain_surgery[1])
        self.assertEqual(self.controller.view.recording_conditions.txe_tech_description.toPlainText(), "1")
        self.assertEqual(self.controller.view.recording_conditions.lne_edf_location.text(), "1")

    def set_check_list_ones(self, chlist):
        for i in range(chlist.rowCount()):
            chlist.item(i).setCheckState(1)