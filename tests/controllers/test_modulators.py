import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.modulators_controller import ModulatorsController
from score_schema import HyperventilationQuality, Ternary


class TestModulatorsController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.controller = ModulatorsController()
        self.view = self.controller.view
        self.model = self.controller.model

    def test_defaults_are_not_assessed(self):
        self.controller.update_model()
        self.assertEqual(self.model.hyperventilation, Ternary.NOT_ASSESSED)
        self.assertEqual(self.model.photic_stimulation, Ternary.NOT_ASSESSED)

    def test_round_trip(self):
        self.view.cmb_hv.setCurrentIndex(1)  # Present
        self.view.cmb_hv_quality.setCurrentText(HyperventilationQuality.GOOD.value)
        self.view.lne_med_admin.setText("lorazepam")
        self.controller.update_model()
        self.assertEqual(self.model.hyperventilation, Ternary.PRESENT)
        self.assertEqual(self.model.hyperventilation_quality, HyperventilationQuality.GOOD)
        self.assertEqual(self.model.medication_administered, "lorazepam")

        other = ModulatorsController()
        other.model = self.model
        other.update_view()
        self.assertEqual(other.view.cmb_hv.currentIndex(), 1)
        self.assertEqual(other.view.cmb_hv_quality.currentText(), HyperventilationQuality.GOOD.value)
        self.assertEqual(other.view.lne_med_admin.text(), "lorazepam")
