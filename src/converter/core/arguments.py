from typing import List, Optional, Any, Dict
from dataclasses import dataclass, field
from enum import Enum, auto

class ArgumentType(Enum):
    STRING = auto()
    TEXT = auto()      # Multiline text
    FILE_SAVE = auto() # File path for saving
    FLAG = auto()      # Boolean flag

@dataclass
class Argument:
    name: str
    help: str
    metavar: Optional[str] = None
    required: bool = False
    type: ArgumentType = ArgumentType.STRING
    default: Any = None
    action: Optional[str] = None

@dataclass
class ArgumentGroup:
    exclusive: bool = False
    required: bool = False
    arguments: List[Argument] = field(default_factory=list)

    def add_argument(self, name: str, **kwargs):
        self.arguments.append(Argument(name=name, **kwargs))

class InterfaceBuilder:
    """
    Abstract builder that collects arguments.
    Implementations will convert these into CLI parsers or GUI widgets.
    """
    def __init__(self):
        self.groups: List[ArgumentGroup] = []
        self.arguments: List[Argument] = []

    def add_argument(self, name: str, arg_type: ArgumentType = ArgumentType.STRING, **kwargs):
        """Add a global argument for this converter."""
        # Infer FLAG type if action is store_true
        if kwargs.get('action') == 'store_true':
            arg_type = ArgumentType.FLAG
        self.arguments.append(Argument(name=name, type=arg_type, **kwargs))

    def add_group(self, exclusive: bool = False, required: bool = False) -> ArgumentGroup:
        """Create and return a new argument group."""
        group = ArgumentGroup(exclusive=exclusive, required=required)
        self.groups.append(group)
        return group
