import unittest
import base64
from converter.converters.encoding_converter import EncodingConverter
from converter.core.exceptions import ValidationError

class TestEncodingConverter(unittest.TestCase):
    def setUp(self):
        self.converter = EncodingConverter()

    def test_b64enc(self):
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(b64enc="hello")
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "aGVsbG8=")
        finally:
            sys.stdout = sys.__stdout__

    def test_b64dec(self):
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(b64dec="aGVsbG8=")
            output = captured_output.getvalue().strip()
            self.assertEqual(output, "hello")
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
