import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.episodes_controller import EpisodesController
from src.views.episodes import EpisodeDialog
from score_schema import EpisodeType, Ternary


class TestEpisodesController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.controller = EpisodesController()

    def test_add_episode_refreshes_table(self):
        d = EpisodeDialog()
        d.lne_name.setText("Focal to bilateral tonic-clonic")
        d.cmb_type.setCurrentText(EpisodeType.EPILEPTIC_SEIZURE.value)
        d.lst_semiology.item(0).setSelected(True)
        e = d.to_model()
        self.assertEqual(e.name, "Focal to bilateral tonic-clonic")
        self.assertEqual(e.episode_type, EpisodeType.EPILEPTIC_SEIZURE)
        self.assertEqual(len(e.phases), 1)
        self.assertEqual(len(e.phases[0].semiology), 1)

        self.controller.model.episodes.append(e)
        self.controller.refresh_table()
        self.assertEqual(self.controller.view.table.rowCount(), 1)

    def test_dialog_round_trip(self):
        d = EpisodeDialog()
        d.lne_name.setText("Absence")
        d.cmb_awareness.setCurrentIndex(1)  # Present
        e = d.to_model()
        self.assertEqual(e.awareness, Ternary.PRESENT)
        other = EpisodeDialog()
        other.from_model(e)
        self.assertEqual(other.lne_name.text(), "Absence")
        self.assertEqual(other.cmb_awareness.currentIndex(), 1)
