import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import add_import_paths

add_import_paths()

import controllers.analysis_controller as analysis_controller
from parsers.common_parser import CommonParser


class AnalysisControllerTests(unittest.TestCase):
    def setUp(self):
        fd, self.log_path = tempfile.mkstemp(suffix=".log")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(
                '127.0.0.1 - - [10/Aug/2026:12:00:00 +0000] '
                '"GET /index.html HTTP/1.1" 200 1024 \n'
            )

    def tearDown(self):
        os.remove(self.log_path)

    def test_analyze_log_file_returns_analysis_result(self):
        # See BUG report: analyze_log_file() calls itself recursively
        # instead of calling log_analyzer.analyze_logs(), so this is
        # expected to raise TypeError (missing 'parser' argument)
        # rather than returning an analysis dict.
        result = analysis_controller.analyze_log_file(self.log_path, CommonParser())
        self.assertIn("total_requests", result)
        self.assertEqual(result["total_requests"], 1)


if __name__ == "__main__":
    unittest.main()
