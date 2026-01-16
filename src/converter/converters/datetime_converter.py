import datetime
from typing import Any
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError
from ..core.arguments import InterfaceBuilder

class DatetimeConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "datetime"

    @property
    def help(self) -> str:
        return "Convert between Timestamp and Datetime (ISO format)"

    def configure_args(self, builder: InterfaceBuilder):
        group = builder.add_group(exclusive=True, required=True)
        group.add_argument("to_ts", metavar="ISO_DATETIME", help="Convert ISO datetime string to timestamp")
        group.add_argument("to_dt", metavar="TIMESTAMP", help="Convert timestamp to ISO datetime string")

    def convert(self, **kwargs: Any):
        if kwargs.get('to_ts'):
            try:
                dt = datetime.datetime.fromisoformat(kwargs['to_ts'])
                print(dt.timestamp())
            except ValueError as e:
                raise ValidationError(f"Invalid ISO datetime format: {e}")
        elif kwargs.get('to_dt'):
            try:
                ts = float(kwargs['to_dt'])
                dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
                print(dt.isoformat())
            except ValueError as e:
                raise ValidationError(f"Invalid timestamp: {e}")

ConverterRegistry.register(DatetimeConverter)
