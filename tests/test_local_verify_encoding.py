"""The local verifier must give child checks a Unicode-safe Python default."""

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("laif_verify", ROOT / "scripts/laif_verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class LocalVerifierEncodingTests(unittest.TestCase):
    def test_child_uses_utf8_even_when_parent_disables_it(self):
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "utf8-mode.txt"
            command = (
                "import sys; from pathlib import Path; "
                "Path(sys.argv[1]).write_text(str(sys.flags.utf8_mode), encoding='ascii')"
            )
            with mock.patch.dict(os.environ, {"PYTHONUTF8": "0"}):
                VERIFY.run(sys.executable, "-c", command, str(result))
            self.assertEqual(result.read_text(encoding="ascii"), "1")


if __name__ == "__main__":
    unittest.main()
