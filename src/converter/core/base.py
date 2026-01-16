from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace

class BaseConverter(ABC):
    """
    Abstract base class for all converters.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the converter (used for CLI command)."""
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        """Help text for the converter."""
        pass

    @abstractmethod
    def setup_parser(self, parser: ArgumentParser):
        """
        Setup arguments for this converter.
        :param parser: The ArgumentParser (or subparser) to add arguments to.
        """
        pass

    @abstractmethod
    def convert(self, args: Namespace):
        """
        Perform the conversion based on the parsed arguments.
        :param args: Parsed arguments from the CLI.
        """
        pass
