import unittest

from src.models.diagnostic_significance import DiagnosticSignificance


class TestDiagnosticSignificance(unittest.TestCase):

    def setUp(self) -> None:
        self.diagnostic_significance = DiagnosticSignificance()

    def test_init(self):
        self.assertIsNone(self.diagnostic_significance.diagnosis)
        self.assertIsNone(self.diagnostic_significance.abnormal_specification)

    def test_nones_to_dict(self):
        self.diagnostic_significance.set_to_nones()
        self.assertIsNone(self.diagnostic_significance.diagnosis)
        self.assertIsNone(self.diagnostic_significance.abnormal_specification)

    def test_set_to_ones(self):
        self.set_to_ones()
        self.details_dict = self.diagnostic_significance.to_dict()
        target_dict = {
            "Diagnosis": "1",
            "Abnormal specification": ["1"]
        }
        self.assertEqual(self.details_dict, target_dict)

    def set_to_ones(self):
        self.diagnostic_significance.diagnosis = "1"
        self.diagnostic_significance.abnormal_specification = ["1"]
