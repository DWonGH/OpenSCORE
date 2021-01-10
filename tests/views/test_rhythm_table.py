import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.views.rhythm_table_widget import RhythmTableWidget


class TestRhythmTableWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.widget = RhythmTableWidget()

    def test_init(self):
        self.assert_default()

    def test_add_rhythm(self):
        self.assert_default()
        data = {
            "Significance": "1",
            "Spectral frequency": "2",
            "Frequency": "3",
            "Amplitude": "4",
            "Modulator effect": "5"
        }
        self.widget.new_rhythm(data)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.rowCount(), 1)
        self.assertEqual(self.widget.item(0, 0).text(), "1")
        self.assertEqual(self.widget.item(0, 1).text(), "2")
        self.assertEqual(self.widget.item(0, 2).text(), "3")
        self.assertEqual(self.widget.item(0, 3).text(), "4")
        self.assertEqual(self.widget.item(0, 4).text(), "5")
        data = {
            "Significance": "5",
            "Spectral frequency": "4",
            "Frequency": "3",
            "Amplitude": "2",
            "Modulator effect": "1"
        }
        self.widget.new_rhythm(data)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.rowCount(), 2)
        self.assertEqual(self.widget.item(1, 0).text(), "5")
        self.assertEqual(self.widget.item(1, 1).text(), "4")
        self.assertEqual(self.widget.item(1, 2).text(), "3")
        self.assertEqual(self.widget.item(1, 3).text(), "2")
        self.assertEqual(self.widget.item(1, 4).text(), "1")

    def test_edit_rhythm(self):
        self.assert_default()
        data = {
            "Significance": "1",
            "Spectral frequency": "2",
            "Frequency": "3",
            "Amplitude": "4",
            "Modulator effect": "5"
        }
        self.widget.new_rhythm(data)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.rowCount(), 1)
        self.assertEqual(self.widget.item(0, 0).text(), "1")
        self.assertEqual(self.widget.item(0, 1).text(), "2")
        self.assertEqual(self.widget.item(0, 2).text(), "3")
        self.assertEqual(self.widget.item(0, 3).text(), "4")
        self.assertEqual(self.widget.item(0, 4).text(), "5")
        data = {
            "Significance": "5",
            "Spectral frequency": "4",
            "Frequency": "3",
            "Amplitude": "2",
            "Modulator effect": "1"
        }
        self.widget.edit_rhythm(data)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.rowCount(), 1)
        self.assertEqual(self.widget.item(0, 0).text(), "5")
        self.assertEqual(self.widget.item(0, 1).text(), "4")
        self.assertEqual(self.widget.item(0, 2).text(), "3")
        self.assertEqual(self.widget.item(0, 3).text(), "2")
        self.assertEqual(self.widget.item(0, 4).text(), "1")

    def test_current_rhythm(self):
        self.assert_default()
        data = {
            "Significance": "1",
            "Spectral frequency": "2",
            "Frequency": "3",
            "Amplitude": "4",
            "Modulator effect": "5"
        }
        self.widget.new_rhythm(data)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.rowCount(), 1)
        self.assertEqual(self.widget.item(0, 0).text(), "1")
        self.assertEqual(self.widget.item(0, 1).text(), "2")
        self.assertEqual(self.widget.item(0, 2).text(), "3")
        self.assertEqual(self.widget.item(0, 3).text(), "4")
        self.assertEqual(self.widget.item(0, 4).text(), "5")
        self.assertEqual(data, self.widget.current_rhythm())

    def test_table_to_dict(self):
        self.assert_default()
        data = {
            "Significance": "1",
            "Spectral frequency": "2",
            "Frequency": "3",
            "Amplitude": "4",
            "Modulator effect": "5"
        }
        self.widget.new_rhythm(data)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.rowCount(), 1)
        self.assertEqual(self.widget.item(0, 0).text(), "1")
        self.assertEqual(self.widget.item(0, 1).text(), "2")
        self.assertEqual(self.widget.item(0, 2).text(), "3")
        self.assertEqual(self.widget.item(0, 3).text(), "4")
        self.assertEqual(self.widget.item(0, 4).text(), "5")
        self.assertEqual(data, self.widget.table_to_dict()[0])

    def test_update_from_dict(self):
        self.assert_default()
        data = [{
            "Significance": "1",
            "Spectral frequency": "2",
            "Frequency": "3",
            "Amplitude": "4",
            "Modulator effect": "5"
        }]
        self.widget.update_from_dict(data)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.rowCount(), 1)
        self.assertEqual(self.widget.item(0, 0).text(), "1")
        self.assertEqual(self.widget.item(0, 1).text(), "2")
        self.assertEqual(self.widget.item(0, 2).text(), "3")
        self.assertEqual(self.widget.item(0, 3).text(), "4")
        self.assertEqual(self.widget.item(0, 4).text(), "5")
        self.assertEqual(data, self.widget.table_to_dict())


    def assert_default(self):
        self.assertEqual(self.widget.rowCount(), 0)
        self.assertEqual(self.widget.columnCount(), 5)
        self.assertEqual(self.widget.horizontalHeaderItem(0).text(), "Significance")
        self.assertEqual(self.widget.horizontalHeaderItem(1).text(), "Spectral Freq")
        self.assertEqual(self.widget.horizontalHeaderItem(2).text(), "Frequency (Hz)")
        self.assertEqual(self.widget.horizontalHeaderItem(3).text(), "Amplitude (μV)")
        self.assertEqual(self.widget.horizontalHeaderItem(4).text(), "Mod Effect")