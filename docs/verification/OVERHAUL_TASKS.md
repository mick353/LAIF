# Overhaul delivery record

Updated 16 November 2026, 23:12 Canberra. See [current checkpoint](CURRENT.md)
for exact revisions, deployments and acceptance evidence.

| Work | Owner | State | Evidence / next dependency |
|---|---|---|---|
| Extractor fallback | Delivery lead | Merged previously | PR #118; latest full gate passes |
| Redundant-file removal | Delivery lead | Released | PR #125; four exact aliases removed, all unique evidence retained; [manifest](2026-11-16-deduplication.json) |
| Strong/weak comparison | Research owner | Exploratory release complete | PR #126; 40 predictions, 29 matches and 11 failures; preferred comparator intake still HTTP403 |
| Engine modules | Engineering owner | Merged and live | PR #127; behavior comparison, full gate; Site v19 bundles all modules |
| Reader summaries | Reporting owner | Merged and live | PR #128; separate summaries and jargon gate, original reasoning preserved |
| Current-report navigation | Reporting owner | Released | Ten current links fixed; four historical defects retained with evidence hashes |
| Shorter documentation | Delivery lead | Released | Site and Python guides separate; CLAUDE below8KB, detailed reference linked; public guide routes added |
| Public read-only Site | Site owner | Live and read back | Public guide v2; main-workspace link and companion explanation; v1 anonymous HTTP200, v2 browser observation; no upload endpoint |
| Main workspace journey | Site owner | Live and read back | Private v19; selected older run preserved, correct source/findings/evidence steps, distinct run labels; focused tests/build and live navigation passed |
| Hosted engine/export acceptance | Delivery lead | Observed | Private v18 fresh synthetic run, downloads parsed, save/reload; [receipt](2026-11-16-hosted-acceptance.md) |
| User/device acceptance | Product owner | Open | Fresh owner document, recovery and physical phone/screen reader observations needed; issue #110 |
| Independent/source/legal evidence | Research/source owners | Open | Independent adjudication, real operational evidence and issue #93; not closed by software checks |

Historical generated assessments were distinct source/processing evidence, so
none was deleted merely for age. Local packaging archives are rebuildable;
retention decisions and kept release archives are recorded separately.
