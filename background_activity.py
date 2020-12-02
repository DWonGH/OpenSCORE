from PyQt5.QtWidgets import QFormLayout, QLabel, QWidget, QComboBox, QSpinBox, QCheckBox, QLineEdit, QHBoxLayout


class BackgroundActivityTab(QWidget):

    def __init__(self, parent):
        """
        Build a widget containing options for scoring background activity and rhythms
        :param parent: The FindingsTab widget
        """
        super(QWidget, self).__init__(parent)

        """Add options for scoring the posterior dominant rhythm"""
        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Posterior Dominant Rhythm"))

        self.txt_pdr_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_pdr_significance = QLabel("Significance")
        self.cmb_pdr_significance = QComboBox()
        self.cmb_pdr_significance.addItems(self.txt_pdr_significance)
        self.layout.addRow(self.lbl_pdr_significance, self.cmb_pdr_significance)

        self.lbl_pdr_frequency = QLabel("Frequency")
        self.spb_pdr_frequency = QSpinBox()
        self.spb_pdr_frequency.setRange(0, 20000)
        self.spb_pdr_frequency.setSuffix("hz")
        self.spb_pdr_frequency.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_pdr_frequency, self.spb_pdr_frequency)

        self.lbl_pdr_freq_asymmetry = QLabel("Frequency Asymmetry")
        self.hbx_pdr_freq_asymmetry = QHBoxLayout()
        self.chb_pdr_freq_asymmetry = QCheckBox("Symmetrical")
        self.chb_pdr_freq_asymmetry.setChecked(True)
        self.chb_pdr_freq_asymmetry.toggled.connect(self.toggle_pdr_symmetry)
        self.hbx_pdr_freq_asymmetry.addWidget(self.chb_pdr_freq_asymmetry)
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

        self.txt_pdr_absense = ["",
                                "Artifacts",
                                "Extreme low voltage",
                                "Eye closure could not be achieved",
                                "Lack of awake period",
                                "Lack of compliance",
                                "Other causes"]
        self.lbl_pdr_absense = QLabel("Absense of PDR")
        self.cmb_pdr_absense = QComboBox()
        self.cmb_pdr_absense.addItems(self.txt_pdr_absense)
        self.layout.addRow(self.lbl_pdr_absense, self.cmb_pdr_absense)

        """Add options for scoring the Mu Rhythm"""
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Mu Rhythm"))

        self.txt_mu_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_mu_significance = QLabel("Significance")
        self.cmb_mu_significance = QComboBox()
        self.cmb_mu_significance.addItems(self.txt_mu_significance)
        self.layout.addRow(self.lbl_mu_significance, self.cmb_mu_significance)

        self.txt_mu_spectral = ["", "Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.lbl_mu_spectral = QLabel("Spectral Frequency")
        self.cmb_mu_spectral = QComboBox()
        self.cmb_mu_spectral.addItems(self.txt_mu_spectral)
        self.layout.addRow(self.lbl_mu_spectral, self.cmb_mu_spectral)

        self.lbl_mu_frequency = QLabel("Frequency")
        self.spb_mu_frequency = QSpinBox()
        self.spb_mu_frequency.setSuffix("hz")
        self.spb_mu_frequency.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_mu_frequency, self.spb_mu_frequency)

        self.lbl_mu_amplitude = QLabel("Amplitude")
        self.spb_mu_amplitude = QSpinBox()
        self.spb_mu_amplitude.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_mu_amplitude, self.spb_mu_amplitude)

        self.txt_mu_modulator_effect = ["", "Small effect", "Medium effect", "Large effect"]
        self.lbl_mu_modulator_effect = QLabel("Modulator effect")
        self.cmb_mu_modulator_effect = QComboBox()
        self.cmb_mu_modulator_effect.addItems(self.txt_mu_modulator_effect)
        self.layout.addRow(self.lbl_mu_modulator_effect, self.cmb_mu_modulator_effect)

        """Add options for scoring other organised rhythms"""
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Other Organised Rhythms"))

        self.txt_other_significance = ["", "Normal", "No definite abnormality", "Abnormal"]
        self.lbl_other_significance = QLabel("Significance")
        self.cmb_other_significance = QComboBox()
        self.cmb_other_significance.addItems(self.txt_other_significance)
        self.layout.addRow(self.lbl_other_significance, self.cmb_other_significance)

        self.txt_other_spectral = ["", "Delta", "Theta", "Alpha", "Beta", "Gamma"]
        self.lbl_other_spectral = QLabel("Spectral Frequency")
        self.cmb_other_spectral = QComboBox()
        self.cmb_other_spectral.addItems(self.txt_mu_spectral)
        self.layout.addRow(self.lbl_other_spectral, self.cmb_other_spectral)

        self.lbl_other_frequency = QLabel("Frequency")
        self.spb_other_frequency = QSpinBox()
        self.spb_other_frequency.setSuffix("hz")
        self.spb_other_frequency.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_other_frequency, self.spb_other_frequency)

        self.lbl_other_amplitude = QLabel("Amplitude")
        self.spb_other_amplitude = QSpinBox()
        self.spb_other_amplitude.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_other_amplitude, self.spb_other_amplitude)

        self.txt_other_modulator_effect = ["", "Small effect", "Medium effect", "Large effect"]
        self.lbl_other_modulator_effect = QLabel("Modulator effect")
        self.cmb_other_modulator_effect = QComboBox()
        self.cmb_other_modulator_effect.addItems(self.txt_other_modulator_effect)
        self.layout.addRow(self.lbl_other_modulator_effect, self.cmb_other_modulator_effect)

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
        self.cmb_critical_features = QComboBox()
        self.cmb_critical_features.addItems(self.txt_critical_features)
        self.layout.addRow(self.lbl_critical_features, self.cmb_critical_features)

        self.setLayout(self.layout)

    def get_details(self):
        """
        Collects the information from the user inputs
        :return: A dictionary to merge into the master report dictionary in main tab
        """
        background_activity = {
            "Posterior dominant rhythm": {
                "Significance": self.cmb_pdr_significance.currentText(),
                "Frequency": self.spb_pdr_frequency.text(),
                "Frequency Asymmetry": {
                    "Symmetrical": self.chb_pdr_freq_asymmetry.isChecked(),
                    "Hz lower on left side": self.txe_pdr_freq_asymmetry_left.text(),
                    "Hz lower on right side": self.txe_pdr_freq_asymmetry_right.text()
                },
                "Amplitude": self.cmb_pdr_amplitude.currentText(),
                "Reactivity to eye opening": self.cmb_pdr_eye_opening.currentText(),
                "Organisation": self.cmb_pdr_organisation.currentText(),
                "Caveat": self.cmb_pdr_caveat.currentText(),
                "Absense of PDR": self.cmb_pdr_absense.currentText()
            },
            "Mu Rhythm": {
                "Significance": self.cmb_mu_significance.currentText(),
                "Spectral frequency": self.cmb_mu_spectral.currentText(),
                "Frequency": self.spb_mu_frequency.text(),
                "Amplitude": self.spb_mu_amplitude.text(),
                "Modulator effect": self.cmb_mu_modulator_effect.currentText()
            },
            "Other organised rhythms": {
                "Significance": self.cmb_other_significance.currentText(),
                "Spectral frequency": self.cmb_other_spectral.currentText(),
                "Frequency": self.spb_other_frequency.text(),
                "Amplitude": self.spb_other_amplitude.text(),
                "Modulator effect": self.cmb_other_modulator_effect.currentText()
            },
            "Special features": {
                "Critically ill background activity": self.cmb_critical_features.currentText()
            }
        }
        return background_activity

    def toggle_pdr_symmetry(self):
        """
        Restricts user from entering more than 1 option for the frequency asymmetry field
        :return: None
        """
        if self.chb_pdr_freq_asymmetry.isChecked() and (self.txe_pdr_freq_asymmetry_left.text() == "") and (self.txe_pdr_freq_asymmetry_right.text() == ""):
            self.chb_pdr_freq_asymmetry.setEnabled(True)
            self.txe_pdr_freq_asymmetry_left.setEnabled(False)
            self.txe_pdr_freq_asymmetry_right.setEnabled(False)
        elif (self.chb_pdr_freq_asymmetry.isChecked() is False) and (self.txe_pdr_freq_asymmetry_left.text() == "") and (self.txe_pdr_freq_asymmetry_right.text() == ""):
            self.chb_pdr_freq_asymmetry.setEnabled(True)
            self.txe_pdr_freq_asymmetry_left.setEnabled(True)
            self.txe_pdr_freq_asymmetry_right.setEnabled(True)
        elif (self.chb_pdr_freq_asymmetry.isChecked() is False) and (self.txe_pdr_freq_asymmetry_left.text() != "") and (self.txe_pdr_freq_asymmetry_right.text() == ""):
            self.chb_pdr_freq_asymmetry.setEnabled(False)
            self.txe_pdr_freq_asymmetry_left.setEnabled(True)
            self.txe_pdr_freq_asymmetry_right.setEnabled(False)
        elif (self.chb_pdr_freq_asymmetry.isChecked() is False) and (self.txe_pdr_freq_asymmetry_left.text() == "") and (self.txe_pdr_freq_asymmetry_right.text() != ""):
            self.chb_pdr_freq_asymmetry.setEnabled(False)
            self.txe_pdr_freq_asymmetry_left.setEnabled(False)
            self.txe_pdr_freq_asymmetry_right.setEnabled(True)

    def clear_inputs(self):
        pass


