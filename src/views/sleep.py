from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QListWidget, QAbstractItemView, QLineEdit

from score_schema import NORMAL_SLEEP_GRAPHOELEMENTS, SLEEP_STAGES
from src.views.modulators import ternary_combo


def multi_list(options, max_height=120):
    widget = QListWidget()
    widget.addItems(list(options))
    widget.setSelectionMode(QAbstractItemView.MultiSelection)
    widget.setMaximumHeight(max_height)
    return widget


def selected_items(widget):
    return [widget.item(i).text() for i in range(widget.count()) if widget.item(i).isSelected()]


def set_selected(widget, values):
    widget.clearSelection()
    values = values or []
    for i in range(widget.count()):
        if widget.item(i).text() in values:
            widget.item(i).setSelected(True)


class SleepWidget(QWidget):
    """SCORE §7 — Sleep and drowsiness editor."""

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QFormLayout()

        self.lst_graphoelements = multi_list(NORMAL_SLEEP_GRAPHOELEMENTS)
        self.layout.addRow(QLabel("Normal sleep graphoelements"), self.lst_graphoelements)

        self.lst_stages = multi_list(SLEEP_STAGES, max_height=90)
        self.layout.addRow(QLabel("Achieved sleep stages"), self.lst_stages)

        self.cmb_asymmetry = ternary_combo()
        self.layout.addRow(QLabel("Abnormal asymmetry of sleep graphoelements"), self.cmb_asymmetry)
        self.cmb_soremp = ternary_combo()
        self.layout.addRow(QLabel("Sleep-onset REM period (SOREMP)"), self.cmb_soremp)
        self.cmb_non_reactive = ternary_combo()
        self.layout.addRow(QLabel("Non-reactive sleep activity"), self.cmb_non_reactive)

        self.lne_notes = QLineEdit()
        self.layout.addRow(QLabel("Notes"), self.lne_notes)

        self.setLayout(self.layout)
