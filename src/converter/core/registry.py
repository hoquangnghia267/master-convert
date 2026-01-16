from typing import Dict, Type
from .base import BaseConverter
from ..utils.logger import setup_logger

logger = setup_logger()

class ConverterRegistry:
    """
    Registry for available converters.
    """
    _converters: Dict[str, Type[BaseConverter]] = {}

    @classmethod
    def register(cls, converter_cls: Type[BaseConverter]):
        """
        Register a converter class.
        """
        # Instantiate to get the name property, or we could make name a class property.
        # However, for simplicity, let's assume we can access name via an instance or class attribute.
        # To be safe and clean, we will instantiate it later, but we need the name now.
        # Let's assume the class has a 'name' attribute or property.
        # If it's a property on instance, we might need to instantiate it.
        # Let's instantiate it to register.
        try:
            instance = converter_cls()
            cls._converters[instance.name] = converter_cls
            logger.debug(f"Registered converter: {instance.name}")
        except Exception as e:
            logger.error(f"Failed to register converter {converter_cls}: {e}")

    @classmethod
    def get_converters(cls) -> Dict[str, Type[BaseConverter]]:
        """
        Get all registered converters.
        """
        return cls._converters
