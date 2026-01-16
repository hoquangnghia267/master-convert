import unittest
from argparse import Namespace
from converter.converters.number_converter import NumberConverter
from converter.core.exceptions import ValidationError

class TestNumberConverter(unittest.TestCase):
    def setUp(self):
        self.converter = NumberConverter()

    def test_hex2dec(self):
        args = Namespace(hex2dec="0xA", dec2hex=None)

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(args)
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "10")
        finally:
            sys.stdout = sys.__stdout__

    def test_dec2hex(self):
        args = Namespace(hex2dec=None, dec2hex="10")

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(args)
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "0xa")
        finally:
            sys.stdout = sys.__stdout__

    def test_invalid_hex(self):
        args = Namespace(hex2dec="ZZZ", dec2hex=None)
        with self.assertRaises(ValidationError):
            self.converter.convert(args)

if __name__ == '__main__':
    unittest.main()
