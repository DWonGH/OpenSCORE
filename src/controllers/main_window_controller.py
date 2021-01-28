import json
from datetime import datetime
import os
import subprocess
import traceback

import psutil
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTabWidget
import tobii_research as tr

from src.controllers.background_activity_controller import BackgroundActivityController
from src.controllers.clinical_comments_controller import ClinicalCommentsController
from src.controllers.diagnostic_significance_controller import DiagnosticSignificanceController
from src.controllers.patient_details_controller import PatientDetailsController
from src.controllers.patient_referral_controller import PatientReferralController
from src.controllers.recording_conditions_controller import RecordingConditionsController
from src.dialogs.load_multi import StartSessionDialog
from src.models.main_window_model import MainWindowModel
from src.views.main_window import MainWindow

from src.helpers import eyetracker as eye


class MainWindowController:

    def __init__(self):
        """
        MainWindowController is basically the main/root container/class which holds the whole application.
        """

        # Initialise secondary controllers
        self.patient_details_controller = PatientDetailsController()
        self.patient_referral_controller = PatientReferralController()
        self.recording_conditions_controller = RecordingConditionsController(self)
        self.background_activity_controller = BackgroundActivityController()
        self.diagnostic_significance_controller = DiagnosticSignificanceController()
        self.clinical_comments_controller = ClinicalCommentsController()

        # Connecting the models
        self.model = MainWindowModel()
        self.model.report.patient_details = self.patient_details_controller.model
        self.model.report.patient_referral = self.patient_referral_controller.model
        self.model.report.recording_conditions = self.recording_conditions_controller.model
        self.model.report.background_activity = self.background_activity_controller.model
        self.model.report.diagnostic_significance = self.diagnostic_significance_controller.model
        self.model.report.clinical_comments = self.clinical_comments_controller.model

        # Connecting the main window view
        self.view = MainWindow(self.model)
        self.view.menu.bt_new_report.triggered.connect(self.hdl_new_report)
        self.view.menu.bt_open_file.triggered.connect(self.hdl_open_report)
        self.view.menu.bt_save_file.triggered.connect(self.hdl_save_report)
        self.view.menu.bt_save_as_file.triggered.connect(self.hdl_save_report_as)
        self.view.menu.bt_load_single_eeg.triggered.connect(self.hdl_load_edf)
        # self.view.menu.bt_eeg_sequence.triggered.connect(self.hdl_load_edf_multi)

        # self.view.toolbar.btn_previous_recording.triggered.connect(self.hdl_previous_recording)
        # self.view.toolbar.btn_next_recording.triggered.connect(self.hdl_next_recording)
        # self.view.toolbar.btn_open_in_edfbrowser.triggered.connect(self.hdl_open_in_edfbrowser)

        # self.view.tobii_toolbar.btn_start_analysis.triggered.connect(self.hdl_record_gaze)
        # self.view.tobii_toolbar.btn_stop_analysis.triggered.connect(self.hdl_stop_gaze)
        # self.view.tobii_toolbar.btn_eye_tracker_manager.triggered.connect(self.hdl_call_calibrator)

        # Connecting the widgets to the tab system
        self.patient_info_tab = QTabWidget()
        self.patient_info_tab.addTab(self.patient_details_controller.view, "Patient Details")
        self.patient_info_tab.addTab(self.patient_referral_controller.view, "Patient Referral")
        self.view.tabs.addTab(self.patient_info_tab, "Patient Info")
        self.view.tabs.addTab(self.recording_conditions_controller.view, "Recording Conditions")
        self.findings_tab = QTabWidget()
        self.findings_tab.addTab(self.background_activity_controller.view, "Background Activity")
        self.view.tabs.addTab(self.findings_tab, "Findings")
        self.view.tabs.addTab(self.diagnostic_significance_controller.view, "Diagnostic Significance")
        self.view.tabs.addTab(self.clinical_comments_controller.view, "Clinical Comments")

        self.edfbrowser_path = os.path.join(os.getcwd(), 'edfbrowser', 'edfbrowser.exe')
        if not os.path.exists(self.edfbrowser_path):
            print(f"EDFBrowser is not installed")
        self.edfbrowser_p = None
        self.eyetracker = None
        try:
            found_eyetrackers = tr.find_all_eyetrackers()
            self.eyetracker = found_eyetrackers[0]
        except IndexError as e:
            print("No eye trackers were found")

        #self.view..connect(self.hdl_close_event)

    def hdl_new_report(self):
        """
        Action when user clicks New Report in the Menu. Tell the user to save their changes -
        (TO DO: only ask if the user has made changes) - Then reset the model
        :return: No return
        """
        try:
            dialog = QMessageBox()
            dialog.setWindowTitle("New Score Report")
            dialog.setText("You will lose any changes you haven't saved. Do you want to open a new report?")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dialog.setIcon(QMessageBox.Question)
            answer = dialog.exec_()
            if answer == QMessageBox.Yes:
                if self.edfbrowser_is_open():
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Previous recording")
                    dialog.setText("Please close the current EDFBrowser before clicking previous.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    answer = dialog.exec_()
                else:
                    self.model.reset()
                    self.view.setWindowTitle(f"OpenSCORE - {self.model.report_file_name}")
                    self.view.toolbar.lbl_current_eeg_name.setText("")
                    self.update_view_from_model()
        except Exception as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("New Score Report")
            dialog.setText(
                f"Something went wrong making a new report.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
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
                if self.edfbrowser_is_open():
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Previous recording")
                    dialog.setText("Please close the current EDFBrowser before clicking previous.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    answer = dialog.exec_()
                else:
                    dialog = QFileDialog()
                    dialog.setDefaultSuffix('score')
                    file_path, _ = dialog.getOpenFileName(caption="Open SCORE Report", filter="SCORE Files (*.score)")
                    if file_path:
                        self.model.reset()
                        self.model.open_report(file_path)
                        self.update_view_from_model()
        except KeyError as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Open Score Report")
            dialog.setText(f"The file is not a valid OpenSCORE report. There was a key error when loading: {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
        except json.decoder.JSONDecodeError as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Open Score Report")
            dialog.setText(f"The file is not a valid OpenSCORE report. \n\nIt might be incorrectly formatted or is incompatible.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
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
            dialog = QMessageBox()
            dialog.setWindowTitle("Save Score Report")
            dialog.setText(
                f"Something went wrong saving the report.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
            traceback.print_exc()

    def hdl_save_report_as(self):
        """
        Action when user wants to save but we don't have a path to save the report to. Calls a
        save file dialog for the user to specify a path.
        :return: No return
        """
        try:
            dialog = QFileDialog()
            dialog.setDefaultSuffix('.score')
            file_path, _ = dialog.getSaveFileName(caption="Save Report", filter="SCORE Files (*.score)")
            if file_path:
                self.update_model_from_view()
                result = self.model.save_report_as(file_path)
                self.view.setWindowTitle(f"OpenSCORE - {self.model.report_file_name}")
        except Exception as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Save Score Report As")
            dialog.setText(
                f"Something went wrong saving the report.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
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
                if self.edfbrowser_is_open():
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Previous recording")
                    dialog.setText("Please close the current EDFBrowser before clicking previous.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    answer = dialog.exec_()
                else:
                    dialog = QFileDialog()
                    dialog.setDefaultSuffix('edf')
                    file_path, _ = dialog.getOpenFileName(caption="Create report from EDF", filter="EDF Files (*.edf)")
                    if file_path:
                        self.model.reset()
                        self.update_view_from_model()
                        self.model.open_edf(file_path)
                        self.update_view_from_model()
        except Exception as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Open Report from EDF")
            dialog.setText(
                f"Something went wrong trying to build a new report from the EDF an text file.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
            traceback.print_exc()

    def hdl_load_edf_multi(self):
        """
        Will load a list of paths to edf recordings according to a pre-defined text file (see the specified_paths.txt
        file in the data folder for an example). Can then use the next/back buttons to navigate the edf recordings and
        reports.
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
                if self.edfbrowser_is_open():
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Previous recording")
                    dialog.setText("Please close the current EDFBrowser before continuing.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    answer = dialog.exec_()
                else:
                    dialog = StartSessionDialog()
                    if dialog.exec_():
                        self.model.reset()
                        self.model.open_multi_edf(dialog.lne_specified_paths.text(), dialog.lne_root_output_directory.text(), dialog.lne_interpreter_name.text())
                        self.update_view_from_model()
        except Exception as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Open EEG Sequence")
            dialog.setText(
                f"Something went wrong starting a new session.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
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
                dialog.setText("There are no EEG's to navigate. You can specify a sequence of EEGs using the load sequence option in the menu.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif self.edfbrowser_is_open():
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("Please close the current EDFBrowser before clicking previous.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif eye.gaze_file is not None:
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("Please stop the eye tracker before continuing.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif self.model.previous_recording() is False:
                print("At the beginning of the list")
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("You are at the beginning of the list.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            else:
                self.update_view_from_model()
        except Exception as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Previous EEG")
            dialog.setText(
                f"Something went wrong navigating to the next report.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
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
            elif self.edfbrowser_is_open():
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("Please close the current EDFBrowser before clicking next.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif eye.gaze_file is not None:
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("Please stop the eye tracker before continuing.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif self.model.next_recording() is False:
                print("At the end of the list")
                dialog = QMessageBox()
                dialog.setWindowTitle("Previous recording")
                dialog.setText("You are at the end of the list.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            else:
                self.update_view_from_model()
        except Exception as e:
            dialog = QMessageBox()
            dialog.setWindowTitle("Next EEG")
            dialog.setText(
                f"Something went wrong navigating to the next report.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
            traceback.print_exc()

    def hdl_open_in_edfbrowser(self):
        """
        Opens the current specified edf file in the edfbrowser program. If we are in multi-eeg mode then
        EDFBrowser will start writing a UI log to the output directory.
        :return:
        """
        if not os.path.exists(self.edfbrowser_path):
            dialog = QMessageBox()
            dialog.setWindowTitle("Open in EDFBrowser")
            dialog.setText("EDFBrowser has not been installed in the OpenSCORE directory")
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Information)
            answer = dialog.exec_()
            return False
        try:
            if not self.edfbrowser_is_open():
                if self.model.edf_file_path is not None and os.path.exists(self.model.edf_file_path):
                    if len(self.model.output_paths) > 0 and os.path.exists(self.model.output_paths[self.model.output_idx]):
                        self.model.set_ui_eye()
                        self.edfbrowser_p = subprocess.Popen([self.edfbrowser_path, os.path.normpath(self.model.edf_file_path), self.model.ui_log_directory])
                    else:
                        self.edfbrowser_p = subprocess.Popen([self.edfbrowser_path, os.path.normpath(self.model.edf_file_path)])
                elif self.model.report.recording_conditions.edf_location is not None and os.path.exists(self.model.report.recording_conditions.edf_location):
                    self.model.set_edf(self.model.report.recording_conditions.edf_location)
                    if len(self.model.output_paths) > 0 and os.path.exists(self.model.output_paths[self.model.output_idx]):
                        self.model.set_ui_eye()
                        self.edfbrowser_p = subprocess.Popen([self.edfbrowser_path, os.path.normpath(self.model.edf_file_path), self.model.ui_log_directory])
                    else:
                        self.edfbrowser_p = subprocess.Popen([self.edfbrowser_path, os.path.normpath(self.model.edf_file_path)])
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
            dialog = QMessageBox()
            dialog.setWindowTitle("Open in EDFBrowser")
            dialog.setText(
                f"There was a problem opening the file in EDFBrowser.\n\n {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
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

    def hdl_call_calibrator(self):
        if self.eyetracker is None:
            dialog = QMessageBox()
            dialog.setWindowTitle("Eye Tracker Manager")
            dialog.setText("The eye tracker is not connected.")
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Information)
            answer = dialog.exec_()
        else:
            eye.call_calibrator(self.eyetracker)

    def hdl_record_gaze(self):
        try:
            if len(self.model.output_paths) == 0:
                dialog = QMessageBox()
                dialog.setWindowTitle("Record Gaze")
                dialog.setText("This feature is only available in EEG Sequence mode.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            elif self.edfbrowser_is_open() is False:
                dialog = QMessageBox()
                dialog.setWindowTitle("Record Gaze")
                dialog.setText("Please open the eeg in EDFBrowser before recording gaze data.")
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.setIcon(QMessageBox.Information)
                answer = dialog.exec_()
            else:
                if len(self.model.output_paths) > 0:
                    if self.model.ui_log_directory is not None:
                        gaze_path = os.path.join(self.model.ui_log_directory, 'gaze_data.txt')
                        eye.gaze_file = open(gaze_path, 'w')
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
            dialog = QMessageBox()
            dialog.setWindowTitle("Open Score Report")
            dialog.setText(
                f"There was a problem recording the eye tracker.\n\n Is it connected? \n\n Is the ete tracker manager installed? {e}")
            dialog.setDetailedText(traceback.format_exc())
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
            traceback.print_exc()

    def hdl_stop_gaze(self):
        if eye.gaze_file is not None:
            self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, eye.gaze_data_callback)
            eye.gaze_file.close()
            eye.gaze_file = None
        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Record Gaze")
            dialog.setText("You need to start recording gaze data first.")
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Information)
            answer = dialog.exec_()

    def update_model_from_view(self):
        self.patient_details_controller.update_model()
        self.patient_referral_controller.update_model()
        self.recording_conditions_controller.update_model()
        self.background_activity_controller.update_model()
        self.diagnostic_significance_controller.update_model()
        self.clinical_comments_controller.update_model()

    def update_view_from_model(self):
        self.view.setWindowTitle(f"OpenSCORE - {self.model.report_file_name}")
        if self.model.edf_file_name is not None:
            self.view.toolbar.lbl_current_eeg_name.setText(self.model.edf_file_name.split('.')[0])
        self.patient_details_controller.update_view()
        self.patient_referral_controller.update_view()
        self.recording_conditions_controller.update_view()
        self.background_activity_controller.update_view()
        self.diagnostic_significance_controller.update_view()
        self.clinical_comments_controller.update_view()

    def hdl_close_event(self):
        print("Closed OpenSCORE")
