from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QComboBox, QLineEdit

from score_schema import Ternary, HyperventilationQuality

# (display label, Ternary member) for the tristate combo boxes.
TERNARY_ITEMS = [
    ("Not assessed", Ternary.NOT_ASSESSED),
    ("Present", Ternary.PRESENT),
    ("Absent", Ternary.ABSENT),
]


def ternary_combo():
    combo = QComboBox()
    for label, _ in TERNARY_ITEMS:
        combo.addItem(label)
    return combo


def get_ternary(combo):
    return TERNARY_ITEMS[combo.currentIndex()][1]


def set_ternary(combo, value):
    target = value.value if hasattr(value, "value") else value
    for i, (_, member) in enumerate(TERNARY_ITEMS):
        if member.value == target:
            combo.setCurrentIndex(i)
            return
    combo.setCurrentIndex(0)


class ModulatorsWidget(QWidget):
    """SCORE §4 — Modulators and procedures editor."""

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QFormLayout()

        self.cmb_photic = ternary_combo()
        self.layout.addRow(QLabel("Intermittent photic stimulation"), self.cmb_photic)
        self.lne_photic_effect = QLineEdit()
        self.layout.addRow(QLabel("Photic stimulation effect"), self.lne_photic_effect)

        self.cmb_hv = ternary_combo()
        self.layout.addRow(QLabel("Hyperventilation"), self.cmb_hv)
        self.cmb_hv_quality = QComboBox()
        self.cmb_hv_quality.addItem("")
        for q in HyperventilationQuality:
            self.cmb_hv_quality.addItem(q.value)
        self.layout.addRow(QLabel("Hyperventilation quality"), self.cmb_hv_quality)
        self.lne_hv_effect = QLineEdit()
        self.layout.addRow(QLabel("Hyperventilation effect"), self.lne_hv_effect)

        self.cmb_sleep_dep = ternary_combo()
        self.layout.addRow(QLabel("Sleep deprivation"), self.cmb_sleep_dep)
        self.cmb_natural_sleep = ternary_combo()
        self.layout.addRow(QLabel("Natural sleep"), self.cmb_natural_sleep)
        self.cmb_induced_sleep = ternary_combo()
        self.layout.addRow(QLabel("Induced sleep"), self.cmb_induced_sleep)
        self.cmb_awakening = ternary_combo()
        self.layout.addRow(QLabel("Awakening"), self.cmb_awakening)

        self.lne_med_admin = QLineEdit()
        self.layout.addRow(QLabel("Medication administered during recording"), self.lne_med_admin)
        self.lne_med_withdrawn = QLineEdit()
        self.layout.addRow(QLabel("Medication withdrawal/reduction during recording"), self.lne_med_withdrawn)
        self.lne_other = QLineEdit()
        self.layout.addRow(QLabel("Other modulators and procedures"), self.lne_other)

        self.setLayout(self.layout)
