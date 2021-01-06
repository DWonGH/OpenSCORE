import json

from src.models.clinical_comments import ClinicalComments
from src.models.diagnostic_significance import DiagnosticSignificance
from src.models.patient_details import Patient
from src.models.patient_referral import Referral
from src.models.recording_conditions import RecordingConditions


class Report:

    def __init__(self, model=None):
        self.model = model

        self.directory = None
        self.file_name = None
        self.file_path = None

        self.patient_details = Patient()
        self.patient_referral = Referral()
        self.recording_conditions = RecordingConditions()
        self.diagnostic_significance = DiagnosticSignificance()
        self.clinical_comments = ClinicalComments()

    def to_json(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def from_json(self):
        with open(self.file_path, 'r') as f:
            self.from_dict(json.load(f))

    def to_dict(self):
        data = {
            "Patient details": self.patient_details.to_dict(),
            "Patient referral": self.patient_referral.to_dict(),
            "Recording conditions": self.recording_conditions.to_dict(),
            "Diagnostic significance": self.diagnostic_significance.to_dict(),
            "Clinical comments": self.clinical_comments.to_dict()
        }
        return data

    def from_dict(self, data):
        self.patient_details.update_from_dict(data['Patient details'])
        self.patient_referral.update_from_dict(data['Patient referral'])
        self.recording_conditions.update_from_dict(data['Recording conditions'])
        self.diagnostic_significance.update_from_dict(data['Diagnostic significance'])
        self.clinical_comments.update_from_dict(data['Clinical comments'])

    def reset(self):
        self.patient_details.set_to_nones()
        self.patient_referral.set_to_nones()
        self.recording_conditions.set_to_nones()
        self.diagnostic_significance.set_to_nones()
        self.clinical_comments.set_to_nones()


