"""HED-SCORE binding.

The findings vocabulary in this package (interictal morphology, time-related features,
episode types, sleep graphoelements, special patterns) uses the node names of the
**HED-SCORE library schema** as enum values, so each value is also a HED short tag. This
gives interoperability with the BIDS/HED ecosystem (`hedtools`, the HED online validator)
without HED replacing our report-document schema.

What HED-SCORE does *not* cover (and this schema does): patient/referral, administrative
recording data, diagnostic significance, and clinical comments. See ``score_schema`` README.
"""

from __future__ import annotations

from enum import Enum
from typing import Union

# Pin the HED-SCORE library schema version whose node names we aligned to.
HED_SCORE_VERSION = "score_2.1.0"

# Conventional BIDS namespace/prefix for the SCORE library when used alongside the standard
# HED schema (the exact prefix is set per dataset in its dataset_description.json / sidecar).
HED_LIBRARY_PREFIX = "sc"


def hed_short_tag(value: Union[str, Enum]) -> str:
    """Return the HED-SCORE short tag for an aligned enum member (or pass-through string)."""
    return value.value if isinstance(value, Enum) else value


def hed_tag(value: Union[str, Enum], prefix: str = HED_LIBRARY_PREFIX) -> str:
    """Return a namespaced HED tag, e.g. ``sc:Sharp-wave``.

    The prefix must match the library namespace declared in the dataset's HED configuration.
    """
    return f"{prefix}:{hed_short_tag(value)}"
