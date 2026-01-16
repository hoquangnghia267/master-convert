import unittest
import base64
from argparse import Namespace
from converter.converters.encoding_converter import EncodingConverter
from converter.core.exceptions import ValidationError

class TestEncodingConverter(unittest.TestCase):
    def setUp(self):
        self.converter = EncodingConverter()

    def test_b64enc(self):
        args = Namespace(b64enc="hello", b64dec=None)

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(args)
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "aGVsbG8=")
        finally:
            sys.stdout = sys.__stdout__

    def test_b64dec(self):
        args = Namespace(b64enc=None, b64dec="aGVsbG8=")

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(args)
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "hello")
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
