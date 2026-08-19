"""Shared test utilities: import-path setup for the backend package tree.

Not a test module itself -- contains no TestCase classes, so unittest
discovery will simply ignore it (no test_ prefix on this filename either).
"""
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")


def add_import_paths():
    """Add backend/ and backend/models/ to sys.path.

    backend/ is required so `models.*`, `controllers.*` and `services.*`
    resolve as (namespace) packages.

    backend/models/ is additionally required because
    models/user_model.py and models/session_model.py import their
    sibling `database` module with a bare `from database import
    get_connection` instead of a package-relative import. Without
    backend/models/ directly on sys.path that bare import raises
    ModuleNotFoundError -- see the bug reported for this in the test
    run summary (also reproduced directly in test_imports.py).
    """
    for path in (BACKEND_DIR, MODELS_DIR):
        if path not in sys.path:
            sys.path.insert(0, path)
