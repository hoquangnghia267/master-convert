from abc import ABC, abstractmethod
from typing import Any, Dict
from .arguments import InterfaceBuilder

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
    def configure_args(self, builder: InterfaceBuilder):
        """
        Define arguments for this converter using the generic builder.
        :param builder: The InterfaceBuilder to add arguments/groups to.
        """
        pass

    @abstractmethod
    def convert(self, **kwargs: Any):
        """
        Perform the conversion based on the provided arguments.
        :param kwargs: Dictionary of argument names and values.
        """
        pass
