import json

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QVBoxLayout, QStatusBar
from main_tab import MainTabWidget


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Sets up the main program window and widgets
        """
        super().__init__()

        self.setWindowTitle('OpenSCORE')
        self.resize(500, 300)

        # Setup the Menus and toolbars
        # TODO: Add button/ option for grabbing info from chosen EDF file e.g. name, date of recording, duration etc
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")

        self.bt_new_file = QAction("&New", self)
        self.bt_new_file.setStatusTip("New report")
        # bt_new_file.triggered.connect(self.hdl_new_report)
        self.file_menu.addAction(self.bt_new_file)

        self.bt_open_file = QAction("&Open", self)
        self.bt_open_file.setStatusTip("Open existing report")
        self.bt_open_file.triggered.connect(self.hdl_load_report)
        self.file_menu.addAction(self.bt_open_file)

        self.bt_save_file = QAction("&Save", self)
        self.bt_save_file.setStatusTip("Save a file")
        self.bt_save_file.triggered.connect(self.hdl_save_report)
        self.file_menu.addAction(self.bt_save_file)

        self.bt_close_window = QAction("&Close", self)
        self.bt_close_window.setStatusTip("Exit OpenScore")
        # bt_close_window.triggered.connect(self.close())
        self.file_menu.addAction(self.bt_close_window)

        # Create the central layout and Tab Viewer
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_tab_view = MainTabWidget(self)
        self.layout.addWidget(self.main_tab_view)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        # Status bar at the bottom
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def hdl_save_report(self):
        """
        Pulls the data from the UI into a single dictionary which is then written to a JSON file
        :return:
        """
        # TODO: Add functionality for custom filename and location
        # TODO: Add functionality for producing automated filenames and locations
        score = self.get_info()
        print(score)
        with open('report.json', 'w') as f:
            json.dump(score, f, indent=4)

    def hdl_load_report(self):
        """
        Loads a json report from file and populates the input fields with the information
        :return:
        """
        # Open a dialog to search for the json file path
        # Use the path to open the json file and load into a dictionary
        # Iterate each of the headings, and call the corresponding tabs load function to populate the fields
        report = {}
        with open('report.json', 'r') as f:
            report = json.load(f)
        self.main_tab_view.patient_details_tab.load_details(report["Patient details"])

    def get_info(self):
        """
        Pulls the data from each input in the UI
        :return: A dictionary describing the 5 main categories and various sub categories of the
                    SCORE EEG reporting standard
        """
        # TODO: Need to add the rest of the Findings subsections
        # TODO: Need to add the clinical notes section
        patient_score = {
            "Patient details": self.main_tab_view.patient_details_tab.get_details(),
            "Recording conditions": self.main_tab_view.recording_conditions.get_details(),
            "Findings": {
                "Background Activity": self.main_tab_view.findings_tab.background_activity_tab.get_details()
            },
            "Diagnostic significance": self.main_tab_view.diagnostic_significance_tab.get_details()
        }
        return patient_score