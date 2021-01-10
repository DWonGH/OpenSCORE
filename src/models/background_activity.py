

class PosteriorDominantRhythm:

    def __init__(self):
        self.significance = None
        self.frequency = None
        self.frequency_asymmetry = None
        self.frequency_lower_left = None
        self.frequency_lower_right = None
        self.amplitude = None
        self.amplitude_asymmetry = None
        self.eye_opening = None
        self.organisation = None
        self.caveat = None
        self.absence = None

    def to_dict(self):
        data = {
            "Significance": self.significance,
            "Frequency": self.frequency,
            "Frequency asymmetry": self.frequency_asymmetry,
            "Hz lower left": self.frequency_lower_left,
            "Hz lower right": self.frequency_lower_right,
            "Amplitude": self.amplitude,
            "Amplitude asymmetry": self.amplitude_asymmetry,
            "Reactivity to eye opening": self.eye_opening,
            "Organisation": self.organisation,
            "Caveat": self.caveat,
            "Absence of PDR": self.absence
        }
        return data

    def from_dict(self, data):
        self.significance = data["Significance"]
        self.frequency = data["Frequency"]
        self.frequency_asymmetry = data["Frequency asymmetry"]
        self.frequency_lower_left = data["Hz lower left"]
        self.frequency_lower_right = data["Hz lower right"]
        self.amplitude = data["Amplitude"]
        self.amplitude_asymmetry = data["Amplitude asymmetry"]
        self.eye_opening = data["Reactivity to eye opening"]
        self.organisation = data["Organisation"]
        self.caveat = data["Caveat"]
        self.absence = data["Absence of PDR"]

    def set_to_nones(self):
        self.significance = None
        self.frequency = None
        self.frequency_asymmetry = None
        self.frequency_lower_left = None
        self.frequency_lower_right = None
        self.amplitude = None
        self.amplitude_asymmetry = None
        self.eye_opening = None
        self.organisation = None
        self.caveat = None
        self.absence = None


class Rhythm:

    def __init__(self):
        self.classification = None  # E.g. Mu, Other
        self.significance = None
        self.spectral = None  # E.g. Delta, Theta
        self.frequency = None  # hz
        self.amplitude = None  # μV
        self.modulator = None  # e.g. hyperventilation
        self.modulator_effect = None  # impact of hyperventilation

    def to_dict(self):
        data = {
            "Significance": self.significance,
            "Spectral frequency": self.spectral,
            "Frequency": self.frequency,
            "Amplitude": self.amplitude,
            "Modulator effect": self.modulator_effect
        }
        return data

    def from_dict(self, data):
        self.significance = data["Significance"]
        self.spectral = data["Spectral frequency"]
        self.frequency = data["Frequency"]
        self.amplitude = data["Amplitude"]
        self.modulator_effect = data["Modulator effect"]

    def set_to_nones(self):
        self.classification = None  # E.g. Mu, Other
        self.significance = None
        self.spectral = None  # E.g. Delta, Theta
        self.frequency = None  # hz
        self.amplitude = None  # μV
        self.modulator = None  # e.g. hyperventilation
        self.modulator_effect = None  # impact of hyperventilation


class BackgroundActivity:

    def __init__(self):
        self.pdr = PosteriorDominantRhythm()
        self.other_rhythms = []
        self.critical_features = None

    def other_rhythms_to_dict(self):
        data = []
        for rhythm in self.other_rhythms:
            data.append(rhythm.to_dict())
        return data

    def other_rhythms_from_dict(self, data):
        self.other_rhythms = []
        for rhythm in data:
            r = Rhythm()
            r.significance = rhythm["Significance"]
            r.spectral = rhythm["Spectral frequency"]
            r.frequency = rhythm["Frequency"]
            r.amplitude = rhythm["Amplitude"]
            r.modulator_effect = rhythm["Modulator effect"]
            self.other_rhythms.append(r)

    def to_dict(self):
        data = {
            "Posterior dominant rhythm": self.pdr.to_dict(),
            "Other organised rhythms": self.other_rhythms_to_dict(),
            "Critically ill background activity": self.critical_features
        }
        return data

    def update_from_dict(self, data):
        self.pdr.from_dict(data["Posterior dominant rhythm"])
        self.other_rhythms_from_dict(data["Other organised rhythms"])
        self.critical_features = data["Critically ill background activity"]

    def set_to_nones(self):
        self.pdr.set_to_nones()
        self.other_rhythms = []
        self.critical_features = None