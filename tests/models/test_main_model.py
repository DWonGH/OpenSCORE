import json
import os
import unittest
import shutil
from src.models.main_model import MainModel
from src.models.report import Report
from helpers import eegreportparser as rp


class TestMainModel(unittest.TestCase):

    def setUp(self) -> None:
        self.model = MainModel()

    def test_init(self):
        self.assertIsNone(self.model.view)

        #self.assertIsNone(self.model.report = Report(self)

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

        self.assertFalse(self.model.report_edited)

    def test_reset(self):

        blank_report = Report()
        self.assertEqual(self.model.report.to_dict(), blank_report.to_dict())

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

        test_report = os.path.join(os.getcwd(), 'data', 'test_report.json')
        with open(test_report, 'r') as f:
            test_report_dict = json.load(f)
        self.model.open_report(test_report)
        self.assertNotEqual(self.model.report.to_dict(), blank_report.to_dict())
        self.assertEqual(self.model.report.to_dict(), test_report_dict)

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

        self.assertEqual(len(self.model.input_paths), 1)
        self.assertIsNotNone(self.model.edf_list_directory)
        self.assertIsNotNone(self.model.edf_list_file_name)
        self.assertIsNotNone(self.model.edf_file_path)

        self.assertIsNotNone(self.model.mirror_root)

        self.model.reset()

        self.assertEqual(self.model.report.to_dict(), blank_report.to_dict())

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

    def test_save_report(self):
        cwd = os.getcwd()
        files = next(os.walk(cwd))[2]
        main = False
        test = False
        dummy = False
        for f in files:
            if "main.py" in f:
                main = True
            if "test.py" in f:
                test = True
            if "dummy.json" in f:
                dummy = True
        self.assertTrue(main)
        self.assertTrue(test)
        self.assertFalse(dummy)

        self.model.report_file_name = "dummy.json"
        self.model.report_directory = cwd
        self.model.report_file_path = os.path.join(self.model.report_directory, self.model.report_file_name)
        self.assertTrue(self.model.report_file_path)

        self.model.save_report()
        files = next(os.walk(cwd))[2]
        main = False
        test = False
        dummy = False
        for f in files:
            if "main.py" in f:
                main = True
            if "test.py" in f:
                test = True
            if "dummy.json" in f:
                dummy = True
        self.assertTrue(main)
        self.assertTrue(test)
        self.assertTrue(dummy)

        os.remove(self.model.report_file_path)

    def test_save_report_as(self):
        cwd = os.getcwd()
        files = next(os.walk(cwd))[2]
        main = False
        test = False
        dummy = False
        for f in files:
            if "main.py" in f:
                main = True
            if "test.py" in f:
                test = True
            if "dummy.json" in f:
                dummy = True
        self.assertTrue(main)
        self.assertTrue(test)
        self.assertFalse(dummy)

        test_report = os.path.join(cwd, 'dummy.json')

        self.assertIsNone(self.model.report_file_path)
        self.assertIsNone(self.model.report_directory)
        self.assertIsNone(self.model.report_file_path)
        self.assertFalse(os.path.exists(test_report))

        self.model.save_report_as(test_report)

        self.assertEqual(self.model.report_directory, cwd)
        self.assertEqual(self.model.report_file_name, 'dummy.json')
        self.assertEqual(self.model.report_file_path, test_report)

        os.remove(self.model.report_file_path)

    def test_open_report(self):
        cwd = os.getcwd()
        files = next(os.walk(cwd))[2]
        main = False
        test = False
        for f in files:
            if "main.py" in f:
                main = True
            if "test.py" in f:
                test = True
        self.assertTrue(main)
        self.assertTrue(test)

        test_report = os.path.join(cwd, 'data', 'test_report.json')

        self.assertIsNone(self.model.report.patient_details.name)
        self.assertIsNone(self.model.report_directory)
        self.assertIsNone(self.model.report_file_name)
        self.assertIsNone(self.model.report_file_path)

        self.model.open_report(test_report)

        self.assertEqual(self.model.report_directory, os.path.join(cwd, 'data'))
        self.assertTrue(os.path.exists(self.model.report_directory))
        self.assertEqual(self.model.report_file_name, 'test_report.json')
        self.assertTrue(os.path.exists(self.model.report_file_path))
        self.assertIsNotNone(self.model.report.patient_details.name)
        with open(self.model.report_file_path, 'r') as f:
            report = json.load(f)
            self.assertEqual(report, self.model.report.to_dict())

    def test_open_edf(self):
        raise NotImplementedError

    def test_open_multi_edf(self):
        self.open_multi_edf(True)

    def open_multi_edf(self, clean=None):
        self.num_paths = 7
        # Check defaults
        self.assertEqual(len(self.model.input_paths), 0)
        self.assertEqual(self.model.input_idx, 0)
        self.assertEqual(len(self.model.output_paths), 0)
        self.assertEqual(self.model.output_idx, 0)
        blank_report = Report()
        self.assertEqual(self.model.report.to_dict(), blank_report.to_dict())
        self.assertIsNone(self.model.report_directory)
        self.assertIsNone(self.model.report_file_name)
        self.assertIsNone(self.model.report_file_path)
        self.assertIsNone(self.model.eeg_description_directory)
        self.assertIsNone(self.model.eeg_description_file_name)
        self.assertIsNone(self.model.eeg_description_file_path)
        self.assertIsNone(self.model.edf_directory)
        self.assertIsNone(self.model.edf_file_name)
        self.assertIsNone(self.model.edf_file_path)

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
        with open(paths_file, 'r') as f:
            paths = f.read().splitlines()
