import sys
import argparse
from typing import Optional
from .core.registry import ConverterRegistry
from .utils.logger import setup_logger
from .core.exceptions import ConverterError
from .core.arguments import InterfaceBuilder, ArgumentGroup, Argument

# Import converters to register them
from .converters import datetime_converter, number_converter, encoding_converter

logger = setup_logger()

class CLIBuilder(InterfaceBuilder):
    """
    Adapts abstract arguments to argparse.
    """
    def __init__(self, parser: argparse.ArgumentParser):
        super().__init__()
        self.parser = parser

    def add_argument(self, name: str, **kwargs):
        # Convert simple name to CLI flag (e.g. 'to_ts' -> '--to-ts')
        flag_name = "--" + name.replace("_", "-")
        self.parser.add_argument(flag_name, dest=name, **kwargs)

    def add_group(self, exclusive: bool = False, required: bool = False) -> ArgumentGroup:
        # We override this to return a wrapped group that calls argparse immediately
        # But ArgumentGroup stores args in a list.
        # We need to adapt the ArgumentGroup to call argparse on its arguments.
        # So we return a custom Group object or we hook into the process.

        # Better approach: Use the base class structure to collect args,
        # then build argparse from that structure.
        return super().add_group(exclusive, required)

    def build(self):
        """Apply collected arguments to argparse."""
        for group_def in self.groups:
            if group_def.exclusive:
                group = self.parser.add_mutually_exclusive_group(required=group_def.required)
            else:
                group = self.parser.add_argument_group() # argparse doesn't have "required" normal groups in same way

            for arg in group_def.arguments:
                flag_name = "--" + arg.name.replace("_", "-")
                # Filter out None values from kwargs
                kwargs = {k: v for k, v in vars(arg).items() if k != 'name' and v is not None}
                group.add_argument(flag_name, dest=arg.name, **kwargs)

        for arg in self.arguments:
             flag_name = "--" + arg.name.replace("_", "-")
             kwargs = {k: v for k, v in vars(arg).items() if k != 'name' and v is not None}
             self.parser.add_argument(flag_name, dest=arg.name, **kwargs)


def main():
    parser = argparse.ArgumentParser(description="Universal Converter Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available converters")

    converters = ConverterRegistry.get_converters()

    for name, converter_cls in converters.items():
        converter_instance = converter_cls()
        subparser = subparsers.add_parser(name, help=converter_instance.help)

        # Build arguments
        builder = CLIBuilder(subparser)
        converter_instance.configure_args(builder)
        builder.build()

        subparser.set_defaults(converter=converter_instance)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, 'converter'):
        try:
            # Convert Namespace to dict
            kwargs = vars(args)
            args.converter.convert(**kwargs)
        except ConverterError as e:
            logger.error(str(e))
            sys.exit(1)
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
