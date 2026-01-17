import pandas as pd
from typing import Any
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError
from ..core.arguments import InterfaceBuilder, ArgumentType

class NumberConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "number"

    @property
    def help(self) -> str:
        return "Convert between Hex and Decimal (Batch supported)"

    def configure_args(self, builder: InterfaceBuilder):
        group = builder.add_group(exclusive=True, required=True)
        group.add_argument("hex2dec", type=ArgumentType.TEXT, metavar="HEX_VALUE", help="Convert Hex string(s) to Decimal")
        group.add_argument("dec2hex", type=ArgumentType.TEXT, metavar="DECIMAL_VALUE", help="Convert Decimal(s) to Hex string")

        builder.add_argument("export_excel", type=ArgumentType.FILE_SAVE, metavar="OUTPUT_FILE", help="Export result to Excel file")

    def convert(self, **kwargs: Any):
        results = []

        if kwargs.get('hex2dec'):
            lines = kwargs['hex2dec'].splitlines()
            for line in lines:
                line = line.strip()
                if not line: continue
                try:
                    res = int(line, 16)
                    results.append({"Input": line, "Output": res})
                    print(res)
                except ValueError:
                    print(f"Error parsing '{line}'")
                    results.append({"Input": line, "Output": "Error"})

        elif kwargs.get('dec2hex'):
            lines = kwargs['dec2hex'].splitlines()
            for line in lines:
                line = line.strip()
                if not line: continue
                try:
                    val = int(line)
                    res = hex(val)
                    results.append({"Input": line, "Output": res})
                    print(res)
                except ValueError:
                    print(f"Error parsing '{line}'")
                    results.append({"Input": line, "Output": "Error"})

        if kwargs.get('export_excel') and results:
            try:
                df = pd.DataFrame(results)
                df.to_excel(kwargs['export_excel'], index=False)
                print(f"\nSuccessfully exported to {kwargs['export_excel']}")
            except Exception as e:
                print(f"\nFailed to export Excel: {e}")

ConverterRegistry.register(NumberConverter)
