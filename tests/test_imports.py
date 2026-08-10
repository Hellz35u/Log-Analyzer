"""Reproduces broken imports by importing modules the same way the real
application does (only backend/ on sys.path), in a clean subprocess so
results aren't affected by the sys.path hacks other test modules use to
work around these same bugs.
"""
import os
import subprocess
import sys
import unittest

BACKEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"
)


def _run(code):
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        cwd=BACKEND_DIR,
    )


class ImportIntegrityTests(unittest.TestCase):
    def test_models_user_model_imports_cleanly(self):
        # See BUG report: models/user_model.py does
        # `from database import get_connection` (bare import) instead
        # of a package-relative import, so this is expected to fail
        # with ModuleNotFoundError when only backend/ is on sys.path.
        code = f"import sys; sys.path.insert(0, {BACKEND_DIR!r}); import models.user_model"
        proc = _run(code)
        self.assertEqual(
            proc.returncode, 0,
            msg=f"import of models.user_model failed:\n{proc.stderr}",
        )

    def test_models_session_model_imports_cleanly(self):
        # Same bare-import bug as above, in models/session_model.py.
        code = f"import sys; sys.path.insert(0, {BACKEND_DIR!r}); import models.session_model"
        proc = _run(code)
        self.assertEqual(
            proc.returncode, 0,
            msg=f"import of models.session_model failed:\n{proc.stderr}",
        )

    def test_server_module_imports_cleanly(self):
        # See BUG report: server.py does
        # `from controller.analysis_controller import analyze_log_file`
        # but the actual directory is `controllers` (plural), so this
        # is expected to fail with ModuleNotFoundError.
        code = f"import sys; sys.path.insert(0, {BACKEND_DIR!r}); import server"
        proc = _run(code)
        self.assertEqual(
            proc.returncode, 0,
            msg=f"import of server failed:\n{proc.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
