import traceback

from PyQt5.QtWidgets import QMessageBox

from score_schema import Episodes
from src.views.episodes import EpisodeDialog, EpisodesWidget


class EpisodesController:
    """SCORE §10 — Episodes. The score_schema model is the source of truth; the table
    is a read-only summary refreshed from it."""

    def __init__(self):
        self.model = Episodes()
        self.view = EpisodesWidget()
        self.view.btn_add.clicked.connect(self.hdl_add)
        self.view.btn_edit.clicked.connect(self.hdl_edit)
        self.view.btn_delete.clicked.connect(self.hdl_delete)

    def refresh_table(self):
        self.view.table.set_episodes(self.model.episodes)

    def _current_row(self):
        row = self.view.table.currentRow()
        if 0 <= row < len(self.model.episodes):
            return row
        return None

    def hdl_add(self):
        try:
            dialog = EpisodeDialog()
            if dialog.exec_():
                self.model.episodes.append(dialog.to_model())
                self.refresh_table()
        except Exception:
            traceback.print_exc()

    def hdl_edit(self):
        try:
            row = self._current_row()
            if row is None:
                self._warn("Select an episode from the table.")
                return
            dialog = EpisodeDialog()
            dialog.from_model(self.model.episodes[row])
            if dialog.exec_():
                self.model.episodes[row] = dialog.to_model()
                self.refresh_table()
        except Exception:
            traceback.print_exc()

    def hdl_delete(self):
        row = self._current_row()
        if row is not None:
            del self.model.episodes[row]
            self.refresh_table()

    @staticmethod
    def _warn(text):
        dialog = QMessageBox()
        dialog.setWindowTitle("Episodes")
        dialog.setText(text)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setIcon(QMessageBox.Information)
        dialog.exec_()

    def update_model(self):
        # Episodes are edited directly on the model; nothing to pull from simple widgets.
        pass

    def update_view(self):
        self.refresh_table()
