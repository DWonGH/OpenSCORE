import os
import subprocess
import json

from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QDialog, QMessageBox

import modules.standard_dialogs as dlg


class MainToolBar(QToolBar):
    def __init__(self, parent, ui_model):
        super().__init__()

        self.parent = parent
        self.ui_model = ui_model

        self.lbl_current_eeg = QLabel("Current EEG: ")
        self.addWidget(self.lbl_current_eeg)

        self.lbl_current_eeg_name = QLabel("")
        self.lbl_current_eeg_name.setMinimumWidth(110)
        self.addWidget(self.lbl_current_eeg_name)

        self.bt_previous_recording = QAction("&Previous", self)
        self.bt_previous_recording.triggered.connect(self.hdl_previous_recording)
        self.addAction(self.bt_previous_recording)

        self.bt_next_recording = QAction("&Next", self)
        self.bt_next_recording.triggered.connect(self.hdl_next_recording)
        self.addAction(self.bt_next_recording)

        self.bt_open_in_edfbrowser = QAction("&Open in EDFBrowser", self)
        self.bt_open_in_edfbrowser.triggered.connect(self.hdl_open_in_edfbrowser)
        self.addAction(self.bt_open_in_edfbrowser)

        self.start_analysis = QAction("&Start Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.start_analysis)
        self.addAction(self.start_analysis)

        self.stop_analysis = QAction("&Stop Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.stop_analysis)
        self.addAction(self.stop_analysis)

    def hdl_next_recording(self):
        try:
            if os.path.exists(self.ui_model.report_path):
                print(f"report path 1 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    self.parent.menu.hdl_save_report()
            elif os.path.exists(self.ui_model.current_output_directory):
                self.ui_model.report_path = f"{os.path.join(self.ui_model.current_output_directory, self.ui_model.current_output_filename)}.json"
                print(f"report path 2 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    with open(self.ui_model.report_path, 'w') as f:
                        report = self.parent.main_tab_view.get_fields()
                        json.dump(report, f, indent=4)

            if self.ui_model.current_input_index < len(self.ui_model.input_directories) - 1:
                self.ui_model.current_input_index += 1
                self.ui_model.current_output_index += 1
                self.ui_model.set_current_names_and_directories()
                self.parent.update()
            else:
                result = dlg.message_dialog("End of input files", "You have reached the end of the specified eeg recordings", QMessageBox.Warning)

        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, str(e))
            print(f"Exception {e}")

    def hdl_previous_recording(self):
        try:
            if os.path.exists(self.ui_model.report_path):
                print(f"report path 1 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    self.parent.menu.hdl_save_report()
            elif os.path.exists(self.ui_model.current_output_directory):
                self.ui_model.report_path = f"{os.path.join(self.ui_model.current_output_directory, self.ui_model.current_output_filename)}.json"
                print(f"report path 2 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    with open(self.ui_model.report_path, 'w') as f:
                        report = self.parent.main_tab_view.get_fields()
                        json.dump(report, f, indent=4)
            if self.ui_model.current_input_index > 0:
                self.ui_model.current_input_index -= 1
                self.ui_model.current_output_index -= 1
                self.ui_model.set_current_names_and_directories()
                self.parent.update()
            else:
                result = dlg.message_dialog("End of input files",
                                            "You have reached the end of the specified eeg recordings",
                                            QMessageBox.Warning)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, str(e))
            print(f"Exception {e}")

    def hdl_open_in_edfbrowser(self):
        # C:\Program Files\EDFbrowser\edfbrowser.exe
        edfbrowser_path = os.path.join('C:\\Program Files\\EDFbrowser\\edfbrowser.exe')
        try:
            if os.path.exists(self.ui_model.current_edf_path):
                subprocess.Popen([edfbrowser_path, self.ui_model.current_edf_path])
            #elif os.path.exists(self.parent.main_tab_view.recording_conditions.)
            else:
                print(f"EDF Path {self.ui_model.current_edf_path}")
                result = dlg.message_dialog("Open in EDFBrowser", "OpenSCORE cannot find a valid EDF file. To open an EDF "
                                                                  "in EDFBroswer, either use the load EEG / load EEG "
                                                                  "sequence; or specify the path to the EDF recording in "
                                                                  "the recording conditions tab.", QMessageBox.Warning)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, str(e))
            print(e)

    def hdl_start_analysis(self):
        # get the specified output directory
        # get the input directory path
        # starting from root of tueg directory,
        # if the next directory isnt there, create it and change into it
        # otherwise change into the next one
        #
        pass