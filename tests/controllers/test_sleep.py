import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.sleep_controller import SleepController
from score_schema import Ternary


class TestSleepController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.controller = SleepController()
        self.view = self.controller.view
        self.model = self.controller.model

    def test_round_trip(self):
        self.view.lst_stages.item(0).setSelected(True)   # Sleep-stage-N1
        self.view.lst_graphoelements.item(0).setSelected(True)
        self.view.cmb_soremp.setCurrentIndex(2)          # Absent
        self.view.lne_notes.setText("settled quickly")
        self.controller.update_model()
        self.assertIn("Sleep-stage-N1", self.model.achieved_stages)
        self.assertEqual(self.model.soremp, Ternary.ABSENT)
        self.assertEqual(self.model.notes, "settled quickly")

        other = SleepController()
        other.model = self.model
        other.update_view()
        self.assertTrue(other.view.lst_stages.item(0).isSelected())
        self.assertEqual(other.view.cmb_soremp.currentIndex(), 2)
        self.assertEqual(other.view.lne_notes.text(), "settled quickly")
