"""
Controller test template
"""

import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.controller import Controller


class TestController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = Controller()
        self.model = self.controller.model
        self.view = self.controller.view

    def test_init(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.view)

    def test_update_model(self):
        pass

    def test_update_view(self):
        pass

