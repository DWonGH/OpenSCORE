"""Top-level SCORE EEG report model and (de)serialisation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Union

from pydantic import Field

from .common import Provenance, ScoreModel
from .patient import PatientInformation, Referral
from .recording import ModulatorsAndProcedures, RecordingConditions
from .background import BackgroundActivity, SleepAndDrowsiness
from .interictal import InterictalFindings
from .episodes import Episodes
from .diagnostic import ClinicalComments, DiagnosticSignificance

SCHEMA_VERSION = "0.1.0"


class EegReport(ScoreModel):
    """A complete SCORE-aligned EEG report (clinical-core subset).

    Top-level aliases preserve OpenSCORE's legacy ``.score`` section keys for the six
    original sections and add keys for the new modules (Modulators, Sleep, Interictal,
    Episodes). Serialise with ``model_dump(mode='json', by_alias=True)`` to produce the
    ``.score`` JSON shape.
    """

    schema_version: str = Field(default=SCHEMA_VERSION, alias="Schema version")
    patient_details: PatientInformation = Field(default_factory=PatientInformation, alias="Patient details")
    patient_referral: Referral = Field(default_factory=Referral, alias="Patient referral")
    recording_conditions: RecordingConditions = Field(default_factory=RecordingConditions, alias="Recording conditions")
    modulators: ModulatorsAndProcedures = Field(default_factory=ModulatorsAndProcedures, alias="Modulators and procedures")
    background_activity: BackgroundActivity = Field(default_factory=BackgroundActivity, alias="Background activity")
    sleep: SleepAndDrowsiness = Field(default_factory=SleepAndDrowsiness, alias="Sleep and drowsiness")
    interictal: InterictalFindings = Field(default_factory=InterictalFindings, alias="Interictal findings")
    episodes: Episodes = Field(default_factory=Episodes, alias="Episodes")
    diagnostic_significance: DiagnosticSignificance = Field(default_factory=DiagnosticSignificance, alias="Diagnostic significance")
    clinical_comments: ClinicalComments = Field(default_factory=ClinicalComments, alias="Clinical comments")
    # Forward-compat hook for the (deferred) LLM extraction pipeline; null for authoring tools.
    provenance: Optional[Provenance] = Field(default=None, alias="Extraction")

    # --- (de)serialisation helpers -------------------------------------------------

    def to_score_dict(self) -> dict:
        """Return the ``.score`` JSON-compatible dict (human-readable keys, plain values)."""
        return self.model_dump(mode="json", by_alias=True)

    def save(self, path: Union[str, Path]) -> None:
        """Write a validated ``.score`` file (matches the legacy 4-space-indented format)."""
        with open(path, "w", encoding="utf8") as f:
            json.dump(self.to_score_dict(), f, indent=4)

    @classmethod
    def from_score_dict(cls, data: dict) -> "EegReport":
        """Validate a ``.score`` dict (keyed by the human-readable aliases) into a report."""
        return cls.model_validate(data)

    @classmethod
    def load(cls, path: Union[str, Path]) -> "EegReport":
        """Read and validate a ``.score`` file."""
        with open(path, "r", encoding="utf8") as f:
            return cls.from_score_dict(json.load(f))


def validate(data: dict) -> EegReport:
    """Validate a ``.score`` dict, raising ``pydantic.ValidationError`` on failure."""
    return EegReport.from_score_dict(data)
