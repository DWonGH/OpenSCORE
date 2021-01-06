from src.models.diagnostic_significance import DiagnosticSignificance
from src.views.diagnostic_significance import DiagnosticSignificanceWidget


class DiagnosticSignificanceController:

    def __init__(self):
        self.model = DiagnosticSignificance()
        self.view = DiagnosticSignificanceWidget()

        self.view.rbt_abnormal.toggled.connect(self.abnormal_toggled)

    def abnormal_toggled(self):
        """
        Disable and ignore checks in each of the abnormal specification checkboxes if the recording is not considered
        abnormal
        :return:
        """
        if self.view.rbt_abnormal.isChecked():
            self.view.chbx_brain_death.setEnabled(True)
            self.view.chbx_diffuse_dysfunction.setEnabled(True)
            self.view.chbx_focal_dysfunction.setEnabled(True)
            self.view.chbx_pnes.setEnabled(True)
            self.view.chbx_coma.setEnabled(True)
            self.view.chbx_other_nonepileptic.setEnabled(True)
            self.view.chbx_uncertain.setEnabled(True)
        else:
            self.view.chbx_brain_death.setEnabled(False)
            self.view.chbx_diffuse_dysfunction.setEnabled(False)
            self.view.chbx_focal_dysfunction.setEnabled(False)
            self.view.chbx_pnes.setEnabled(False)
            self.view.chbx_coma.setEnabled(False)
            self.view.chbx_other_nonepileptic.setEnabled(False)
            self.view.chbx_uncertain.setEnabled(False)

    def update_model(self):
        self.model.update_from_dict(self.view.to_dict())

    def update_view(self):
        self.view.update_from_dict(self.model.to_dict())
        #self.abnormal_toggled()
