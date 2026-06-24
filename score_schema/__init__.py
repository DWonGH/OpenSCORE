"""score_schema — a SCORE-2017-aligned schema for EEG reports.

The canonical, language-neutral artefact is the exported JSON Schema (see
``score_schema.export_schema``); the Pydantic models here are the authoring binding and the
single source of truth for both OpenSCORE (authoring/validation) and any future
schema-constrained LLM extraction.
"""

from __future__ import annotations

from .common import Laterality, Location, Provenance, Region, ScoreModel, Ternary
from .patient import Handedness, PatientInformation, Referral, Sex
from .recording import (
    ALERTNESS_CHOICES,
    HyperventilationQuality,
    ModulatorsAndProcedures,
    RecordingConditions,
    RecordingType,
)
from .background import (
    Amplitude,
    BackgroundActivity,
    OrganisedRhythm,
    Organisation,
    PdrAbsence,
    PdrCaveat,
    PosteriorDominantRhythm,
    Reactivity,
    Significance,
    SleepAndDrowsiness,
    SpectralBand,
)
from .interictal import (
    DischargePattern,
    Incidence,
    InterictalFindings,
    InterictalGraphoelement,
    ModeOfAppearance,
    Morphology,
    Prevalence,
    TimeRelatedFeatures,
)
from .episodes import Consciousness, Episode, EpisodeType, Episodes, PhaseName, SemiologyPhase
from .diagnostic import ClinicalComments, Diagnosis, DiagnosticSignificance, IlaeClassification
from .hed import HED_LIBRARY_PREFIX, HED_SCORE_VERSION, hed_short_tag, hed_tag
from .report import SCHEMA_VERSION, EegReport, validate

__all__ = [
    "SCHEMA_VERSION",
    "EegReport",
    "validate",
    # HED-SCORE binding
    "HED_SCORE_VERSION",
    "HED_LIBRARY_PREFIX",
    "hed_short_tag",
    "hed_tag",
    # common
    "ScoreModel",
    "Ternary",
    "Laterality",
    "Region",
    "Location",
    "Provenance",
    # patient / referral
    "PatientInformation",
    "Referral",
    "Sex",
    "Handedness",
    # recording / modulators
    "RecordingConditions",
    "RecordingType",
    "ModulatorsAndProcedures",
    "HyperventilationQuality",
    "ALERTNESS_CHOICES",
    # background / sleep
    "BackgroundActivity",
    "PosteriorDominantRhythm",
    "OrganisedRhythm",
    "SleepAndDrowsiness",
    "Significance",
    "Amplitude",
    "Organisation",
    "Reactivity",
    "PdrCaveat",
    "PdrAbsence",
    "SpectralBand",
    # interictal
    "InterictalFindings",
    "InterictalGraphoelement",
    "TimeRelatedFeatures",
    "Morphology",
    "ModeOfAppearance",
    "DischargePattern",
    "Incidence",
    "Prevalence",
    # episodes
    "Episodes",
    "Episode",
    "SemiologyPhase",
    "EpisodeType",
    "PhaseName",
    "Consciousness",
    # diagnostic
    "DiagnosticSignificance",
    "ClinicalComments",
    "Diagnosis",
    "IlaeClassification",
]
