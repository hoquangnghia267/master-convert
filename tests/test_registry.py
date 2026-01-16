import unittest
from converter.core.registry import ConverterRegistry
from converter.core.base import BaseConverter
from argparse import ArgumentParser, Namespace

class MockConverter(BaseConverter):
    @property
    def name(self):
        return "mock"
    @property
    def help(self):
        return "mock help"
    def setup_parser(self, parser):
        pass
    def convert(self, args):
        pass

class TestRegistry(unittest.TestCase):
    def test_registry(self):
        ConverterRegistry.register(MockConverter)
        converters = ConverterRegistry.get_converters()
        self.assertIn("mock", converters)
        self.assertEqual(converters["mock"], MockConverter)

if __name__ == '__main__':
    unittest.main()
