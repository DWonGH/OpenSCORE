import os

from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QSpinBox, \
    QComboBox, QTextEdit, QDoubleSpinBox, QHBoxLayout, QPushButton, QFileDialog, \
    QListWidget, QAbstractItemView

from src.views.custom_widgets import IntegerLineEdit, FloatLineEdit
from src.views.form_helpers import set_combo
from score_schema import ALERTNESS_CHOICES


class RecordingConditionsWidget(QWidget):

    def __init__(self, parent=None):

        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QFormLayout()

        #self.layout.addRow(QLabel("Admin"))

        self.lbl_study_id = QLabel("Study ID")
        self.lne_study_id = QLineEdit()
        self.layout.addRow(self.lbl_study_id, self.lne_study_id)

        self.lbl_study_date = QLabel("Date & Time")
        self.lne_study_date = QLineEdit()
        self.lne_study_date.setPlaceholderText("e.g. 30/09/2012")
        self.layout.addRow(self.lbl_study_date, self.lne_study_date)

        self.lbl_duration = QLabel("Recording Duration (mins)")
        self.lne_duration = FloatLineEdit()
        self.layout.addRow(self.lbl_duration, self.lne_duration)

        self.lbl_technologist = QLabel("Technologist Name")
        self.lne_technologist = QLineEdit()
        self.layout.addRow(self.lbl_technologist, self.lne_technologist)

        self.lbl_physician = QLabel("Physician Name")
        self.lne_physician = QLineEdit()
        self.layout.addRow(self.lbl_physician, self.lne_physician)

        self.layout.addRow(QLabel(""))
        #self.layout.addRow(QLabel("Technical Description"))

        self.txt_sensor_group = ["",
                                 "Bipolar old longitudinal",
                                 "Bipolar new longitudinal",
                                 "Bipolar old transverse",
                                 "Bipolar new transverse",
                                 "Referential"]
        self.lbl_sensor_group = QLabel("Sensor Group")
        self.cmb_sensor_group = QComboBox()
        self.cmb_sensor_group.addItems(self.txt_sensor_group)
        self.layout.addRow(self.lbl_sensor_group, self.cmb_sensor_group)

        self.txt_recording_type = ["",
                                   "Standard EEG",
                                   "Sleep EEG",
                                   "Short-term video-EEG",
                                   "Long-term video-EEG",
                                   "Ambulatory recording",
                                   "Recording in the ICU",
                                   "Intraoperative recording"]
        self.lbl_recording_type = QLabel("Recording Type")
        self.cmb_recording_type = QComboBox()
        self.cmb_recording_type.addItems(self.txt_recording_type)
        self.layout.addRow(self.lbl_recording_type, self.cmb_recording_type)

        # Issue #17: alertness can vary across a recording -> multiple selection.
        self.txt_alertness = list(ALERTNESS_CHOICES)
        self.lbl_alertness = QLabel("Alertness")
        self.lst_alertness = QListWidget()
        self.lst_alertness.addItems(self.txt_alertness)
        self.lst_alertness.setSelectionMode(QAbstractItemView.MultiSelection)
        self.lst_alertness.setMaximumHeight(120)
        self.layout.addRow(self.lbl_alertness, self.lst_alertness)

        self.txt_cooperation = ["", "Good cooperation", "Bad cooperation", "Unresponsive", "Comatose"]
        self.lbl_cooperation = QLabel("Cooperation")
        self.cmb_cooperation = QComboBox()
        self.cmb_cooperation.addItems(self.txt_cooperation)
        self.layout.addRow(self.lbl_cooperation, self.cmb_cooperation)

        self.lbl_age = QLabel("Age")
        self.lne_age = IntegerLineEdit()
        self.layout.addRow(self.lbl_age, self.lne_age)

        self.lbl_latest_meal = QLabel("Latest meal")
        self.lne_latest_meal = QLineEdit()
        self.lne_latest_meal.setPlaceholderText("e.g. 30/09/2012")
        self.layout.addRow(self.lbl_latest_meal, self.lne_latest_meal)

        # TODO: Find standard terms for skull defect locations
        self.txt_skull_defect = ["", "None", "Top", "Right", "Left", "Front", "Back"]
        self.lbl_skull_defect = QLabel("Skull Defect")
        self.cmb_skull_defect = QComboBox()
        self.cmb_skull_defect.addItems(self.txt_skull_defect)
        self.layout.addRow(self.lbl_skull_defect, self.cmb_skull_defect)

        # TODO: Find standard terms for brain surgery locations
        self.txt_brain_surgery = ["", "None", "Top", "Right", "Left", "Front", "Back"]
        self.lbl_brain_surgery = QLabel("Brain Surgery")
        self.cmb_brain_surgery = QComboBox()
        self.cmb_brain_surgery.addItems(self.txt_brain_surgery)
        self.layout.addRow(self.lbl_brain_surgery, self.cmb_brain_surgery)

        self.lbl_tech_description = QLabel("Additional technical description")
        self.txe_tech_description = QTextEdit()
        self.layout.addRow(self.lbl_tech_description, self.txe_tech_description)

        self.lbl_edf_location = QLabel("EDF location")
        self.hbx_edf_location = QHBoxLayout()
        self.lne_edf_location = QLineEdit()
        self.hbx_edf_location.addWidget(self.lne_edf_location)
        self.btn_edf_location = QPushButton("Browse")
        self.hbx_edf_location.addWidget(self.btn_edf_location)
        self.layout.addRow(self.lbl_edf_location, self.hbx_edf_location)

        self.setLayout(self.layout)

    def selected_alertness(self):
        """Return the list of ticked alertness states, in display order (issue #17)."""
        return [self.lst_alertness.item(i).text()
                for i in range(self.lst_alertness.count())
                if self.lst_alertness.item(i).isSelected()]

    def set_alertness(self, values):
        """Select the alertness items present in ``values`` (tolerates None / legacy str)."""
        self.lst_alertness.clearSelection()
        if values is None:
            return
        if isinstance(values, str):  # legacy single-value files
            values = [values] if values else []
        for i in range(self.lst_alertness.count()):
            item = self.lst_alertness.item(i)
            if item.text() in values:
                item.setSelected(True)

    def to_dict(self):
        data = {
            "Study ID": self.lne_study_id.text(),
            "Date & Time": self.lne_study_date.text(),
            "Recording duration": self.lne_duration.text(),
            "Technologist name": self.lne_technologist.text(),
            "Physician name": self.lne_physician.text(),
            "Sensor group": self.cmb_sensor_group.currentText(),
            "Recording type": self.cmb_recording_type.currentText(),
            "Alertness": self.selected_alertness(),
            "Cooperation": self.cmb_cooperation.currentText(),
            "Patient age": self.lne_age.text(),
            "Latest meal": self.lne_latest_meal.text(),
            "Skull defect": self.cmb_skull_defect.currentText(),
            "Brain surgery": self.cmb_brain_surgery.currentText(),
            "Additional technical description": self.txe_tech_description.toPlainText(),
            "EDF location": self.lne_edf_location.text()
        }
        return data

    def update_from_dict(self, data):
        self.lne_study_id.setText(data["Study ID"])
        self.lne_study_date.setText(data["Date & Time"])
        self.lne_duration.setText(data["Recording duration"])
        self.lne_technologist.setText(data["Technologist name"])
        self.lne_physician.setText(data["Physician name"])
        set_combo(self.cmb_sensor_group, data["Sensor group"])
        set_combo(self.cmb_recording_type, data["Recording type"])
        self.set_alertness(data.get("Alertness"))
        set_combo(self.cmb_cooperation, data["Cooperation"])
        self.lne_age.setText(data["Patient age"])
        self.lne_latest_meal.setText(data["Latest meal"])
        set_combo(self.cmb_skull_defect, data["Skull defect"])
        set_combo(self.cmb_brain_surgery, data["Brain surgery"])
        self.txe_tech_description.setText(data["Additional technical description"])
        self.lne_edf_location.setText(data["EDF location"])
