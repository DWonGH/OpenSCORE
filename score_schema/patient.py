"""SCORE §2 — Patient information and referral."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .common import ScoreModel


class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class Handedness(str, Enum):
    RIGHT = "right"
    LEFT = "left"
    AMBIDEXTROUS = "ambidextrous"
    UNKNOWN = "unknown"


class PatientInformation(ScoreModel):
    """SCORE §2. Aliases preserve OpenSCORE's legacy ``.score`` keys."""

    name: Optional[str] = Field(default=None, alias="Patient name")
    patient_id: Optional[str] = Field(default=None, alias="Patient ID")
    dob: Optional[str] = Field(default=None, alias="Patient DOB", description="Date of birth (ISO 8601 if known).")
    sex: Optional[Sex] = Field(default=None, alias="Patient gender")
    handedness: Optional[Handedness] = Field(default=None, alias="Patient handedness")
    address: Optional[str] = Field(default=None, alias="Patient address")
    medication: Optional[str] = Field(default=None, alias="Patient medication")
    history: Optional[str] = Field(default=None, alias="Patient history")


class Referral(ScoreModel):
    """SCORE §2 / Table 1 — referral details and indication for EEG."""

    referrer_name: Optional[str] = Field(default=None, alias="Referrer name")
    referrer_details: Optional[str] = Field(default=None, alias="Referrer details")
    diagnosis: Optional[str] = Field(default=None, alias="Diagnosis at referral", description="Free text or ICD-10 code.")
    seizure_frequency: Optional[str] = Field(default=None, alias="Seizure frequency")
    last_seizure: Optional[str] = Field(default=None, alias="Time since last seizure")
    # Indication groups (Table 1): "select all that apply". An empty list is unambiguous
    # ("none of these"), so these stay lists rather than per-item tristates.
    epilepsy_indications: list[str] = Field(default_factory=list, alias="Epilepsy-related indications")
    differential_indications: list[str] = Field(default_factory=list, alias="Other differential diagnostic questions")
    paediatric_indications: list[str] = Field(default_factory=list, alias="Specific paediatric indication")
    other_indications: Optional[str] = Field(default=None, alias="Other indications")
