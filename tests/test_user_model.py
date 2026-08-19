import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import add_import_paths

add_import_paths()

import database
import models.user_model as user_model


class UserModelTests(unittest.TestCase):
    def setUp(self):
        self._orig_path = database.DATABASE_PATH
        self.tmp_dir = tempfile.mkdtemp()
        database.DATABASE_PATH = os.path.join(self.tmp_dir, "test.db")
        database.create_table()

    def tearDown(self):
        database.DATABASE_PATH = self._orig_path
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _seed_user(self, username, password_hash=b"hashed-bytes"):
        """Insert a user directly via the real schema (password_hash),
        bypassing add_new_user, so read-path tests aren't blinded by the
        write-path bug documented below."""
        conn = database.get_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
        finally:
            conn.close()

    def test_add_new_user_then_get_by_username_roundtrip(self):
        # Exercises add_new_user() as specified: insert a user, then
        # look it up. See BUG report: add_new_user() inserts into a
        # `password` column that does not exist in the `users` table
        # schema (the real column is `password_hash`), so this is
        # expected to fail with sqlite3.OperationalError.
        user_model.add_new_user("alice", b"hashed-bytes")
        fetched = user_model.get_user_by_username("alice")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["username"], "alice")

    def test_get_user_by_username_found(self):
        self._seed_user("bob")
        fetched = user_model.get_user_by_username("bob")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["username"], "bob")

    def test_get_user_by_username_missing_returns_none(self):
        fetched = user_model.get_user_by_username("nobody")
        self.assertIsNone(fetched)

    def test_get_user_by_id_found(self):
        self._seed_user("carol")
        by_username = user_model.get_user_by_username("carol")
        fetched = user_model.get_user_by_id(by_username["id"])
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["username"], "carol")

    def test_get_user_by_id_missing_returns_none(self):
        fetched = user_model.get_user_by_id(999999)
        self.assertIsNone(fetched)


if __name__ == "__main__":
    unittest.main()
