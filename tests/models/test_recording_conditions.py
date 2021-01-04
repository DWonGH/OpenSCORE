import unittest
from src.models.recording_conditions import RecordingConditions


class TestRecordingConditions(unittest.TestCase):

    def setUp(self) -> None:
        self.recording_conditions = RecordingConditions()
        self.data = None

    def test_init(self):
        self.is_nones()

    def test_nones_to_dict(self):
        self.recording_conditions.set_to_nones()
        self.is_nones()
        self.data = self.recording_conditions.to_dict()
        target_dict = {
            "Study ID": None,
            "Date & Time": None,
            "Recording duration": None,
            "Technologist name": None,
            "Physician name": None,
            "Sensor group": None,
            "Recording type": None,
            "Alertness": None,
            "Cooperation": None,
            "Patient age": None,
            "Latest meal": None,
            "Skull defect": None,
            "Brain surgery": None,
            "Additional technical description": None,
            "EDF location": None
        }
        self.assertEqual(self.data, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.data = self.recording_conditions.to_dict()
        target_dict = {
            "Study ID": "1",
            "Date & Time": "1",
            "Recording duration": "1",
            "Technologist name": "1",
            "Physician name": "1",
            "Sensor group": "1",
            "Recording type": "1",
            "Alertness": "1",
            "Cooperation": "1",
            "Patient age": "1",
            "Latest meal": "1",
            "Skull defect": "1",
            "Brain surgery": "1",
            "Additional technical description": "1",
            "EDF location": "1"
        }
        self.assertEqual(self.data, target_dict)

    def set_to_ones(self):
        self.recording_conditions.study_id = "1"
        self.recording_conditions.study_date = "1"
        self.recording_conditions.recording_duration = "1"
        self.recording_conditions.technologist_name = "1"
        self.recording_conditions.physician_name = "1"
        self.recording_conditions.sensor_group = "1"
        self.recording_conditions.recording_type = "1"
        self.recording_conditions.alertness = "1"
        self.recording_conditions.cooperation = "1"
        self.recording_conditions.age = "1"
        self.recording_conditions.latest_meal = "1"
        self.recording_conditions.skull_defect = "1"
        self.recording_conditions.brain_surgery = "1"
        self.recording_conditions.tech_description = "1"
        self.recording_conditions.edf_location = "1"

    def is_nones(self):
        self.assertIsNone(self.recording_conditions.study_id)
        self.assertIsNone(self.recording_conditions.study_date)
        self.assertIsNone(self.recording_conditions.recording_duration)
        self.assertIsNone(self.recording_conditions.technologist_name)
        self.assertIsNone(self.recording_conditions.physician_name)
        self.assertIsNone(self.recording_conditions.sensor_group)
        self.assertIsNone(self.recording_conditions.recording_type)
        self.assertIsNone(self.recording_conditions.alertness)
        self.assertIsNone(self.recording_conditions.cooperation)
        self.assertIsNone(self.recording_conditions.age)
        self.assertIsNone(self.recording_conditions.latest_meal)
        self.assertIsNone(self.recording_conditions.skull_defect)
        self.assertIsNone(self.recording_conditions.brain_surgery)
        self.assertIsNone(self.recording_conditions.tech_description)
        self.assertIsNone(self.recording_conditions.edf_location)