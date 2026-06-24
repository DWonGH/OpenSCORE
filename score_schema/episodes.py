"""SCORE §10 — Episodes (clinical and electroencephalographic seizures and other events).

New module (absent in legacy OpenSCORE). Each episode is scored as a sequence of phases
(initial / subsequent / postictal) with semiology (Tables 10/11) and ictal EEG (Table 12),
plus timing and context (Table 13).
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .common import Location, ScoreModel, Ternary


class EpisodeType(str, Enum):
    """SCORE Table 9 — names of episodes."""

    EPILEPTIC_SEIZURE = "Epileptic seizure"
    PNES = "Psychogenic non-epileptic seizure (PNES)"
    EEG_SEIZURE = "Electroencephalographic seizure"
    SLEEP_RELATED = "Sleep-related episode"
    PAEDIATRIC = "Pediatric episode"
    PAROXYSMAL_MOTOR = "Paroxysmal motor event"
    SYNCOPE = "Syncope"
    OTHER = "Other"


class PhaseName(str, Enum):
    INITIAL = "initial"
    SUBSEQUENT = "subsequent"
    POSTICTAL = "postictal"


class Consciousness(str, Enum):
    """SCORE Table 13."""

    NOT_TESTED = "Not tested"
    AFFECTED = "Affected"
    MILDLY_AFFECTED = "Mildly affected"
    NOT_AFFECTED = "Not affected"


# Representative ictal EEG patterns (SCORE Table 12) for constrained selection; free text
# is also permitted via the phase's `ictal_eeg` list.
ICTAL_EEG_PATTERNS = (
    "No observable change", "Obscured by artifacts", "Polyspikes",
    "Fast spike activity or repetitive spikes", "Low voltage fast activity",
    "Spike-and-slow-waves", "Sharp-and-slow-waves", "Rhythmic activity",
    "Slow wave of large amplitude", "Burst-suppression pattern",
    "Electrodecremental change", "DC-shift", "High frequency oscillation (HFO)",
    "Disappearance of ongoing activity",
)


class SemiologyPhase(ScoreModel):
    """One phase of an episode (SCORE §10)."""

    phase: Optional[PhaseName] = Field(default=None, alias="Phase")
    semiology: list[str] = Field(default_factory=list, alias="Semiology", description="ILAE semiologic findings (Tables 10/11).")
    ictal_eeg: list[str] = Field(default_factory=list, alias="Ictal EEG", description="Ictal EEG patterns (Table 12).")
    location: Location = Field(default_factory=Location, alias="Location")


class Episode(ScoreModel):
    """A single scored clinical/EEG episode (SCORE §10)."""

    name: Optional[str] = Field(default=None, alias="Name", description="Episode name / ILAE seizure type.")
    episode_type: Optional[EpisodeType] = Field(default=None, alias="Type")
    phases: list[SemiologyPhase] = Field(default_factory=list, alias="Phases")
    consciousness: Optional[Consciousness] = Field(default=None, alias="Consciousness")
    awareness: Ternary = Field(default=Ternary.NOT_ASSESSED, alias="Awareness of the episode")
    duration: Optional[str] = Field(default=None, alias="Duration")
    number_of_episodes: Optional[int] = Field(default=None, alias="Number of stereotypical episodes")
    timing_context: Optional[str] = Field(default=None, alias="Timing and context")


class Episodes(ScoreModel):
    """SCORE §10 container."""

    episodes: list[Episode] = Field(default_factory=list, alias="Episodes")
