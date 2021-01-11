import json
import os
from datetime import datetime

from src.models.report import Report
from src.helpers import eegreportparser as rp


class MainWindowModel:

    def __init__(self):

        self.view = None

        self.report = Report(self)

        self.report_directory = None
        self.report_file_name = None
        self.report_file_path = None

        self.edf_directory = None
        self.edf_file_name = None
        self.edf_file_path = None

        self.eeg_description_directory = None
        self.eeg_description_file_name = None
        self.eeg_description_file_path = None

        self.ui_log_directory = None
        self.ui_log_file_name = None
        self.ui_log_file_path = None

        self.eye_directory = None
        self.eye_file_name = None
        self.eye_file_path = None

        self.edf_list_directory = None
        self.edf_list_file_name = None
        self.edf_list_file_path = None

        self.input_paths = []
        self.input_idx = 0

        self.mirror_root = None
        self.output_paths = []
        self.output_idx = 0

        self.interpreter_name = None

        # TODO: Listen for changes in report and ask user if they need to save
        self.report_edited = False

    def open_report(self, file_path):
        """
        Loads a report from an existing json file
        :param file_path: string - should be an absolute path to a report.json file
        :return:
        """
        self.set_report(file_path)
        with open(self.report_file_path, 'r', encoding='utf8') as f:
            data = json.load(f)
            self.report.from_dict(data)
        if self.interpreter_name is not None:
            self.report.clinical_comments.interpreter_name = self.interpreter_name
        # if os.path.exists(self.report.recording_conditions.edf_location):
        #     self.set_edf(self.report.recording_conditions.edf_location)
        self.set_edf(self.report.recording_conditions.edf_location)
        print(self.report.recording_conditions.edf_location)

    def save_report(self):
        """
        Writes the current report to the current specified report path
        :return:
        """
        with open(self.report_file_path, 'w', encoding='utf8') as f:
            json.dump(self.report.to_dict(), f, indent=4)

    def save_report_as(self, file_path):
        """
        Fixes the current report paths then writes the report
        :param file_path: string - should be an absolute path to desired save location.
        :return:
        """
        self.report_file_path = file_path
        self.report_directory = os.path.dirname(file_path)
        self.report_file_name = os.path.basename(file_path)
        self.save_report()

    def open_edf(self, file_path):
        """
        Attempts to build a base report and link it to an edf file.
        :param file_path: string - should be an absolute path to an edf file
        :return:
        """
        try:
            self.set_edf(file_path)

            # When we open an EDF file, look for a corresponding text report which we can
            # use as a base to convert to score standard
            files = next(os.walk(self.edf_directory))[2]
            target_text_file_name = f"{self.edf_file_name.rsplit('_', 1)[0]}.txt"
            if files.count(target_text_file_name) == 1:
                self.set_text_report(os.path.join(self.edf_directory, target_text_file_name))
                self.report_from_text_description()
        except Exception as e:
            print(f"Exception {e}")

    def report_from_text_description(self):
        """Parse text descriptions (e.g. TUEG reports) and try autocomplete report"""
        with open(self.eeg_description_file_path, 'r', encoding='utf8') as f:
            text = f.read()
            stripped = rp.strip_interpretation(text)
            self.report.patient_details.history = stripped

    def open_multi_edf(self, list_path, root_location, interpreter_name=None):
        """
        Setup the model to work with a sequence of EEG recordings. We want to use some pre-specified
        paths to EDF files which we can then navigate.
        :param list_path: string - an absolute path to a txt file - which describes absolute paths to edf files.
        :param root_location: string - an absolute path to a directory - to build the mirror output directories.
        :param interpreter_name: string - the name of the eeg interpreter for the session.
        :return:
        """
        try:
            self.set_edf_list(list_path)
            self.mirror_root = os.path.normpath(root_location)
            self.interpreter_name = interpreter_name
            with open(self.edf_list_file_path, 'r') as f:
                self.input_paths = f.read().splitlines()
            # Throw away invalid paths
            for line in self.input_paths:
                if '.edf' not in line:
                    self.input_paths.remove(line)
            self.setup_mirror()
            self.open_edf(self.input_paths[0])
            self.report_directory = self.output_paths[self.output_idx]
            self.report_file_name = f"{self.edf_file_name.split('.')[0]}.score"
            self.report_file_path = os.path.join(self.report_directory, self.report_file_name)
            if os.path.exists(self.report_file_path):
                self.open_report(self.report_file_path)
            self.save_report()

        except Exception as e:
            print(f"Exception {e}")

    def setup_mirror(self):
        """
        Creates a directory structure using the current input directories in a specified location
        :return:
        """
        for entry in self.input_paths:
            # Eliminate ambiguity with different path slashes
            delim = entry.replace('/', '\\')
            delim = delim.split('\\')
            # Split at the root of the TUEG dataset
            delim = delim[delim.index('v2.0.0'):]
            # Combine specified root and mirror tail to OS friendly path
            temp_path = self.mirror_root
            for step in delim[:-1]:
                temp_path = os.path.join(temp_path, step)
            if os.path.exists(temp_path):
                pass
            else:
                os.makedirs(temp_path)
            self.output_paths.append(temp_path)

    def next_recording(self):
        if self.input_idx < len(self.input_paths)-1 and self.output_idx < len(self.output_paths)-1:
            print(f"idx {self.input_idx}")
            self.input_idx += 1
            self.output_idx += 1
            self.update_current_eeg()
        else:
            return False

    def previous_recording(self):
        if self.input_idx > 0 and self.output_idx > 0:
            print(f"idx {self.input_idx}")
            self.input_idx -= 1
            self.output_idx -= 1
            self.update_current_eeg()
        else:
            return False

    def update_current_eeg(self):
        try:
            self.save_report()
            self.report.reset()
            self.set_edf(self.input_paths[self.input_idx])
            self.report_directory = self.output_paths[self.output_idx]
            self.report_file_name = f"{self.edf_file_name.split('.')[0]}.score"
            self.report_file_path = os.path.join(self.report_directory, self.report_file_name)
            if os.path.exists(self.report_file_path):
                self.open_report(self.report_file_path)
            else:
                self.open_edf(self.input_paths[self.input_idx])
                self.save_report()
        except Exception as e:
            print(f"Exception {e}")

    def set_report(self, file_path):
        self.report_file_path = file_path
        self.report_directory = os.path.dirname(file_path)
        self.report_file_name = os.path.basename(file_path)

    def set_edf(self, file_path):
        self.edf_file_path = os.path.normpath(file_path)
        self.edf_directory = os.path.dirname(os.path.normpath(file_path))
        self.edf_file_name = os.path.basename(os.path.normpath(file_path))
        self.report.recording_conditions.edf_location = self.edf_file_path

    def set_text_report(self, file_path):
        self.eeg_description_file_path = os.path.normpath(file_path)
        self.eeg_description_directory = os.path.dirname(os.path.normpath(file_path))
        self.eeg_description_file_name = os.path.basename(os.path.normpath(file_path))

    def set_edf_list(self, file_path):
        self.edf_list_directory = os.path.dirname(os.path.normpath(file_path))
        self.edf_list_file_name = os.path.basename(file_path)
        self.edf_list_file_path = os.path.normpath(file_path)

    def set_ui_eye(self):
        now = datetime.now()
        now = now.strftime("%d-%m-%Y-%H-%M-%S")
        self.ui_log_directory = os.path.join(self.output_paths[self.output_idx], now)
        self.eye_directory = self.ui_log_directory
        os.makedirs(self.ui_log_directory)

    def reset(self):
        self.report.reset()

        self.report_directory = None
        self.report_file_name = None
        self.report_file_path = None

        self.edf_directory = None
        self.edf_file_name = None
        self.edf_file_path = None

        self.eeg_description_directory = None
        self.eeg_description_file_name = None
        self.eeg_description_file_path = None

        self.ui_log_directory = None
        self.ui_log_file_name = None
        self.ui_log_file_path = None

        self.eye_directory = None
        self.eye_file_name = None
        self.eye_file_path = None

        self.edf_list_directory = None
        self.edf_list_file_name = None
        self.edf_list_file_path = None

        self.input_paths = []
        self.input_idx = 0

        self.mirror_root = None
        self.output_paths = []
        self.output_idx = 0

        self.interpreter_name = None
