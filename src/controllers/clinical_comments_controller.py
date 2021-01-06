from src.models.clinical_comments import ClinicalComments
from src.views.clinical_comments import ClinicalCommentsWidget


class ClinicalCommentsController:

    def __init__(self):
        self.model = ClinicalComments()
        self.view = ClinicalCommentsWidget()

    def update_model(self):
        self.model.update_from_dict(self.view.to_dict())

    def update_view(self):
        self.view.update_from_dict(self.model.to_dict())
