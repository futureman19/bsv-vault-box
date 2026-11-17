import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from recovery import backup, restore, safe, sha, verify


class RecoveryTests(unittest.TestCase):
    def test_portable_paths(self):
        for name in ('../x', '/x', 'a\\b', 'C:x', 'a//b', './a', 'NUL.txt', 'aux', 'a.', 'a ', 'a:b', 'a?b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                safe(name)
        safe('regtest/transaction-01.json')

    def test_archive_guards(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            root = Path(directory); source = root / 'source'; source.mkdir()
            (source / 'fixture.txt').write_bytes(b'public fixture')
            row = {'path': 'fixture.txt', 'bytes': 14, 'sha256': sha(b'public fixture')}
            (source / 'sha256.json').write_text(json.dumps([row]))
            manifest_hash = sha((source / 'sha256.json').read_bytes())
            archive = root / 'good.zip'
            result = backup(source, archive, manifest_hash)
            self.assertEqual(len(verify(archive, result['archiveSha256'])), 2)
            restore(archive, result['archiveSha256'], root / 'restored')
            for variant in ('duplicate', 'missing', 'tampered', 'symlink'):
                bad = root / (variant + '.zip')
                with zipfile.ZipFile(bad, 'w') as z:
                    z.writestr('sha256.json', (source / 'sha256.json').read_bytes())
                    if variant != 'missing':
                        item = zipfile.ZipInfo('fixture.txt')
                        if variant == 'symlink':
                            item.external_attr = 0o120777 << 16
                        z.writestr(item, b'changed' if variant == 'tampered' else b'public fixture')
                    if variant == 'duplicate':
                        z.writestr('FIXTURE.TXT', b'public fixture')
                with self.subTest(variant=variant), self.assertRaises(ValueError):
                    restore(bad, sha(bad.read_bytes()), root / ('restore-' + variant))
                self.assertFalse((root / ('restore-' + variant)).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
