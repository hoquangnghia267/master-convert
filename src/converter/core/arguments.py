from typing import List, Optional, Any, Dict
from dataclasses import dataclass, field

@dataclass
class Argument:
    name: str
    help: str
    metavar: Optional[str] = None
    required: bool = False
    type: Any = str
    action: Optional[str] = None # e.g., 'store_true'

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

    def add_argument(self, name: str, **kwargs):
        """Add a global argument for this converter."""
        self.arguments.append(Argument(name=name, **kwargs))

    def add_group(self, exclusive: bool = False, required: bool = False) -> ArgumentGroup:
        """Create and return a new argument group."""
        group = ArgumentGroup(exclusive=exclusive, required=required)
        self.groups.append(group)
        return group
