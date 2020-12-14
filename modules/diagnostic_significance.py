from PyQt5.QtWidgets import QSizePolicy, QRadioButton, QSpacerItem, QCheckBox, QFormLayout, QLabel, QWidget, \
    QVBoxLayout, QMessageBox

import modules.standard_dialogs as dlg


class DiagnosticSignificanceTab(QWidget):

    def __init__(self, main_tab):
        """
        A top level tab describing diagnostic significance
        :param main_tab:
        """
        super(QWidget, self).__init__(main_tab)

        self.main_tab = main_tab
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

    def get_fields(self):
        """
        Pull user input from the boxes and buttons
        :return:
        """
        diagnostic_significance = {
            "Normal recording": self.rbt_normal.isChecked(),
            "No Definite Abnormality": self.rbt_no_definite.isChecked(),
            "Abnormal recording": self.rbt_abnormal.isChecked(),
            "Abnormal specification": {
                "Epilepsy": (self.chbx_pnes.isChecked() or self.chbx_other_nonepileptic.isChecked()) and self.rbt_abnormal.isChecked(),
                "Psychogenic non-epileptic seizures (PNES)": self.chbx_pnes.isChecked() and self.rbt_abnormal.isChecked(),
                "Other non-epileptic clinical episode": self.chbx_other_nonepileptic.isChecked() and self.rbt_abnormal.isChecked(),
                "Status epilepticus": (self.chbx_focal_dysfunction.isChecked() or self.chbx_diffuse_dysfunction.isChecked()) and self.rbt_abnormal.isChecked(),
                "Focal dysfunction of the central nervous system": self.chbx_focal_dysfunction.isChecked() and self.rbt_abnormal.isChecked(),
                "Diffuse dysfunction of the central nervous system": self.chbx_diffuse_dysfunction.isChecked() and self.rbt_abnormal.isChecked(),
                "Continuous spikes and waves during slow sleep (CSWS) or electrical status epilepticus in sleep (ESES)": (self.chbx_coma.isChecked() or self.chbx_brain_death.isChecked() or self.chbx_uncertain.isChecked()) and self.rbt_abnormal.isChecked(),
                "Coma": self.chbx_coma.isChecked() and self.rbt_abnormal.isChecked(),
                "Brain death": self.chbx_brain_death.isChecked() and self.rbt_abnormal.isChecked(),
                "EEG abnormality of uncertain clinical significance": self.chbx_uncertain.isChecked() and self.rbt_abnormal.isChecked()
            }
        }
        return diagnostic_significance

    def set_fields(self, details):
        """
        Populate the boxes and buttons using given dictionary
        :param details:
        :return:
        """
        try:
            print(details)
            if details["Normal recording"]: self.rbt_normal.setChecked(True)
            elif details["No Definite Abnormality"]: self.rbt_no_definite.setChecked(True)
            elif details["Abnormal recording"]:
                print("True")
                self.rbt_abnormal.setChecked(True)
                self.abnormal_toggled()
                print("Toggled")
                if details["Abnormal specification"]['Psychogenic non-epileptic seizures (PNES)']: self.chbx_pnes.setChecked(True)
                if details["Abnormal specification"]["Other non-epileptic clinical episode"]: self.chbx_other_nonepileptic.setChecked(True)
                if details["Abnormal specification"]["Focal dysfunction of the central nervous system"]: self.chbx_focal_dysfunction.setChecked(True)
                if details["Abnormal specification"]["Diffuse dysfunction of the central nervous system"]: self.chbx_diffuse_dysfunction.setChecked(True)
                if details["Abnormal specification"]["Coma"]: self.chbx_coma.setChecked(True)
                if details["Abnormal specification"]["Brain death"]: self.chbx_brain_death.setChecked(True)
                if details["Abnormal specification"]["EEG abnormality of uncertain clinical significance"]: self.chbx_uncertain.setChecked(True)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(e)

    def abnormal_toggled(self):
        """
        Disable and ignore checks in each of the abnormal specification checkboxes if the recording is not considered
        abnormal
        :return:
        """
        if self.rbt_abnormal.isChecked():
            self.chbx_brain_death.setEnabled(True)
            self.chbx_diffuse_dysfunction.setEnabled(True)
            self.chbx_focal_dysfunction.setEnabled(True)
            self.chbx_pnes.setEnabled(True)
            self.chbx_coma.setEnabled(True)
            self.chbx_other_nonepileptic.setEnabled(True)
            self.chbx_uncertain.setEnabled(True)
        else:
            self.chbx_brain_death.setEnabled(False)
            self.chbx_diffuse_dysfunction.setEnabled(False)
            self.chbx_focal_dysfunction.setEnabled(False)
            self.chbx_pnes.setEnabled(False)
            self.chbx_coma.setEnabled(False)
            self.chbx_other_nonepileptic.setEnabled(False)
            self.chbx_uncertain.setEnabled(False)