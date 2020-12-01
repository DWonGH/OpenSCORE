from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QTimeEdit, QSpinBox, \
    QComboBox, QTextEdit, QDateTimeEdit, QDoubleSpinBox


class RecordingConditionsTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # TODO: Add some form of loader to load EDF details into boxes e.g. EDF ID -> study id
        #  EDF time / date -> study time & date, edf recording duration -> Recording duration etc

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

        self.setLayout(self.layout)

    def get_details(self):
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
            "Additional technical description": self.txe_tech_description.toPlainText()
        }
        return recording_conditions
