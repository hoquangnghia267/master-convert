from typing import Any
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError
from ..core.arguments import InterfaceBuilder

class NumberConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "number"

    @property
    def help(self) -> str:
        return "Convert between Hex and Decimal"

    def configure_args(self, builder: InterfaceBuilder):
        group = builder.add_group(exclusive=True, required=True)
        group.add_argument("hex2dec", metavar="HEX_VALUE", help="Convert Hex string to Decimal")
        group.add_argument("dec2hex", metavar="DECIMAL_VALUE", help="Convert Decimal to Hex string")

    def convert(self, **kwargs: Any):
        if kwargs.get('hex2dec'):
            try:
                hex_val = kwargs['hex2dec']
                print(int(hex_val, 16))
            except ValueError:
                raise ValidationError(f"Invalid hex value: {kwargs['hex2dec']}")
        elif kwargs.get('dec2hex'):
            try:
                dec_val = int(kwargs['dec2hex'])
                print(hex(dec_val))
            except ValueError:
                raise ValidationError(f"Invalid decimal value: {kwargs['dec2hex']}")

ConverterRegistry.register(NumberConverter)
