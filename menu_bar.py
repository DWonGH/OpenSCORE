import json
from PyQt5.QtWidgets import QMenuBar, QAction
from start_session_dialog import StartSessionDialog


class MainMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.file_menu = self.addMenu("&File")

        self.bt_new_session = QAction("&Load EEG sequence", self)
        self.bt_new_session.setStatusTip("Load a specified set of EEG recording to analyze")
        self.bt_new_session.triggered.connect(self.hdl_new_session)
        self.file_menu.addAction(self.bt_new_session)

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

    def hdl_new_session(self):
        try:
            dialog = StartSessionDialog(self)
            if dialog.exec_():
                self.parent.interpreter_name = dialog.txe_interpreter_name.text()
                self.parent.eeg_sequence_list_location = dialog.txe_specified_paths.text()
                self.parent.root_output_directory = dialog.txe_root_output_directory.text()
                with open(self.parent.eeg_sequence_list_location, 'r') as f:
                    self.parent.eeg_sequence_list = f.read().splitlines()
                self.parent.load_tueg_recording(0)
            else:
                print("It didnt work :(")
        except Exception as e:
            print(f"Exception starting a new analysis session {e}")

    def hdl_save_report(self):
        """
        Pulls the data from the UI into a single dictionary which is then written to a JSON file
        :return:
        """
        score = self.parent.main_tab_view.get_info()
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
        print("Loading report")
        with open('report.json', 'r') as f:
            report = json.load(f)
        self.main_tab_view.patient_details_tab.load_details(report["Patient details"])
