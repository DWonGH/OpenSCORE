from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QFormLayout, QDialogButtonBox

from src.views.custom_widgets import IntegerLineEdit


class AddRhythmDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add background activity")
        self.setMinimumWidth(500)

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Record a new background rhythm"))

        self.txt_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_significance = QLabel("Significance")
        self.cmb_significance = QComboBox()
        self.cmb_significance.addItems(self.txt_significance)
        self.layout.addRow(self.lbl_significance, self.cmb_significance)

        self.txt_spectral = ["", "Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.lbl_spectral = QLabel("Spectral Frequency")
        self.cmb_spectral = QComboBox()
        self.cmb_spectral.addItems(self.txt_spectral)
        self.layout.addRow(self.lbl_spectral, self.cmb_spectral)

        self.lbl_frequency = QLabel("Frequency (Hz)")
        self.lne_frequency = IntegerLineEdit()
        self.layout.addRow(self.lbl_frequency, self.lne_frequency)

        self.lbl_amplitude = QLabel("Amplitude (μV)")
        self.lne_amplitude = IntegerLineEdit()
        self.layout.addRow(self.lbl_amplitude, self.lne_amplitude)

        self.txt_modulator_effect = ["", "Unknown", "Small effect", "Medium effect", "Large effect"]
        self.lbl_modulator_effect = QLabel("Modulator effect")
        self.cmb_modulator_effect = QComboBox()
        self.cmb_modulator_effect.addItems(self.txt_modulator_effect)
        self.layout.addRow(self.lbl_modulator_effect, self.cmb_modulator_effect)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def to_dict(self):
        data = {
            "Significance": self.cmb_significance.currentText(),
            "Spectral frequency": self.cmb_spectral.currentText(),
            "Frequency": self.lne_frequency.text(),
            "Amplitude": self.lne_amplitude.text(),
            "Modulator effect": self.cmb_modulator_effect.currentText()
        }
        return data

    def from_dict(self, data):
        if data["Significance"] is not None:
            self.cmb_significance.setCurrentIndex(self.txt_significance.index(data["Significance"]))
        else:
            self.cmb_significance.setCurrentIndex(0)
        if data["Spectral frequency"] is not None:
            self.cmb_spectral.setCurrentIndex(self.txt_spectral.index(data["Spectral frequency"]))
        else:
            self.cmb_spectral.setCurrentIndex(0)
        self.lne_frequency.setText(data["Frequency"])
        self.lne_amplitude.setText(data["Amplitude"])
        if data["Modulator effect"] is not None:
            self.cmb_modulator_effect.setCurrentIndex(self.txt_modulator_effect.index(data["Modulator effect"]))
        else:
            self.cmb_spectral.setCurrentIndex(0)