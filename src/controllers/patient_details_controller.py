from src.models.patient_details import Patient
from src.views.patient_details import PatientDetailsWidget


class PatientDetailsController:

    def __init__(self):
        self.model = Patient()
        self.view = PatientDetailsWidget()

    def update_model(self):
        self.model.update_from_dict(self.view.to_dict())

    def update_view(self):
        self.view.update_from_dict(self.model.to_dict())
