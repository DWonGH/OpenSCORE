import sys
import unittest
import traceback

from PyQt5.QtWidgets import QApplication

from src.views.diagnostic_significance import DiagnosticSignificanceWidget


class TestDiagnosticSignificanceWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.diagnostic_significance_widget = DiagnosticSignificanceWidget()

    def test_init(self):

        self.assertFalse(self.diagnostic_significance_widget.rbt_normal.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.rbt_no_definite.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.rbt_abnormal.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_pnes.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_pnes.isEnabled())
        self.assertFalse(self.diagnostic_significance_widget.chbx_other_nonepileptic.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_other_nonepileptic.isEnabled())
        self.assertFalse(self.diagnostic_significance_widget.chbx_focal_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_focal_dysfunction.isEnabled())
        self.assertFalse(self.diagnostic_significance_widget.chbx_diffuse_dysfunction.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_diffuse_dysfunction.isEnabled())
        self.assertFalse(self.diagnostic_significance_widget.chbx_coma.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_coma.isEnabled())
        self.assertFalse(self.diagnostic_significance_widget.chbx_brain_death.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_brain_death.isEnabled())
        self.assertFalse(self.diagnostic_significance_widget.chbx_uncertain.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.chbx_uncertain.isEnabled())
        target_dict = {
            "Diagnosis": None,
            "Abnormal specification": None
        }
        result_dict = self.diagnostic_significance_widget.to_dict()
        self.assertEqual(target_dict, result_dict)

    def test_ones_to_dict(self):
        self.set_to_ones()
        self.assertFalse(self.diagnostic_significance_widget.rbt_normal.isChecked())
        self.assertFalse(self.diagnostic_significance_widget.rbt_no_definite.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.rbt_abnormal.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_pnes.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_pnes.isEnabled())
        self.assertTrue(self.diagnostic_significance_widget.chbx_other_nonepileptic.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_other_nonepileptic.isEnabled())
        self.assertTrue(self.diagnostic_significance_widget.chbx_focal_dysfunction.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_focal_dysfunction.isEnabled())
        self.assertTrue(self.diagnostic_significance_widget.chbx_diffuse_dysfunction.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_diffuse_dysfunction.isEnabled())
        self.assertTrue(self.diagnostic_significance_widget.chbx_coma.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_coma.isEnabled())
        self.assertTrue(self.diagnostic_significance_widget.chbx_brain_death.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_brain_death.isEnabled())
        self.assertTrue(self.diagnostic_significance_widget.chbx_uncertain.isChecked())
        self.assertTrue(self.diagnostic_significance_widget.chbx_uncertain.isEnabled())
        result_dict = self.diagnostic_significance_widget.to_dict()
        target_dict = {
            "Diagnosis": "Abnormal recording",
            "Abnormal specification": [
                "Psychogenic non-epileptic seizures (PNES)",
                "Other non-epileptic clinical episode",
                "Focal dysfunction of the central nervous system",
                "Diffuse dysfunction of the central nervous system",
                "Coma",
                "Brain death",
                "EEG abnormality of uncertain clinical significance"
            ]
        }
        self.assertEqual(result_dict, target_dict)

    def set_to_ones(self):
        self.diagnostic_significance_widget.rbt_abnormal.setChecked(True)
        self.diagnostic_significance_widget.chbx_pnes.setChecked(True)
        self.diagnostic_significance_widget.chbx_pnes.setEnabled(True)
        self.diagnostic_significance_widget.chbx_other_nonepileptic.setChecked(True)
        self.diagnostic_significance_widget.chbx_other_nonepileptic.setEnabled(True)
        self.diagnostic_significance_widget.chbx_focal_dysfunction.setChecked(True)
        self.diagnostic_significance_widget.chbx_focal_dysfunction.setEnabled(True)
        self.diagnostic_significance_widget.chbx_diffuse_dysfunction.setChecked(True)
        self.diagnostic_significance_widget.chbx_diffuse_dysfunction.setEnabled(True)
        self.diagnostic_significance_widget.chbx_coma.setChecked(True)
        self.diagnostic_significance_widget.chbx_coma.setEnabled(True)
        self.diagnostic_significance_widget.chbx_brain_death.setChecked(True)
        self.diagnostic_significance_widget.chbx_brain_death.setEnabled(True)
        self.diagnostic_significance_widget.chbx_uncertain.setChecked(True)
        self.diagnostic_significance_widget.chbx_uncertain.setEnabled(True)



