

from PyQt5.QtWidgets import QSizePolicy, QRadioButton, QSpacerItem, QCheckBox, QFormLayout, QLabel, QWidget, \
    QVBoxLayout, QMessageBox


class DiagnosticSignificanceWidget(QWidget):

    def __init__(self, parent=None):

        super(QWidget, self).__init__(parent)

        self.parent = parent

        self.layout = QVBoxLayout()
        self.diagnosis_options = QFormLayout()
        self.diagnosis_options.addRow(QLabel("Diagnosis"))

        self.rbt_normal = QRadioButton("Normal recording")
        self.rbt_normal.setChecked(True)
        self.diagnosis_options.addRow(self.rbt_normal)

        self.rbt_no_definite = QRadioButton("No Definite Abnormality")
        self.diagnosis_options.addRow(self.rbt_no_definite)

        self.rbt_abnormal = QRadioButton("Abnormal")
        self.diagnosis_options.addRow(self.rbt_abnormal)

        self.layout.addLayout(self.diagnosis_options)

        self.abnormal_options = QFormLayout()
        self.abnormal_options.addRow(QLabel(""))
        self.abnormal_options.addRow(QLabel("Epilepsy"))

        self.chbx_pnes = QCheckBox("Psychogenic non-epileptic seizures (PNES)")
        self.chbx_pnes.setEnabled(False)
        self.abnormal_options.addRow(self.chbx_pnes)

        self.chbx_other_nonepileptic = QCheckBox("Other non-epileptic clinical episode")
        self.chbx_other_nonepileptic.setEnabled(False)
        self.abnormal_options.addRow(self.chbx_other_nonepileptic)

        self.abnormal_options.addRow(QLabel(""))
        self.lbl_status_epilepticus = QLabel("Status epilepticus")
        self.abnormal_options.addRow(self.lbl_status_epilepticus)

        self.chbx_focal_dysfunction = QCheckBox("Focal dysfunction of the central nervous system")
        self.chbx_focal_dysfunction.setEnabled(False)
        self.abnormal_options.addRow(self.chbx_focal_dysfunction)

        self.chbx_diffuse_dysfunction = QCheckBox("Diffuse dysfunction of the central nervous system")
        self.chbx_diffuse_dysfunction.setEnabled(False)
        self.abnormal_options.addRow(self.chbx_diffuse_dysfunction)

        self.abnormal_options.addRow(QLabel(""))
        self.lbl_csws = QLabel("Continuous spikes and waves during slow sleep (CSWS) or electrical status epilepticus in sleep (ESES)")
        self.abnormal_options.addRow(self.lbl_csws)

        self.chbx_coma = QCheckBox("Coma")
        self.chbx_coma.setEnabled(False)
        self.abnormal_options.addRow(self.chbx_coma)

        self.chbx_brain_death = QCheckBox("Brain death")
        self.chbx_brain_death.setEnabled(False)
        self.abnormal_options.addRow(self.chbx_brain_death)

        self.chbx_uncertain = QCheckBox("EEG abnormality of uncertain clinical significance")
        self.chbx_uncertain.setEnabled(False)
        self.abnormal_options.addRow(self.chbx_uncertain)

        self.layout.addLayout(self.abnormal_options)
        spacerItem = QSpacerItem(20, 237, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addSpacerItem(spacerItem)
        self.setLayout(self.layout)

    def to_dict(self):
        diagnosis = None
        diagnosis_specification = None
        if self.rbt_normal.isChecked():
            diagnosis = "Normal"
        elif self.rbt_no_definite.isChecked():
            diagnosis = "No definite abnormality"
        elif self.rbt_abnormal.isChecked():
            diagnosis = "Abnormal recording"
            diagnosis_specification = []
            if self.chbx_pnes.isChecked():
                diagnosis_specification.append(self.chbx_pnes.text())
            if self.chbx_other_nonepileptic.isChecked():
                diagnosis_specification.append(self.chbx_other_nonepileptic.text())
            if self.chbx_focal_dysfunction.isChecked():
                diagnosis_specification.append(self.chbx_focal_dysfunction.text())
            if self.chbx_diffuse_dysfunction.isChecked():
                diagnosis_specification.append(self.chbx_diffuse_dysfunction.text())
            if self.chbx_coma.isChecked():
                diagnosis_specification.append(self.chbx_coma.text())
            if self.chbx_brain_death.isChecked():
                diagnosis_specification.append(self.chbx_brain_death.text())
            if self.chbx_uncertain.isChecked():
                diagnosis_specification.append(self.chbx_uncertain.text())
        else:
            print("Error getting the diagnosis")
        data = {
            "Diagnosis": diagnosis,
            "Abnormal specification": diagnosis_specification
        }
        return data

    def update_from_dict(self, data):
        if data["Diagnosis"] is None:
            self.set_default()
        elif data["Diagnosis"] == "Normal":
            self.rbt_normal.setChecked(True)
        elif data["Diagnosis"] == "No Definite Abnormality":
            self.rbt_no_definite.setChecked(True)
        elif data["Diagnosis"] == "Abnormal recording":
            self.rbt_abnormal.setChecked(True)
            # self.abnormal_toggled()
            if data["Abnormal specification"]:
                for entry in data["Abnormal specification"]:
                    print(f"Entry: {entry}")
                    if entry == "Psychogenic non-epileptic seizures (PNES)":
                        self.chbx_pnes.setChecked(True)
                    if entry == "Other non-epileptic clinical episode":
                        self.chbx_other_nonepileptic.setChecked(True)
                    if entry == "Focal dysfunction of the central nervous system":
                        self.chbx_focal_dysfunction.setChecked(True)
                    if entry == "Diffuse dysfunction of the central nervous system":
                        self.chbx_diffuse_dysfunction.setChecked(True)
                    if entry == "Coma":
                        self.chbx_coma.setChecked(True)
                    if entry == "Brain death":
                        self.chbx_brain_death.setChecked(True)
                    if entry == "EEG abnormality of uncertain clinical significance":
                        self.chbx_uncertain.setChecked(True)

    def set_default(self):
        self.rbt_normal.setChecked(True)
        self.rbt_no_definite.setChecked(False)
        self.rbt_abnormal.setChecked(False)
        self.chbx_pnes.setChecked(False)
        self.chbx_other_nonepileptic.setChecked(False)
        self.chbx_focal_dysfunction.setChecked(False)
        self.chbx_diffuse_dysfunction.setChecked(False)
        self.chbx_coma.setChecked(False)
        self.chbx_brain_death.setChecked(False)
        self.chbx_uncertain.setChecked(False)

