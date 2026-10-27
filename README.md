# Black Swan — Verified Artifacts

This public repository is a **curated record of independently checked, explicitly scoped deliverables**, not a source-code dump, development branch, backup location, or declaration that the Black Swan detection engine is production-ready.

## Published, verified artifacts

| Release | What was verified | Evidence | Status |
|---|---|---|---|
| [Archive Inspector v1.0.0](verified/archive-inspector/v1.0.0/README.md) | Original stand-alone ZIP inspection utility: 8/8 unit tests and positive/negative CLI smoke checks on Python 3.13.5 | [Verification record](verified/archive-inspector/v1.0.0/VERIFICATION.json) · [Test output](verified/archive-inspector/v1.0.0/TEST_RESULTS.txt) | **PASS — scoped utility only** |

## Publication standard

Each published artifact must have: (1) an identified, reproducible source revision; (2) test evidence that supports **only its stated claims**; (3) a clear license and disclosure boundary; (4) no private datasets, credentials, or hidden evaluation labels; and (5) an independent publication decision for that component. A passing isolated test does **not** imply certification of its parent product.

This repository does not currently publish Black Swan Logic v8, the telemetry dataset, model benchmarks, pending research notes or project development roadmaps as verified releases. Those are separate and may be added **only after their own acceptance criteria are met**.

## Licensing

The root `LICENSE` is Apache License 2.0. Some independently distributed historical project components have different original licenses. The [Archive Inspector](verified/archive-inspector/v1.0.0/LICENSE) is **GPL version 3** and remains under that license; it is **not relicensed under Apache 2.0**. Always follow the license included with the specific artifact.