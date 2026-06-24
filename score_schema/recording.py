"""SCORE §3 — Recording conditions; SCORE §4 — Modulators and procedures."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .common import ScoreModel, Ternary


class RecordingType(str, Enum):
    """SCORE §3 type of EEG recording."""

    STANDARD = "standard EEG"
    SLEEP = "sleep EEG"
    SHORT_TERM_VIDEO = "short-term video-EEG monitoring"
    LONG_TERM_VIDEO = "long-term video-EEG monitoring (LTM)"
    AMBULATORY = "ambulatory recording"
    ICU = "recording in the ICU"
    INTRAOPERATIVE = "intraoperative monitoring"


# SCORE §3 alertness/cooperation multiple-choice list (issue #17 — multi-select).
ALERTNESS_CHOICES = (
    "awake", "oriented", "good cooperation", "poor cooperation",
    "disoriented", "drowsy", "asleep", "unresponsive", "comatose",
)


class RecordingConditions(ScoreModel):
    """SCORE §3. Aliases preserve OpenSCORE's legacy ``.score`` keys."""

    study_id: Optional[str] = Field(default=None, alias="Study ID")
    study_date: Optional[str] = Field(default=None, alias="Date & Time")
    recording_duration: Optional[str] = Field(default=None, alias="Recording duration")
    technologist_name: Optional[str] = Field(default=None, alias="Technologist name")
    physician_name: Optional[str] = Field(default=None, alias="Physician name")
    sensor_group: Optional[str] = Field(default=None, alias="Sensor group")
    recording_type: Optional[RecordingType] = Field(default=None, alias="Recording type")
    # Issue #17: alertness can vary during a recording -> multiple choice.
    alertness: list[str] = Field(default_factory=list, alias="Alertness")
    cooperation: Optional[str] = Field(default=None, alias="Cooperation")
    age: Optional[str] = Field(default=None, alias="Patient age")
    latest_meal: Optional[str] = Field(default=None, alias="Latest meal")
    skull_defect: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Skull defect")
    brain_surgery: Optional[str] = Field(default=None, alias="Brain surgery")
    tech_description: Optional[str] = Field(default=None, alias="Additional technical description")
    edf_location: Optional[str] = Field(default=None, alias="EDF location")


class HyperventilationQuality(str, Enum):
    EXCELLENT = "excellent effort"
    GOOD = "good effort"
    POOR = "poor effort"
    REFUSED = "refused the procedure"
    UNABLE = "unable to do the procedure"


class ModulatorsAndProcedures(ScoreModel):
    """SCORE §4 / Table 2 — provocation methods and medication during the recording.

    New module (absent in legacy OpenSCORE). Each procedure records whether it was done
    (tristate) and, where relevant, a graded quality and its effect on the EEG.
    """

    photic_stimulation: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Intermittent photic stimulation")
    photic_effect: Optional[str] = Field(default=None, alias="Photic stimulation effect")
    hyperventilation: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Hyperventilation")
    hyperventilation_quality: Optional[HyperventilationQuality] = Field(default=None, alias="Hyperventilation quality")
    hyperventilation_effect: Optional[str] = Field(default=None, alias="Hyperventilation effect")
    sleep_deprivation: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Sleep deprivation")
    natural_sleep: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Natural sleep")
    induced_sleep: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Induced sleep")
    awakening: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Awakening")
    medication_administered: Optional[str] = Field(default=None, alias="Medication administered during recording")
    medication_withdrawn: Optional[str] = Field(default=None, alias="Medication withdrawal or reduction during recording")
    other_modulators: Optional[str] = Field(default=None, alias="Other modulators and procedures")