#        self.assertEqual(len(paths), self.num_paths)
        self.assertEqual(self.model.edf_file_name, os.path.basename(paths[0]))
        self.assertEqual(self.model.edf_directory, os.path.dirname(paths[0]))
        self.assertEqual(self.model.edf_file_path, paths[0])
        self.assertEqual(self.model.report_file_name, f"{self.model.edf_file_name.split('.')[0]}.json")
        self.assertEqual(self.model.report_directory, self.model.output_paths[0])
        self.assertEqual(self.model.report_file_path, os.path.join(self.model.report_directory, self.model.report_file_name))
        self.assertTrue(os.path.exists(self.model.report_file_path))

        # Test the initial report was generated correctly
        self.assertIsNotNone(self.model.report.patient_details.history)
        self.assertTrue('CLINICAL HISTORY' or 'MEDICATIONS' or 'INTRODUCTION' in self.model.report.patient_details.history)
        with open(self.model.eeg_description_file_path, 'r') as f:
            text = f.read()
            self.assertEqual(self.model.report.patient_details.history, rp.strip_interpretation(text))
        if clean:
            shutil.rmtree(root_directory)

    def test_navigate_eeg_list(self):

        self.open_multi_edf()

    # Load the list of edfs
    # Test the list and initial report loaded correctly.
    # Call next recording
    # Test index is += 1
    # Test file names are += 1
    # Save a report
    # Call next recording
    # Test index is += 1
    # Test file names are += 1
    # Call previous recording
    # Test index is -= 1
    # Test file names are -= 1
    # Test the saved report is loaded instead of auto from text report

    def test_next_edf(self):
        self.open_multi_edf()

        # Overwrite report
        self.model.report.patient_details.history = "1"
        self.model.report.patient_details.name = "1"

        # Then change to the index to edf 2
        self.model.next_recording()

        # Then test model has updated correctly
        self.assertEqual(self.model.input_idx, 1)
        self.assertEqual(self.model.output_idx, 1)

        paths_file = os.path.join(os.getcwd(), 'data', 'specified_paths.txt')
        with open(paths_file, 'r') as f:
            paths = f.read().splitlines()
        self.assertEqual(self.model.edf_file_name, os.path.basename(paths[1]))
        self.assertEqual(self.model.edf_directory, os.path.dirname(paths[1]))
        self.assertEqual(self.model.edf_file_path, paths[1])

        self.assertEqual(self.model.eeg_description_directory, self.model.edf_directory)
        self.assertEqual(self.model.eeg_description_file_name, f"{self.model.edf_file_name.rsplit('_', 1)[0]}.txt")
        self.assertEqual(self.model.eeg_description_file_path, os.path.join(self.model.eeg_description_directory, self.model.eeg_description_file_name))

        self.assertEqual(self.model.report_file_name, f"{self.model.edf_file_name.split('.')[0]}.json")
        self.assertEqual(self.model.report_directory, self.model.output_paths[1])
        self.assertEqual(self.model.report_file_path, os.path.join(self.model.report_directory, self.model.report_file_name))

        self.assertTrue(os.path.exists(self.model.report_file_path))
        self.assertIsNotNone(self.model.report.patient_details.history)
        self.assertTrue('CLINICAL HISTORY' or 'MEDICATIONS' or 'INTRODUCTION' in self.model.report.patient_details.history)
        with open(self.model.eeg_description_file_path, 'r') as f:
            text = f.read()
            self.assertEqual(self.model.report.patient_details.history, rp.strip_interpretation(text))
        self.assertEqual(self.model.report.patient_details.history, "1")
        self.assertEqual(self.model.report.patient_details.name, "1")


        # Overwrite report
        self.model.report.patient_details.history = "1"
        self.model.report.patient_details.name = "1"
        self.assertIsNone(self.model.report_directory)
        self.assertIsNone(self.model.report_file_name)
        self.assertIsNone(self.model.report_file_path)






    def test_open_text_report(self):
        raise NotImplementedError

    def test_report_from_text_description(self):
        cwd = os.getcwd()
        files = next(os.walk(cwd))[2]
        main = False
        test = False
        for f in files:
            if "main.py" in f:
                main = True
            if "test.py" in f:
                test = True
        self.assertTrue(main)
        self.assertTrue(test)

        self.model.eeg_description_directory = os.path.join(cwd, 'data', 'eeg_sample')
        self.model.eeg_description_file_name = '00000768_s003.txt'
        self.model.eeg_description_file_path = os.path.join(self.model.eeg_description_directory, self.model.eeg_description_file_name)
        self.assertTrue(os.path.exists(self.model.eeg_description_file_path))

        self.assertIsNone(self.model.report.patient_details.history)
        self.model.report_from_text_description()
        self.assertIsNotNone(self.model.report.patient_details.history)

        post_analysis = ['DESCRIPTION OF THE RECORD', 'HR', 'IMPRESSION', 'CLINICAL CORRELATION']

        for header in post_analysis:
            self.assertFalse(header in self.model.report.patient_details.history)

