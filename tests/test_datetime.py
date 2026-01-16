import unittest
import datetime
from converter.converters.datetime_converter import DatetimeConverter
from converter.core.exceptions import ValidationError

class TestDatetimeConverter(unittest.TestCase):
    def setUp(self):
        self.converter = DatetimeConverter()

    def test_to_ts(self):
        # 2023-01-01 12:00:00 UTC -> 1672574400.0
        iso_str = "2023-01-01T12:00:00+00:00"

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # New signature: kwargs
            self.converter.convert(to_ts=iso_str)
            output = captured_output.getvalue().strip()
            self.assertEqual(float(output), 1672574400.0)
        finally:
            sys.stdout = sys.__stdout__

    def test_to_dt(self):
        ts = 1672574400.0

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(to_dt=ts)
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "2023-01-01T12:00:00+00:00")
        finally:
            sys.stdout = sys.__stdout__

    def test_invalid_input(self):
        with self.assertRaises(ValidationError):
            self.converter.convert(to_ts="invalid")

if __name__ == '__main__':
    unittest.main()
