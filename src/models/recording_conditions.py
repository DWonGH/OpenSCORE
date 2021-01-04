

class RecordingConditions:

    def __init__(self):

        self.study_id = None
        self.study_date = None
        self.recording_duration = None
        self.technologist_name = None
        self.physician_name = None
        self.sensor_group = None
        self.recording_type = None
        self.alertness = None
        self.cooperation = None
        self.age = None
        self.latest_meal = None
        self.skull_defect = None
        self.brain_surgery = None
        self.tech_description = None
        self.edf_location = None

    def to_dict(self):
        data = {
            "Study ID": self.study_id,
            "Date & Time": self.study_date,
            "Recording duration": self.recording_duration,
            "Technologist name": self.technologist_name,
            "Physician name": self.physician_name,
            "Sensor group": self.sensor_group,
            "Recording type": self.recording_type,
            "Alertness": self.alertness,
            "Cooperation": self.cooperation,
            "Patient age": self.age,
            "Latest meal": self.latest_meal,
            "Skull defect": self.skull_defect,
            "Brain surgery": self.brain_surgery,
            "Additional technical description": self.tech_description,
            "EDF location": self.edf_location
        }
        return data

    def update_from_dict(self, data):
        self.study_id = data["Study ID"]
        self.study_date = data["Date & Time"]
        self.recording_duration = data["Recording duration"]
        self.technologist_name = data["Technologist name"]
        self.physician_name = data["Physician name"]
        self.sensor_group = data["Sensor group"]
        self.recording_type = data["Recording type"]
        self.alertness = data["Alertness"]
        self.cooperation = data["Cooperation"]
        self.age = data["Patient age"]
        self.latest_meal = data["Latest meal"]
        self.skull_defect = data["Skull defect"]
        self.brain_surgery = data["Brain surgery"]
        self.tech_description = data["Additional technical description"]
        self.edf_location = data["EDF location"]

    def set_to_nones(self):
        self.study_id = None
        self.study_date = None
        self.recording_duration = None
        self.technologist_name = None
        self.physician_name = None
        self.sensor_group = None
        self.recording_type = None
        self.alertness = None
        self.cooperation = None
        self.age = None
        self.latest_meal = None
        self.skull_defect = None
        self.brain_surgery = None
        self.tech_description = None
        self.edf_location = None