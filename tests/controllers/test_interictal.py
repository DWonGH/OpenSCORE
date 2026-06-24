import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.interictal_controller import InterictalController
from src.views.interictal import InterictalDialog
from score_schema import Laterality, Morphology, Region


def _select(list_widget, text):
    for i in range(list_widget.count()):
        if list_widget.item(i).text() == text:
            list_widget.item(i).setSelected(True)


class TestInterictalController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.controller = InterictalController()

    def test_add_graphoelement_refreshes_table(self):
        d = InterictalDialog()
        d.cmb_morphology.setCurrentText(Morphology.SHARP_WAVE.value)
        d.cmb_laterality.setCurrentText(Laterality.RIGHT.value)
        _select(d.lst_regions, Region.TEMPORAL.value)
        g = d.to_model()
        self.assertEqual(g.morphology, Morphology.SHARP_WAVE)
        self.assertEqual(g.location.laterality, Laterality.RIGHT)
        self.assertEqual([r.value for r in g.location.regions], [Region.TEMPORAL.value])

        self.controller.model.graphoelements.append(g)
        self.controller.refresh_table()
        self.assertEqual(self.controller.view.table.rowCount(), 1)

    def test_special_patterns_sync(self):
        self.controller.view.lst_special.item(0).setSelected(True)
        self.controller.update_model()
        self.assertEqual(len(self.controller.model.special_patterns), 1)
        self.controller.view.lst_special.clearSelection()
        self.controller.update_view()
        self.assertTrue(self.controller.view.lst_special.item(0).isSelected())

    def test_dialog_round_trip(self):
        d = InterictalDialog()
        d.cmb_morphology.setCurrentText(Morphology.SPIKE.value)
        g = d.to_model()
        other = InterictalDialog()
        other.from_model(g)
        self.assertEqual(other.cmb_morphology.currentText(), Morphology.SPIKE.value)
