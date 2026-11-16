"""LAIF engine: identity. Moved without changing assessment rules."""

import hashlib
import functools
from pathlib import Path


@functools.lru_cache(maxsize=1)
def toolchain_fingerprint():
    """Identity of the code that produced an assessment.

    Every generated artifact records the corpus it read; none recorded the
    engine that read it. An audit found committed batch outputs carrying
    findings and wording the current engine no longer produces, with nothing in
    them to say which version was responsible — a reproducibility claim that
    could not be checked from the artifact.

    A content hash of the engine and the runner, so it changes exactly when the
    detection or reporting logic changes and needs no manual version bumping.
    Falls back to "unavailable" rather than failing an assessment: this is
    provenance metadata, not a gate.
    """
    try:
        here = Path(__file__).resolve().parents[1]
        parts = []
        for name in ("assessment_engine.py", "validate.py", "laif_spec.py",
                     "scripts/laif_process_document.py", "scripts/laif_evidence_display.py",
                     "scripts/laif_auto_criteria.py", "scripts/laif_reader_summaries.py",
                     *tuple(str(p.relative_to(here)).replace("\\", "/")
                            for p in sorted((here / "laif_engine").glob("*.py")))):
            path = here / name
            parts.append(path.read_bytes())
        return hashlib.sha256(b"\x00".join(parts)).hexdigest()[:16]
    except Exception:
        return "unavailable"


def _corpus_fingerprint(assessments):
    """Stable identity of exactly which texts produced a set of results.

    Every artifact derives its fingerprint from this one function. It was
    previously recomputed inline in the markdown generator, so a change to the
    definition would have made two artifacts describing the same run disagree
    about which corpus produced it.
    """
    return hashlib.sha256("".join(
        r.get("assessed_text_sha256", "") for r in assessments
    ).encode("utf-8")).hexdigest()
