import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.views.main_window import MainWindow


class TestMainWindow(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.details_dict = None

    def test_init(self):
        self.assertIsNotNone(self.main_window.menu)
        self.assertIsNotNone(self.main_window.toolbar)
        self.assertIsNotNone(self.main_window.tabs)
        self.assertIsNotNone(self.main_window.patient_details)
        self.assertIsNotNone(self.main_window.patient_referral)
        self.assertIsNotNone(self.main_window.recording_conditions)
        self.assertIsNotNone(self.main_window.centralWidget())
