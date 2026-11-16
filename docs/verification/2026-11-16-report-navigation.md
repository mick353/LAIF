# Report navigation fix — 16 November 2026

Owner: Codex engine-module worker. Status: implemented and focused checks passed;
full integrated release gate and Site acceptance belong to the delivery lead.
Dependency: integrate after the engine split and refresh the Site canonical sources.
No push, merge or deployment performed here.

The old heading helper collapsed the two spaces left after removing an em dash or
ampersand. GitHub replaces each ordinary space with a hyphen, so the generated
contents links missed the actual heading IDs. The Peer Exemplars link also hardcoded
the wrong target. It now derives its target from the same heading string.

Reference: [GitHub section-link rules](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links).

Validation: two navigation regressions passed, covering every one of the ten current
corpus document targets and Peer Exemplars; all 86 assessment fragility tests passed.
Current reports were regenerated twice with byte-identical results. The JSON comparison
against the preceding split commit changes only `/toolchain_fingerprint`.
The current corpus Markdown changes only ten contents links (document 7 was already
correct); assessment findings and authored reasoning are unchanged.

## Historical defects intentionally retained

The following four evidence reports retain their original incorrect Peer Exemplars
anchor. They are historical outputs with recorded provenance, not current generated
reports. They were checked against Git and left unchanged; their existing event hashes
remain authoritative. Working-copy hashes below are observation receipts and may
reflect checkout line endings. These navigation defects are acknowledged, not described
as repaired or counted as current report failures.

- `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/au_dta_policy_v2_1/Policy-for-the-responsible-use-of-AI-in-government-2_1_1.laif.md` — working-copy SHA-256 `10378afb3ffabcf06c85237d438fcc4acae8d125e2623fb03a370c74732244a5`.
- `docs/verification/2026-11-07/regulatory/pypdf-diagnostic/eu_ai_act_amendment_2026_1744/OJ_L_202601744_EN_TXT.laif.md` — working-copy SHA-256 `e1743923311e84868e360ee016d101bdd28647e46ce3ce94f17cca116f31f00e`.
- `docs/verification/2026-11-07/regulatory/reviewed-text/au_dta_policy_v2_1/au_dta_policy_v2_1.laif.md` — working-copy SHA-256 `cd68a5e0d099765e492c21571eb2f93f30c6f83d5c3714fe33831b64b603319a`.
- `docs/verification/2026-11-07/regulatory/reviewed-text/eu_ai_act_amendment_2026_1744/eu_ai_act_amendment_2026_1744.laif.md` — working-copy SHA-256 `f5e45af20bb9c17f6a713a1dda12922e6f631b9ca062863b7b148e74e14e3ed8`.
