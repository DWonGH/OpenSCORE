import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.recording_conditions_controller import RecordingConditionsController


class TestRecordingConditionsController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = RecordingConditionsController()
        self.model = self.controller.model
        self.view = self.controller.view

    def test_init(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.view)

    def test_update_model(self):
        self.assertIsNone(self.model.study_id)
        self.assertIsNone(self.model.study_date)
        self.assertIsNone(self.model.recording_duration)
        self.assertIsNone(self.model.technologist_name)
        self.assertIsNone(self.model.physician_name)
        self.assertIsNone(self.model.sensor_group)
        self.assertIsNone(self.model.recording_type)
        self.assertIsNone(self.model.alertness)
        self.assertIsNone(self.model.cooperation)
        self.assertIsNone(self.model.age)
        self.assertIsNone(self.model.latest_meal)
        self.assertIsNone(self.model.skull_defect)
        self.assertIsNone(self.model.brain_surgery)
        self.assertIsNone(self.model.tech_description)

        self.view.lne_study_id.setText("1")
        self.view.lne_study_date.setText("1")
        self.view.spb_duration.setValue(1)
        self.view.lne_technologist.setText("1")
        self.view.lne_physician.setText("1")
        self.view.cmb_sensor_group.setCurrentIndex(1)
        self.view.cmb_recording_type.setCurrentIndex(1)
        self.view.cmb_alertness.setCurrentIndex(1)
        self.view.cmb_cooperation.setCurrentIndex(1)
        self.view.spb_age.setValue(1)
        self.view.lne_latest_meal.setText("1")
        self.view.cmb_skull_defect.setCurrentIndex(1)
        self.view.cmb_brain_surgery.setCurrentIndex(1)
        self.view.txe_tech_description.setText("1")

        self.controller.update_model()

        self.assertEqual(self.model.study_id, "1")
        self.assertEqual(self.model.study_date, "1")
        self.assertEqual(self.model.recording_duration, "1.00")
        self.assertEqual(self.model.technologist_name, "1")
        self.assertEqual(self.model.physician_name, "1")
        self.assertEqual(self.model.sensor_group, self.view.txt_sensor_group[1])
        self.assertEqual(self.model.recording_type, self.view.txt_recording_type[1])
        self.assertEqual(self.model.alertness, self.view.txt_alertness[1])
        self.assertEqual(self.model.cooperation, self.view.txt_cooperation[1])
        self.assertEqual(self.model.age, "1")
        self.assertEqual(self.model.latest_meal, "1")
        self.assertEqual(self.model.skull_defect, self.view.txt_skull_defect[1])
        self.assertEqual(self.model.brain_surgery, self.view.txt_brain_surgery[1])
        self.assertEqual(self.model.tech_description, "1")

    def test_update_view(self):
        self.assertEqual(self.view.lne_study_id.text(), '')
        self.assertEqual(self.view.lne_study_date.text(), '')
        self.assertEqual(self.view.spb_duration.text(), ' ')
        self.assertEqual(self.view.lne_technologist.text(), '')
        self.assertEqual(self.view.lne_physician.text(), '')
        self.assertEqual(self.view.cmb_sensor_group.currentText(), '')
        self.assertEqual(self.view.cmb_recording_type.currentText(), '')
        self.assertEqual(self.view.cmb_alertness.currentText(), '')
        self.assertEqual(self.view.cmb_cooperation.currentText(), '')
        self.assertEqual(self.view.spb_age.text(), ' ')
        self.assertEqual(self.view.lne_latest_meal.text(), '')
        self.assertEqual(self.view.cmb_skull_defect.currentText(), '')
        self.assertEqual(self.view.cmb_brain_surgery.currentText(), '')
        self.assertEqual(self.view.txe_tech_description.toPlainText(), '')
        self.assertEqual(self.view.lne_edf_location.text(), '')

        self.model.study_id = "1"
        self.model.study_date = "1"
        self.model.recording_duration = "1.00"
        self.model.technologist_name = "1"
        self.model.physician_name = "1"
        self.model.sensor_group = self.view.txt_sensor_group[1]
        self.model.recording_type = self.view.txt_recording_type[1]
        self.model.alertness = self.view.txt_alertness[1]
        self.model.cooperation = self.view.txt_cooperation[1]
        self.model.age = "1"
        self.model.latest_meal = "1"
        self.model.skull_defect = self.view.txt_skull_defect[1]
        self.model.brain_surgery = self.view.txt_brain_surgery[1]
        self.model.tech_description = "1"
        self.model.edf_location = "1"
        
        self.controller.update_view()

        self.assertEqual(self.view.lne_study_id.text(), "1")
        self.assertEqual(self.view.lne_study_date.text(), "1")
        self.assertEqual(self.view.spb_duration.text(), "1.00")
        self.assertEqual(self.view.lne_technologist.text(), "1")
        self.assertEqual(self.view.lne_physician.text(), "1")
        self.assertEqual(self.view.cmb_sensor_group.currentText(), self.view.txt_sensor_group[1])
        self.assertEqual(self.view.cmb_recording_type.currentText(), self.view.txt_recording_type[1])
        self.assertEqual(self.view.cmb_alertness.currentText(), self.view.txt_alertness[1])
        self.assertEqual(self.view.cmb_cooperation.currentText(), self.view.txt_cooperation[1])
        self.assertEqual(self.view.spb_age.text(), "1")
        self.assertEqual(self.view.lne_latest_meal.text(), "1")
        self.assertEqual(self.view.cmb_skull_defect.currentText(), self.view.txt_skull_defect[1])
        self.assertEqual(self.view.cmb_brain_surgery.currentText(),  self.view.txt_brain_surgery[1])
        self.assertEqual(self.view.txe_tech_description.toPlainText(), "1")
        self.assertEqual(self.view.lne_edf_location.text(), "1")



