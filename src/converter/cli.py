import sys
import argparse
from typing import Optional
from .core.registry import ConverterRegistry
from .utils.logger import setup_logger
from .core.exceptions import ConverterError
from .core.arguments import InterfaceBuilder, ArgumentGroup, Argument, ArgumentType

# Import converters
from .converters import datetime_converter, number_converter, csr_converter

logger = setup_logger()

class CLIBuilder(InterfaceBuilder):
    """
    Adapts abstract arguments to argparse.
    """
    def __init__(self, parser: argparse.ArgumentParser):
        super().__init__()
        self.parser = parser

    def build(self):
        """Apply collected arguments to argparse."""
        for group_def in self.groups:
            if group_def.exclusive:
                group = self.parser.add_mutually_exclusive_group(required=group_def.required)
            else:
                group = self.parser.add_argument_group()

            for arg in group_def.arguments:
                self._add_arg_to_parser(group, arg)

        for arg in self.arguments:
             self._add_arg_to_parser(self.parser, arg)

    def _add_arg_to_parser(self, parser, arg):
        flag_name = "--" + arg.name.replace("_", "-")
        # Filter vars
        kwargs = {k: v for k, v in vars(arg).items() if k not in ['name', 'type'] and v is not None}
        parser.add_argument(flag_name, dest=arg.name, **kwargs)


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
            # Remove system args
            clean_kwargs = {k:v for k,v in kwargs.items() if k != 'command' and k != 'converter'}
            args.converter.convert(**clean_kwargs)
        except ConverterError as e:
            logger.error(str(e))
            sys.exit(1)
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
