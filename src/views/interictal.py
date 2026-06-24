from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem, QHeaderView,
)

from score_schema import (
    DischargePattern, Incidence, InterictalGraphoelement, Laterality, Location,
    ModeOfAppearance, Morphology, Prevalence, Region, Significance, TimeRelatedFeatures,
)
from score_schema.interictal import SPECIAL_PATTERNS
from src.views.form_helpers import combo_enum, enum_combo, set_combo_text
from src.views.sleep import multi_list, selected_items, set_selected


class InterictalDialog(QDialog):
    """Add/edit a single interictal graphoelement (SCORE §8)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interictal graphoelement")
        self.setMinimumWidth(500)
        self.layout = QFormLayout()

        self.cmb_morphology = enum_combo(Morphology)
        self.layout.addRow(QLabel("Morphology"), self.cmb_morphology)
        self.cmb_significance = enum_combo(Significance)
        self.layout.addRow(QLabel("Significance"), self.cmb_significance)
        self.cmb_laterality = enum_combo(Laterality)
        self.layout.addRow(QLabel("Laterality"), self.cmb_laterality)
        self.lst_regions = multi_list([r.value for r in Region], max_height=110)
        self.layout.addRow(QLabel("Regions"), self.lst_regions)
        self.lne_electrodes = QLineEdit()
        self.layout.addRow(QLabel("Electrode maxima"), self.lne_electrodes)
        self.cmb_mode = enum_combo(ModeOfAppearance)
        self.layout.addRow(QLabel("Mode of appearance"), self.cmb_mode)
        self.cmb_discharge = enum_combo(DischargePattern)
        self.layout.addRow(QLabel("Discharge pattern"), self.cmb_discharge)
        self.cmb_incidence = enum_combo(Incidence)
        self.layout.addRow(QLabel("Incidence"), self.cmb_incidence)
        self.cmb_prevalence = enum_combo(Prevalence)
        self.layout.addRow(QLabel("Prevalence"), self.cmb_prevalence)
        self.lne_modulator = QLineEdit()
        self.layout.addRow(QLabel("Modulator effect"), self.lne_modulator)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
        self.setLayout(self.layout)

    def to_model(self):
        location = Location(
            laterality=combo_enum(self.cmb_laterality, Laterality),
            regions=[Region(r) for r in selected_items(self.lst_regions)],
            electrode_maxima=self.lne_electrodes.text() or None,
        )
        time_features = TimeRelatedFeatures(
            mode_of_appearance=combo_enum(self.cmb_mode, ModeOfAppearance),
            discharge_pattern=combo_enum(self.cmb_discharge, DischargePattern),
            incidence=combo_enum(self.cmb_incidence, Incidence),
            prevalence=combo_enum(self.cmb_prevalence, Prevalence),
        )
        return InterictalGraphoelement(
            morphology=combo_enum(self.cmb_morphology, Morphology),
            significance=combo_enum(self.cmb_significance, Significance),
            location=location,
            time_features=time_features,
            modulator_effect=self.lne_modulator.text() or None,
        )

    def from_model(self, g):
        set_combo_text(self.cmb_morphology, g.morphology)
        set_combo_text(self.cmb_significance, g.significance)
        set_combo_text(self.cmb_laterality, g.location.laterality)
        set_selected(self.lst_regions, [r.value for r in g.location.regions])
        self.lne_electrodes.setText(g.location.electrode_maxima or "")
        set_combo_text(self.cmb_mode, g.time_features.mode_of_appearance)
        set_combo_text(self.cmb_discharge, g.time_features.discharge_pattern)
        set_combo_text(self.cmb_incidence, g.time_features.incidence)
        set_combo_text(self.cmb_prevalence, g.time_features.prevalence)
        self.lne_modulator.setText(g.modulator_effect or "")


class InterictalTableWidget(QTableWidget):
    """Read-only summary of the scored graphoelements (model is the source of truth)."""

    HEADERS = ["Morphology", "Significance", "Laterality", "Regions", "Mode"]

    def __init__(self):
        super().__init__()
        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)

    @staticmethod
    def _text(value):
        return value.value if hasattr(value, "value") else (value or "")

    def set_graphoelements(self, graphoelements):
        self.setRowCount(0)
        for g in graphoelements:
            row = self.rowCount()
            self.insertRow(row)
            cells = [
                self._text(g.morphology),
                self._text(g.significance),
                self._text(g.location.laterality),
                ", ".join(r.value for r in g.location.regions),
                self._text(g.time_features.mode_of_appearance),
            ]
            for col, text in enumerate(cells):
                self.setItem(row, col, QTableWidgetItem(text))


class InterictalWidget(QWidget):
    """SCORE §8 — Interictal findings editor."""

    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Graphoelements"))
        buttons = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        for b in (self.btn_add, self.btn_edit, self.btn_delete):
            buttons.addWidget(b)
        self.layout.addLayout(buttons)

        self.table = InterictalTableWidget()
        self.layout.addWidget(self.table)

        self.layout.addWidget(QLabel("Special / periodic patterns"))
        self.lst_special = multi_list(list(SPECIAL_PATTERNS))
        self.layout.addWidget(self.lst_special)

        self.setLayout(self.layout)
