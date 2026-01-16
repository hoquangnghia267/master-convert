# Universal Converter Platform

A modular, production-ready conversion tool featuring both a Command Line Interface (CLI) and a Graphical User Interface (GUI).

## Features

- **Multi-Interface**:
  - **CLI**: Standard UNIX-style command line tool.
  - **GUI**: Modern, professional interface using `ttkbootstrap` (Dark/Light themes).
- **Modular Architecture**: Easy to extend with new plugins.
- **Phase 1 Converters**:
  - **Datetime**: ISO 8601 <-> Timestamp (Timezone aware).
  - **Number**: Hex <-> Decimal.
  - **Encoding**: Base64 Encode/Decode.

## Installation

```bash
git clone <repo-url>
cd universal-converter
pip install -e .
```

## Usage

### Graphical User Interface (GUI)

To launch the professional GUI:
```bash
universal-converter-gui
```
The interface is tab-based, allowing you to switch between converters easily. It supports dynamic form generation based on the converter's requirements.

### Command Line Interface (CLI)

**Datetime Conversion**
```bash
universal-converter datetime --to-ts "2023-01-01T12:00:00+00:00"
universal-converter datetime --to-dt 1672574400.0
```

**Number Conversion**
```bash
universal-converter number --hex2dec 0xA
universal-converter number --dec2hex 10
```

**Encoding**
```bash
universal-converter encoding --b64enc "Hello World"
universal-converter encoding --b64dec "SGVsbG8gV29ybGQ="
```

## Architecture

The project uses a **Builder Pattern** to abstract argument definitions.
- `BaseConverter` defines arguments using `configure_args(builder)`.
- `CLIBuilder` maps these to `argparse`.
- `GUIBuilder` maps these to `ttkbootstrap` widgets.

This ensures that adding a new converter requires writing the logic only once, and it automatically becomes available in both CLI and GUI.

## Testing

```bash
python -m unittest discover tests
```
