from PyQt5.QtWidgets import QFormLayout, QLabel, QWidget, QComboBox, QSpinBox, QCheckBox, QLineEdit, QHBoxLayout


class BackgroundActivityTab(QWidget):

    def __init__(self, findings_tab):
        """
        Build a widget containing options for scoring background activity and rhythms
        :param findings_tab: The FindingsTab widget
        """
        super(QWidget, self).__init__(findings_tab)

        """Add options for scoring the posterior dominant rhythm"""
        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Posterior Dominant Rhythm"))

        self.txt_pdr_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_pdr_significance = QLabel("Significance")
        self.cbx_pdr_significance = QComboBox()
        self.cbx_pdr_significance.addItems(self.txt_pdr_significance)
        self.layout.addRow(self.lbl_pdr_significance, self.cbx_pdr_significance)

        self.lbl_pdr_frequency = QLabel("Frequency")
        self.sbx_pdr_frequency = QSpinBox()
        self.sbx_pdr_frequency.setRange(0, 20000)
        self.sbx_pdr_frequency.setSuffix("hz")
        self.sbx_pdr_frequency.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_pdr_frequency, self.sbx_pdr_frequency)

        self.lbl_pdr_freq_asymmetry = QLabel("Frequency Asymmetry")
        self.hbx_pdr_freq_asymmetry = QHBoxLayout()
        self.chbx_pdr_freq_asymmetry = QCheckBox("Symmetrical")
        self.chbx_pdr_freq_asymmetry.setChecked(True)
        self.chbx_pdr_freq_asymmetry.toggled.connect(self.toggle_pdr_symmetry)
        self.hbx_pdr_freq_asymmetry.addWidget(self.chbx_pdr_freq_asymmetry)
        self.txe_pdr_freq_asymmetry_left = QLineEdit()
        self.txe_pdr_freq_asymmetry_left.setPlaceholderText("Hz lower left")
        self.txe_pdr_freq_asymmetry_left.setEnabled(False)
        self.txe_pdr_freq_asymmetry_left.textChanged.connect(self.toggle_pdr_symmetry)
        self.hbx_pdr_freq_asymmetry.addWidget(self.txe_pdr_freq_asymmetry_left)
        self.txe_pdr_freq_asymmetry_right = QLineEdit()
        self.txe_pdr_freq_asymmetry_right.setEnabled(False)
        self.txe_pdr_freq_asymmetry_right.textChanged.connect(self.toggle_pdr_symmetry)
        self.txe_pdr_freq_asymmetry_right.setPlaceholderText("Hz lower right")
        self.hbx_pdr_freq_asymmetry.addWidget(self.txe_pdr_freq_asymmetry_right)
        self.layout.addRow(self.lbl_pdr_freq_asymmetry, self.hbx_pdr_freq_asymmetry)

        self.txt_pdr_amplitude = ["", "Low (<20mV)", "Medium (20-70mV)", "High (>70mV)"]
        self.lbl_pdr_amplitude = QLabel("Amplitude")
        self.cbx_pdr_amplitude = QComboBox()
        self.cbx_pdr_amplitude.addItems(self.txt_pdr_amplitude)
        self.layout.addRow(self.lbl_pdr_amplitude, self.cbx_pdr_amplitude)

        self.txt_pdr_amp_asymmetry = ["", "Symmetrical", "Right < Left", "Left < Right"]
        self.lbl_pdr_amp_asymmetry = QLabel("Amplitude Asymmetry")
        self.cbx_pdr_amp_asymmetry = QComboBox()
        self.cbx_pdr_amp_asymmetry.addItems(self.txt_pdr_amp_asymmetry)
        self.layout.addRow(self.lbl_pdr_amp_asymmetry, self.cbx_pdr_amp_asymmetry)

        self.txt_pdr_eye_opening = ["", "Yes", "Reduced left side reactivity", "Reduced right side reactivity", "Reduced reactivity on both sides"]
        self.lbl_pdr_eye_opening = QLabel("Reactivity to eye opening")
        self.cbx_pdr_eye_opening = QComboBox()
        self.cbx_pdr_eye_opening.addItems(self.txt_pdr_eye_opening)
        self.layout.addRow(self.lbl_pdr_eye_opening, self.cbx_pdr_eye_opening)

        self.txt_pdr_organisation = ["", "Normal", "Poorly organised", "Disorganised", "Markedly disorganised"]
        self.lbl_pdr_organisation = QLabel("Organisation")
        self.cbx_pdr_organisation = QComboBox()
        self.cbx_pdr_organisation.addItems(self.txt_pdr_organisation)
        self.layout.addRow(self.lbl_pdr_organisation, self.cbx_pdr_organisation)

        self.txt_pdr_caveat = ["", "No", "Only open eyes during the recording", "Sleep-deprived", "Drowsy", "Only following hyperventillation"]
        self.lbl_pdr_caveat = QLabel("Caveat")
        self.cbx_pdr_caveat = QComboBox()
        self.cbx_pdr_caveat.addItems(self.txt_pdr_caveat)
        self.layout.addRow(self.lbl_pdr_caveat, self.cbx_pdr_caveat)

        self.txt_pdr_absence = ["",
                                "Artifacts",
                                "Extreme low voltage",
                                "Eye closure could not be achieved",
                                "Lack of awake period",
                                "Lack of compliance",
                                "Other causes"]
        self.lbl_pdr_absence = QLabel("Absense of PDR")
        self.cbx_pdr_absence = QComboBox()
        self.cbx_pdr_absence.addItems(self.txt_pdr_absence)
        self.layout.addRow(self.lbl_pdr_absence, self.cbx_pdr_absence)

        """Add options for scoring the Mu Rhythm"""
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Mu Rhythm"))

        self.txt_mu_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_mu_significance = QLabel("Significance")
        self.cbx_mu_significance = QComboBox()
        self.cbx_mu_significance.addItems(self.txt_mu_significance)
        self.layout.addRow(self.lbl_mu_significance, self.cbx_mu_significance)

        self.txt_mu_spectral = ["", "Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.lbl_mu_spectral = QLabel("Spectral Frequency")
        self.cbx_mu_spectral = QComboBox()
        self.cbx_mu_spectral.addItems(self.txt_mu_spectral)
        self.layout.addRow(self.lbl_mu_spectral, self.cbx_mu_spectral)

        self.lbl_mu_frequency = QLabel("Frequency")
        self.sbx_mu_frequency = QSpinBox()
        self.sbx_mu_frequency.setSuffix("hz")
        self.sbx_mu_frequency.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_mu_frequency, self.sbx_mu_frequency)

        self.lbl_mu_amplitude = QLabel("Amplitude")
        self.sbx_mu_amplitude = QSpinBox()
        self.sbx_mu_amplitude.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_mu_amplitude, self.sbx_mu_amplitude)

        self.txt_mu_modulator_effect = ["", "Small effect", "Medium effect", "Large effect"]
        self.lbl_mu_modulator_effect = QLabel("Modulator effect")
        self.cbx_mu_modulator_effect = QComboBox()
        self.cbx_mu_modulator_effect.addItems(self.txt_mu_modulator_effect)
        self.layout.addRow(self.lbl_mu_modulator_effect, self.cbx_mu_modulator_effect)

        """Add options for scoring other organised rhythms"""
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Other Organised Rhythms"))

        self.txt_other_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_other_significance = QLabel("Significance")
        self.cbx_other_significance = QComboBox()
        self.cbx_other_significance.addItems(self.txt_other_significance)
        self.layout.addRow(self.lbl_other_significance, self.cbx_other_significance)

        self.txt_other_spectral = ["", "Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.lbl_other_spectral = QLabel("Spectral Frequency")
        self.cbx_other_spectral = QComboBox()
        self.cbx_other_spectral.addItems(self.txt_mu_spectral)
        self.layout.addRow(self.lbl_other_spectral, self.cbx_other_spectral)

        self.lbl_other_frequency = QLabel("Frequency")
        self.sbx_other_frequency = QSpinBox()
        self.sbx_other_frequency.setSuffix("hz")
        self.sbx_other_frequency.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_other_frequency, self.sbx_other_frequency)

        self.lbl_other_amplitude = QLabel("Amplitude")
        self.sbx_other_amplitude = QSpinBox()
        self.sbx_other_amplitude.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_other_amplitude, self.sbx_other_amplitude)

        self.txt_other_modulator_effect = ["", "Small effect", "Medium effect", "Large effect"]
        self.lbl_other_modulator_effect = QLabel("Modulator effect")
        self.cbx_other_modulator_effect = QComboBox()
        self.cbx_other_modulator_effect.addItems(self.txt_other_modulator_effect)
        self.layout.addRow(self.lbl_other_modulator_effect, self.cbx_other_modulator_effect)

        """Add options for scoring special / critically ill features"""
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Special features"))

        self.txt_critical_features = ["",
                                      "Continuous background activity",
                                      "Nearly continuous background activity",
                                      "Discontinuous background activity",
                                      "burst-suppression",
                                      "Burst attenuation",
                                      "Suppression and electrocerebral inactivity"]
        self.lbl_critical_features = QLabel("Critically ill background activity")
        self.cbx_critical_features = QComboBox()
        self.cbx_critical_features.addItems(self.txt_critical_features)
        self.layout.addRow(self.lbl_critical_features, self.cbx_critical_features)

        self.setLayout(self.layout)

    def get_fields(self):
        """
        Collects the information from the user inputs
        :return: A dictionary to merge into the master report dictionary in main tab
        """
        background_activity = {
            "Posterior dominant rhythm": {
                "Significance": self.cbx_pdr_significance.currentText(),
                "Frequency": self.sbx_pdr_frequency.text(),
                "Frequency Asymmetry": {
                    "Symmetrical": self.chbx_pdr_freq_asymmetry.isChecked(),
                    "Hz lower on left side": self.txe_pdr_freq_asymmetry_left.text(),
                    "Hz lower on right side": self.txe_pdr_freq_asymmetry_right.text()
                },
                "Amplitude": self.cbx_pdr_amplitude.currentText(),
                "Amplitude asymmetry": self.cbx_pdr_amp_asymmetry.currentText(),
                "Reactivity to eye opening": self.cbx_pdr_eye_opening.currentText(),
                "Organisation": self.cbx_pdr_organisation.currentText(),
                "Caveat": self.cbx_pdr_caveat.currentText(),
                "Absence of PDR": self.cbx_pdr_absence.currentText()
            },
            "Mu Rhythm": {
                "Significance": self.cbx_mu_significance.currentText(),
                "Spectral frequency": self.cbx_mu_spectral.currentText(),
                "Frequency": self.sbx_mu_frequency.text(),
                "Amplitude": self.sbx_mu_amplitude.text(),
                "Modulator effect": self.cbx_mu_modulator_effect.currentText()
            },
            "Other organised rhythms": {
                "Significance": self.cbx_other_significance.currentText(),
                "Spectral frequency": self.cbx_other_spectral.currentText(),
                "Frequency": self.sbx_other_frequency.text(),
                "Amplitude": self.sbx_other_amplitude.text(),
                "Modulator effect": self.cbx_other_modulator_effect.currentText()
            },
            "Special features": {
                "Critically ill background activity": self.cbx_critical_features.currentText()
            }
        }
        return background_activity

    def set_fields(self, data):
        pdr = data["Posterior dominant rhythm"]
        self.cbx_pdr_significance.setCurrentIndex(self.txt_pdr_significance.index(pdr["Significance"]))
        if pdr["Frequency"] != ' ': self.sbx_pdr_frequency.setValue(int(pdr["Frequency"].strip('hz')))
        if pdr["Frequency Asymmetry"]["Symmetrical"]: self.chbx_pdr_freq_asymmetry.setChecked(True)
        self.txe_pdr_freq_asymmetry_left.setText(pdr["Frequency Asymmetry"]["Hz lower on left side"])
        self.txe_pdr_freq_asymmetry_right.setText(pdr["Frequency Asymmetry"]["Hz lower on right side"])
        self.cbx_pdr_amplitude.setCurrentIndex(self.txt_pdr_amplitude.index(pdr["Amplitude"]))
        self.cbx_pdr_amp_asymmetry.setCurrentIndex(self.txt_pdr_amp_asymmetry.index(pdr["Amplitude asymmetry"]))
        self.cbx_pdr_eye_opening.setCurrentIndex(self.txt_pdr_eye_opening.index(pdr["Reactivity to eye opening"]))
        self.cbx_pdr_organisation.setCurrentIndex(self.txt_pdr_organisation.index(pdr["Organisation"]))
        self.cbx_pdr_caveat.setCurrentIndex(self.txt_pdr_caveat.index(pdr["Caveat"]))
        self.cbx_pdr_absence.setCurrentIndex(self.txt_pdr_absence.index(pdr["Absence of PDR"]))

        mu = data["Mu Rhythm"]
        self.cbx_mu_significance.setCurrentIndex(self.txt_mu_significance.index(mu["Significance"]))
        self.cbx_mu_spectral.setCurrentIndex(self.txt_mu_spectral.index(mu["Spectral frequency"]))
        if mu["Frequency"] != ' ': self.sbx_mu_frequency.setValue(int(mu["Frequency"].strip('hz')))
        if mu["Amplitude"] != ' ': self.sbx_mu_amplitude.setValue(int(mu["Frequency"].strip('hz')))
        self.cbx_mu_modulator_effect.setCurrentIndex(self.txt_mu_modulator_effect.index(mu["Modulator effect"]))

        other = data["Other organised rhythms"]
        self.cbx_other_significance.setCurrentIndex(self.txt_other_significance.index(other["Significance"]))
        self.cbx_other_spectral.setCurrentIndex(self.txt_other_spectral.index(other["Spectral frequency"]))
        if other["Frequency"] != ' ': self.sbx_other_frequency.setValue(int(other["Frequency"].strip('hz')))
        if other["Amplitude"] != ' ': self.sbx_other_amplitude.setValue(int(other["Frequency"].strip('hz')))
        self.cbx_other_modulator_effect.setCurrentIndex(self.txt_other_modulator_effect.index(other["Modulator effect"]))

        special = data["Special features"]
        self.cbx_critical_features.setCurrentIndex(self.txt_critical_features.index(special["Critically ill background activity"]))

    def toggle_pdr_symmetry(self):
        """
        Restricts user from entering more than 1 option for the frequency asymmetry field
        :return: None
        """
        if self.chbx_pdr_freq_asymmetry.isChecked() and (self.txe_pdr_freq_asymmetry_left.text() == "") and (self.txe_pdr_freq_asymmetry_right.text() == ""):
            self.chbx_pdr_freq_asymmetry.setEnabled(True)
            self.txe_pdr_freq_asymmetry_left.setEnabled(False)
            self.txe_pdr_freq_asymmetry_right.setEnabled(False)
        elif (self.chbx_pdr_freq_asymmetry.isChecked() is False) and (self.txe_pdr_freq_asymmetry_left.text() == "") and (self.txe_pdr_freq_asymmetry_right.text() == ""):
            self.chbx_pdr_freq_asymmetry.setEnabled(True)
            self.txe_pdr_freq_asymmetry_left.setEnabled(True)
            self.txe_pdr_freq_asymmetry_right.setEnabled(True)
        elif (self.chbx_pdr_freq_asymmetry.isChecked() is False) and (self.txe_pdr_freq_asymmetry_left.text() != "") and (self.txe_pdr_freq_asymmetry_right.text() == ""):
            self.chbx_pdr_freq_asymmetry.setEnabled(False)
            self.txe_pdr_freq_asymmetry_left.setEnabled(True)
            self.txe_pdr_freq_asymmetry_right.setEnabled(False)
        elif (self.chbx_pdr_freq_asymmetry.isChecked() is False) and (self.txe_pdr_freq_asymmetry_left.text() == "") and (self.txe_pdr_freq_asymmetry_right.text() != ""):
            self.chbx_pdr_freq_asymmetry.setEnabled(False)
            self.txe_pdr_freq_asymmetry_left.setEnabled(False)
            self.txe_pdr_freq_asymmetry_right.setEnabled(True)
