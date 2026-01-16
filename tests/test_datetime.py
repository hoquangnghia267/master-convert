import unittest
import datetime
from argparse import Namespace
from converter.converters.datetime_converter import DatetimeConverter
from converter.core.exceptions import ValidationError

class TestDatetimeConverter(unittest.TestCase):
    def setUp(self):
        self.converter = DatetimeConverter()

    def test_to_ts(self):
        # 2023-01-01 12:00:00 UTC
        # Timestamp: 1672574400.0
        iso_str = "2023-01-01T12:00:00+00:00"
        args = Namespace(to_ts=iso_str, to_dt=None)

        # Capture stdout? Or refactor to return value?
        # The prompt says "Working CLI tool", so printing is expected for CLI.
        # But for unit testing, it's better if the method returned the value or we capture stdout.
        # I'll capture stdout.

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(args)
            output = captured_output.getvalue().strip()
            self.assertEqual(float(output), 1672574400.0)
        finally:
            sys.stdout = sys.__stdout__

    def test_to_dt(self):
        ts = 1672574400.0
        args = Namespace(to_ts=None, to_dt=str(ts))

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(args)
            output = captured_output.getvalue().strip()
            # Expect ISO format in UTC
            self.assertEqual(output, "2023-01-01T12:00:00+00:00")
        finally:
            sys.stdout = sys.__stdout__

    def test_invalid_input(self):
        args = Namespace(to_ts="invalid", to_dt=None)
        with self.assertRaises(ValidationError):
            self.converter.convert(args)

if __name__ == '__main__':
    unittest.main()
