# Black Swan Archive Inspector

**Version:** 1.0.0 (scoped, stand-alone publication)  
**Verification date:** 27 October 2026  
**Status:** **Verified for the documented unit-test and CLI-smoke-test scope only**

## Overview

This command-line utility performs a bounded, read-only inspection of ZIP archives. It checks the archive's transport checksum, rejects unsafe member names, duplicate normalized paths, symbolic links, encrypted entries and oversized inputs, and reports a selected set of UTF-8 source files **without extracting or executing their content**.

The original implementation and test suite were preserved byte-for-byte from the project snapshots. It is published as a small, independently testable utility—not as Black Swan Logic v8, a working cybersecurity detector, a dataset validation, or a production-readiness claim.

## Contents

```text
archive-inspector/v1.0.0/
├── README.md
├── LICENSE
├── VERIFICATION.json
├── TEST_RESULTS.txt
├── scripts/
│   └── inspect_general_archive.py
└── tests/
    └── test_general_archive.py
```

## Requirements

- Python 3 standard library only; this release was tested on **Python 3.13.5** on Linux.
- No API credentials, network service, detector package, or additional Python dependency is required.

## Usage

Run from this release directory:

```bash
python3 scripts/inspect_general_archive.py /path/to/archive.zip > inspection.json
```

The command returns exit code **0** for a completed structural inspection and **1** when an archive fails the supported checks. If the file is absent, the original tool returns a JSON `awaiting_archive` status with exit code 0; **do not interpret that as successful verification of an archive**.

The JSON report contains the SHA-256 of the supplied archive, an inventory, selected source text, omitted-source reasons, and a `core_executed: false` indicator. The `matches_previously_reviewed_archive` field compares against a single hard-coded historical fingerprint; it **does not authenticate an archive**.

## Reproduce the verification

From this directory:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The original eight tests were executed without modifying either code or tests. **Result: 8 tests passed, 0 failures**. A separate CLI smoke check accepted a harmless synthetic ZIP and rejected a ZIP with a traversal path. See [`TEST_RESULTS.txt`](TEST_RESULTS.txt) and [`VERIFICATION.json`](VERIFICATION.json) for the exact recorded scope, environment, checksums and provenance.

## Security and operational limits

- **Read-only is not automatically confidential:** the JSON output **includes source-code text** from selected archive entries. Only inspect archives you are authorized to handle; do not publish the resulting JSON without a separate privacy review.
- The sensitive-text filter is heuristic and cannot guarantee that all credentials, private identifiers or proprietary information are excluded.
- The archive content is not executed, imported or extracted; the tool is not an antivirus product, malware sandbox, cryptographic signature verifier or comprehensive vulnerability scanner.
- Size limits in the supplied implementation include a 20 MB maximum ZIP, a 100 MB maximum declared uncompressed size and individual source-size caps. These are implementation constraints, not security certifications.
- This release does **not** validate Logic v8's timeout/recovery behavior or any real-world threat-detection performance.

## Provenance and license

The code, tests and GPL license were preserved byte-for-byte from the verified project snapshot and matched across three available snapshots. The exact input checksums are recorded in `VERIFICATION.json`. No raw ZIPs, telemetry, credentials, hidden labels or unrelated development materials are included.

**This stand-alone component retains the original GNU General Public License, version 3, included as [`LICENSE`](LICENSE).** It has not been relicensed under the repository root's Apache License 2.0. Review the component license independently before redistributing or modifying it.