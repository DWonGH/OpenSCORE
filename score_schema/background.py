"""SCORE §6 — Background activity; SCORE §7 — Sleep and drowsiness."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .common import ScoreModel, Ternary


class Significance(str, Enum):
    NORMAL = "Normal"
    NO_DEFINITE_ABNORMALITY = "No definite abnormality"
    ABNORMAL = "Abnormal"


class FrequencyAsymmetry(str, Enum):
    SYMMETRICAL = "Symmetrical"
    LOWER_LEFT = "Hz lower on the left side"
    LOWER_RIGHT = "Hz lower on the right side"


class Amplitude(str, Enum):
    LOW = "Low (<20 uV)"
    MEDIUM = "Medium (20-70 uV)"
    HIGH = "High (>70 uV)"


class AmplitudeAsymmetry(str, Enum):
    SYMMETRICAL = "Symmetrical"
    RIGHT_LESS_LEFT = "Right < Left"
    LEFT_LESS_RIGHT = "Left < Right"


class Reactivity(str, Enum):
    YES = "Yes"
    REDUCED_LEFT = "Reduced left side reactivity"
    REDUCED_RIGHT = "Reduced right side reactivity"
    REDUCED_BOTH = "Reduced reactivity on both sides"


class Organisation(str, Enum):
    NORMAL = "Normal"
    POORLY_ORGANISED = "Poorly organized"
    DISORGANISED = "Disorganized"
    MARKEDLY_DISORGANISED = "Markedly disorganized"


class PdrCaveat(str, Enum):
    NO = "No"
    ONLY_OPEN_EYES = "Only open eyes during the recording"
    SLEEP_DEPRIVED = "Sleep-deprived"
    DROWSY = "Drowsy"
    ONLY_DURING_HV = "Only following hyperventilation"


class PdrAbsence(str, Enum):
    ARTIFACTS = "Artifacts"
    EXTREME_LOW_VOLTAGE = "Extreme low voltage"
    NO_EYE_CLOSURE = "Eye-closure could not be achieved"
    NO_AWAKE_PERIOD = "Lack of awake period"
    NO_COMPLIANCE = "Lack of compliance"
    OTHER = "Other causes"


class SpectralBand(str, Enum):
    DELTA = "Delta"
    THETA = "Theta"
    ALPHA = "Alpha"
    BETA = "Beta"
    GAMMA = "Gamma"


class PosteriorDominantRhythm(ScoreModel):
    """SCORE §6 / Table 4. Aliases preserve legacy ``.score`` PDR keys."""

    significance: Optional[Significance] = Field(default=None, alias="Significance")
    frequency: Optional[float] = Field(default=None, alias="Frequency", description="Hz")
    frequency_asymmetry: Optional[FrequencyAsymmetry] = Field(default=None, alias="Frequency asymmetry")
    frequency_lower_left: Optional[float] = Field(default=None, alias="Hz lower left")
    frequency_lower_right: Optional[float] = Field(default=None, alias="Hz lower right")
    amplitude: Optional[Amplitude] = Field(default=None, alias="Amplitude")
    amplitude_asymmetry: Optional[AmplitudeAsymmetry] = Field(default=None, alias="Amplitude asymmetry")
    eye_opening: Optional[Reactivity] = Field(default=None, alias="Reactivity to eye opening")
    organisation: Optional[Organisation] = Field(default=None, alias="Organisation")
    caveat: Optional[PdrCaveat] = Field(default=None, alias="Caveat")
    absence: Optional[PdrAbsence] = Field(default=None, alias="Absence of PDR")


class OrganisedRhythm(ScoreModel):
    """SCORE §6 — an organised rhythm other than the PDR (e.g. mu)."""

    classification: Optional[str] = Field(default=None, alias="Classification", description="e.g. Mu, Other")
    significance: Optional[Significance] = Field(default=None, alias="Significance")
    spectral: Optional[SpectralBand] = Field(default=None, alias="Spectral frequency")
    frequency: Optional[float] = Field(default=None, alias="Frequency", description="Hz")
    amplitude: Optional[Amplitude] = Field(default=None, alias="Amplitude")
    modulator: Optional[str] = Field(default=None, alias="Modulator", description="e.g. hyperventilation")
    modulator_effect: Optional[str] = Field(default=None, alias="Modulator effect")


class BackgroundActivity(ScoreModel):
    """SCORE §6 container."""

    pdr: PosteriorDominantRhythm = Field(default_factory=PosteriorDominantRhythm, alias="Posterior dominant rhythm")
    other_rhythms: list[OrganisedRhythm] = Field(default_factory=list, alias="Other organised rhythms")
    critical_features: Optional[str] = Field(default=None, alias="Critically ill background activity")


# --- SCORE §7 -------------------------------------------------------------------------

# HED-SCORE Sleep-and-drowsiness node names.
NORMAL_SLEEP_GRAPHOELEMENTS = (
    "Sleep-spindles", "Vertex-wave", "K-complex", "Saw-tooth-waves",
    "POSTS", "Hypnagogic-hypersynchrony",
)
SLEEP_STAGES = ("Sleep-stage-N1", "Sleep-stage-N2", "Sleep-stage-N3", "Sleep-stage-REM")


class SleepAndDrowsiness(ScoreModel):
    """SCORE §7 — sleep and drowsiness features. New module (absent in legacy OpenSCORE)."""

    normal_graphoelements: list[str] = Field(default_factory=list, alias="Normal sleep graphoelements")
    achieved_stages: list[str] = Field(default_factory=list, alias="Achieved sleep stages")
    abnormal_asymmetry: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Abnormal asymmetry of sleep graphoelements")
    soremp: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Sleep-onset REM period (SOREMP)")
    non_reactive_sleep: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Non-reactive sleep activity")
    notes: Optional[str] = Field(default=None, alias="Notes")
