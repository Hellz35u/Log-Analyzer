import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import add_import_paths

add_import_paths()

import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self._orig_path = database.DATABASE_PATH
        self.tmp_dir = tempfile.mkdtemp()
        database.DATABASE_PATH = os.path.join(self.tmp_dir, "test.db")

    def tearDown(self):
        database.DATABASE_PATH = self._orig_path
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_get_connection_returns_row_factory_connection(self):
        conn = database.get_connection()
        try:
            self.assertIs(conn.row_factory, sqlite3.Row)
        finally:
            conn.close()

    def test_create_table_creates_users_analysis_sessions_tables(self):
        database.create_table()
        conn = database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = {row["name"] for row in cursor.fetchall()}
        finally:
            conn.close()
        self.assertTrue({"users", "analysis", "sessions"}.issubset(table_names))

    def test_create_table_is_idempotent(self):
        database.create_table()
        database.create_table()  # must not raise

    def test_users_table_columns(self):
        database.create_table()
        conn = database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(users)")
            columns = {row["name"] for row in cursor.fetchall()}
        finally:
            conn.close()
        self.assertEqual(columns, {"id", "username", "password_hash", "create_at"})


if __name__ == "__main__":
    unittest.main()
