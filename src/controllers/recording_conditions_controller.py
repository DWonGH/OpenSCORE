import os
import traceback

from PyQt5.QtWidgets import QFileDialog

from src.models.recording_conditions import RecordingConditions
from src.views.recording_conditions import RecordingConditionsWidget


class RecordingConditionsController:

    def __init__(self, parent=None):
        self.parent = parent
        self.model = RecordingConditions()
        self.view = RecordingConditionsWidget()
        self.view.btn_edf_location.clicked.connect(self.hdl_edf_location)

    def hdl_edf_location(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(caption="Select associated recording", filter="EDF files (*.edf)")
            if file_path:
                self.view.lne_edf_location.setText(file_path)
                self.update_model()
                self.parent.model.set_edf(file_path)
                self.parent.view.toolbar.lbl_current_eeg_name.setText(os.path.basename(file_path).strip('.')[0])
        except Exception as e:
            traceback.print_exc()

    def update_model(self):
        self.model.update_from_dict(self.view.to_dict())

    def update_view(self):
        self.view.update_from_dict(self.model.to_dict())