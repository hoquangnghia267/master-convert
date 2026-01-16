import datetime
from argparse import ArgumentParser, Namespace
from ..core.base import BaseConverter
from ..core.registry import ConverterRegistry
from ..core.exceptions import ValidationError, ConversionError

class DatetimeConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "datetime"

    @property
    def help(self) -> str:
        return "Convert between Timestamp and Datetime (ISO format)"

    def setup_parser(self, parser: ArgumentParser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--to-ts", metavar="ISO_DATETIME", help="Convert ISO datetime string to timestamp")
        group.add_argument("--to-dt", metavar="TIMESTAMP", help="Convert timestamp to ISO datetime string")

    def convert(self, args: Namespace):
        if args.to_ts:
            try:
                # Assuming ISO format. Using datetime.fromisoformat which supports timezones in newer python versions.
                # If the string doesn't have timezone, we assume local or UTC?
                # "Timestamp <-> datetime (timezone aware)" requirement.
                dt = datetime.datetime.fromisoformat(args.to_ts)
                print(dt.timestamp())
            except ValueError as e:
                raise ValidationError(f"Invalid ISO datetime format: {e}")
        elif args.to_dt:
            try:
                ts = float(args.to_dt)
                # Using fromtimestamp with timezone info (UTC by default for clarity or local?)
                # Requirement: "timezone aware".
                # Let's output in UTC ISO format.
                dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
                print(dt.isoformat())
            except ValueError as e:
                raise ValidationError(f"Invalid timestamp: {e}")

ConverterRegistry.register(DatetimeConverter)
