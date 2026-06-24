from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem, QHeaderView,
)

from score_schema import Consciousness, Episode, EpisodeType, SemiologyPhase
from score_schema.episodes import ICTAL_EEG_PATTERNS
from src.views.form_helpers import combo_enum, enum_combo, set_combo_text
from src.views.modulators import ternary_combo, get_ternary, set_ternary
from src.views.sleep import multi_list, selected_items, set_selected

# Representative ILAE semiology terms (SCORE Tables 10/11) for the multi-select.
SEMIOLOGY_CHOICES = (
    "Motor or behavioral arrest", "Dyscognitive", "Myoclonic jerk", "Clonic", "Tonic",
    "Tonic-clonic", "Atonic", "Epileptic spasm", "Versive", "Eye blinking",
    "Oroalimentary automatism", "Manual automatism", "Hypermotor", "Aphasia",
    "Visual", "Auditory", "Epigastric", "Autonomic - cardiovascular", "Experiential",
)


class EpisodeDialog(QDialog):
    """Add/edit a single episode (SCORE §10).

    Semiology and ictal EEG are captured as one phase here; full multi-phase
    (initial/subsequent/postictal) editing is a future enhancement.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Episode")
        self.setMinimumWidth(520)
        self.layout = QFormLayout()

        self.lne_name = QLineEdit()
        self.layout.addRow(QLabel("Name / seizure type"), self.lne_name)
        self.cmb_type = enum_combo(EpisodeType)
        self.layout.addRow(QLabel("Type"), self.cmb_type)
        self.cmb_consciousness = enum_combo(Consciousness)
        self.layout.addRow(QLabel("Consciousness"), self.cmb_consciousness)
        self.cmb_awareness = ternary_combo()
        self.layout.addRow(QLabel("Awareness of the episode"), self.cmb_awareness)
        self.lne_duration = QLineEdit()
        self.layout.addRow(QLabel("Duration"), self.lne_duration)
        self.lne_timing = QLineEdit()
        self.layout.addRow(QLabel("Timing and context"), self.lne_timing)

        self.lst_semiology = multi_list(SEMIOLOGY_CHOICES, max_height=120)
        self.layout.addRow(QLabel("Semiology"), self.lst_semiology)
        self.lst_ictal = multi_list(ICTAL_EEG_PATTERNS, max_height=120)
        self.layout.addRow(QLabel("Ictal EEG"), self.lst_ictal)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
        self.setLayout(self.layout)

    def to_model(self):
        semiology = selected_items(self.lst_semiology)
        ictal_eeg = selected_items(self.lst_ictal)
        phases = []
        if semiology or ictal_eeg:
            phases = [SemiologyPhase(semiology=semiology, ictal_eeg=ictal_eeg)]
        return Episode(
            name=self.lne_name.text() or None,
            episode_type=combo_enum(self.cmb_type, EpisodeType),
            consciousness=combo_enum(self.cmb_consciousness, Consciousness),
            awareness=get_ternary(self.cmb_awareness),
            duration=self.lne_duration.text() or None,
            timing_context=self.lne_timing.text() or None,
            phases=phases,
        )

    def from_model(self, e):
        self.lne_name.setText(e.name or "")
        set_combo_text(self.cmb_type, e.episode_type)
        set_combo_text(self.cmb_consciousness, e.consciousness)
        set_ternary(self.cmb_awareness, e.awareness)
        self.lne_duration.setText(e.duration or "")
        self.lne_timing.setText(e.timing_context or "")
        semiology = e.phases[0].semiology if e.phases else []
        ictal_eeg = e.phases[0].ictal_eeg if e.phases else []
        set_selected(self.lst_semiology, semiology)
        set_selected(self.lst_ictal, ictal_eeg)


class EpisodeTableWidget(QTableWidget):
    """Read-only summary of scored episodes (model is the source of truth)."""

    HEADERS = ["Name", "Type", "Consciousness", "Duration"]

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

    def set_episodes(self, episodes):
        self.setRowCount(0)
        for e in episodes:
            row = self.rowCount()
            self.insertRow(row)
            cells = [e.name or "", self._text(e.episode_type), self._text(e.consciousness), e.duration or ""]
            for col, text in enumerate(cells):
                self.setItem(row, col, QTableWidgetItem(text))


class EpisodesWidget(QWidget):
    """SCORE §10 — Episodes editor."""

    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Episodes"))

        buttons = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        for b in (self.btn_add, self.btn_edit, self.btn_delete):
            buttons.addWidget(b)
        self.layout.addLayout(buttons)

        self.table = EpisodeTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
