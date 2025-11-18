from pathlib import Path
import unittest

from TPS2TOPAS import parse_cli_arguments
TEST_DATA_FILE = Path(__file__).with_name("data") / "sample_inputfile.txt"


class CLISmokeTests(unittest.TestCase):
    def test_cli_defaults_to_gui(self):
        mode, path = parse_cli_arguments([])
        self.assertEqual(mode, "gui")
        self.assertEqual(path, "")

    def test_cli_requires_input_file_for_input_mode(self):
        mode, path = parse_cli_arguments(["--mode", "inputfile", "--input-file", str(TEST_DATA_FILE)])
        self.assertEqual(mode, "file")
        self.assertEqual(path, str(TEST_DATA_FILE))

    def test_cli_rejects_unexpected_input_file(self):
        with self.assertRaises(SystemExit):
            parse_cli_arguments(["--input-file", "params.txt"])

    def test_cli_accepts_legacy_positional_argument(self):
        mode, path = parse_cli_arguments(["--mode", "inputfile", str(TEST_DATA_FILE)])
        self.assertEqual(mode, "file")
        self.assertEqual(path, str(TEST_DATA_FILE))


if __name__ == "__main__":
    unittest.main()
