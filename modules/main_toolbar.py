import json
import os
import subprocess

from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QMessageBox

import modules.standard_dialogs as dlg


class MainToolBar(QToolBar):

    def __init__(self, main_window, ui_model):
        """
        Options for navigating a list of recordings/ reports and opening the corresponding EDF files in EDFBrowser
        :param main_window: MainWindow
        :param ui_model: Manges the paths
        """
        super().__init__()

        self.main_window = main_window
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
        """
        Used when a list of EEG recordings have been specified. Loads the next recording and report (if exists).
        :return:
        """
        try:
            if os.path.exists(self.ui_model.report_path):
                print(f"report path 1 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    self.main_window.menu.hdl_save_report()
            elif os.path.exists(self.ui_model.current_output_directory):
                self.ui_model.report_path = f"{os.path.join(self.ui_model.current_output_directory, self.ui_model.current_output_filename)}.json"
                print(f"report path 2 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    with open(self.ui_model.report_path, 'w') as f:
                        report = self.main_window.main_tab_view.get_fields()
                        json.dump(report, f, indent=4)

            if self.ui_model.current_input_index < len(self.ui_model.input_directories) - 1:
                self.ui_model.current_input_index += 1
                self.ui_model.current_output_index += 1
                self.ui_model.set_current_names_and_directories()
                self.main_window.update()
            else:
                result = dlg.message_dialog("End of input files", "You have reached the end of the specified eeg recordings", QMessageBox.Warning)

        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, str(e))
            print(f"Exception {e}")

    def hdl_previous_recording(self):
        """
        Used when a list of EEG recordings have been specified. Loads the previous recording and report (if exists).
        :return:
        """
        try:
            if os.path.exists(self.ui_model.report_path):
                print(f"report path 1 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    self.main_window.menu.hdl_save_report()
            elif os.path.exists(self.ui_model.current_output_directory):
                self.ui_model.report_path = f"{os.path.join(self.ui_model.current_output_directory, self.ui_model.current_output_filename)}.json"
                print(f"report path 2 {self.ui_model.report_path}")
                result = dlg.confirmation_dialog("Change Report",
                                                 f"Do you want to save changes to this report in {self.ui_model.report_path}",
                                                 QMessageBox.Warning)
                if result == 1024:
                    with open(self.ui_model.report_path, 'w') as f:
                        report = self.main_window.main_tab_view.get_fields()
                        json.dump(report, f, indent=4)
            if self.ui_model.current_input_index > 0:
                self.ui_model.current_input_index -= 1
                self.ui_model.current_output_index -= 1
                self.ui_model.set_current_names_and_directories()
                self.main_window.update()
            else:
                result = dlg.message_dialog("End of input files",
                                            "You have reached the end of the specified eeg recordings",
                                            QMessageBox.Warning)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, str(e))
            print(f"Exception {e}")

    def hdl_open_in_edfbrowser(self):
        """
        Opens the current EDF file in the external EDFBrowser application.
        TODO: Pass the current output path to EDFBrowsers arguments so that it saves the log file to the correct output location
        :return:
        """
        # C:\Program Files\EDFbrowser\edfbrowser.exe
        edfbrowser_path = os.path.join('C:\\Program Files\\EDFbrowser\\edfbrowser.exe')
        try:
            if os.path.exists(self.ui_model.current_edf_path):
                subprocess.Popen([edfbrowser_path, self.ui_model.current_edf_path])
            else:
                print(f"EDF Path {self.ui_model.current_edf_path}")
                result = dlg.message_dialog("Open in EDFBrowser", "OpenSCORE cannot find a valid EDF file. To open an EDF "
                                                                  "in EDFBroswer, either use the load EEG / load EEG "
                                                                  "sequence; or specify the path to the EDF recording in "
                                                                  "the recording conditions tab.", QMessageBox.Warning)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, str(e))
            print(e)
