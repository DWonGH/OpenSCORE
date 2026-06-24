"""Tests for the score_schema package (SCORE-2017 clinical-core subset)."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from score_schema import (
    Diagnosis,
    EegReport,
    EpisodeType,
    Incidence,
    InterictalGraphoelement,
    Morphology,
    Ternary,
    hed_tag,
    validate,
)
from score_schema.export_schema import build_schema

FIXTURE = Path(__file__).parent / "fixtures" / "synthetic_report.score"

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


def test_empty_report_round_trips():
    report = EegReport()
    data = report.to_score_dict()
    assert EXPECTED_SECTIONS.issubset(data.keys())
    # Re-validating the serialised form reproduces an equal report.
    assert EegReport.from_score_dict(data).to_score_dict() == data


def test_tristate_default_is_not_assessed():
    """Issue #23: an unconsidered tristate is explicitly NOT_ASSESSED, never false/null."""
    report = EegReport()
    assert report.recording_conditions.skull_defect == Ternary.NOT_ASSESSED
    assert report.modulators.hyperventilation == Ternary.NOT_ASSESSED
    assert report.to_score_dict()["Recording conditions"]["Skull defect"] == "not_assessed"


def test_diagnosis_not_defaulted_to_normal():
    """Issue #24: diagnosis must be chosen deliberately; default is None, not 'Normal'."""
    assert EegReport().diagnostic_significance.diagnosis is None


def test_alertness_is_multi_value():
    """Issue #17: alertness can hold several states seen across a recording."""
    report = EegReport()
    report.recording_conditions.alertness = ["awake", "drowsy", "asleep"]
    assert report.to_score_dict()["Recording conditions"]["Alertness"] == ["awake", "drowsy", "asleep"]


def test_construct_by_field_name_and_alias():
    """populate_by_name lets us build with Python names; output uses aliases."""
    g = InterictalGraphoelement(morphology=Morphology.SPIKE, significance="Abnormal")
    dumped = g.model_dump(mode="json", by_alias=True)
    assert dumped["Morphology"] == "Spike"
    assert dumped["Significance"] == "Abnormal"


def test_invalid_enum_value_fails():
    data = EegReport().to_score_dict()
    data["Diagnostic significance"]["Diagnosis"] = "definitely not a SCORE term"
    with pytest.raises(ValidationError):
        validate(data)


def test_invalid_frequency_type_fails():
    data = EegReport().to_score_dict()
    data["Background activity"]["Posterior dominant rhythm"]["Frequency"] = "seven"
    with pytest.raises(ValidationError):
        validate(data)


def test_json_schema_builds_and_lists_sections():
    schema = build_schema()
    assert schema["type"] == "object"
    assert EXPECTED_SECTIONS.issubset(schema["properties"].keys())
    # Enum constraints are exported (useful for schema-guided LLM decoding).
    assert "$defs" in schema


def test_synthetic_fixture_validates():
    report = EegReport.load(FIXTURE)
    assert report.diagnostic_significance.diagnosis == Diagnosis.ABNORMAL
    assert report.background_activity.pdr.frequency == 7.0
    ge = report.interictal.graphoelements
    assert len(ge) == 1
    assert ge[0].morphology == Morphology.SHARP_WAVE
    assert ge[0].location.regions[0].value == "temporal"


def test_findings_vocab_is_hed_score_aligned():
    """Findings enum values are HED-SCORE node names (so a value is also a HED short tag)."""
    assert Morphology.HFO.value == "High-frequency-oscillation"
    assert Morphology.FIRDA.value == "Frontal-intermittent-rhythmic-delta-activity"
    assert Incidence.OCCASIONAL.value == "Occasional-feature-incidence"
    assert EpisodeType.PNES.value == "Seizure-PNES"


def test_hed_tag_helper_and_field():
    assert hed_tag(Morphology.SHARP_WAVE) == "sc:Sharp-wave"
    g = InterictalGraphoelement(morphology=Morphology.SHARP_WAVE, hed_tags=["sc:Sharp-wave"])
    dumped = g.model_dump(mode="json", by_alias=True)
    assert dumped["HED tags"] == ["sc:Sharp-wave"]


def test_save_load_file_round_trip(tmp_path):
    original = EegReport.load(FIXTURE)
    out = tmp_path / "out.score"
    original.save(out)
    reloaded = EegReport.load(out)
    assert reloaded.to_score_dict() == original.to_score_dict()
    # File is valid JSON with the human-readable section keys.
    on_disk = json.loads(out.read_text(encoding="utf8"))
    assert EXPECTED_SECTIONS.issubset(on_disk.keys())
