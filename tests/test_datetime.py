import unittest
import os
import pandas as pd
from converter.converters.datetime_converter import DatetimeConverter

class TestDatetimeConverter(unittest.TestCase):
    def setUp(self):
        self.converter = DatetimeConverter()

    def test_batch_to_ts(self):
        # Batch input
        iso_str = "2023-01-01T12:00:00+00:00\n2023-01-02T12:00:00+00:00"

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(to_ts=iso_str)
            output = captured_output.getvalue().strip()
            self.assertIn("1672574400.0", output)
            self.assertIn("1672660800.0", output)
        finally:
            sys.stdout = sys.__stdout__

    def test_excel_export(self):
        iso_str = "2023-01-01T12:00:00+00:00"
        output_file = "test_dt_output.xlsx"
        try:
            from io import StringIO
            import sys
            # Suppress output
            sys.stdout = StringIO()

            self.converter.convert(to_ts=iso_str, export_excel=output_file)

            self.assertTrue(os.path.exists(output_file))
            df = pd.read_excel(output_file)
            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]['Output'], 1672574400.0)

        finally:
             sys.stdout = sys.__stdout__
             if os.path.exists(output_file):
                 os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
