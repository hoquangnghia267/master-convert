import unittest
from converter.core.registry import ConverterRegistry
from converter.core.base import BaseConverter
from converter.core.arguments import InterfaceBuilder

class MockConverter(BaseConverter):
    @property
    def name(self):
        return "mock"
    @property
    def help(self):
        return "mock help"
    def configure_args(self, builder: InterfaceBuilder):
        pass
    def convert(self, **kwargs):
        pass

class TestRegistry(unittest.TestCase):
    def test_registry(self):
        ConverterRegistry.register(MockConverter)
        converters = ConverterRegistry.get_converters()
        self.assertIn("mock", converters)
        self.assertEqual(converters["mock"], MockConverter)

if __name__ == '__main__':
    unittest.main()
