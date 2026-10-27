#!/usr/bin/env python3
"""Deterministic offline file-tree integrity manifests (stdlib only)."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys

SCHEMA = 'black-swan-file-integrity-v1'
SHA256_RE = re.compile(r'[0-9a-f]{64}\Z')


class IntegrityError(ValueError):
    pass


def _file_digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def _tree(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise IntegrityError('Root must be a real directory, not a symlink')
    root = root.resolve(strict=True)
    entries = {}
    def _raise_walk_error(exc):
        raise IntegrityError(f'Cannot traverse directory: {exc}')
    for base, dirs, files in os.walk(root, followlinks=False, onerror=_raise_walk_error):
        base = Path(base)
        for name in dirs + files:
            p = base / name
            if p.is_symlink():
                raise IntegrityError(f'Symlink is not permitted: {p.relative_to(root)}')
        for name in files:
            p = base / name
            if not p.is_file():
                raise IntegrityError(f'Nonregular file: {p.relative_to(root)}')
            key = p.relative_to(root).as_posix()
            entries[key] = {'sha256': _file_digest(p), 'size': p.stat().st_size}
    return {k: entries[k] for k in sorted(entries)}


def _valid_path(key):
    if not isinstance(key, str) or not key or '\\' in key or '\x00' in key:
        return False
    pp = PurePosixPath(key)
    return not pp.is_absolute() and all(x not in ('', '.', '..') for x in key.split('/'))


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise IntegrityError(f'Duplicate JSON member: {key!r}')
        result[key] = value
    return result


def _load_manifest(path):
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'),
                          object_pairs_hook=_reject_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IntegrityError(f'Cannot read manifest: {exc}') from exc
    if not isinstance(data, dict) or set(data) != {'schema', 'files'} or data['schema'] != SCHEMA:
        raise IntegrityError('Unsupported manifest schema')
    files = data['files']
    if not isinstance(files, dict):
        raise IntegrityError('Manifest files must be an object')
    for key, item in files.items():
        if not _valid_path(key):
            raise IntegrityError(f'Unsafe manifest path: {key!r}')
        if (not isinstance(item, dict) or set(item) != {'size', 'sha256'}
                or type(item['size']) is not int or item['size'] < 0
                or not isinstance(item['sha256'], str) or not SHA256_RE.fullmatch(item['sha256'])):
            raise IntegrityError(f'Invalid metadata: {key!r}')
    return files


def _ensure_outside_root(root, manifest):
    root = Path(root).resolve(strict=True)
    candidate = Path(manifest).absolute().resolve(strict=False)
    if candidate == root or root in candidate.parents:
        raise IntegrityError('Manifest path must be outside checked directory')


def create(root, manifest):
    _ensure_outside_root(root, manifest)
    files = _tree(root)
    target = Path(manifest)
    if target.exists():
        raise IntegrityError('Refusing to overwrite existing manifest')
    target.write_text(json.dumps({'schema': SCHEMA, 'files': files}, indent=2,
                                 ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    return len(files)


def verify(root, manifest):
    _ensure_outside_root(root, manifest)
    expected = _load_manifest(manifest)
    observed = _tree(root)
    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    changed = sorted(k for k in set(expected) & set(observed) if expected[k] != observed[k])
    return {'ok': not (missing or extra or changed), 'expected_count': len(expected),
            'observed_count': len(observed), 'missing': missing, 'extra': extra, 'changed': changed}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('create', 'verify'))
    parser.add_argument('root', help='Directory to inspect')
    parser.add_argument('manifest', help='JSON manifest outside the root directory')
    args = parser.parse_args(argv)
    try:
        if args.command == 'create':
            print(json.dumps({'ok': True, 'files': create(args.root, args.manifest)}))
            return 0
        result = verify(args.root, args.manifest)
        print(json.dumps(result, sort_keys=True))
        return 0 if result['ok'] else 1
    except (IntegrityError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
