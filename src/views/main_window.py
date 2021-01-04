from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar, QPushButton, QTabWidget
from src.views.menu_bar import MainMenuBar
from src.views.tool_bar import MainToolBar
from src.views.patient_details import PatientDetailsWidget
from src.views.patient_referral import PatientReferralWidget
from src.views.recording_conditions import RecordingConditionsWidget


class MainWindow(QMainWindow):

    def __init__(self, model=None, controller=None):
        """
        Sets up the main program window and widgets
        """
        super().__init__()

        self.model = model
        self.controller = controller

        self.setWindowTitle('OpenSCORE')
        self.resize(558, 500)

        self.menu = MainMenuBar(self)
        self.setMenuBar(self.menu)

        self.toolbar = MainToolBar(self)
        self.addToolBar(self.toolbar)

        self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.patient_details = PatientDetailsWidget(self)
        self.patient_referral = PatientReferralWidget(self)
        self.recording_conditions = RecordingConditionsWidget(self)

        self.tabs.addTab(self.patient_details, "Patient Details")
        self.tabs.addTab(self.patient_referral, "Patient Referral")
        self.tabs.addTab(self.recording_conditions, "Recording Conditions")

        self.main_layout.addWidget(self.tabs)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)