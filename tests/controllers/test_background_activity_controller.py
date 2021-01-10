"""
Controller test template
"""

import sys
import unittest

from PyQt5.Qt import QApplication

from src.controllers.background_activity_controller import BackgroundActivityController
from src.models.background_activity import Rhythm


class TestBackgroundActivityController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = BackgroundActivityController()
        self.model = self.controller.model
        self.view = self.controller.view
        self.ones_dict = {
            "Posterior dominant rhythm": {
                "Significance": self.view.txt_pdr_significance[1],
                "Frequency": "1",
                "Frequency asymmetry": True,
                "Hz lower left": "1",
                "Hz lower right": "1",
                "Amplitude": self.view.txt_pdr_amplitude[1],
                "Amplitude asymmetry": self.view.txt_pdr_amp_asymmetry[1],
                "Reactivity to eye opening": self.view.txt_pdr_eye_opening[1],
                "Organisation": self.view.txt_pdr_organisation[1],
                "Caveat": self.view.txt_pdr_caveat[1],
                "Absence of PDR": self.view.txt_pdr_absence[1]
            },
            "Critically ill background activity": self.view.txt_critical_features[1],
            "Other organised rhythms": [
                {
                    "Significance": "1",
                    "Spectral frequency": "1",
                    "Frequency": "1",
                    "Amplitude": "1",
                    "Modulator effect": "1"
                }
            ]
        }

    def test_init(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.view)

    def test_update_model(self):
        self.assert_model_default()
        self.assert_view_default()
        self.set_view_to_ones()
        self.assertEqual(self.ones_dict, self.view.to_dict())
        self.controller.update_model()
        self.assertEqual(self.ones_dict, self.view.to_dict())
        self.assertEqual(self.ones_dict, self.model.to_dict())

    def test_update_view(self):
        self.assert_view_default()
        self.assert_model_default()
        self.set_model_to_ones()
        self.assertEqual(self.ones_dict, self.model.to_dict())
        self.controller.update_view()
        self.assertEqual(self.ones_dict, self.model.to_dict())
        self.assertEqual(self.ones_dict, self.view.to_dict())

    def assert_model_default(self):
        self.assertIsNone(self.model.pdr.significance)
        self.assertIsNone(self.model.pdr.frequency)
        self.assertIsNone(self.model.pdr.frequency_asymmetry)
        self.assertIsNone(self.model.pdr.frequency_lower_left)
        self.assertIsNone(self.model.pdr.frequency_lower_right)
        self.assertIsNone(self.model.pdr.amplitude)
        self.assertIsNone(self.model.pdr.amplitude_asymmetry)
        self.assertIsNone(self.model.pdr.eye_opening)
        self.assertIsNone(self.model.pdr.organisation)
        self.assertIsNone(self.model.pdr.caveat)
        self.assertIsNone(self.model.pdr.absence)
        self.assertEqual(len(self.model.other_rhythms), 0)
        self.assertIsNone(self.model.critical_features)

    def set_model_to_ones(self):
        self.model.pdr.significance = self.view.txt_pdr_significance[1]
        self.model.pdr.frequency = "1"
        self.model.pdr.frequency_asymmetry = True
        self.model.pdr.frequency_lower_left = "1"
        self.model.pdr.frequency_lower_right = "1"
        self.model.pdr.amplitude = self.view.txt_pdr_amplitude[1]
        self.model.pdr.amplitude_asymmetry = self.view.txt_pdr_amp_asymmetry[1]
        self.model.pdr.eye_opening = self.view.txt_pdr_eye_opening[1]
        self.model.pdr.organisation = self.view.txt_pdr_organisation[1]
        self.model.pdr.caveat = self.view.txt_pdr_caveat[1]
        self.model.pdr.absence = self.view.txt_pdr_absence[1]
        test_rhythm = Rhythm()
        test_rhythm.significance = "1"
        test_rhythm.spectral = "1"
        test_rhythm.frequency = "1"
        test_rhythm.amplitude = "1"
        test_rhythm.modulator_effect = "1"
        self.model.other_rhythms.append(test_rhythm)
        self.model.critical_features = self.view.txt_critical_features[1]

    def assert_view_default(self):
        target_dict = {
            "Posterior dominant rhythm": {
                "Significance": '',
                "Frequency": '',
                "Frequency asymmetry": True,
                "Hz lower left": '',
                "Hz lower right": '',
                "Amplitude": '',
                "Amplitude asymmetry": '',
                "Reactivity to eye opening": '',
                "Organisation": '',
                "Caveat": '',
                "Absence of PDR": ''
            },
            "Critically ill background activity": '',
            "Other organised rhythms": []
        }
        results_dict = self.view.to_dict()
        self.assertEqual(results_dict, target_dict)

    def set_view_to_ones(self):
        self.view.cmb_pdr_significance.setCurrentIndex(1)
        self.view.lne_pdr_frequency.setText("1")
        self.view.chbx_pdr_freq_asymmetry.setChecked(True)
        self.view.lne_pdr_freq_asymmetry_left.setText("1")
        self.view.lne_pdr_freq_asymmetry_right.setText("1")
        self.view.cmb_pdr_amplitude.setCurrentIndex(1)
        self.view.cmb_pdr_amp_asymmetry.setCurrentIndex(1)
        self.view.cmb_pdr_eye_opening.setCurrentIndex(1)
        self.view.cmb_pdr_organisation.setCurrentIndex(1)
        self.view.cmb_pdr_caveat.setCurrentIndex(1)
        self.view.cmb_pdr_absence.setCurrentIndex(1)
        self.view.cmb_critical_features.setCurrentIndex(1)
        test_rhythm = {
            "Significance": "1",
            "Spectral frequency": "1",
            "Frequency": "1",
            "Amplitude": "1",
            "Modulator effect": "1"
        }
        self.view.rhythm_table.new_rhythm(test_rhythm)
