import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import add_import_paths

add_import_paths()

import database
import models.session_model as session_model

FMT = "%Y-%m-%d %H:%M:%S"


class SessionModelTests(unittest.TestCase):
    def setUp(self):
        self._orig_path = database.DATABASE_PATH
        self.tmp_dir = tempfile.mkdtemp()
        database.DATABASE_PATH = os.path.join(self.tmp_dir, "test.db")
        database.create_table()

        conn = database.get_connection()
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("dummy", b"hash"),
        )
        conn.commit()
        self.user_id = conn.execute(
            "SELECT id FROM users WHERE username = ?", ("dummy",)
        ).fetchone()["id"]
        conn.close()

    def tearDown(self):
        database.DATABASE_PATH = self._orig_path
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_create_session_returns_row_id(self):
        expires_at = (datetime.now() + timedelta(hours=1)).strftime(FMT)
        session_id = session_model.create_session(self.user_id, "tok-hash-1", expires_at)
        self.assertIsInstance(session_id, int)
        self.assertGreater(session_id, 0)

    def test_get_session_by_token_hash_found(self):
        expires_at = (datetime.now() + timedelta(hours=1)).strftime(FMT)
        session_model.create_session(self.user_id, "tok-hash-2", expires_at)
        row = session_model.get_session_by_token_hash("tok-hash-2")
        self.assertIsNotNone(row)
        self.assertEqual(row["user_id"], self.user_id)

    def test_get_session_by_token_hash_missing_returns_none(self):
        row = session_model.get_session_by_token_hash("does-not-exist")
        self.assertIsNone(row)

    def test_delete_session_removes_row(self):
        expires_at = (datetime.now() + timedelta(hours=1)).strftime(FMT)
        session_model.create_session(self.user_id, "tok-hash-3", expires_at)
        session_model.delete_session("tok-hash-3")
        row = session_model.get_session_by_token_hash("tok-hash-3")
        self.assertIsNone(row)

    def test_delete_session_nonexistent_does_not_raise(self):
        session_model.delete_session("no-such-token")

    def test_delete_expired_session_removes_only_expired(self):
        past = (datetime.now() - timedelta(hours=1)).strftime(FMT)
        future = (datetime.now() + timedelta(hours=1)).strftime(FMT)
        session_model.create_session(self.user_id, "tok-expired", past)
        session_model.create_session(self.user_id, "tok-active", future)

        session_model.delete_expired_session()

        self.assertIsNone(session_model.get_session_by_token_hash("tok-expired"))
        self.assertIsNotNone(session_model.get_session_by_token_hash("tok-active"))


if __name__ == "__main__":
    unittest.main()
