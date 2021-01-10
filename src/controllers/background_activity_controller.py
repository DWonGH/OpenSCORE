import traceback

from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from src.dialogs.add_rhythm import AddRhythmDialog
from src.models.background_activity import BackgroundActivity, Rhythm
from src.views.background_activity import BackgroundActivityWidget


class BackgroundActivityController:

    def __init__(self):
        self.model = BackgroundActivity()
        self.view = BackgroundActivityWidget()

        self.view.chbx_pdr_freq_asymmetry.toggled.connect(self.toggle_pdr_symmetry)
        self.view.lne_pdr_freq_asymmetry_left.textChanged.connect(self.toggle_pdr_symmetry)
        self.view.lne_pdr_freq_asymmetry_right.textChanged.connect(self.toggle_pdr_symmetry)
        self.view.btn_add_rhythm.clicked.connect(self.hdl_add_rhythm)
        self.view.btn_edit_rhythm.clicked.connect(self.hdl_edit_rhythm)
        self.view.btn_delete_rhythm.clicked.connect(self.hdl_delete_rhythm)

    def hdl_add_rhythm(self):
        try:
            dialog = AddRhythmDialog()
            if dialog.exec_():
                data = dialog.to_dict()
                print(data)
                self.view.rhythm_table.new_rhythm(data)
                #self.update_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_edit_rhythm(self):
        try:
            current_rhythm = self.view.rhythm_table.current_rhythm()
            print(f"current rhythm {current_rhythm}")
            if current_rhythm is not False:
                if current_rhythm is not None:
                    dialog = AddRhythmDialog()
                    dialog.from_dict(current_rhythm)
                    if dialog.exec_():
                        data = dialog.to_dict()
                        self.view.rhythm_table.edit_rhythm(data)
                else:
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Edit Rhythm")
                    dialog.setText("Select a rhythm from the table.")
                    dialog.setStandardButtons(QMessageBox.Ok)
                    dialog.setIcon(QMessageBox.Information)
                    dialog.exec_()
                # self.update_model()
        except Exception as e:
            traceback.print_exc()

    def hdl_delete_rhythm(self):
        self.view.rhythm_table.delete_current_rhythm()

    def toggle_pdr_symmetry(self):
        if self.view.chbx_pdr_freq_asymmetry.isChecked() and (self.view.lne_pdr_freq_asymmetry_left.text() == "") and (self.view.lne_pdr_freq_asymmetry_right.text() == ""):
            self.view.chbx_pdr_freq_asymmetry.setEnabled(True)
            self.view.lne_pdr_freq_asymmetry_left.setEnabled(False)
            self.view.lne_pdr_freq_asymmetry_right.setEnabled(False)
        elif (self.view.chbx_pdr_freq_asymmetry.isChecked() is False) and (self.view.lne_pdr_freq_asymmetry_left.text() == "") and (self.view.lne_pdr_freq_asymmetry_right.text() == ""):
            self.view.chbx_pdr_freq_asymmetry.setEnabled(True)
            self.view.lne_pdr_freq_asymmetry_left.setEnabled(True)
            self.view.lne_pdr_freq_asymmetry_right.setEnabled(True)
        elif (self.view.chbx_pdr_freq_asymmetry.isChecked() is False) and (self.view.lne_pdr_freq_asymmetry_left.text() != "") and (self.view.lne_pdr_freq_asymmetry_right.text() == ""):
            self.view.chbx_pdr_freq_asymmetry.setEnabled(False)
            self.view.lne_pdr_freq_asymmetry_left.setEnabled(True)
            self.view.lne_pdr_freq_asymmetry_right.setEnabled(False)
        elif (self.view.chbx_pdr_freq_asymmetry.isChecked() is False) and (self.view.lne_pdr_freq_asymmetry_left.text() == "") and (self.view.lne_pdr_freq_asymmetry_right.text() != ""):
            self.view.chbx_pdr_freq_asymmetry.setEnabled(False)
            self.view.lne_pdr_freq_asymmetry_left.setEnabled(False)
            self.view.lne_pdr_freq_asymmetry_right.setEnabled(True)

    def update_model(self):
        self.model.update_from_dict(self.view.to_dict())

    def update_view(self):
        self.view.update_from_dict(self.model.to_dict())
