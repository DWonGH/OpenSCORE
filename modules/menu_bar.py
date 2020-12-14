import json
import os

from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QDialog, QMessageBox

from modules.start_session_dialog import StartSessionDialog
import modules.standard_dialogs as dlg
#from modules.main_window import MainWindow
from modules.ui_state import UiModel


class MainMenuBar(QMenuBar):

    def __init__(self, main_window):
        """
        Options for opening/ closing files
        :param main_window:
        :param ui_model:
        """
        super().__init__(main_window)

        self.main_window = main_window
        self.ui_model = self.main_window.ui_model

        self.dialog = QFileDialog()

        self.file_menu = self.addMenu("&File")

        self.bt_new_report = QAction("&New", self)
        self.bt_new_report.setStatusTip("New report")
        self.bt_new_report.triggered.connect(self.hdl_new_report)
        self.file_menu.addAction(self.bt_new_report)

        self.bt_open_file = QAction("&Open", self)
        self.bt_open_file.setStatusTip("Open existing report")
        self.bt_open_file.triggered.connect(self.hdl_open_report)
        self.file_menu.addAction(self.bt_open_file)

        self.bt_save_file = QAction("&Save", self)
        self.bt_save_file.setStatusTip("Save to current file")
        self.bt_save_file.triggered.connect(self.hdl_save_report)
        self.file_menu.addAction(self.bt_save_file)

        self.bt_save_as_file = QAction("&Save as", self)
        self.bt_save_as_file.setStatusTip("Save to new file")
        self.bt_save_as_file.triggered.connect(self.hdl_save_report_as)
        self.file_menu.addAction(self.bt_save_file)

        self.bt_load_single_eeg = QAction("&Load EEG", self)
        self.bt_load_single_eeg.setStatusTip("Load a directory containing an EDF (and txt file)")
        self.bt_load_single_eeg.triggered.connect(self.hdl_load_edf_directory)
        self.file_menu.addAction(self.bt_load_single_eeg)

        self.bt_eeg_sequence = QAction("&Load EEG sequence", self)
        self.bt_eeg_sequence.setStatusTip("Load a set of paths to directories containing EDF's")
        self.bt_eeg_sequence.triggered.connect(self.hdl_new_session)
        self.file_menu.addAction(self.bt_eeg_sequence)

        self.bt_close_window = QAction("&Close", self)
        self.bt_close_window.setStatusTip("Exit OpenScore")
        # bt_close_window.triggered.connect(self.close())
        self.file_menu.addAction(self.bt_close_window)

    def hdl_new_report(self):
        """
        Clears the viewer and input data
        :return:
        """
        result = dlg.confirmation_dialog("Save", "Unsaved progress will be lost, do you want to continue?", QMessageBox.Warning)
        if result == 1024:
            self.main_window.clear()
            self.ui_model.clear_session()
            self.main_window.toolbar.lbl_current_eeg_name.setText("")

    def hdl_save_report(self):
        """
        Saves the current score report to the current report file. If there is no report file specified show the user
        a file browser dialog to choose.
        :return:
        """
        try:
            score = self.main_window.main_tab_view.get_fields()
            print(score)
            if os.path.exists(self.ui_model.report_path):
                with open(self.ui_model.report_path, 'w') as f:
                    json.dump(score, f, indent=4)
            else:
                self.hdl_save_report_as()
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(e)

    def hdl_save_report_as(self):
        """
        Ask the user for a location to save the current report
        :return:
        """
        try:
            self.dialog.setDefaultSuffix('json')
            # self.dialog.setModal(True)
            # self.dialog
            save_file, _ = self.dialog.getSaveFileName(caption="Save Report", filter="JSON Files (*.json)")
            if save_file:
                score = self.main_window.main_tab_view.get_fields()
                print(score)
                self.ui_model.report_path = save_file
                with open(save_file, 'w') as f:
                    json.dump(score, f, indent=4)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(e)

    def hdl_open_report(self):
        """
        Loads a json report from file and populates the input fields with the information
        :return:
        """
        try:
            dialog = QFileDialog()
            dialog.setDefaultSuffix('json')
            open_file, _ = dialog.getOpenFileName(caption="Open SCORE Report", filter="JSON Files (*.json)")
            if open_file:
                with open(open_file, 'r') as f:
                    report = json.load(f)
                    self.main_window.main_tab_view.set_fields(report)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(f"Exception {e}")

    def hdl_load_edf_directory(self):
        """
        Ask the user to find a directory where an EDF is located. If the directory contains
        a txt file then it will try and load information from that into the score report
        :return:
        """
        try:
            browse_dir = QFileDialog.getExistingDirectory(self, caption="Select Directory", options=QFileDialog.ShowDirsOnly)
            if browse_dir:
                print(f"browse directory {browse_dir}")
                self.ui_model.current_input_directory = browse_dir
                self.ui_model.update_load_eeg(browse_dir)
                self.main_window.update()
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(f"Exception choosing the input directory {e}")

    def hdl_new_session(self):
        """
        Prepares a user to analyze multiple EEG recordings. The user must specify a set of paths
        in a txt file to each of the directories containing the required EDFs. The user
        will then be able to move between the files using the "previous" and "next" buttons
        :return:
        """
        try:
            dialog = StartSessionDialog(self)
            if dialog.exec_():
                # Load the input directories
                self.ui_model.input_directories_path_file = dialog.txe_specified_paths.text()
                with open(self.ui_model.input_directories_path_file, 'r') as f:
                    self.ui_model.input_directories = f.read().splitlines()
                self.ui_model.current_input_index = 0

                # Setup the output directories
                self.ui_model.root_output_directory = dialog.txe_root_output_directory.text()
                self.ui_model.setup_output_directories()
                self.ui_model.current_output_index = 0

                # Update the current working file names and directories
                self.ui_model.set_current_names_and_directories()
                self.ui_model.interpreter_name = dialog.txe_interpreter_name.text()

                # Update the UI with the new file names and directories
                self.main_window.update()
            else:
                print("It didnt work :(")
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, e)
            print(f"Exception starting a new analysis session {e}")


