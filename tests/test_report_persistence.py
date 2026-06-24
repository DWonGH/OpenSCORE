"""Headless tests for the score_schema-backed persistence layer (src/models/report.py).

These need no QApplication: the section *models* are plain Python; only the *views* use Qt.
"""

import copy

from src.models.report import Report
from score_schema import SCHEMA_VERSION, EegReport, Ternary

EXPECTED_SECTIONS = {
    "Schema version",
    "Patient details",
    "Patient referral",
    "Recording conditions",
    "Modulators and procedures",
    "Background activity",
    "Sleep and drowsiness",
    "Interictal findings",
    "Episodes",
    "Diagnostic significance",
    "Clinical comments",
}


def test_report_has_all_eleven_sections():
    data = Report().to_dict()
    assert EXPECTED_SECTIONS.issubset(data.keys())
    assert data["Schema version"] == SCHEMA_VERSION


def test_empty_report_validates_cleanly():
    # Should not raise; an empty/default report is valid (every field optional/empty).
    Report().validate()


def test_round_trip_through_from_dict():
    report = Report()
    report.recording_conditions.alertness = ["awake", "drowsy"]  # issue #17 multi-value
    report.diagnostic_significance.diagnosis = "Abnormal"
    report.diagnostic_significance.abnormal_specification = [
        "Focal dysfunction of the central nervous system"
    ]
    report.modulators.hyperventilation = Ternary.PRESENT

    data = report.to_dict()
    report.validate()  # populated report still validates

    other = Report()
    other.from_dict(copy.deepcopy(data))
    assert other.recording_conditions.alertness == ["awake", "drowsy"]
    assert other.diagnostic_significance.diagnosis == "Abnormal"
    assert other.modulators.hyperventilation == Ternary.PRESENT
    assert other.to_dict() == data


def test_loads_legacy_six_section_file():
    """A pre-existing 6-section .score (no new modules) still loads; new sections default."""
    legacy = {
        "Patient details": Report().patient_details.to_dict(),
        "Patient referral": Report().patient_referral.to_dict(),
        "Recording conditions": Report().recording_conditions.to_dict(),
        "Background activity": Report().background_activity.to_dict(),
        "Diagnostic significance": Report().diagnostic_significance.to_dict(),
        "Clinical comments": Report().clinical_comments.to_dict(),
    }
    report = Report()
    report.from_dict(legacy)  # must not raise on the missing new-section keys
    assert report.modulators.hyperventilation == Ternary.NOT_ASSESSED
    assert report.episodes.episodes == []


def test_report_dict_matches_schema_dump_shape():
    """The assembled report validates into an EegReport with the same section keys."""
    report = Report()
    report.diagnostic_significance.diagnosis = "Normal"
    validated = report.validate()
    assert isinstance(validated, EegReport)
    assert set(validated.to_score_dict().keys()) == EXPECTED_SECTIONS | {"Extraction"}
