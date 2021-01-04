
from src.models.patient_details import Patient
from src.models.patient_referral import Referral
from src.models.recording_conditions import RecordingConditions


class Report:

    def __init__(self, model=None):
        self.model = model
        self.patient_details = Patient()
        self.patient_referral = Referral()
        self.recording_conditions = RecordingConditions()

    def to_dict(self):
        data = {
            "Patient details": self.patient_details.to_dict(),
            "Patient referral": self.patient_referral.to_dict(),
            "Recording conditions": self.recording_conditions.to_dict()
        }
        return data

    def from_dict(self, data):
        self.patient_details.update_from_dict(data['Patient details'])
        self.patient_referral.update_from_dict(data['Patient referral'])
        self.recording_conditions.update_from_dict(data['Recording conditions'])

    def reset(self):
        self.patient_details.set_to_nones()
        self.patient_referral.set_to_nones()
        self.recording_conditions.set_to_nones()


