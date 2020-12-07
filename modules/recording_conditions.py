import os

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QTimeEdit, QSpinBox, \
    QComboBox, QTextEdit, QDateTimeEdit, QDoubleSpinBox, QHBoxLayout, QPushButton, QFileDialog


class RecordingConditionsTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # TODO: Add some form of loader to load EDF details into boxes e.g. EDF ID -> study id
        #  EDF time / date -> study time & date, edf recording duration -> Recording duration etc

        self.parent = parent
        self.layout = QFormLayout()

        self.layout.addRow(QLabel("Admin"))

        self.lbl_study_id = QLabel("Study ID")
        self.txe_study_id = QLineEdit()
        self.layout.addRow(self.lbl_study_id, self.txe_study_id)

        self.lbl_study_date = QLabel("Date & Time")
        self.dtm_study_date = QDateTimeEdit()
        self.dtm_study_date.setDateTime(QDateTime.currentDateTime())
        self.dtm_study_date.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_study_date, self.dtm_study_date)

        self.lbl_duration = QLabel("Recording Duration")
        self.spb_duration = QDoubleSpinBox()
        self.spb_duration.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_duration, self.spb_duration)

        self.lbl_technologist = QLabel("Technologist Name")
        self.txe_technologist = QLineEdit()
        self.layout.addRow(self.lbl_technologist, self.txe_technologist)

        self.lbl_physician = QLabel("Physician Name")
        self.txe_physician = QLineEdit()
        self.layout.addRow(self.lbl_physician, self.txe_physician)

        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Technical Description"))

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

        self.txt_alertness = ["", "Awake", "Drowsy", "Asleep", "Comatose"]
        self.lbl_alertness = QLabel("Alertness")
        self.cmb_alertness = QComboBox()
        self.cmb_alertness.addItems(self.txt_alertness)
        self.layout.addRow(self.lbl_alertness, self.cmb_alertness)

        self.txt_cooperation = ["", "Good cooperation", "Bad cooperation", "Unresponsive", "Comatose"]
        self.lbl_cooperation = QLabel("Cooperation")
        self.cmb_cooperation = QComboBox()
        self.cmb_cooperation.addItems(self.txt_cooperation)
        self.layout.addRow(self.lbl_cooperation, self.cmb_cooperation)

        self.lbl_age = QLabel("Age")
        self.spb_age = QSpinBox()
        self.spb_age.setSpecialValueText(" ")
        self.layout.addRow(self.lbl_age, self.spb_age)

        self.lbl_latest_meal = QLabel("Latest meal")
        self.dtm_latest_meal = QDateTimeEdit()
        self.dtm_latest_meal.setDateTime(QDateTime.currentDateTime())
        self.layout.addRow(self.lbl_latest_meal, self.dtm_latest_meal)

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

        self.lbl_recording_data = QLabel("Recorded data")
        self.hbx_recording_data = QHBoxLayout()
        self.txe_recording_data = QLineEdit()
        self.hbx_recording_data.addWidget(self.txe_recording_data)
        self.btn_recording_data = QPushButton("Browse")
        self.btn_recording_data.clicked.connect(self.hdl_recording_data)
        self.hbx_recording_data.addWidget(self.btn_recording_data)
        self.layout.addRow(self.lbl_recording_data, self.hbx_recording_data)

        self.setLayout(self.layout)

    def get_fields(self):
        recording_conditions = {
            "Study ID": self.txe_study_id.text(),
            "Date & Time": self.dtm_study_date.text(),
            "Recording duration": self.spb_duration.text(),
            "Technologist name": self.txe_technologist.text(),
            "Physician name": self.txe_physician.text(),
            "Sensor group": self.cmb_sensor_group.currentText(),
            "Recording type": self.cmb_recording_type.currentText(),
            "Alertness": self.cmb_alertness.currentText(),
            "Cooperation": self.cmb_cooperation.currentText(),
            "Patient age": self.spb_age.text(),
            "Latest meal": self.dtm_latest_meal.text(),
            "Skull defect": self.cmb_skull_defect.currentText(),
            "Brain surgery": self.cmb_brain_surgery.currentText(),
            "Additional technical description": self.txe_tech_description.toPlainText(),
            "Recording data": self.txe_recording_data.text()
        }
        return recording_conditions

    def set_fields(self, data):
        print(data)
        self.txe_study_id.setText(data["Study ID"])
        self.dtm_study_date.setDateTime(QDateTime.fromString(data["Date & Time"]))
        if data["Recording duration"] != ' ': self.spb_duration.setValue(float(data["Recording duration"]))
        self.txe_technologist.setText(data["Technologist name"])
        self.txe_physician.setText(data["Physician name"])
        self.cmb_sensor_group.setCurrentIndex(self.txt_sensor_group.index(data["Sensor group"]))
        self.cmb_recording_type.setCurrentIndex(self.txt_recording_type.index(data["Recording type"]))
        self.cmb_alertness.setCurrentIndex(self.txt_alertness.index(data["Alertness"]))
        self.cmb_cooperation.setCurrentIndex(self.txt_cooperation.index(data["Cooperation"]))
        if data["Patient age"] != ' ': self.spb_age.setValue(int(data["Patient age"]))
        self.dtm_latest_meal.setDateTime(QDateTime.fromString(data["Latest meal"]))
        self.cmb_skull_defect.setCurrentIndex(self.txt_skull_defect.index(data["Skull defect"]))
        self.cmb_brain_surgery.setCurrentIndex(self.txt_brain_surgery.index(data["Brain surgery"]))
        self.txe_tech_description.setText(data["Additional technical description"])
        self.txe_recording_data.setText(data["Recording data"])
        self.parent.parent.current_edf_path = data["Recording data"]
        self.parent.parent.toolbar.lbl_current_eeg_name.setText(os.path.basename(data["Recording data"]).strip('.edf'))

    def hdl_recording_data(self):
        try:
            browse_data, _ = QFileDialog.getOpenFileName(self, caption="Select associated recording", filter="EDF files (*.edf)")
            if browse_data:
                self.txe_recording_data.setText(browse_data)
                self.parent.parent.ui_model.current_edf_path = browse_data
                self.parent.parent.toolbar.lbl_current_eeg_name.setText(os.path.basename(self.txe_recording_data.text()).strip('.edf'))
        except Exception as e:
            print(f"Exception choosing the associated recording {e}")