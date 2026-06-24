"""SCORE §8 — Interictal findings.

The single biggest gap in legacy OpenSCORE. Models epileptiform and abnormal rhythmic
interictal graphoelements with their localization and time-related features (Tables 5/6),
plus special/periodic patterns.

Enum *values* are the node names of the HED-SCORE library schema (``score_2.1.0``,
Modulator/Interictal-activity/Feature-property branches), so a finding's value is also its
HED short tag. See ``score_schema.hed``.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .common import Location, ScoreModel
from .background import Significance


class Morphology(str, Enum):
    """SCORE Table 5 — names/morphology of interictal findings (HED-SCORE node names)."""

    # Epileptiform interictal activity (HED Feature-property/Signal-morphology-property)
    SPIKE = "Spike"
    SPIKE_AND_SLOW_WAVE = "Spike-and-slow-wave"
    RUNS_OF_RAPID_SPIKES = "Runs-of-rapid-spikes"
    POLYSPIKES = "Polyspikes"
    POLYSPIKE_AND_SLOW_WAVE = "Polyspike-and-slow-wave"
    SHARP_WAVE = "Sharp-wave"
    SHARP_AND_SLOW_WAVE = "Sharp-and-slow-wave"
    SLOW_SHARP_WAVE = "Slow-sharp-wave"
    HFO = "High-frequency-oscillation"
    HYPSARRHYTHMIA = "Hypsarrhythmia-classic"
    HYPSARRHYTHMIA_MODIFIED = "Hypsarrhythmia-modified"
    POLYSHARP_WAVES = "Polysharp-waves"
    # Abnormal interictal rhythmic activity (HED Signal-morphology-property/Rhythmic-property)
    DELTA = "Delta-activity"
    THETA = "Theta-activity"
    ALPHA = "Alpha-activity"
    BETA = "Beta-activity"
    GAMMA = "Gamma-activity"
    POLYMORPHIC_DELTA = "Polymorphic-delta-activity"
    FIRDA = "Frontal-intermittent-rhythmic-delta-activity"
    OIRDA = "Occipital-intermittent-rhythmic-delta-activity"
    TIRDA = "Temporal-intermittent-rhythmic-delta-activity"


class ModeOfAppearance(str, Enum):
    """SCORE Table 6 — mode of appearance (HED Time-related-property/Appearance-mode)."""

    RANDOM = "Random"
    PERIODIC = "Periodic"
    VARIABLE = "Variable"


class DischargePattern(str, Enum):
    """HED Time-related-property/Discharge-pattern."""

    SINGLE = "Single-discharge"
    RHYTHMIC_TRAINS = "Rhythmic-trains-or-bursts"
    ARRHYTHMIC_TRAINS = "Arrhythmic-trains-or-bursts"
    FRAGMENTED = "Fragmented-discharge"


class Incidence(str, Enum):
    """SCORE Table 6 incidence for single discharges (HED Feature-incidence)."""

    ONLY_ONCE = "One-time-incidence"
    RARE = "Rare-feature-incidence"
    UNCOMMON = "Uncommon-feature-incidence"
    OCCASIONAL = "Occasional-feature-incidence"
    FREQUENT = "Frequent-feature-incidence"
    ABUNDANT = "Abundant-feature-incidence"


class Prevalence(str, Enum):
    """SCORE Table 6 prevalence for trains/bursts (HED Feature-prevalence)."""

    RARE = "Rare-prevalence"
    OCCASIONAL = "Occasional-prevalence"
    FREQUENT = "Frequent-prevalence"
    ABUNDANT = "Abundant-prevalence"
    CONTINUOUS = "Continuous-prevalence"


# HED Interictal-activity/Interictal-special-patterns (periodic discharges live here;
# burst-suppression/attenuation are HED Background-activity features, not interictal).
SPECIAL_PATTERNS = (
    "Generalized-periodic-discharges",
    "Lateralized-periodic-discharges",
    "Bilateral-independent-periodic-discharges",
    "Multifocal-periodic-discharges",
    "Extreme-delta-brush",
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
    # Optional explicit HED-SCORE tag string(s) for BIDS/HED export of this finding.
    hed_tags: list[str] = Field(default_factory=list, alias="HED tags")


class InterictalFindings(ScoreModel):
    """SCORE §8 container."""

    graphoelements: list[InterictalGraphoelement] = Field(default_factory=list, alias="Graphoelements")
    special_patterns: list[str] = Field(default_factory=list, alias="Special patterns")
