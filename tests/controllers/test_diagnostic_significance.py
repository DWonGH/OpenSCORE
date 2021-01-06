import sys
import unittest

from PyQt5.QtWidgets import QApplication

from src.controllers.diagnostic_significance_controller import DiagnosticSignificanceController


class TestClinicalDiagnosticSignificanceController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = QApplication(sys.argv)
        self.controller = DiagnosticSignificanceController()
        self.model = self.controller.model
        self.view = self.controller.view

    def test_init(self):
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.view)

    def test_update_model(self):
        self.assertIsNone(self.model.diagnosis)
        self.assertIsNone(self.model.abnormal_specification)
        self.controller.update_model()
        self.assertIsNone(self.model.diagnosis)
        self.assertIsNone(self.model.abnormal_specification)
        self.view.rbt_normal.setChecked(True)
        self.controller.update_model()
        self.assertEqual(self.model.diagnosis, "Normal")
        self.view.rbt_abnormal.setChecked(True)
        self.controller.update_model()
        self.assertEqual(self.model.diagnosis, "Abnormal recording")
        self.assertEqual(self.model.abnormal_specification, [])
        self.view.chbx_pnes.setChecked(True)
        self.view.chbx_other_nonepileptic.setChecked(True)
        self.view.chbx_focal_dysfunction.setChecked(True)
        self.view.chbx_diffuse_dysfunction.setChecked(True)
        self.view.chbx_coma.setChecked(True)
        self.view.chbx_brain_death.setChecked(True)
        self.view.chbx_uncertain.setChecked(True)
        self.controller.update_model()
        self.assertEqual(self.model.diagnosis, "Abnormal recording")
        self.assertEqual(self.model.abnormal_specification, [
                "Psychogenic non-epileptic seizures (PNES)",
                "Other non-epileptic clinical episode",
                "Focal dysfunction of the central nervous system",
                "Diffuse dysfunction of the central nervous system",
                "Coma",
                "Brain death",
                "EEG abnormality of uncertain clinical significance"
            ])

    def test_update_view(self):
        self.assertFalse(self.view.rbt_normal.isChecked())
        self.assertFalse(self.view.rbt_no_definite.isChecked())
        self.assertFalse(self.view.rbt_abnormal.isChecked())
        self.assertFalse(self.view.chbx_pnes.isChecked())
        self.assertFalse(self.view.chbx_pnes.isEnabled())
        self.assertFalse(self.view.chbx_other_nonepileptic.isChecked())
        self.assertFalse(self.view.chbx_other_nonepileptic.isEnabled())
        self.assertFalse(self.view.chbx_focal_dysfunction.isChecked())
        self.assertFalse(self.view.chbx_focal_dysfunction.isEnabled())
        self.assertFalse(self.view.chbx_diffuse_dysfunction.isChecked())
        self.assertFalse(self.view.chbx_diffuse_dysfunction.isEnabled())
        self.assertFalse(self.view.chbx_coma.isChecked())
        self.assertFalse(self.view.chbx_coma.isEnabled())
        self.assertFalse(self.view.chbx_brain_death.isChecked())
        self.assertFalse(self.view.chbx_brain_death.isEnabled())
        self.assertFalse(self.view.chbx_uncertain.isChecked())
        self.assertFalse(self.view.chbx_uncertain.isEnabled())
        self.model.diagnosis = "Abnormal recording"
        self.model.abnormal_specification = [
                "Psychogenic non-epileptic seizures (PNES)",
                "Other non-epileptic clinical episode",
                "Focal dysfunction of the central nervous system",
                "Diffuse dysfunction of the central nervous system",
                "Coma",
                "Brain death",
                "EEG abnormality of uncertain clinical significance"
            ]
        self.controller.update_view()
        self.assertFalse(self.view.rbt_normal.isChecked())
        self.assertFalse(self.view.rbt_no_definite.isChecked())
        self.assertTrue(self.view.rbt_abnormal.isChecked())
        self.assertTrue(self.view.chbx_pnes.isChecked())
        self.assertTrue(self.view.chbx_pnes.isEnabled())
        self.assertTrue(self.view.chbx_other_nonepileptic.isChecked())
        self.assertTrue(self.view.chbx_other_nonepileptic.isEnabled())
        self.assertTrue(self.view.chbx_focal_dysfunction.isChecked())
        self.assertTrue(self.view.chbx_focal_dysfunction.isEnabled())
        self.assertTrue(self.view.chbx_diffuse_dysfunction.isChecked())
        self.assertTrue(self.view.chbx_diffuse_dysfunction.isEnabled())
        self.assertTrue(self.view.chbx_coma.isChecked())
        self.assertTrue(self.view.chbx_coma.isEnabled())
        self.assertTrue(self.view.chbx_brain_death.isChecked())
        self.assertTrue(self.view.chbx_brain_death.isEnabled())
        self.assertTrue(self.view.chbx_uncertain.isChecked())
        self.assertTrue(self.view.chbx_uncertain.isEnabled())






