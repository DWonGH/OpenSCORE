from PyQt5.QtWidgets import QFormLayout, QLabel, QWidget, QComboBox, QCheckBox, QHBoxLayout, \
    QPushButton

from src.views.custom_widgets import IntegerLineEdit
from src.views.rhythm_table_widget import RhythmTableWidget


class BackgroundActivityWidget(QWidget):

    def __init__(self):

        super(QWidget, self).__init__()

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Posterior Dominant Rhythm"))

        self.txt_pdr_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_pdr_significance = QLabel("Significance")
        self.cmb_pdr_significance = QComboBox()
        self.cmb_pdr_significance.addItems(self.txt_pdr_significance)
        self.layout.addRow(self.lbl_pdr_significance, self.cmb_pdr_significance)

        self.lbl_pdr_frequency = QLabel("Frequency (Hz)")
        self.lne_pdr_frequency = IntegerLineEdit()
        self.layout.addRow(self.lbl_pdr_frequency, self.lne_pdr_frequency)

        self.lbl_pdr_freq_asymmetry = QLabel("Frequency Asymmetry")
        self.hbx_pdr_freq_asymmetry = QHBoxLayout()
        self.chbx_pdr_freq_asymmetry = QCheckBox("Symmetrical")
        self.chbx_pdr_freq_asymmetry.setChecked(True)
        self.hbx_pdr_freq_asymmetry.addWidget(self.chbx_pdr_freq_asymmetry)
        self.lne_pdr_freq_asymmetry_left = IntegerLineEdit()
        self.lne_pdr_freq_asymmetry_left.setPlaceholderText("Hz lower left")
        self.lne_pdr_freq_asymmetry_left.setEnabled(False)
        self.hbx_pdr_freq_asymmetry.addWidget(self.lne_pdr_freq_asymmetry_left)
        self.lne_pdr_freq_asymmetry_right = IntegerLineEdit()
        self.lne_pdr_freq_asymmetry_right.setEnabled(False)
        self.lne_pdr_freq_asymmetry_right.setPlaceholderText("Hz lower right")
        self.hbx_pdr_freq_asymmetry.addWidget(self.lne_pdr_freq_asymmetry_right)
        self.layout.addRow(self.lbl_pdr_freq_asymmetry, self.hbx_pdr_freq_asymmetry)

        self.txt_pdr_amplitude = ["", "Low (<20μV)", "Medium (20-70μV)", "High (>70μV)"]
        self.lbl_pdr_amplitude = QLabel("Amplitude (μV)")
        self.cmb_pdr_amplitude = QComboBox()
        self.cmb_pdr_amplitude.addItems(self.txt_pdr_amplitude)
        self.layout.addRow(self.lbl_pdr_amplitude, self.cmb_pdr_amplitude)

        self.txt_pdr_amp_asymmetry = ["", "Symmetrical", "Right < Left", "Left < Right"]
        self.lbl_pdr_amp_asymmetry = QLabel("Amplitude Asymmetry")
        self.cmb_pdr_amp_asymmetry = QComboBox()
        self.cmb_pdr_amp_asymmetry.addItems(self.txt_pdr_amp_asymmetry)
        self.layout.addRow(self.lbl_pdr_amp_asymmetry, self.cmb_pdr_amp_asymmetry)

        self.txt_pdr_eye_opening = ["", "Yes", "Reduced left side reactivity", "Reduced right side reactivity", "Reduced reactivity on both sides"]
        self.lbl_pdr_eye_opening = QLabel("Reactivity to eye opening")
        self.cmb_pdr_eye_opening = QComboBox()
        self.cmb_pdr_eye_opening.addItems(self.txt_pdr_eye_opening)
        self.layout.addRow(self.lbl_pdr_eye_opening, self.cmb_pdr_eye_opening)

        self.txt_pdr_organisation = ["", "Normal", "Poorly organised", "Disorganised", "Markedly disorganised"]
        self.lbl_pdr_organisation = QLabel("Organisation")
        self.cmb_pdr_organisation = QComboBox()
        self.cmb_pdr_organisation.addItems(self.txt_pdr_organisation)
        self.layout.addRow(self.lbl_pdr_organisation, self.cmb_pdr_organisation)

        self.txt_pdr_caveat = ["", "No", "Only open eyes during the recording", "Sleep-deprived", "Drowsy", "Only following hyperventillation"]
        self.lbl_pdr_caveat = QLabel("Caveat")
        self.cmb_pdr_caveat = QComboBox()
        self.cmb_pdr_caveat.addItems(self.txt_pdr_caveat)
        self.layout.addRow(self.lbl_pdr_caveat, self.cmb_pdr_caveat)

        self.txt_pdr_absence = ["",
                                "Is present",
                                "Artifacts",
                                "Extreme low voltage",
                                "Eye closure could not be achieved",
                                "Lack of awake period",
                                "Lack of compliance",
                                "Other causes"]
        self.lbl_pdr_absence = QLabel("Absence of PDR")
        self.cmb_pdr_absence = QComboBox()
        self.cmb_pdr_absence.addItems(self.txt_pdr_absence)
        self.layout.addRow(self.lbl_pdr_absence, self.cmb_pdr_absence)

        """Add options for scoring special / critically ill features"""
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Critical features"))
        self.txt_critical_features = ["",
                                      "None",
                                      "Continuous background activity",
                                      "Nearly continuous background activity",
                                      "Discontinuous background activity",
                                      "Burst-suppression",
                                      "Burst attenuation",
                                      "Suppression and electrocerebral inactivity"]
        self.lbl_critical_features = QLabel("Critically ill background activity")
        self.cmb_critical_features = QComboBox()
        self.cmb_critical_features.addItems(self.txt_critical_features)
        self.layout.addRow(self.lbl_critical_features, self.cmb_critical_features)

        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Other organised rhythms"))

        self.hbx_rhythm_table = QHBoxLayout()
        self.btn_add_rhythm = QPushButton("Add Rhythm")
        self.hbx_rhythm_table.addWidget(self.btn_add_rhythm)
        self.btn_edit_rhythm = QPushButton("Edit Rhythm")
        self.hbx_rhythm_table.addWidget(self.btn_edit_rhythm)
        self.btn_delete_rhythm = QPushButton("Delete Rhythm")
        self.hbx_rhythm_table.addWidget(self.btn_delete_rhythm)
        self.layout.addRow(self.hbx_rhythm_table)

        self.rhythm_table = RhythmTableWidget()

        self.layout.addRow(self.rhythm_table)
        self.setLayout(self.layout)

    def to_dict(self):
        data = {
            "Posterior dominant rhythm": {
                "Significance": self.cmb_pdr_significance.currentText(),
                "Frequency": self.lne_pdr_frequency.text(),
                "Frequency asymmetry": self.chbx_pdr_freq_asymmetry.isChecked(),
                "Hz lower left": self.lne_pdr_freq_asymmetry_left.text(),
                "Hz lower right": self.lne_pdr_freq_asymmetry_right.text(),
                "Amplitude": self.cmb_pdr_amplitude.currentText(),
                "Amplitude asymmetry": self.cmb_pdr_amp_asymmetry.currentText(),
                "Reactivity to eye opening": self.cmb_pdr_eye_opening.currentText(),
                "Organisation": self.cmb_pdr_organisation.currentText(),
                "Caveat": self.cmb_pdr_caveat.currentText(),
                "Absence of PDR": self.cmb_pdr_absence.currentText()
            },
            "Critically ill background activity": self.cmb_critical_features.currentText(),
            "Other organised rhythms": self.rhythm_table.table_to_dict()
        }
        return data

    def update_from_dict(self, data):
        pdr = data["Posterior dominant rhythm"]
        if pdr["Significance"] is not None:
            self.cmb_pdr_significance.setCurrentIndex(self.txt_pdr_significance.index(pdr["Significance"]))
        else:
            self.cmb_pdr_significance.setCurrentIndex(0)
        self.lne_pdr_frequency.setText(pdr["Frequency"])
        if pdr["Frequency asymmetry"] is True:
            self.chbx_pdr_freq_asymmetry.setChecked(True)
        else:
            self.chbx_pdr_freq_asymmetry.setChecked(False)
        self.lne_pdr_freq_asymmetry_left.setText(pdr["Hz lower left"])
        self.lne_pdr_freq_asymmetry_right.setText(pdr["Hz lower right"])
        if pdr["Amplitude"] is not None:
            self.cmb_pdr_amplitude.setCurrentIndex(self.txt_pdr_amplitude.index(pdr["Amplitude"]))
        else:
            self.cmb_pdr_amplitude.setCurrentIndex(0)
        if pdr["Amplitude asymmetry"] is not None:
            self.cmb_pdr_amp_asymmetry.setCurrentIndex(self.txt_pdr_amp_asymmetry.index(pdr["Amplitude asymmetry"]))
        else:
            self.cmb_pdr_amp_asymmetry.setCurrentIndex(0)
        if pdr["Reactivity to eye opening"] is not None:
            self.cmb_pdr_eye_opening.setCurrentIndex(self.txt_pdr_eye_opening.index(pdr["Reactivity to eye opening"]))
        else:
            self.cmb_pdr_eye_opening.setCurrentIndex(0)
        if pdr["Organisation"] is not None:
            self.cmb_pdr_organisation.setCurrentIndex(self.txt_pdr_organisation.index(pdr["Organisation"]))
        else:
            self.cmb_pdr_organisation.setCurrentIndex(0)
        if pdr["Caveat"] is not None:
            self.cmb_pdr_caveat.setCurrentIndex(self.txt_pdr_caveat.index(pdr["Caveat"]))
        else:
            self.cmb_pdr_caveat.setCurrentIndex(0)
        if pdr["Absence of PDR"] is not None:
            self.cmb_pdr_absence.setCurrentIndex(self.txt_pdr_absence.index(pdr["Absence of PDR"]))
        else:
            self.cmb_pdr_absence.setCurrentIndex(0)
        if data["Critically ill background activity"] is not None:
            self.cmb_critical_features.setCurrentIndex(self.txt_critical_features.index(data["Critically ill background activity"]))
        else:
            self.cmb_critical_features.setCurrentIndex(0)
        self.rhythm_table.update_from_dict(data["Other organised rhythms"])
