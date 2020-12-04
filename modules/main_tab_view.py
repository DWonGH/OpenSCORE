from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QMessageBox

from modules.patient_details import PatientDetailTab
from modules.recording_conditions import RecordingConditionsTab
from modules.findings import FindingsTab
from modules.diagnostic_significance import DiagnosticSignificanceTab
from modules.clinical_comment import ClinicalComments
import modules.standard_dialogs as dlg


class MainTabWidget(QWidget):

    def __init__(self, parent):
        """
        The MainTabWidget goes in the MainWindow widget and allows the user to browse and access each
        of the 5 main SCORE categories and their subsections
        :param parent: MainWindow
        """
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.patient_details_tab = PatientDetailTab(self)
        self.recording_conditions = RecordingConditionsTab(self)
        self.findings_tab = FindingsTab(self)
        self.diagnostic_significance_tab = DiagnosticSignificanceTab(self)
        self.clinical_comments = ClinicalComments(self)
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.patient_details_tab, "Patient details")
        self.tabs.addTab(self.recording_conditions, "Recording Conditions")
        self.tabs.addTab(self.findings_tab, "Findings")
        self.tabs.addTab(self.diagnostic_significance_tab, "Diagnostic Significance")
        self.tabs.addTab(self.clinical_comments, "Clinical Comments")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def get_fields(self):
        """
        Pulls the data from each input in the UI
        :return: A dictionary describing the 5 main categories and various sub categories of the
                    SCORE EEG reporting standard
        """
        patient_score = {
            "Patient details": self.patient_details_tab.get_fields(),
            "Recording conditions": self.recording_conditions.get_fields(),
            "Findings": {
                "Background Activity": self.findings_tab.background_activity_tab.get_fields()
            },
            "Diagnostic significance": self.diagnostic_significance_tab.get_fields(),
            "Clinical comments": self.clinical_comments.get_fields()
        }
        return patient_score

    def set_fields(self, report):
        try:
            self.patient_details_tab.set_fields(report["Patient details"])
            self.recording_conditions.set_fields(report["Recording conditions"])
            self.findings_tab.set_fields(report["Findings"])
            self.diagnostic_significance_tab.set_fields(report["Diagnostic significance"])
            self.clinical_comments.set_fields(report["Clinical comments"])
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, e)
            print(e)