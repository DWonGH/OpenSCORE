from PyQt5.QtWidgets import QSizePolicy, QRadioButton, QSpacerItem, QCheckBox, QFormLayout, QLabel, QWidget, QVBoxLayout


class DiagnosticSignificanceTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.diagnosis_options = QFormLayout()
        self.diagnosis_options.addRow(QLabel("Diagnosis"))

        self.rbt_normal = QRadioButton("Normal recording")
        self.rbt_normal.setChecked(True)
        self.diagnosis_options.addRow(self.rbt_normal)

        self.rbt_no_definite = QRadioButton("No Definite Abnormality")
        self.diagnosis_options.addRow(self.rbt_no_definite)

        self.rbt_abnormal = QRadioButton("Abnormal")
        self.rbt_abnormal.toggled.connect(self.abnormal_toggled)
        self.diagnosis_options.addRow(self.rbt_abnormal)

        self.layout.addLayout(self.diagnosis_options)

        self.abnormal_options = QFormLayout()
        self.abnormal_options.addRow(QLabel(""))
        self.abnormal_options.addRow(QLabel("Epilepsy"))

        self.chb_pnes = QCheckBox("Psychogenic non-epileptic seizures (PNES)")
        self.chb_pnes.setEnabled(False)
        self.abnormal_options.addRow(self.chb_pnes)

        self.chb_other_nonepileptic = QCheckBox("Other non-epileptic clinical episode")
        self.chb_other_nonepileptic.setEnabled(False)
        self.abnormal_options.addRow(self.chb_other_nonepileptic)

        self.abnormal_options.addRow(QLabel(""))
        self.lbl_status_epilepticus = QLabel("Status epilepticus")
        self.abnormal_options.addRow(self.lbl_status_epilepticus)

        self.chb_focal_dysfunction = QCheckBox("Focal dysfunction of the central nervous system")
        self.chb_focal_dysfunction.setEnabled(False)
        self.abnormal_options.addRow(self.chb_focal_dysfunction)

        self.chb_diffuse_dysfunction = QCheckBox("Diffuse dysfunction of the central nervous system")
        self.chb_diffuse_dysfunction.setEnabled(False)
        self.abnormal_options.addRow(self.chb_diffuse_dysfunction)

        self.abnormal_options.addRow(QLabel(""))
        self.lbl_csws = QLabel("Continuous spikes and waves during slow sleep (CSWS) or electrical status epilepticus in sleep (ESES)")
        self.abnormal_options.addRow(self.lbl_csws)

        self.chb_coma = QCheckBox("Coma")
        self.chb_coma.setEnabled(False)
        self.abnormal_options.addRow(self.chb_coma)

        self.chb_brain_death = QCheckBox("Brain death")
        self.chb_brain_death.setEnabled(False)
        self.abnormal_options.addRow(self.chb_brain_death)

        self.chb_uncertain = QCheckBox("EEG abnormality of uncertain clinical significance")
        self.chb_uncertain.setEnabled(False)
        self.abnormal_options.addRow(self.chb_uncertain)

        self.layout.addLayout(self.abnormal_options)
        spacerItem = QSpacerItem(20, 237, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addSpacerItem(spacerItem)
        self.setLayout(self.layout)

    def get_details(self):
        diagnostic_significance = {
            "Normal recording": self.rbt_normal.isChecked(),
            "No Definite Abnormality": self.rbt_no_definite.isChecked(),
            "Abnormal recording": self.rbt_abnormal.isChecked(),
            "Abnormal specification": {
                "Epilepsy": (self.chb_pnes.isChecked() or self.chb_other_nonepileptic.isChecked()) and self.rbt_abnormal.isChecked(),
                "Psychogenic non-epileptic seizures (PNES)": self.chb_pnes.isChecked() and self.rbt_abnormal.isChecked(),
                "Other non-epileptic clinical episode": self.chb_other_nonepileptic.isChecked() and self.rbt_abnormal.isChecked(),
                "Status epilepticus": (self.chb_focal_dysfunction.isChecked() or self.chb_diffuse_dysfunction.isChecked()) and self.rbt_abnormal.isChecked(),
                "Focal dysfunction of the central nervous system": self.chb_focal_dysfunction.isChecked() and self.rbt_abnormal.isChecked(),
                "Diffuse dysfunction of the central nervous system": self.chb_diffuse_dysfunction.isChecked() and self.rbt_abnormal.isChecked(),
                "Continuous spikes and waves during slow sleep (CSWS) or electrical status epilepticus in sleep (ESES)": (self.chb_coma.isChecked() or self.chb_brain_death.isChecked() or self.chb_uncertain.isChecked()) and self.rbt_abnormal.isChecked(),
                "Coma": self.chb_coma.isChecked() and self.rbt_abnormal.isChecked(),
                "Brain death": self.chb_brain_death.isChecked() and self.rbt_abnormal.isChecked(),
                "EEG abnormality of uncertain clinical significance": self.chb_uncertain.isChecked() and self.rbt_abnormal.isChecked()
            }
        }
        return diagnostic_significance

    def abnormal_toggled(self):
        print("Toggle")
        if self.rbt_abnormal.isChecked():
            self.chb_brain_death.setEnabled(True)
            self.chb_diffuse_dysfunction.setEnabled(True)
            self.chb_focal_dysfunction.setEnabled(True)
            self.chb_pnes.setEnabled(True)
            self.chb_coma.setEnabled(True)
            self.chb_other_nonepileptic.setEnabled(True)
            self.chb_uncertain.setEnabled(True)
        else:
            self.chb_brain_death.setEnabled(False)
            self.chb_diffuse_dysfunction.setEnabled(False)
            self.chb_focal_dysfunction.setEnabled(False)
            self.chb_pnes.setEnabled(False)
            self.chb_coma.setEnabled(False)
            self.chb_other_nonepileptic.setEnabled(False)
            self.chb_uncertain.setEnabled(False)