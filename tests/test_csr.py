import unittest
from converter.converters.csr_converter import CSRConverter
from converter.core.exceptions import ValidationError

class TestCSRConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CSRConverter()

    def test_generate_csr(self):
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.converter.convert(generate_csr=True, cn="example.com", c="US")
            output = captured_output.getvalue().strip()
            self.assertIn("=== Private Key (Keep Secret) ===", output)
            self.assertIn("=== CSR ===", output)
            self.assertIn("BEGIN CERTIFICATE REQUEST", output)
        finally:
            sys.stdout = sys.__stdout__

    def test_generate_csr_missing_cn(self):
        with self.assertRaises(ValidationError):
            self.converter.convert(generate_csr=True, c="US") # Missing CN

if __name__ == '__main__':
    unittest.main()
