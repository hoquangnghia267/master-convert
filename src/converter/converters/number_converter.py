from argparse import ArgumentParser, Namespace
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError

class NumberConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "number"

    @property
    def help(self) -> str:
        return "Convert between Hex and Decimal"

    def setup_parser(self, parser: ArgumentParser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--hex2dec", metavar="HEX_VALUE", help="Convert Hex string to Decimal")
        group.add_argument("--dec2hex", metavar="DECIMAL_VALUE", help="Convert Decimal to Hex string")

    def convert(self, args: Namespace):
        if args.hex2dec:
            try:
                # Handle optional 0x prefix
                hex_val = args.hex2dec
                print(int(hex_val, 16))
            except ValueError:
                raise ValidationError(f"Invalid hex value: {args.hex2dec}")
        elif args.dec2hex:
            try:
                dec_val = int(args.dec2hex)
                print(hex(dec_val))
            except ValueError:
                raise ValidationError(f"Invalid decimal value: {args.dec2hex}")

ConverterRegistry.register(NumberConverter)
