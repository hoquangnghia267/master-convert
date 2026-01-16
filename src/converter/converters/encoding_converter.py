import base64
from typing import Any
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError, ConversionError
from ..core.arguments import InterfaceBuilder

class EncodingConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "encoding"

    @property
    def help(self) -> str:
        return "Encode/Decode Base64"

    def configure_args(self, builder: InterfaceBuilder):
        group = builder.add_group(exclusive=True, required=True)
        group.add_argument("b64enc", metavar="STRING", help="Encode string to Base64")
        group.add_argument("b64dec", metavar="BASE64_STRING", help="Decode Base64 string")

    def convert(self, **kwargs: Any):
        if kwargs.get('b64enc'):
            try:
                data = kwargs['b64enc'].encode('utf-8')
                encoded = base64.b64encode(data).decode('utf-8')
                print(encoded)
            except Exception as e:
                raise ConversionError(f"Encoding failed: {e}")
        elif kwargs.get('b64dec'):
            try:
                data = kwargs['b64dec']
                decoded = base64.b64decode(data).decode('utf-8')
                print(decoded)
            except Exception as e:
                raise ValidationError(f"Decoding failed: {e}")

ConverterRegistry.register(EncodingConverter)
