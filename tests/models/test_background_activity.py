import unittest

from src.models.background_activity import BackgroundActivity, Rhythm


class TestBackgroundActivity(unittest.TestCase):

    def setUp(self) -> None:
        self.background_activity = BackgroundActivity()
        self.pdr = self.background_activity.pdr

    def test_init(self):
        self.assert_default()

    def test_set_to_ones(self):
        self.set_to_ones()
        self.details_dict = self.background_activity.to_dict()
        target_dict = {
            "Posterior dominant rhythm": {
                "Significance": "1",
                "Frequency": "1",
                "Frequency asymmetry": "1",
                "Hz lower left": "1",
                "Hz lower right": "1",
                "Amplitude": "1",
                "Amplitude asymmetry": "1",
                "Reactivity to eye opening": "1",
                "Organisation": "1",
                "Caveat": "1",
                "Absence of PDR": "1"
            },
            "Other organised rhythms": [
                {
                    "Significance": "1",
                    "Spectral frequency": "1",
                    "Frequency": "1",
                    "Amplitude": "1",
                    "Modulator effect": "1"
                }
            ],
            "Critically ill background activity": "1"
        }
        self.assertEqual(self.details_dict, target_dict)

    def set_to_ones(self):
        self.pdr.significance = "1"
        self.pdr.frequency = "1"
        self.pdr.frequency_asymmetry = "1"
        self.pdr.frequency_lower_left = "1"
        self.pdr.frequency_lower_right = "1"
        self.pdr.amplitude = "1"
        self.pdr.amplitude_asymmetry = "1"
        self.pdr.eye_opening = "1"
        self.pdr.organisation = "1"
        self.pdr.caveat = "1"
        self.pdr.absence = "1"
        test_rhythm = Rhythm()
        test_rhythm.significance = "1"
        test_rhythm.spectral = "1"
        test_rhythm.frequency = "1"
        test_rhythm.amplitude = "1"
        test_rhythm.modulator_effect = "1"
        self.background_activity.other_rhythms.append(test_rhythm)
        self.background_activity.critical_features = "1"

    def test_other_rhythms_to_dict(self):
        self.assert_default()
        data = {
            "Posterior dominant rhythm": {
                "Significance": "1",
                "Frequency": "1",
                "Frequency asymmetry": "1",
                "Hz lower left": "1",
                "Hz lower right": "1",
                "Amplitude": "1",
                "Amplitude asymmetry": "1",
                "Reactivity to eye opening": "1",
                "Organisation": "1",
                "Caveat": "1",
                "Absence of PDR": "1"
            },
            "Other organised rhythms": [
                {
                    "Significance": "1",
                    "Spectral frequency": "1",
                    "Frequency": "1",
                    "Amplitude": "1",
                    "Modulator effect": "1"
                }
            ],
            "Critically ill background activity": "1"
        }
        self.background_activity.update_from_dict(data)
        self.assertEqual(data, self.background_activity.to_dict())
        self.assertEqual(len(self.background_activity.other_rhythms), 1)
        other_rhythms = self.background_activity.other_rhythms_to_dict()
        self.assertEqual(data["Other organised rhythms"], other_rhythms)
        self.assertEqual(len(self.background_activity.other_rhythms), 1)

    def assert_default(self):
        self.assertIsNone(self.background_activity.pdr.significance)
        self.assertIsNone(self.background_activity.pdr.frequency)
        self.assertIsNone(self.background_activity.pdr.frequency_asymmetry)
        self.assertIsNone(self.background_activity.pdr.frequency_lower_left)
        self.assertIsNone(self.background_activity.pdr.frequency_lower_right)
        self.assertIsNone(self.background_activity.pdr.amplitude)
        self.assertIsNone(self.background_activity.pdr.amplitude_asymmetry)
        self.assertIsNone(self.background_activity.pdr.eye_opening)
        self.assertIsNone(self.background_activity.pdr.organisation)
        self.assertIsNone(self.background_activity.pdr.caveat)
        self.assertIsNone(self.background_activity.pdr.absence)
        self.assertEqual(len(self.background_activity.other_rhythms), 0)
        self.assertIsNone(self.background_activity.critical_features)
