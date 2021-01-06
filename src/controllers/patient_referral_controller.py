from src.models.patient_referral import Referral
from src.views.patient_referral import PatientReferralWidget


class PatientReferralController:

    def __init__(self):
        self.model = Referral()
        self.view = PatientReferralWidget()

    def update_model(self):
        self.model.update_from_dict(self.view.to_dict())

    def update_view(self):
        self.view.update_from_dict(self.model.to_dict())