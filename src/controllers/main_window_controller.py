from datetime import datetime
import os
import subprocess
import traceback

import psutil
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import tobii_research as tr

from src.dialogs.load_multi import StartSessionDialog
from src.models.main_model import MainModel
from src.views.main_window import MainWindow

from helpers import eyetracker as eye


class MainWindowController:

    def __init__(self):
        """
        MainWindowController is basically the main/root container/class which holds the whole application.
        """
        # Connecting the model to the controller
        self.model = MainModel()

        # Connecting the view to the controller
        self.view = MainWindow(self.model)
        self.view.menu.bt_new_report.triggered.connect(self.hdl_new_report)
        self.view.menu.bt_open_file.triggered.connect(self.hdl_open_report)
        self.view.menu.bt_save_file.triggered.connect(self.hdl_save_report)
        self.view.menu.bt_save_as_file.triggered.connect(self.hdl_save_report_as)
        self.view.menu.bt_load_single_eeg.triggered.connect(self.hdl_load_edf)
        self.view.menu.bt_eeg_sequence.triggered.connect(self.hdl_load_edf_multi)

        self.view.toolbar.btn_previous_recording.triggered.connect(self.hdl_previous_recording)
        self.view.toolbar.btn_next_recording.triggered.connect(self.hdl_next_recording)
        self.view.toolbar.btn_open_in_edfbrowser.triggered.connect(self.hdl_open_in_edfbrowser)
        # self.view.toolbar.btn_eye_tracker_manager.triggered.connect(self.hdl_call_calibrator)

        self.view.tobii_toolbar.btn_start_analysis.triggered.connect(self.hdl_record_gaze)
        self.view.tobii_toolbar.btn_stop_analysis.triggered.connect(self.hdl_stop_gaze)
        self.view.tobii_toolbar.btn_eye_tracker_manager.triggered.connect(self.hdl_call_calibrator)


        self.view.recording_conditions.btn_edf_location.clicked.connect(self.hdl_edf_location_bt_press)

        self.edfbrowser_p = None
        found_eyetrackers = tr.find_all_eyetrackers()
        self.eyetracker = found_eyetrackers[0]

    def hdl_new_report(self):
        """
        Action when user clicks New Report in the Menu. Tell the user to save their changes -
        (TO DO: only ask if the user has made changes) - Then reset the model
        :return: No return
        """
        try:
            dialog = QMessageBox()
            dialog.setWindowTitle("New Score Report")
            dialog.setText("You will lose any changes you haven't saved. Do you want to create a new report?")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dialog.setIcon(QMessageBox.Question)
            answer = dialog.exec_()
            if answer == QMessageBox.Yes:
                self.model.reset()
                self.view.setWindowTitle(f"OpenSCORE - {self.model.report_file_name}")
                self.update_view_from_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_open_report(self):
        """
        Action when user clicks Open Report. Loads a pre-existing score report from a json file.
        TODO: Only ask user if they have saved their changes, if a change has been made.
        :return: No return
        """
        try:
            dialog = QMessageBox()
            dialog.setWindowTitle("Open Score Report")
            dialog.setText("You will lose any changes you haven't saved. Do you want to open an existing report?")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dialog.setIcon(QMessageBox.Question)
            answer = dialog.exec_()
            if answer == QMessageBox.Yes:
                dialog = QFileDialog()
                dialog.setDefaultSuffix('json')
                file_path, _ = dialog.getOpenFileName(caption="Open SCORE Report", filter="JSON Files (*.json)")
                if file_path:
                    self.model.open_report(file_path)
                    self.update_view_from_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_save_report(self):
        """
        Action when user clicks Save. If there is a path to a report then save it, otherwise
        will need to use Save As to give user File Dialog for path
        :return: No return
        """
        try:
            if self.model.report_directory is None or self.model.report_file_name is None or self.model.report_file_path is None:
                self.hdl_save_report_as()
            else:
                self.update_model_from_view()
                self.model.save_report()
                self.view.setWindowTitle(f"OpenSCORE - {self.model.report_file_name}")
        except Exception as e:
            traceback.print_exc()

    def hdl_save_report_as(self):
        """
        Action when user wants to save but we don't have a path to save the report to. Calls a
        save file dialog for the user to specify a path.
        :return: No return
        """
        try:
            dialog = QFileDialog()
            dialog.setDefaultSuffix('.json')
            file_path, _ = dialog.getSaveFileName(caption="Save Report", filter="JSON Files (*.json)")
            if file_path:
                self.update_model_from_view()
                self.model.save_report_as(file_path)
                self.view.setWindowTitle(f"OpenSCORE - {self.model.report_file_name}")
        except Exception as e:
            traceback.print_exc()

    def hdl_load_edf(self):
        """
        Action when user clicks Load EDF. Use this to link and generate a base report from an
        edf file.
        :return:
        """
        try:
            dialog = QMessageBox()
            dialog.setWindowTitle("Load from EDF")
            dialog.setText("You will lose any changes you haven't saved. Do you want to create a new report?")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dialog.setIcon(QMessageBox.Question)
            answer = dialog.exec_()
            if answer == QMessageBox.Yes:
                dialog = QFileDialog()
                dialog.setDefaultSuffix('edf')
                file_path, _ = dialog.getOpenFileName(caption="Create report from EDF", filter="EDF Files (*.edf)")
                if file_path:
                    self.model.reset()
                    self.update_view_from_model()
                    self.model.open_edf(file_path)
                    self.update_view_from_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_load_edf_multi(self):
        """
        This function is tightly coupled with requirements for TEETACSI. Although, the basic idea
        is pre-specify a set of paths to EDF files, and then have the option to navigate through
        the list as required. Some issues here include:
         - Should there be an option to make a separate mirror directory? Or should it be fixed?
         - When creating the mirror directory, should we generate the report files then? Or only
            after they have been edited?
         - Should the user be forced to specify where to save each report? Should they have the option?
            or should it just be done automatic to the mirror directory?
        Anyway... At the moment, it will load the list of specified EDFs, create a mirror output
        directory structure, load the list of output directories, load the first report and save the first
        report.
        :return:
        """
        try:
            print("Loading multiple EDFs")
            dialog = QMessageBox()
            dialog.setWindowTitle("Load multiple EDFs")
            dialog.setText("You will lose any changes you haven't saved. Do you want to continue?")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dialog.setIcon(QMessageBox.Question)
            answer = dialog.exec_()
            if answer == QMessageBox.Yes:
                dialog = StartSessionDialog()
                if dialog.exec_():
                    self.model.open_multi_edf(dialog.txe_specified_paths.text(), dialog.txe_root_output_directory.text(), dialog.txe_interpreter_name.text())
                    self.update_view_from_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_previous_recording(self):
        """
        Called when the "Previous" button is pressed on the toolbar. Idea is to save the current report,
        then move to the next one in the list. It should either generate a base report from the edf
        and description, or load the existing json report - if it exists.
        :return:
        """
        try:
            self.update_model_from_view()
            if len(self.model.input_paths) == 0:
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("There are no EEG's to navigate.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif self.model.previous_recording() is False:
                print("At the beginning of the list")
                if len(self.model.input_paths) == 0:
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Previous recording")
                    dialog.setText("You are at the beginning of the list. You can specify a sequence of EEGs using the load sequence option in the menu.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    answer = dialog.exec_()
            else:
                self.update_view_from_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_next_recording(self):
        """
        Called when the "Next" button is pressed on the toolbar. Idea is to save the current report,
        then move to the next one in the list. It should either generate a base report from the edf
        and description, or load the existing json report - if it exists.
        :return:
        """
        try:
            self.update_model_from_view()
            if len(self.model.input_paths) == 0:
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("There are no EEG's to navigate. You can specify a sequence of EEGs using the load sequence option in the menu.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif self.model.next_recording() is False:
                print("At the end of the list")
                if len(self.model.input_paths) == 0:
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Previous recording")
                    dialog.setText("You are at the end of the list.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    answer = dialog.exec_()
            else:
                self.update_view_from_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_open_in_edfbrowser(self):
        """
        Opens the current specified edf file in the edfbrowser program. If we are in multi-eeg mode then
        EDFBrowser will start writing a UI log to the output directory.
        :return:
        """
        edfbrowser_path = os.path.join(os.getcwd(), 'release', 'edfbrowser.exe')
        if not os.path.exists(edfbrowser_path):
            dialog = QMessageBox()
            dialog.setWindowTitle("Open in EDFBrowser")
            dialog.setText("EDFBrowser has not been installed in the OpenSCORE directory")
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Information)
            answer = dialog.exec_()
            return False
        #edfbrowser_path = os.path.join('E:\\computer_science\\living_lab\\2020TEETACSI\\Analyzer\\REDFBrowser\\build-edfbrowser-Desktop_Qt_5_14_2_MinGW_64_bit-Release\\release\\edfbrowser.exe')
        try:
            if not self.edfbrowser_is_open():
                if self.model.edf_file_path is not None and os.path.exists(self.model.edf_file_path):
                    if len(self.model.output_paths) > 0 and os.path.exists(self.model.output_paths[self.model.output_idx]):
                        self.edfbrowser_p = subprocess.Popen([edfbrowser_path, self.model.edf_file_path, self.model.output_paths[self.model.output_idx]])
                    else:
                        self.edfbrowser_p = subprocess.Popen([edfbrowser_path, self.model.edf_file_path])
                else:
                    print(f"EDF Path {self.model.edf_file_path}")
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Open in EDFBrowser")
                    dialog.setText("OpenSCORE cannot find a valid EDF file. You can specify the location of an EDF in the recording conditions tab.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    answer = dialog.exec_()
            else:
                dialog = QMessageBox()
                dialog.setWindowTitle("Open in EDFBrowser")
                dialog.setText("You need to close the current EDFBrowser before opening a new one.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
        except Exception as e:
            traceback.print_exc()

    def edfbrowser_is_open(self):
        """
        Check if edfbrowser is running. Ideally we only want 1 instance at a time and the user
        should close the browser each time to keep logs consistent.
        :return:
        """
        if self.edfbrowser_p is None:
            return False
        else:
            return psutil.pid_exists(self.edfbrowser_p.pid)

    #TODO: Move to separate controller for recording conditions
    def hdl_edf_location_bt_press(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(caption="Select associated recording", filter="EDF files (*.edf)")
            if file_path:
                self.view.recording_conditions.lne_edf_location.setText(file_path)
                self.model.set_edf(file_path)
                self.update_view_from_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_call_calibrator(self):
        eye.call_calibrator(self.eyetracker)

    def hdl_record_gaze(self):
        try:
            if self.edfbrowser_is_open() is False:
                dialog = QMessageBox()
                dialog.setWindowTitle("Record Gaze")
                dialog.setText("Please open the eeg in EDFBrowser before recording gaze data.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            else:
                if len(self.model.output_paths) > 0:
                    gaze_path = os.path.join(self.model.output_paths[self.model.output_idx], 'gaze_data.txt')
                else:
                    gaze_path = os.path.join(os.getcwd(), 'data', 'gaze_recordings')
                    if not os.path.exists(gaze_path):
                        os.makedirs(gaze_path)
                    now = datetime.now()
                    now = now.strftime("%d-%m-%Y-%H-%M-%S")
                    gaze_path = os.path.join(gaze_path, f"{now}.txt")
                eye.gaze_file = open(gaze_path, 'w')
                self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, eye.gaze_data_callback, as_dictionary=True)
        except Exception as e:
            traceback.print_exc()

    def hdl_stop_gaze(self):
        self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, eye.gaze_data_callback)
        eye.gaze_file.close()

    def update_model_from_view(self):
        self.model.report.patient_details.update_from_dict(self.view.patient_details.to_dict())
        self.model.report.patient_referral.update_from_dict(self.view.patient_referral.to_dict())
        self.model.report.recording_conditions.update_from_dict(self.view.recording_conditions.to_dict())

    def update_view_from_model(self):
        self.view.setWindowTitle(f"OpenSCORE - {self.model.report_file_name}")
        self.view.toolbar.lbl_current_eeg_name.setText(self.model.edf_file_name.split('.')[0])
        self.view.patient_details.update_from_dict(self.model.report.patient_details.to_dict())
        self.view.patient_referral.update_from_dict(self.model.report.patient_referral.to_dict())
        self.view.recording_conditions.update_from_dict(self.model.report.recording_conditions.to_dict())

