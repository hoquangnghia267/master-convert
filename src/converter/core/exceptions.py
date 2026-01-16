class ConverterError(Exception):
    """Base exception for converter errors."""
    pass

class ValidationError(ConverterError):
    """Raised when input validation fails."""
    pass

class ConversionError(ConverterError):
    """Raised when conversion fails."""
    pass
