import base64
from argparse import ArgumentParser, Namespace
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError, ConversionError

class EncodingConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "encoding"

    @property
    def help(self) -> str:
        return "Encode/Decode Base64"

    def setup_parser(self, parser: ArgumentParser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--b64enc", metavar="STRING", help="Encode string to Base64")
        group.add_argument("--b64dec", metavar="BASE64_STRING", help="Decode Base64 string")

    def convert(self, args: Namespace):
        if args.b64enc:
            try:
                data = args.b64enc.encode('utf-8')
                encoded = base64.b64encode(data).decode('utf-8')
                print(encoded)
            except Exception as e:
                raise ConversionError(f"Encoding failed: {e}")
        elif args.b64dec:
            try:
                data = args.b64dec
                decoded = base64.b64decode(data).decode('utf-8')
                print(decoded)
            except Exception as e:
                raise ValidationError(f"Decoding failed: {e}")

ConverterRegistry.register(EncodingConverter)
