import os
import shutil
import sys
import tempfile
import unittest

import bcrypt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import add_import_paths

add_import_paths()

import database
import controllers.auth_controller as auth_controller


class AuthControllerTests(unittest.TestCase):
    def setUp(self):
        self._orig_path = database.DATABASE_PATH
        self.tmp_dir = tempfile.mkdtemp()
        database.DATABASE_PATH = os.path.join(self.tmp_dir, "test.db")
        database.create_table()

    def tearDown(self):
        database.DATABASE_PATH = self._orig_path
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _seed_user(self, username, password):
        """Seed a user directly against the real schema (password_hash)
        so login() tests aren't blocked by the registration bug."""
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        conn = database.get_connection()
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
        conn.close()

    # ---- registration ----

    def test_register_invalid_username_is_rejected(self):
        result = auth_controller.register("ab", "ValidPass1")
        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 400)

    def test_register_invalid_password_is_rejected(self):
        result = auth_controller.register("validuser", "short")
        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 400)

    def test_register_duplicate_username_is_rejected(self):
        self._seed_user("existing", "ValidPass1")
        result = auth_controller.register("existing", "AnotherPass1")
        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 400)
        self.assertIn("already exists", result["message"])

    def test_register_valid_user_succeeds(self):
        # See BUG report: add_new_user() inserts into a non-existent
        # `password` column, so register() is expected to fail here
        # with a 500 "Database Error" instead of succeeding.
        result = auth_controller.register("newuser", "ValidPass1")
        self.assertTrue(
            result["success"],
            msg=f"register() did not report success, got: {result!r}",
        )
        self.assertEqual(result.get("status_code"), 200)

    # ---- login ----

    def test_login_nonexistent_user_is_rejected(self):
        result = auth_controller.login("ghost", "whatever1")
        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 401)

    def test_login_incorrect_password_is_rejected(self):
        # See BUG report: login() reads user["password"], but the
        # actual column is `password_hash` -- expected to raise an
        # uncaught IndexError rather than returning a clean 401.
        self._seed_user("loginuser1", "CorrectPass1")
        result = auth_controller.login("loginuser1", "WrongPass1")
        self.assertFalse(
            result["success"],
            msg=f"login() should reject a wrong password, got: {result!r}",
        )
        self.assertEqual(result.get("status_code"), 401)

    def test_login_success_returns_token(self):
        # Same user["password"] bug as above blocks this from ever
        # reaching the token-issuing / create_session code path.
        self._seed_user("loginuser2", "CorrectPass1")
        result = auth_controller.login("loginuser2", "CorrectPass1")
        self.assertTrue(
            result["success"],
            msg=f"login() did not report success, got: {result!r}",
        )
        self.assertIn("token", result)


if __name__ == "__main__":
    unittest.main()
