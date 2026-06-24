import traceback

from PyQt5.QtWidgets import QMessageBox

from score_schema import InterictalFindings
from src.views.interictal import InterictalDialog, InterictalWidget
from src.views.sleep import selected_items, set_selected


class InterictalController:
    """SCORE §8 — Interictal findings. The score_schema model is the source of truth;
    the table is a read-only summary refreshed from it."""

    def __init__(self):
        self.model = InterictalFindings()
        self.view = InterictalWidget()
        self.view.btn_add.clicked.connect(self.hdl_add)
        self.view.btn_edit.clicked.connect(self.hdl_edit)
        self.view.btn_delete.clicked.connect(self.hdl_delete)

    def refresh_table(self):
        self.view.table.set_graphoelements(self.model.graphoelements)

    def _current_row(self):
        row = self.view.table.currentRow()
        if 0 <= row < len(self.model.graphoelements):
            return row
        return None

    def hdl_add(self):
        try:
            dialog = InterictalDialog()
            if dialog.exec_():
                self.model.graphoelements.append(dialog.to_model())
                self.refresh_table()
        except Exception:
            traceback.print_exc()

    def hdl_edit(self):
        try:
            row = self._current_row()
            if row is None:
                self._warn("Select a graphoelement from the table.")
                return
            dialog = InterictalDialog()
            dialog.from_model(self.model.graphoelements[row])
            if dialog.exec_():
                self.model.graphoelements[row] = dialog.to_model()
                self.refresh_table()
        except Exception:
            traceback.print_exc()

    def hdl_delete(self):
        row = self._current_row()
        if row is not None:
            del self.model.graphoelements[row]
            self.refresh_table()

    @staticmethod
    def _warn(text):
        dialog = QMessageBox()
        dialog.setWindowTitle("Interictal findings")
        dialog.setText(text)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setIcon(QMessageBox.Information)
        dialog.exec_()

    def update_model(self):
        # Graphoelements are edited directly on the model; only sync the special patterns.
        self.model.special_patterns = selected_items(self.view.lst_special)

    def update_view(self):
        set_selected(self.view.lst_special, self.model.special_patterns)
        self.refresh_table()
