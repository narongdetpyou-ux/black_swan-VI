import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'verify_restore.py'
spec = importlib.util.spec_from_file_location('verify_restore', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'src'
        self.root.mkdir()
        (self.root / 'a.txt').write_bytes(b'hello')
        (self.root / 'folder').mkdir()
        (self.root / 'folder' / 'b.bin').write_bytes(b'\x00\xff')
        self.manifest = Path(self.tmp.name) / 'manifest.json'

    def ready(self):
        self.assertEqual(mod.create(self.root, self.manifest), 2)

    def test_matching_tree(self):
        self.ready()
        self.assertTrue(mod.verify(self.root, self.manifest)['ok'])

    def test_modified_file_detected(self):
        self.ready()
        (self.root / 'a.txt').write_bytes(b'evil')
        self.assertEqual(mod.verify(self.root, self.manifest)['changed'], ['a.txt'])

    def test_missing_file_detected(self):
        self.ready()
        (self.root / 'a.txt').unlink()
        self.assertEqual(mod.verify(self.root, self.manifest)['missing'], ['a.txt'])

    def test_extra_file_detected(self):
        self.ready()
        (self.root / 'extra').touch()
        self.assertEqual(mod.verify(self.root, self.manifest)['extra'], ['extra'])

    def test_manifest_determinism(self):
        self.ready()
        first = self.manifest.read_bytes()
        self.manifest.unlink()
        mod.create(self.root, self.manifest)
        self.assertEqual(self.manifest.read_bytes(), first)

    def test_manifest_cannot_be_inside_root(self):
        with self.assertRaises(mod.IntegrityError):
            mod.create(self.root, self.root / 'manifest.json')

    def test_no_overwrite(self):
        self.ready()
        with self.assertRaises(mod.IntegrityError):
            mod.create(self.root, self.manifest)

    def test_file_symlink_rejected(self):
        (self.root / 'link').symlink_to(self.root / 'a.txt')
        with self.assertRaises(mod.IntegrityError):
            mod.create(self.root, self.manifest)

    def test_dir_symlink_rejected(self):
        (self.root / 'linkdir').symlink_to(self.root / 'folder', target_is_directory=True)
        with self.assertRaises(mod.IntegrityError):
            mod.create(self.root, self.manifest)

    def test_unsafe_manifest_path_rejected(self):
        self.ready()
        data = json.loads(self.manifest.read_text())
        data['files']['../escape'] = data['files'].pop('a.txt')
        self.manifest.write_text(json.dumps(data))
        with self.assertRaises(mod.IntegrityError):
            mod.verify(self.root, self.manifest)

    def test_invalid_manifest_hash_rejected(self):
        self.ready()
        data = json.loads(self.manifest.read_text())
        data['files']['a.txt']['sha256'] = 'bad'
        self.manifest.write_text(json.dumps(data))
        with self.assertRaises(mod.IntegrityError):
            mod.verify(self.root, self.manifest)

    def test_cli_success_and_failure_codes(self):
        cmd = [sys.executable, str(SCRIPT)]
        a = subprocess.run(cmd + ['create', str(self.root), str(self.manifest)], capture_output=True)
        self.assertEqual(a.returncode, 0, a.stderr)
        b = subprocess.run(cmd + ['verify', str(self.root), str(self.manifest)], capture_output=True)
        self.assertEqual(b.returncode, 0, b.stderr)
        (self.root / 'a.txt').write_bytes(b'wrong')
        c = subprocess.run(cmd + ['verify', str(self.root), str(self.manifest)], capture_output=True)
        self.assertEqual(c.returncode, 1, c.stderr)
        self.assertEqual(json.loads(c.stdout)['changed'], ['a.txt'])

    def test_non_regular_root_rejected(self):
        with self.assertRaises(mod.IntegrityError):
            mod.create(self.root / 'a.txt', self.manifest)

    def test_duplicate_json_keys_rejected(self):
        self.ready()
        raw = self.manifest.read_text()
        self.manifest.write_text(raw.replace('"schema":', '"schema": "bad", "schema":', 1))
        with self.assertRaises(mod.IntegrityError):
            mod.verify(self.root, self.manifest)

    def test_false_size_bool_rejected(self):
        self.ready()
        data = json.loads(self.manifest.read_text())
        data['files']['a.txt']['size'] = True
        self.manifest.write_text(json.dumps(data))
        with self.assertRaises(mod.IntegrityError):
            mod.verify(self.root, self.manifest)


if __name__ == '__main__':
    unittest.main()
