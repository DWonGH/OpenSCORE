

import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.models.background_activity import BackgroundActivity, Rhythm
from src.views.background_activity import BackgroundActivityWidget


class TestBackgroundActivityWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.widget = BackgroundActivityWidget()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertIsNotNone(self.widget.cmb_pdr_significance)
        self.assertIsNotNone(self.widget.lne_pdr_frequency)
        self.assertIsNotNone(self.widget.chbx_pdr_freq_asymmetry)
        self.assertIsNotNone(self.widget.lne_pdr_freq_asymmetry_left)
        self.assertIsNotNone(self.widget.lne_pdr_freq_asymmetry_right)
        self.assertIsNotNone(self.widget.cmb_pdr_amplitude)
        self.assertIsNotNone(self.widget.cmb_pdr_amp_asymmetry)
        self.assertIsNotNone(self.widget.cmb_pdr_eye_opening)
        self.assertIsNotNone(self.widget.cmb_pdr_organisation)
        self.assertIsNotNone(self.widget.cmb_pdr_caveat)
        self.assertIsNotNone(self.widget.cmb_pdr_absence)
        self.assertIsNotNone(self.widget.cmb_critical_features)
        self.assertIsNotNone(self.widget.btn_add_rhythm)
        self.assertIsNotNone(self.widget.btn_edit_rhythm)
        self.assertIsNotNone(self.widget.btn_delete_rhythm)
        self.assertIsNotNone(self.widget.rhythm_table)
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
        results_dict = self.widget.to_dict()
        self.assertEqual(results_dict, target_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.results_dict = self.widget.to_dict()
        target_dict = {
            "Posterior dominant rhythm": {
                "Significance": self.widget.txt_pdr_significance[1],
                "Frequency": "1",
                "Frequency asymmetry": True,
                "Hz lower left": "1",
                "Hz lower right": "1",
                "Amplitude": self.widget.txt_pdr_amplitude[1],
                "Amplitude asymmetry": self.widget.txt_pdr_amp_asymmetry[1],
                "Reactivity to eye opening": self.widget.txt_pdr_eye_opening[1],
                "Organisation": self.widget.txt_pdr_organisation[1],
                "Caveat": self.widget.txt_pdr_caveat[1],
                "Absence of PDR": self.widget.txt_pdr_absence[1]
            },
            "Critically ill background activity": self.widget.txt_critical_features[1],
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
        self.assertEqual(self.results_dict, target_dict)

    def set_to_ones(self):
        self.widget.cmb_pdr_significance.setCurrentIndex(1)
        self.widget.lne_pdr_frequency.setText("1")
        self.widget.chbx_pdr_freq_asymmetry.setChecked(True)
        self.widget.lne_pdr_freq_asymmetry_left.setText("1")
        self.widget.lne_pdr_freq_asymmetry_right.setText("1")
        self.widget.cmb_pdr_amplitude.setCurrentIndex(1)
        self.widget.cmb_pdr_amp_asymmetry.setCurrentIndex(1)
        self.widget.cmb_pdr_eye_opening.setCurrentIndex(1)
        self.widget.cmb_pdr_organisation.setCurrentIndex(1)
        self.widget.cmb_pdr_caveat.setCurrentIndex(1)
        self.widget.cmb_pdr_absence.setCurrentIndex(1)
        self.widget.cmb_critical_features.setCurrentIndex(1)
        test_rhythm = {
            "Significance": "1",
            "Spectral frequency": "1",
            "Frequency": "1",
            "Amplitude": "1",
            "Modulator effect": "1"
        }
        self.widget.rhythm_table.new_rhythm(test_rhythm)

