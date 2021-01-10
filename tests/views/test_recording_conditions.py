import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.views.recording_conditions import RecordingConditionsWidget


class TestRecordingConditionsView(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.recording_conditions = RecordingConditionsWidget()

    def test_init(self):
        self.assertIsNotNone(self.recording_conditions.lne_study_id)
        self.assertIsNotNone(self.recording_conditions.lne_study_date)
        self.assertIsNotNone(self.recording_conditions.lne_duration)
        self.assertIsNotNone(self.recording_conditions.lne_technologist)
        self.assertIsNotNone(self.recording_conditions.lne_physician)
        self.assertIsNotNone(self.recording_conditions.cmb_sensor_group)
        self.assertIsNotNone(self.recording_conditions.cmb_recording_type)
        self.assertIsNotNone(self.recording_conditions.cmb_alertness)
        self.assertIsNotNone(self.recording_conditions.cmb_cooperation)
        self.assertIsNotNone(self.recording_conditions.lne_latest_meal)
        self.assertIsNotNone(self.recording_conditions.cmb_skull_defect)
        self.assertIsNotNone(self.recording_conditions.cmb_brain_surgery)
        self.assertIsNotNone(self.recording_conditions.txe_tech_description)
        self.assertIsNotNone(self.recording_conditions.lne_edf_location)
        self.assertIsNotNone(self.recording_conditions.btn_edf_location)
        target_dict = {
            "Study ID": '',
            "Date & Time": '',
            "Recording duration": '',
            "Technologist name": '',
            "Physician name": '',
            "Sensor group": '',
            "Recording type": '',
            "Alertness": '',
            "Cooperation": '',
            "Patient age": '',
            "Latest meal": '',
            "Skull defect": '',
            "Brain surgery": '',
            "Additional technical description": '',
            "EDF location": ''
        }
        results_dict = self.recording_conditions.to_dict()
        self.assertEqual(results_dict, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        target_dict = {
            "Study ID": '1',
            "Date & Time": '1',
            "Recording duration": '1',
            "Technologist name": '1',
            "Physician name": '1',
            "Sensor group": self.recording_conditions.txt_sensor_group[1],
            "Recording type": self.recording_conditions.txt_recording_type[1],
            "Alertness": self.recording_conditions.txt_alertness[1],
            "Cooperation": self.recording_conditions.txt_cooperation[1],
            "Patient age": '1',
            "Latest meal": '1',
            "Skull defect": self.recording_conditions.txt_skull_defect[1],
            "Brain surgery": self.recording_conditions.txt_brain_surgery[1],
            "Additional technical description": '1',
            "EDF location": "1"
        }
        results_dict = self.recording_conditions.to_dict()
        self.assertEqual(results_dict, target_dict)

    def set_to_ones(self):
        self.recording_conditions.lne_study_id.setText("1")
        self.recording_conditions.lne_study_date.setText("1")
        self.recording_conditions.lne_duration.setText("1")
        self.recording_conditions.lne_technologist.setText("1")
        self.recording_conditions.lne_physician.setText("1")
        self.recording_conditions.cmb_sensor_group.setCurrentIndex(1)
        self.recording_conditions.cmb_recording_type.setCurrentIndex(1)
        self.recording_conditions.cmb_alertness.setCurrentIndex(1)
        self.recording_conditions.cmb_cooperation.setCurrentIndex(1)
        self.recording_conditions.lne_age.setText("1")
        self.recording_conditions.lne_latest_meal.setText("1")
        self.recording_conditions.cmb_skull_defect.setCurrentIndex(1)
        self.recording_conditions.cmb_brain_surgery.setCurrentIndex(1)
        self.recording_conditions.txe_tech_description.setText("1")
        self.recording_conditions.lne_edf_location.setText("1")
