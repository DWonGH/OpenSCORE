"""SCORE §8 — Interictal findings.

The single biggest gap in legacy OpenSCORE. Models epileptiform and abnormal rhythmic
interictal graphoelements with their localization and time-related features (Tables 5/6),
plus special/periodic patterns.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .common import Location, ScoreModel
from .background import Significance


class Morphology(str, Enum):
    """SCORE Table 5 — names/morphology of interictal findings."""

    # Epileptiform interictal activity
    SPIKE = "Spike"
    SPIKE_AND_SLOW_WAVE = "Spike-and-slow-wave"
    RUNS_OF_RAPID_SPIKES = "Runs of rapid spikes"
    POLYSPIKES = "Polyspikes"
    POLYSPIKE_AND_SLOW_WAVE = "Polyspike-and-slow-wave"
    SHARP_WAVE = "Sharp-wave"
    SHARP_AND_SLOW_WAVE = "Sharp-and-slow-wave"
    SLOW_SHARP_WAVE = "Slow sharp-wave"
    HFO = "High frequency oscillation (HFO)"
    HYPSARRHYTHMIA = "Hypsarrhythmia - classic"
    HYPSARRHYTHMIA_MODIFIED = "Hypsarrhythmia - modified"
    # Abnormal interictal rhythmic activity
    DELTA = "Delta activity"
    THETA = "Theta activity"
    ALPHA = "Alpha activity"
    BETA = "Beta activity"
    GAMMA = "Gamma activity"
    POLYMORPHIC_DELTA = "Polymorphic delta"
    FIRDA = "Frontal intermittent rhythmic delta activity (FIRDA)"
    OIRDA = "Occipital intermittent rhythmic delta activity (OIRDA)"
    TIRDA = "Temporal intermittent rhythmic delta activity (TIRDA)"


class ModeOfAppearance(str, Enum):
    RANDOM = "Random"
    PERIODIC = "Periodic"
    VARIABLE = "Variable"


class DischargePattern(str, Enum):
    SINGLE = "Single discharges"
    RHYTHMIC_TRAINS = "Rhythmic trains or bursts"
    ARRHYTHMIC_TRAINS = "Arrhythmic trains or bursts"
    FRAGMENTED = "Fragmented"


class Incidence(str, Enum):
    """SCORE Table 6 — incidence for single discharges."""

    ONLY_ONCE = "Only once"
    RARE = "Rare (less than 1/h)"
    UNCOMMON = "Uncommon (1/5 min to 1/h)"
    OCCASIONAL = "Occasional (1/min to 1/5min)"
    FREQUENT = "Frequent (1/10 s to 1/min)"
    ABUNDANT = "Abundant (>1/10 s)"


class Prevalence(str, Enum):
    """SCORE Table 6 — prevalence for trains/bursts."""

    RARE = "Rare (<1%)"
    OCCASIONAL = "Occasional (1-9%)"
    FREQUENT = "Frequent (10-49%)"
    ABUNDANT = "Abundant (50-89%)"
    CONTINUOUS = "Continuous (>90%)"


SPECIAL_PATTERNS = (
    "Periodic discharges not further specified (PDs)",
    "Generalized periodic discharges (GPDs)",
    "Lateralized periodic discharges (LPDs)",
    "Bilateral independent periodic discharges (BIPDs)",
    "Multifocal periodic discharges (MPDs)",
    "Extreme delta brush",
    "Burst suppression",
    "Burst attenuation",
)


class TimeRelatedFeatures(ScoreModel):
    """SCORE Table 6."""

    mode_of_appearance: Optional[ModeOfAppearance] = Field(default=None, alias="Mode of appearance")
    discharge_pattern: Optional[DischargePattern] = Field(default=None, alias="Discharge pattern")
    incidence: Optional[Incidence] = Field(default=None, alias="Incidence")
    prevalence: Optional[Prevalence] = Field(default=None, alias="Prevalence")


class InterictalGraphoelement(ScoreModel):
    """A single scored interictal finding (SCORE §8)."""

    morphology: Optional[Morphology] = Field(default=None, alias="Morphology")
    significance: Optional[Significance] = Field(default=None, alias="Significance")
    location: Location = Field(default_factory=Location, alias="Location")
    time_features: TimeRelatedFeatures = Field(default_factory=TimeRelatedFeatures, alias="Time-related features")
    modulator_effect: Optional[str] = Field(default=None, alias="Modulator effect")


class InterictalFindings(ScoreModel):
    """SCORE §8 container."""

    graphoelements: list[InterictalGraphoelement] = Field(default_factory=list, alias="Graphoelements")
    special_patterns: list[str] = Field(default_factory=list, alias="Special patterns")
