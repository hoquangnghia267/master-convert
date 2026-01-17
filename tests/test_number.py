import unittest
import os
import pandas as pd
from converter.converters.number_converter import NumberConverter

class TestNumberConverter(unittest.TestCase):
    def setUp(self):
        self.converter = NumberConverter()

    def test_batch_hex2dec(self):
        input_str = "0xA\n0xB"

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(hex2dec=input_str)
            output = captured_output.getvalue().strip()
            self.assertIn("10", output)
            self.assertIn("11", output)
        finally:
            sys.stdout = sys.__stdout__

    def test_excel_export(self):
        input_str = "0xA"
        output_file = "test_num_output.xlsx"
        try:
            from io import StringIO
            import sys
            sys.stdout = StringIO()

            self.converter.convert(hex2dec=input_str, export_excel=output_file)

            self.assertTrue(os.path.exists(output_file))
            df = pd.read_excel(output_file)
            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]['Output'], 10)

        finally:
             sys.stdout = sys.__stdout__
             if os.path.exists(output_file):
                 os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
