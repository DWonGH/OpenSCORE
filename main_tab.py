from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from patient_details import PatientDetailTab
from recording_conditions import RecordingConditionsTab
from findings import FindingsTab
from diagnostic_significance import DiagnosticSignificanceTab


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
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.patient_details_tab, "Patient details")
        self.tabs.addTab(self.recording_conditions, "Recording Conditions")
        self.tabs.addTab(self.findings_tab, "Findings")
        self.tabs.addTab(self.diagnostic_significance_tab, "Diagnostic Significance")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)