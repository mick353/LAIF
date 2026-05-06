## Summary

- 

## Governance checklist

- [ ] This PR preserves LAIF scoring, detector, interpretation, and assessment-artifact semantics.
- [ ] Protected assessment artifacts were not changed, or any change is intentionally isolated and explained.
- [ ] Semantic-boundary notices, if any, are treated as advisory governance signals only.
- [ ] Provenance, manifest, or verified-corpus changes include authoritative source and transformation context where applicable.

## Testing

- [ ] `python3 tests/test_governance.py`
- [ ] `python3 scripts/governance/check_governance_config.py`
- [ ] `python3 scripts/governance/check_protected_artifacts.py`
- [ ] `python3 scripts/governance/check_semantic_boundaries.py`
- [ ] `python3 validate.py`
- [ ] `python3 validate.py --verified-corpus`
- [ ] `python3 validate.py --check-evidence-traces`
- [ ] `python3 test_adversarial.py`
- [ ] `python3 test_real_world.py`

## Notes for reviewers

- Semantic-boundary automation is advisory/warn-only and performs no semantic interpretation.
