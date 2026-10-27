# Restore Integrity Verifier v1.0.0

**Scope: PASS — standalone offline SHA-256 file-tree integrity verifier only.**
Not a validation of Black Swan Logic v8, detection quality, backup authenticity or production readiness.

## Functions

With Python 3.13.5 or another compatible Python 3 runtime (unverified), run:

```bash
python scripts/verify_restore.py create /path/to/files /path/outside/files_manifest.json
python scripts/verify_restore.py verify /path/to/restored/files /path/outside/files_manifest.json
python -m unittest discover -s tests -v
```

`create` refuses to overwrite an existing manifest and requires the manifest outside the checked tree. `verify` reports missing, extra and modified files, and rejects symlinks and malformed/unsafe manifest paths. Return codes: 0 match, 1 mismatch, 2 invalid input/error. No dependencies outside the Python standard library. `sha256` records exact file bytes, not cryptographic authenticity of the manifest itself.

## Evidence

- 15/15 self-contained unit tests PASS on Python 3.13.5, including CLI positive/negative and adversarial paths.
- Offline snapshot smoke test: a 111-file recovery export (110 original repository members plus one checksum sidecar) was extracted to an isolated directory and matched a freshly created manifest: 111/111; no contents were uploaded.
- See `TEST_RESULTS.txt` and `VERIFICATION.json` for artifact SHA-256 and limitations.

## Restrictions / limitations

- No signed or independently trusted baseline: an attacker who can change both files and manifest can defeat this check.
- No guarantees against concurrent filesystem mutation / symlink swap races or unusual device files under privileged adversaries. Inspect immutable/controlled copies.
- Does not prove source correctness, absence of credentials, licensing of the scanned snapshot, or external backup availability.
- The original project engine, rejected telemetry datasets, internal manifests and secrets are deliberately absent.

## License

This independently authored utility is licensed under the repository root **Apache License 2.0**. Existing separately licensed Archive Inspector remains under its own GPL-3.0 license.
