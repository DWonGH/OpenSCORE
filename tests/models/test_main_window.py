import json
import os
import unittest
import shutil
from src.models.main_window_model import MainWindowModel
from src.models.report import Report
from src.helpers import eegreportparser as rp


class TestMainModel(unittest.TestCase):

    def setUp(self) -> None:
        self.model = MainWindowModel()

    def test_init(self):
        self.assertIsNone(self.model.view)
        self.assert_paths_are_nones()
        self.assertFalse(self.model.report_edited)

    def test_reset(self):
        self.assert_report_is_blank()
        self.assert_paths_are_nones()
        self.set_paths_to_ones()
        self.assert_paths_not_nones()
        test_report = os.path.join(os.getcwd(), 'data', 'test_report.score')
        self.maxDiff = True
        with open(test_report, 'r', encoding='utf8') as f:
            test_report_dict = json.load(f)
        self.model.open_report(test_report)
        self.assert_report_not_blank()
        self.maxDiff = None
        self.assertEqual(self.model.report.to_dict(), test_report_dict)
        self.model.reset()
        self.assert_report_is_blank()
        self.assert_paths_are_nones()

    def test_save_report(self):
        dummy = os.path.join(os.getcwd(), 'data', 'dummy.score')
        self.model.set_report(dummy)
        self.assertIsNotNone(self.model.report_file_path)
        self.assertEqual(self.model.report_file_path, dummy)
        self.assertFalse(os.path.exists(dummy))
        self.model.save_report()
        self.assertTrue(os.path.exists(dummy))
        with open(dummy, 'r', encoding='utf8') as f:
            dummy_dict = json.load(f)
        self.assertEqual(self.model.report.to_dict(), dummy_dict)
        os.remove(self.model.report_file_path)
        self.assertFalse(os.path.exists(dummy))

    def test_save_report_as(self):
        self.assert_report_is_blank()
        self.assert_paths_are_nones()
        dummy = os.path.join(os.getcwd(), 'data', 'dummy.score')
        if os.path.exists(dummy):
            os.remove(dummy)
        self.assertFalse(os.path.exists(dummy))
        self.assert_paths_are_nones()
        self.model.save_report_as(dummy)
        self.assertEqual(self.model.report_directory, os.path.dirname(dummy))
        self.assertEqual(self.model.report_file_name, os.path.basename(dummy))
        self.assertEqual(self.model.report_file_path, dummy)
        with open(dummy, 'r', encoding='utf8') as f:
            dummy_dict = json.load(f)
        self.assertEqual(self.model.report.to_dict(), dummy_dict)
        os.remove(self.model.report_file_path)
        self.assertFalse(os.path.exists(dummy))

    def test_open_report(self):
        self.assert_report_is_blank()
        self.assert_paths_are_nones()
        test_report = os.path.join(os.getcwd(), 'data', 'test_report.score')
        self.assertTrue(os.path.exists(test_report))
        # Adjust the file for the test - we want to test we can set edf path correctly
        with open(test_report, 'r', encoding='utf8') as f:
            report = json.load(f)
            report["Recording conditions"]["EDF location"] = os.path.join(os.getcwd(), 'data', 'eeg_sample', '00000768_s003_t000.edf')
        with open(test_report, 'w', encoding='utf8') as f:
            json.dump(report, f, indent=4)
        self.model.open_report(test_report)
        self.assert_report_paths_not_none()
        self.assert_edf_paths_not_none()
        self.assert_report_not_blank()
        self.assertEqual(self.model.report_directory, os.path.join(os.getcwd(), 'data'))
        self.assertEqual(self.model.report_file_name, 'test_report.score')
        self.assertTrue(os.path.exists(self.model.report_file_path))
        self.assertEqual(self.model.edf_file_path, os.path.join(os.getcwd(), 'data', 'eeg_sample', '00000768_s003_t000.edf'))
        self.maxDiff = None
        # Reset the file
        with open(self.model.report_file_path, 'r', encoding='utf8') as f:
            report = json.load(f)
            self.assertEqual(report, self.model.report.to_dict())
        report["Recording conditions"]["EDF location"] = "1"
        with open(test_report, 'w', encoding='utf8') as f:
            json.dump(report, f, indent=4)

    def test_open_edf(self):
        self.assert_report_is_blank()
        self.assert_paths_are_nones()
        self.assertIsNone(self.model.report.recording_conditions.edf_location)
        self.assertIsNone(self.model.report.patient_details.history)
        test_edf = os.path.join(os.getcwd(), 'data', 'eeg_sample', '00000768_s003_t000.edf')
        self.assertTrue(os.path.exists(test_edf))
        self.model.open_edf(test_edf)
        self.assert_edf_paths_not_none()
        self.assert_edf_text_not_none()
        self.assertEqual(self.model.edf_file_path, test_edf)
        self.assertIsNotNone(self.model.report.recording_conditions.edf_location)
        self.assertEqual(self.model.report.recording_conditions.edf_location, test_edf)
        self.assertIsNotNone(self.model.report.patient_details.history)

    def assert_mirror_directory(self):
        pass

    def open_multi_edf(self, clean=None):
        self.num_paths = 1
        self.assert_paths_are_nones()
        self.assert_report_is_blank()

        # Create a test output directory
        root_directory = os.path.join(os.getcwd(), 'data', 'dummy_root')
        print(root_directory)
        if os.path.exists(root_directory):
            shutil.rmtree(root_directory)
        self.assertFalse(os.path.exists(root_directory))
        os.makedirs(root_directory)
        self.assertTrue(os.path.exists(root_directory))
        self.assertTrue(len(os.listdir(root_directory)) == 0)

        # Use a test paths file
        paths_file = os.path.join(os.getcwd(), 'data', 'specified_paths.txt')
        self.assertTrue(os.path.exists(paths_file))

        # Call the open multi method
        self.model.open_multi_edf(paths_file, root_directory, "Name")

        # Test the input paths have been loaded into the model
        self.assertTrue(len(self.model.input_paths) > 0)
        self.assertEqual(len(self.model.input_paths), self.num_paths)

        # Test the output paths have been generated correctly
        self.assertTrue(len(self.model.output_paths) > 0)
        self.assertEqual(len(self.model.output_paths), self.num_paths)

        # Test the paths and files have been updated/ generated correctly
        with open(paths_file, 'r', encoding='utf8') as f:
            paths = f.read().splitlines()
        self.assertEqual(self.model.edf_file_name, os.path.basename(paths[0]))
        self.assertEqual(self.model.edf_directory, os.path.dirname(paths[0]))
        self.assertEqual(self.model.edf_file_path, paths[0])
        self.assertEqual(self.model.report_file_name, f"{self.model.edf_file_name.split('.')[0]}.score")
        self.assertEqual(self.model.report_directory, self.model.output_paths[0])
        self.assertEqual(self.model.report_file_path, os.path.join(self.model.report_directory, self.model.report_file_name))
        self.assertTrue(os.path.exists(self.model.report_file_path))

        # Test the initial report was generated correctly
        print(self.model.report.patient_details.history)
        self.assertIsNotNone(self.model.report.patient_details.history)
        self.assertTrue('CLINICAL HISTORY' or 'MEDICATIONS' or 'INTRODUCTION' in self.model.report.patient_details.history)
        with open(self.model.eeg_description_file_path, 'r', encoding='utf8') as f:
            text = f.read()
            self.assertEqual(self.model.report.patient_details.history, rp.strip_interpretation(text))
        if clean:
            shutil.rmtree(root_directory)

    # def test_next_edf(self):
    #     self.open_multi_edf()
    #
    #     # Overwrite report
    #     self.model.report.patient_details.history = "1"
    #     self.model.report.patient_details.name = "1"
    #
    #     # Then change to the index to edf 2
    #     self.model.next_recording()
    #
    #     # Then test model has updated correctly
    #     self.assertEqual(self.model.input_idx, 1)
    #     self.assertEqual(self.model.output_idx, 1)
    #
    #     paths_file = os.path.join(os.getcwd(), 'data', 'specified_paths.txt')
    #     with open(paths_file, 'r') as f:
    #         paths = f.read().splitlines()
    #     self.assertEqual(self.model.edf_file_name, os.path.basename(paths[1]))
    #     self.assertEqual(self.model.edf_directory, os.path.dirname(paths[1]))
    #     self.assertEqual(self.model.edf_file_path, paths[1])
    #
    #     self.assertEqual(self.model.eeg_description_directory, self.model.edf_directory)
    #     self.assertEqual(self.model.eeg_description_file_name, f"{self.model.edf_file_name.rsplit('_', 1)[0]}.txt")
    #     self.assertEqual(self.model.eeg_description_file_path, os.path.join(self.model.eeg_description_directory, self.model.eeg_description_file_name))
    #
    #     self.assertEqual(self.model.report_file_name, f"{self.model.edf_file_name.split('.')[0]}.json")
    #     self.assertEqual(self.model.report_directory, self.model.output_paths[1])
    #     self.assertEqual(self.model.report_file_path, os.path.join(self.model.report_directory, self.model.report_file_name))
    #
    #     self.assertTrue(os.path.exists(self.model.report_file_path))
    #     self.assertIsNotNone(self.model.report.patient_details.history)
    #     self.assertTrue('CLINICAL HISTORY' or 'MEDICATIONS' or 'INTRODUCTION' in self.model.report.patient_details.history)
    #     with open(self.model.eeg_description_file_path, 'r') as f:
    #         text = f.read()
    #         self.assertEqual(self.model.report.patient_details.history, rp.strip_interpretation(text))
    #     self.assertEqual(self.model.report.patient_details.history, "1")
    #     self.assertEqual(self.model.report.patient_details.name, "1")
    #
    #
    #     # Overwrite report
    #     self.model.report.patient_details.history = "1"
    #     self.model.report.patient_details.name = "1"
    #     self.assertIsNone(self.model.report_directory)
    #     self.assertIsNone(self.model.report_file_name)
    #     self.assertIsNone(self.model.report_file_path)

    def test_report_from_text_description(self):
        self.assert_report_is_blank()
        self.assert_paths_are_nones()
        test_text = os.path.join(os.getcwd(), 'data', 'eeg_sample', '00000768_s003.txt')
        self.model.set_text_report(test_text)
        self.assert_edf_text_not_none()
        self.model.report_from_text_description()
        self.assertTrue(os.path.exists(self.model.eeg_description_file_path))
        self.assertIsNotNone(self.model.report.patient_details.history)
        post_analysis = ['DESCRIPTION OF THE RECORD', 'HR', 'IMPRESSION', 'CLINICAL CORRELATION']
        for header in post_analysis:
            self.assertFalse(header in self.model.report.patient_details.history)

    def assert_report_is_blank(self):
        blank_report = Report()
        self.assertEqual(self.model.report.to_dict(), blank_report.to_dict())

    def assert_report_not_blank(self):
        blank_report = Report()
        self.assertNotEqual(self.model.report.to_dict(), blank_report.to_dict())

    def assert_paths_are_nones(self):
        self.assertIsNone(self.model.report_directory)
        self.assertIsNone(self.model.report_file_name)
        self.assertIsNone(self.model.report_file_path)

        self.assertIsNone(self.model.edf_directory)
        self.assertIsNone(self.model.edf_file_name)
        self.assertIsNone(self.model.edf_file_path)

        self.assertIsNone(self.model.ui_log_directory)
        self.assertIsNone(self.model.ui_log_file_name)
        self.assertIsNone(self.model.ui_log_file_path)

        self.assertIsNone(self.model.eye_directory)
        self.assertIsNone(self.model.eye_file_name)
        self.assertIsNone(self.model.eye_file_path)

        self.assertIsNone(self.model.edf_list_directory)
        self.assertIsNone(self.model.edf_file_name)
        self.assertIsNone(self.model.edf_file_path)

        self.assertEqual(len(self.model.input_paths), 0)
        self.assertEqual(self.model.input_idx, 0)

        self.assertIsNone(self.model.mirror_root)
        self.assertEqual(len(self.model.output_paths), 0)
        self.assertEqual(self.model.output_idx, 0)

    def set_paths_to_ones(self):
        self.model.report_directory = "1"
        self.model.report_file_name = "1"
        self.model.report_file_path = "1"

        self.model.edf_directory = "1"
        self.model.edf_file_name = "1"
        self.model.edf_file_path = "1"

        self.model.ui_log_directory = "1"
        self.model.ui_log_file_name = "1"
        self.model.ui_log_file_path = "1"

        self.model.eye_directory = "1"
        self.model.eye_file_name = "1"
        self.model.eye_file_path = "1"

        self.model.input_paths = ["1"]
        self.model.edf_list_directory = "1"
        self.model.edf_list_file_name = "1"
        self.model.edf_file_path = "1"

        self.model.mirror_root = "1"

    def assert_paths_not_nones(self):
        self.assertIsNotNone(self.model.report_directory)
        self.assertIsNotNone(self.model.report_file_name)
        self.assertIsNotNone(self.model.report_file_path)

        self.assertIsNotNone(self.model.edf_directory)
        self.assertIsNotNone(self.model.edf_file_name)
        self.assertIsNotNone(self.model.edf_file_path)

        self.assertIsNotNone(self.model.ui_log_directory)
        self.assertIsNotNone(self.model.ui_log_file_name)
        self.assertIsNotNone(self.model.ui_log_file_path)

        self.assertIsNotNone(self.model.eye_directory)
        self.assertIsNotNone(self.model.eye_file_name)
        self.assertIsNotNone(self.model.eye_file_path)

        self.assertTrue(len(self.model.input_paths) > 0)
        self.assertIsNotNone(self.model.edf_list_directory)
        self.assertIsNotNone(self.model.edf_list_file_name)
        self.assertIsNotNone(self.model.edf_file_path)

        self.assertIsNotNone(self.model.mirror_root)

    def assert_report_paths_not_none(self):
        self.assertIsNotNone(self.model.report_directory)
        self.assertIsNotNone(self.model.report_file_name)
        self.assertIsNotNone(self.model.report_file_path)

    def assert_edf_paths_not_none(self):
        self.assertIsNotNone(self.model.edf_directory)
        self.assertIsNotNone(self.model.edf_file_name)
        self.assertIsNotNone(self.model.edf_file_path)

    def assert_edf_list_not_none(self):
        self.assertIsNotNone(self.model.edf_list_directory)
        self.assertIsNotNone(self.model.edf_list_file_name)
        self.assertIsNotNone(self.model.edf_file_path)

    def assert_edf_text_not_none(self):
        self.assertIsNotNone(self.model.eeg_description_file_name)
        self.assertIsNotNone(self.model.eeg_description_file_path)
        self.assertIsNotNone(self.model.eeg_description_directory)