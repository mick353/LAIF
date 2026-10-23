# See what a LAIF review produces

This example is an invented supplier policy for an AI assistant supporting public services. It includes some safeguards and deliberately leaves several controls unspecified. It is synthetic demonstration material, not a customer case study, production evidence or a recommended policy template.

- [Read the source policy](vendor-policy.md).
- [Read the actual generated institutional assessment](sample-assessment.md).
- [Inspect the actual generated quote bank](sample-quote-bank.md).

Run it yourself from the repository root:

```bash
python3 scripts/laif_process_document.py docs/examples/vendor-policy.md --extractor builtin
```

The committed sample outputs were copied from the local runner without editorial changes. The institutional assessment contains the source SHA-256, and the quote bank contains source quotations. Neither file establishes operational effectiveness. The runner's generated `.laif.md`/JSON metadata includes run-specific timestamps and output paths; these are not a promise of whole-file identity across different machines or run times.

Look for the discussion of monitoring without thresholds or escalation, obligations without consequences, missing precedence and lifecycle controls, and protections already expressed. Review the automatic document classification as well: it is a heuristic suggestion, not an authoritative description of the source's legal form.

To reproduce the committed outputs into a separate folder:

```bash
python3 scripts/laif_process_document.py docs/examples/vendor-policy.md --extractor builtin --output-dir laif_outputs/product-demo
```

Compare `laif_outputs/product-demo/vendor-policy.institutional_report.md` with `docs/examples/sample-assessment.md`, and `laif_outputs/product-demo/analyst/vendor-policy/quote_bank.md` with `docs/examples/sample-quote-bank.md`.

[Back to the product overview](../../README.md) · [Full getting-started guide](../GETTING_STARTED.md)
