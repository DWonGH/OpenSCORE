import json
import os
import sys
import unittest
import filecmp
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton

from modules.main_window import MainWindow


app = QApplication(sys.argv)


class OpenSCORETest(unittest.TestCase):

    def setUp(self):
        # Setup test data files
        self.test_directory = os.path.join(os.getcwd(), "tests", "test_data")
        self.test_report_dummy = os.path.join(self.test_directory, "a_test_report.json")
        self.test_report_default = os.path.join(self.test_directory, 'test_report_default.json')
        self.test_report_complete = os.path.join(self.test_directory, 'test_report_complete.json')

        if os.path.exists(self.test_report_dummy):
            os.remove(self.test_report_dummy)
        self.assertFalse(os.path.exists(os.path.join(os.getcwd(), self.test_report_dummy)))
        with open(self.test_report_dummy, 'w') as f:
            f.write("")
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), self.test_report_dummy)))
        self.assertTrue(os.stat(self.test_report_dummy).st_size == 0)
        self.main_window = MainWindow()
        self.ui_model = self.main_window.ui_model
        self.diagnostic_significance = self.main_window.main_tab_view.diagnostic_significance_tab
        self.clinical_comments = self.main_window.main_tab_view.clinical_comments

    def test_diagnosticSignificanceDefaults(self):
        """
        Test button states on load
        :return:
        """
        self.assertTrue(self.diagnostic_significance.rbt_normal.isChecked())
        self.assertFalse(self.diagnostic_significance.rbt_no_definite.isChecked())
        self.assertFalse(self.diagnostic_significance.rbt_abnormal.isChecked())
        self.diagnostic_significance_abnormal_off()

    def test_diagnostic_significance_radios(self):
        """
        Test radio buttons switch correctly
        :return:
        """
        self.diagnostic_significance.rbt_no_definite.click()
        self.assertFalse(self.diagnostic_significance.rbt_normal.isChecked())
        self.assertTrue(self.diagnostic_significance.rbt_no_definite.isChecked())
        self.assertFalse(self.diagnostic_significance.rbt_abnormal.isChecked())
        self.diagnostic_significance_abnormal_off()

        self.diagnostic_significance.rbt_abnormal.click()
        self.assertFalse(self.diagnostic_significance.rbt_normal.isChecked())
        self.assertFalse(self.diagnostic_significance.rbt_no_definite.isChecked())
        self.assertTrue(self.diagnostic_significance.rbt_abnormal.isChecked())
        self.diagnostic_significance_abnormal_on()

    def diagnostic_significance_abnormal_off(self):
        """
        Test the check boxes are disabled when abnormal radio button is not selected
        :return:
        """
        self.assertFalse(self.diagnostic_significance.chbx_pnes.isEnabled())
        self.assertFalse(self.diagnostic_significance.chbx_other_nonepileptic.isEnabled())
        self.assertFalse(self.diagnostic_significance.chbx_focal_dysfunction.isEnabled())
        self.assertFalse(self.diagnostic_significance.chbx_diffuse_dysfunction.isEnabled())
        self.assertFalse(self.diagnostic_significance.chbx_coma.isEnabled())
        self.assertFalse(self.diagnostic_significance.chbx_brain_death.isEnabled())
        self.assertFalse(self.diagnostic_significance.chbx_uncertain.isEnabled())

        self.assertFalse(self.diagnostic_significance.chbx_pnes.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_other_nonepileptic.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_focal_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_diffuse_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_coma.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_brain_death.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_uncertain.isChecked())

    def diagnostic_significance_abnormal_on(self):
        """
        Test the check boxes become enabled and checkable when the abnormal button is selected
        :return:
        """
        self.assertTrue(self.diagnostic_significance.chbx_pnes.isEnabled())
        self.assertTrue(self.diagnostic_significance.chbx_other_nonepileptic.isEnabled())
        self.assertTrue(self.diagnostic_significance.chbx_focal_dysfunction.isEnabled())
        self.assertTrue(self.diagnostic_significance.chbx_diffuse_dysfunction.isEnabled())
        self.assertTrue(self.diagnostic_significance.chbx_coma.isEnabled())
        self.assertTrue(self.diagnostic_significance.chbx_brain_death.isEnabled())
        self.assertTrue(self.diagnostic_significance.chbx_uncertain.isEnabled())

        self.assertFalse(self.diagnostic_significance.chbx_pnes.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_other_nonepileptic.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_focal_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_diffuse_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_coma.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_brain_death.isChecked())
        self.assertFalse(self.diagnostic_significance.chbx_uncertain.isChecked())

    def test_diagnostic_significance_get_fields(self):
        """
        Test the correct information can be gathered from each of the buttons and boxes
        :return:
        """
        self.diagnostic_significance.rbt_normal.click()
        target = {
            "Normal recording": True,
            "No Definite Abnormality": False,
            "Abnormal recording": False,
            "Abnormal specification": {
                "Epilepsy": False,
                "Psychogenic non-epileptic seizures (PNES)": False,
                "Other non-epileptic clinical episode": False,
                "Status epilepticus": False,
                "Focal dysfunction of the central nervous system": False,
                "Diffuse dysfunction of the central nervous system": False,
                "Continuous spikes and waves during slow sleep (CSWS) or electrical status epilepticus in sleep (ESES)": False,
                "Coma": False,
                "Brain death": False,
                "EEG abnormality of uncertain clinical significance": False
            }
        }
        result = self.diagnostic_significance.get_fields()
        self.assertEqual(target, result)

        self.diagnostic_significance.rbt_abnormal.click()
        self.diagnostic_significance.chbx_pnes.click()
        self.diagnostic_significance.chbx_other_nonepileptic.click()
        self.diagnostic_significance.chbx_focal_dysfunction.click()
        self.diagnostic_significance.chbx_diffuse_dysfunction.click()
        self.diagnostic_significance.chbx_coma.click()
        self.diagnostic_significance.chbx_brain_death.click()
        self.diagnostic_significance.chbx_uncertain.click()
        target = {
            "Normal recording": False,
            "No Definite Abnormality": False,
            "Abnormal recording": True,
            "Abnormal specification": {
                "Epilepsy": True,
                "Psychogenic non-epileptic seizures (PNES)": True,
                "Other non-epileptic clinical episode": True,
                "Status epilepticus": True,
                "Focal dysfunction of the central nervous system": True,
                "Diffuse dysfunction of the central nervous system": True,
                "Continuous spikes and waves during slow sleep (CSWS) or electrical status epilepticus in sleep (ESES)": True,
                "Coma": True,
                "Brain death": True,
                "EEG abnormality of uncertain clinical significance": True
            }
        }
        result = self.diagnostic_significance.get_fields()
        self.assertEqual(target, result)

    def test_clinical_comments_defaults(self):
        """
        Test clinical comments is blank on load
        :return:
        """
        self.assertEqual(self.clinical_comments.txe_interpreter_name.text(), "")
        self.assertEqual(self.clinical_comments.txe_clinical_comments.toPlainText(), "")

    def test_clinical_comments_get_info(self):
        """
        Test clinical comments can retrieve info from UI
        :return:
        """
        target = {
            "Interpreter name": "",
            "Clinical comments": ""
        }
        result = self.clinical_comments.get_fields()
        self.assertEqual(target, result)

        self.clinical_comments.txe_interpreter_name.setText("Someones name")
        self.clinical_comments.txe_clinical_comments.setText("Someones comments")
        target = {
            "Interpreter name": "Someones name",
            "Clinical comments": "Someones comments"
        }
        result = self.clinical_comments.get_fields()
        self.assertEqual(target, result)

    def test_save_action(self):
        """
        Test the save functionality works. Create a test file manually first as we are unable to
        simulate the user selecting a file using the QFileDialog getSaveName modal dialog.

        Test the correct saved default file with no modifications, then test a modified report
        with all abnormal buttons checked and text added to the clinical comments page
        :return:
        """
        self.main_window.ui_model.report_path = self.test_report_dummy
        self.main_window.menu.bt_save_file.trigger()
        self.assertTrue(os.stat(self.test_report_dummy).st_size > 0)
        self.assertTrue(self.text_compare(os.path.join(self.test_directory, self.test_report_default), os.path.join(self.test_directory, self.test_report_dummy)))
        self.diagnostic_significance.rbt_abnormal.click()
        self.assertFalse(self.diagnostic_significance.rbt_normal.isChecked())
        self.assertFalse(self.diagnostic_significance.rbt_no_definite.isChecked())
        self.assertTrue(self.diagnostic_significance.rbt_abnormal.isChecked())
        self.diagnostic_significance.rbt_abnormal.click()
        self.diagnostic_significance.chbx_pnes.click()
        self.diagnostic_significance.chbx_other_nonepileptic.click()
        self.diagnostic_significance.chbx_focal_dysfunction.click()
        self.diagnostic_significance.chbx_diffuse_dysfunction.click()
        self.diagnostic_significance.chbx_coma.click()
        self.diagnostic_significance.chbx_brain_death.click()
        self.diagnostic_significance.chbx_uncertain.click()
        self.clinical_comments.txe_interpreter_name.setText("The interpreters name")
        self.clinical_comments.txe_clinical_comments.setText("Some clinical comments")
        self.main_window.menu.bt_save_file.trigger()
        self.assertTrue(os.stat(self.test_report_dummy).st_size > 0)
        self.assertTrue(self.text_compare(os.path.join(self.test_directory, self.test_report_complete), os.path.join(self.test_directory, self.test_report_dummy)))

    def test_open_report(self):
        """
        Test that the open functionality works. Open a pre-generated report from json and ensure
        that each field and option is populated as per the information in the file.
        :return:
        """
        with open(self.test_report_complete, 'r') as f:
            report = json.load(f)
        self.main_window.main_tab_view.set_fields(report)
        target = report["Diagnostic significance"]
        self.assertEqual(self.diagnostic_significance.rbt_normal.isChecked(), target["Normal recording"])
        self.assertEqual(self.diagnostic_significance.rbt_no_definite.isChecked(), target["No Definite Abnormality"])
        self.assertEqual(self.diagnostic_significance.rbt_abnormal.isChecked(), target["Abnormal recording"])
        target = report["Diagnostic significance"]["Abnormal specification"]
        self.assertEqual(self.diagnostic_significance.chbx_pnes.isChecked(), target["Psychogenic non-epileptic seizures (PNES)"])
        self.assertEqual(self.diagnostic_significance.chbx_other_nonepileptic.isChecked(), target["Other non-epileptic clinical episode"])
        self.assertEqual(self.diagnostic_significance.chbx_focal_dysfunction.isChecked(), target["Focal dysfunction of the central nervous system"])
        self.assertEqual(self.diagnostic_significance.chbx_diffuse_dysfunction.isChecked(), target["Diffuse dysfunction of the central nervous system"])
        self.assertEqual(self.diagnostic_significance.chbx_coma.isChecked(), target["Coma"])
        self.assertEqual(self.diagnostic_significance.chbx_brain_death.isChecked(), target["Brain death"])
        self.assertEqual(self.diagnostic_significance.chbx_uncertain.isChecked(), target["EEG abnormality of uncertain clinical significance"])
        target = report["Clinical comments"]
        self.assertEqual(self.clinical_comments.txe_interpreter_name.text(), target["Interpreter name"])
        self.assertEqual(self.clinical_comments.txe_clinical_comments.toPlainText(), target["Clinical comments"])

    def text_compare(self, fl1, fl2):
        """
        Compare the text in two files.
        Skip the date and time fields as they need to be reimplemented without auto-generated dates.
        :param fl1:
        :param fl2:
        :return:
        """
        with open(fl1, 'r') as file_1:
            with open(fl2, 'r') as file_2:
                lines1 = file_1.readlines()
                lines2 = file_2.readlines()
                for i in range(len(lines1)):
                    if ("Latest meal" in lines1[i]) or ("Date & Time" in lines1[i]):
                        pass
                    else:
                        self.assertEqual(lines1[i], lines2[i])
        return True

    def test_load_eeg_from_folder(self):
        """
        Test loading an EDF and txt file from a specified folder - and test the automated field completion and setup
        using their information.
        :return:
        """
        eeg_directory = "eeg_sample"
        browse_dir = os.path.join(self.test_directory, eeg_directory)
        self.assertTrue(os.path.exists(browse_dir))
        self.ui_model.current_input_directory = browse_dir
        self.ui_model.update_load_eeg(browse_dir)
        self.main_window.update()
        self.assertEqual(self.ui_model.current_input_directory, browse_dir)
        self.assertEqual(self.ui_model.current_edf_filename, '00000768_s003_t000.edf')
        self.assertEqual(self.ui_model.current_edf_path, os.path.join(browse_dir, '00000768_s003_t000.edf'))
        self.assertEqual(self.ui_model.current_txt_filename, '00000768_s003.txt')
        self.assertEqual(self.ui_model.current_txt_path, os.path.join(browse_dir, '00000768_s003.txt'))
        self.assertEqual(self.main_window.main_tab_view.recording_conditions.txe_recording_data.text(), os.path.join(browse_dir, '00000768_s003_t000.edf'))
        self.assertEqual(self.main_window.toolbar.lbl_current_eeg_name.text(), '00000768_s003_t000')
        with open(os.path.join(browse_dir, os.path.join(browse_dir, '00000768_s003.txt')), 'r') as f:
            target_text = f.read()
        self.assertEqual(self.main_window.main_tab_view.patient_details_tab.patient_info_tab.txe_history.toPlainText(), target_text)


if __name__ == "__main__":
    unittest.main()
