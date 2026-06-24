"""Export the SCORE schema as a JSON Schema artefact.

Run as a module to (re)generate ``score_schema.json`` at the repo root:

    python -m score_schema.export_schema

The emitted JSON Schema is the canonical, language-neutral contract: it can validate
``.score`` files from any language and can constrain schema-guided LLM decoding.
"""

from __future__ import annotations

import json
from pathlib import Path

from .report import EegReport

# Repo root is the parent of the score_schema package directory.
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "score_schema.json"


def build_schema() -> dict:
    """Return the JSON Schema for an EEG report, keyed by the human-readable aliases."""
    return EegReport.model_json_schema(by_alias=True)


def write_schema(output: Path = DEFAULT_OUTPUT) -> Path:
    schema = build_schema()
    with open(output, "w", encoding="utf8") as f:
        json.dump(schema, f, indent=2)
    return output


if __name__ == "__main__":
    path = write_schema()
    print(f"Wrote JSON Schema to {path}")
