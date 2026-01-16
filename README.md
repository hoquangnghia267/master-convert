# Universal Converter Platform

A modular, production-ready CLI tool for various conversions, built with Python.

## Features

**Phase 1 (Implemented):**
- **Datetime**: Convert between Timestamp and ISO 8601 Datetime (Timezone aware).
- **Number**: Convert between Hexadecimal and Decimal.
- **Encoding**: Base64 Encode/Decode.

**Phase 2 (Planned):**
- DOCX to PDF
- Image format conversions (JPG, PNG, WEBP)

## Architecture

The project follows a modular, plugin-based architecture.

- **Core**: Contains the base converter interface (`BaseConverter`), the registry (`ConverterRegistry`), and custom exceptions.
- **Converters**: Individual converter implementations that inherit from `BaseConverter`.
- **CLI**: The main entry point that dynamically loads registered converters and exposes them as subcommands.

This design allows for easy extension. To add a new converter, simply create a new class inheriting from `BaseConverter` and register it.

## Installation

```bash
git clone <repo-url>
cd universal-converter
pip install -e .
```

## Usage

### Datetime Conversion

Convert ISO string to Timestamp:
```bash
universal-converter datetime --to-ts "2023-01-01T12:00:00+00:00"
```

Convert Timestamp to ISO string:
```bash
universal-converter datetime --to-dt 1672574400.0
```

### Number Conversion

Convert Hex to Decimal:
```bash
universal-converter number --hex2dec 0xA
```

Convert Decimal to Hex:
```bash
universal-converter number --dec2hex 10
```

### Encoding

Base64 Encode:
```bash
universal-converter encoding --b64enc "Hello World"
```

Base64 Decode:
```bash
universal-converter encoding --b64dec "SGVsbG8gV29ybGQ="
```

## Running Tests

```bash
python -m unittest discover tests
```

## DevOps

- **CI/CD**: GitHub Actions workflow configured in `.github/workflows/ci.yml` runs tests on every Push and PR.
