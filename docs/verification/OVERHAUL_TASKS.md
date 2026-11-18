# Overhaul delivery record

Updated 18 November 2026, Canberra. See [current checkpoint](CURRENT.md)
for exact revisions, deployments and acceptance evidence.

| Work | Owner | State | Evidence / next dependency |
|---|---|---|---|
| Local cancellation/recovery | Engineering owner | Released | PR #131; accurate saved-output/resume messages; 26 focused checks and 649-test full gate, two skips |
| NIST cited-prose fidelity | Source owner | Released, bounded evidence | PR #132; 16/16 raw and normalized PDF quotation matches; no provenance promotion |
| NIST historical citation erratum | Research owner | Approved and merged | PR #133; eight incorrect descriptions identified; original trace/report retained; substantive reassessment remains open |
| Explicit multi-document case map | Product owner | Local and private Site workflow released | PR #134 adds the shared Python checker. PR #136 clarifies input and output errors. The Site preview replay matched the local checker. Chrome canceled file transfers, so hosted case download verification stays open |
| Recover after competing saves | Site owner | Private v22 deployed and read back | Two live tabs saved different cases and both survived reload. Staged overlap and lost-acknowledgement checks passed. Hosted network-outage recovery remains unobserved |
| Original EU Act extraction | Source owner | Reproducible receipt merged | PR #137 compares all 144 original-edition PDF pages after whitespace removal and locates the Articles and Annexes. Attributed assessment and legal applicability review stay open |
| Keyboard and narrow reflow | Site owner | Bounded checks observed | Private v19 all nine sections/public v2 at 320 CSS px without body overflow; focus return checked; true zoom, screen reader and physical phone remain unobserved |
| Publisher byte acquisition | Source owner | External retrieval blocked | Ordinary Ombudsman PDF and DTAC DOCX GETs returned HTTP403 again on 18 November; no bytes/source-status promotion |
| Automatic relationship discovery | Engineering/research owners | Separate unimplemented scope | Declared case links do not infer contradictions, governing authority or control operation; requires designed and reviewed semantics |
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
