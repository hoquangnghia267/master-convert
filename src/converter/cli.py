import sys
import argparse
from .core.registry import ConverterRegistry
from .utils.logger import setup_logger
from .core.exceptions import ConverterError

# Import converters to register them
from .converters import datetime_converter, number_converter, encoding_converter

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Universal Converter Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available converters")

    converters = ConverterRegistry.get_converters()

    for name, converter_cls in converters.items():
        converter_instance = converter_cls()
        subparser = subparsers.add_parser(name, help=converter_instance.help)
        converter_instance.setup_parser(subparser)
        subparser.set_defaults(converter=converter_instance)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, 'converter'):
        try:
            args.converter.convert(args)
        except ConverterError as e:
            logger.error(str(e))
            sys.exit(1)
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
