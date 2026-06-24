"""SCORE §15 — Diagnostic significance; and the Clinical comments section."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .common import ScoreModel


class Diagnosis(str, Enum):
    """SCORE §15 — the mandatory interpretation of diagnostic significance."""

    NORMAL = "Normal"
    NO_DEFINITE_ABNORMALITY = "No definite abnormality"
    ABNORMAL = "Abnormal"


class IlaeClassification(str, Enum):
    """ILAE classification for abnormal recordings (Scheffer et al., 2017)."""

    FOCAL = "Focal"
    GENERALIZED = "Generalized"
    COMBINED = "Combined generalized and focal"
    UNKNOWN = "Unknown"


class DiagnosticSignificance(ScoreModel):
    """SCORE §15 / Table 17.

    Issue #24 fix: ``diagnosis`` defaults to ``None`` (not assessed), never silently to
    "Normal" — a value must be chosen deliberately.
    """

    diagnosis: Optional[Diagnosis] = Field(default=None, alias="Diagnosis")
    abnormal_specification: Optional[str] = Field(default=None, alias="Abnormal specification")
    ilae_classification: Optional[IlaeClassification] = Field(default=None, alias="ILAE classification")
    syndromes: list[str] = Field(default_factory=list, alias="Syndrome classification")
    diagnostic_yield: list[str] = Field(default_factory=list, alias="Diagnostic yield")


class ClinicalComments(ScoreModel):
    """Free-text interpretation / clinical correlation."""

    interpreter_name: Optional[str] = Field(default=None, alias="Interpreter name")
    clinical_comments: Optional[str] = Field(default=None, alias="Clinical comments")
