"""Shared types and base config for the SCORE schema.

The models in this package are a SCORE-2017-aligned (Beniczky et al., Clin Neurophysiol
2017) data model for an EEG report. They serialise to the same human-readable JSON keys that
OpenSCORE's legacy ``.score`` files use (via field aliases), so the GUI can adopt them with
minimal churn, while also exporting a JSON Schema usable by external tools (a future C++/Qt
EDFBrowser fork, or schema-constrained LLM extraction).
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ScoreModel(BaseModel):
    """Base for every model in the schema.

    - ``populate_by_name`` lets callers construct models with either the Python field
      name or the human-readable alias (the legacy ``.score`` key).
    - ``extra='ignore'`` tolerates unknown keys when reading older/foreign files.
    - Dump with ``model_dump(mode='json', by_alias=True)`` to reproduce the ``.score`` shape.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore", use_enum_values=False)


class Ternary(str, Enum):
    """Tristate for present / absent / not-yet-assessed features.

    Fixes the OpenSCORE ambiguity (issues #23/#24) where an unticked checkbox serialised
    as ``false``/``null`` and could not be distinguished from a deliberate "absent".
    ``NOT_ASSESSED`` is the explicit default for "the reporter has not considered this".
    """

    PRESENT = "present"
    ABSENT = "absent"
    NOT_ASSESSED = "not_assessed"


class Laterality(str, Enum):
    """SCORE §8 location laterality for graphoelements/findings."""

    LEFT = "left"
    RIGHT = "right"
    MIDLINE = "midline"
    BILATERAL_SYNCHRONOUS = "bilateral synchronous"
    BILATERAL_INDEPENDENT = "bilateral independent"
    DIFFUSE = "diffuse"
    GENERALIZED = "generalized"
    MULTIFOCAL = "multifocal"
    UNCLEAR = "unclear"


class Region(str, Enum):
    """SCORE §8 scalp region (lobar)."""

    FRONTAL = "frontal"
    CENTRAL = "central"
    TEMPORAL = "temporal"
    PARIETAL = "parietal"
    OCCIPITAL = "occipital"


class Location(ScoreModel):
    """Where a finding is seen on the scalp (SCORE §8 localization)."""

    laterality: Optional[Laterality] = Field(default=None, alias="Laterality")
    regions: list[Region] = Field(default_factory=list, alias="Regions")
    electrode_maxima: Optional[str] = Field(
        default=None,
        alias="Electrode maxima",
        description="Electrode site(s) of peak negativity, e.g. 'F7' or 'T3/T5'.",
    )


class Provenance(ScoreModel):
    """Optional extraction metadata.

    Forward-compatibility hook for the (deferred) LLM extraction pipeline so it can record
    which model produced a report and how confident it was, to support inter-model agreement
    testing. Authoring tools (OpenSCORE) leave this null.
    """

    model: Optional[str] = Field(default=None, alias="Model")
    confidence: Optional[float] = Field(default=None, alias="Confidence", ge=0.0, le=1.0)
    notes: Optional[str] = Field(default=None, alias="Notes")
