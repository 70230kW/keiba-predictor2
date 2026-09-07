import tempfile
import unittest
from pathlib import Path
from collector.windows.preflight import inspect_environment


class PreflightTests(unittest.TestCase):
    def test_supported_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            checks = inspect_environment("Windows", (3, 14), 64, directory)
        self.assertTrue(all(checks.values()))

    def test_rejects_linux_old_python_and_missing_sdk(self):
        checks = inspect_environment("Linux", (3, 12), 64, "missing-sdk-directory")
        self.assertFalse(checks["windows"])
        self.assertFalse(checks["python_3_14_or_newer"])
        self.assertFalse(checks["sdk_path_exists"])

    def test_rejects_32_bit_python(self):
        with tempfile.TemporaryDirectory() as directory:
            checks = inspect_environment("Windows", (3, 14), 32, directory)
        self.assertFalse(checks["python_64_bit"])
