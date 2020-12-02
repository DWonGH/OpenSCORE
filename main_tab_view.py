from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from patient_details import PatientDetailTab
from recording_conditions import RecordingConditionsTab
from findings import FindingsTab
from diagnostic_significance import DiagnosticSignificanceTab
from clinical_comment import ClinicalComments


class MainTabWidget(QWidget):

    def __init__(self, parent):
        """
        The MainTabWidget goes in the MainWindow widget and allows the user to browse and access each
        of the 5 main SCORE categories and their subsections
        :param parent: MainWindow
        """
        super(QWidget, self).__init__(parent)
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

    def get_info(self):
        """
        Pulls the data from each input in the UI
        :return: A dictionary describing the 5 main categories and various sub categories of the
                    SCORE EEG reporting standard
        """
        patient_score = {
            "Patient details": self.patient_details_tab.get_details(),
            "Recording conditions": self.recording_conditions.get_details(),
            "Findings": {
                "Background Activity": self.findings_tab.background_activity_tab.get_details()
            },
            "Diagnostic significance": self.diagnostic_significance_tab.get_details(),
            "Clinical comments": self.clinical_comments.get_details()
        }
        return patient_score

    def reset_score(self):
        """
        Make each box in score empty for fresh report
        :return:
        """
        items = (self.layout.itemAt(i) for i in range(self.layout.count()))
        for widget in items:
            print(widget)