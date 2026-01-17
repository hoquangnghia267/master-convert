import datetime
import pandas as pd
from typing import Any
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError
from ..core.arguments import InterfaceBuilder, ArgumentType

class DatetimeConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "datetime"

    @property
    def help(self) -> str:
        return "Convert between Timestamp and Datetime (Batch supported)"

    def configure_args(self, builder: InterfaceBuilder):
        group = builder.add_group(exclusive=True, required=True)
        group.add_argument("to_ts", type=ArgumentType.TEXT, metavar="ISO_DATETIME", help="Convert ISO datetime string(s) to timestamp")
        group.add_argument("to_dt", type=ArgumentType.TEXT, metavar="TIMESTAMP", help="Convert timestamp(s) to ISO datetime string")

        builder.add_argument("export_excel", type=ArgumentType.FILE_SAVE, metavar="OUTPUT_FILE", help="Export result to Excel file")

    def convert(self, **kwargs: Any):
        results = []
        mode = ""

        if kwargs.get('to_ts'):
            mode = "to_ts"
            lines = kwargs['to_ts'].splitlines()
            for line in lines:
                line = line.strip()
                if not line: continue
                try:
                    dt = datetime.datetime.fromisoformat(line)
                    res = dt.timestamp()
                    results.append({"Input": line, "Output": res})
                    print(res)
                except ValueError as e:
                    print(f"Error parsing '{line}': {e}")
                    results.append({"Input": line, "Output": "Error"})

        elif kwargs.get('to_dt'):
            mode = "to_dt"
            lines = kwargs['to_dt'].splitlines()
            for line in lines:
                line = line.strip()
                if not line: continue
                try:
                    ts = float(line)
                    dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
                    res = dt.isoformat()
                    results.append({"Input": line, "Output": res})
                    print(res)
                except ValueError as e:
                    print(f"Error parsing '{line}': {e}")
                    results.append({"Input": line, "Output": "Error"})

        if kwargs.get('export_excel') and results:
            try:
                df = pd.DataFrame(results)
                df.to_excel(kwargs['export_excel'], index=False)
                print(f"\nSuccessfully exported to {kwargs['export_excel']}")
            except Exception as e:
                print(f"\nFailed to export Excel: {e}")

ConverterRegistry.register(DatetimeConverter)
