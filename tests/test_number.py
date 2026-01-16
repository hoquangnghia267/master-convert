import unittest
from converter.converters.number_converter import NumberConverter
from converter.core.exceptions import ValidationError

class TestNumberConverter(unittest.TestCase):
    def setUp(self):
        self.converter = NumberConverter()

    def test_hex2dec(self):
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(hex2dec="0xA")
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "10")
        finally:
            sys.stdout = sys.__stdout__

    def test_dec2hex(self):
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(dec2hex="10")
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "0xa")
        finally:
            sys.stdout = sys.__stdout__

    def test_invalid_hex(self):
        with self.assertRaises(ValidationError):
            self.converter.convert(hex2dec="ZZZ")

if __name__ == '__main__':
    unittest.main()
