import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ..core.arguments import InterfaceBuilder
from ..core.exceptions import ConverterError
from ..utils.logger import setup_logger
from threading import Thread
import io
import sys

logger = setup_logger()

class GUIBuilder(InterfaceBuilder):
    """
    Builds the UI form for a specific converter.
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.entries = {} # Store entry widgets by arg name
        self.vars = {}    # Store variables

    def build_form(self):
        """Generates widgets based on collected arguments."""

        # We need to handle groups.
        # For mutual exclusive groups, we might use a Combobox to select mode,
        # or just list fields and rely on logic (or Radio buttons).
        # Given the "platform" nature, Radio buttons + Dynamic Input is best for exclusive groups.

        current_row = 0

        for group in self.groups:
            if group.exclusive:
                # Create a frame for the group
                frame = tb.Labelframe(self.parent, text="Select Mode", bootstyle="info")
                frame.pack(fill=X, padx=10, pady=5)

                self.mode_var = tk.StringVar()
                self.mode_var.set(group.arguments[0].name) # Default to first

                # Radio buttons for mode
                for arg in group.arguments:
                    rb = tb.Radiobutton(
                        frame,
                        text=arg.help,
                        variable=self.mode_var,
                        value=arg.name,
                        command=lambda: self._update_visibility()
                    )
                    rb.pack(anchor=W, padx=5, pady=2)

                    # Create input field for this option
                    # Initially hidden? Or always visible but enabled/disabled?
                    # Let's create a container for the input
                    container = tb.Frame(self.parent)
                    container.pack(fill=X, padx=10, pady=5)
                    self.entries[arg.name] = {
                        'container': container,
                        'widget': None,
                        'var': tk.StringVar()
                    }

                    lbl = tb.Label(container, text=f"{arg.metavar or arg.name}:")
                    lbl.pack(side=LEFT, padx=5)

                    ent = tb.Entry(container, textvariable=self.entries[arg.name]['var'])
                    ent.pack(side=LEFT, fill=X, expand=True, padx=5)
                    self.entries[arg.name]['widget'] = ent

                self._update_visibility()
            else:
                # Normal group
                for arg in group.arguments:
                    self._create_field(arg)

        for arg in self.arguments:
            self._create_field(arg)

    def _create_field(self, arg):
        container = tb.Frame(self.parent)
        container.pack(fill=X, padx=10, pady=5)

        lbl = tb.Label(container, text=f"{arg.help}:")
        lbl.pack(side=LEFT, padx=5)

        var = tk.StringVar()
        ent = tb.Entry(container, textvariable=var)
        ent.pack(side=LEFT, fill=X, expand=True, padx=5)

        self.entries[arg.name] = {
            'container': container,
            'widget': ent,
            'var': var
        }

    def _update_visibility(self):
        # For exclusive groups, show/enable only the selected input
        selected = getattr(self, 'mode_var', None)
        if selected:
            val = selected.get()
            for name, data in self.entries.items():
                # This logic assumes all entries are part of the exclusive group if mode_var exists
                # This is a simplification.
                # Real implementation should track which args belong to the group.
                # For now, based on our converters, this is true.
                if name == val:
                    data['container'].pack(fill=X, padx=10, pady=5)
                else:
                    data['container'].pack_forget()

    def get_values(self):
        values = {}
        # If exclusive mode
        selected = getattr(self, 'mode_var', None)
        if selected:
            active_name = selected.get()
            val = self.entries[active_name]['var'].get()
            values[active_name] = val
        else:
            for name, data in self.entries.items():
                values[name] = data['var'].get()
        return values

class ConverterTab(tb.Frame):
    def __init__(self, parent, converter_cls):
        super().__init__(parent)
        self.converter = converter_cls()
        self.builder = GUIBuilder(self)

        # Title/Description
        lbl_title = tb.Label(self, text=self.converter.name.upper(), font=("Helvetica", 16, "bold"), bootstyle="primary")
        lbl_title.pack(pady=(20, 10))

        lbl_help = tb.Label(self, text=self.converter.help, font=("Helvetica", 10))
        lbl_help.pack(pady=(0, 20))

        # Build Form
        self.converter.configure_args(self.builder)
        self.builder.build_form()

        # Convert Button
        btn_convert = tb.Button(self, text="Convert", bootstyle="success", command=self.on_convert)
        btn_convert.pack(pady=20)

        # Output Area
        lbl_out = tb.Label(self, text="Output:", font=("Helvetica", 12, "bold"))
        lbl_out.pack(anchor=W, padx=10)

        self.txt_output = tb.Text(self, height=5)
        self.txt_output.pack(fill=X, padx=10, pady=5)

    def on_convert(self):
        kwargs = self.builder.get_values()

        # Capture stdout to show in text box
        # This is a bit hacky but fits the current "print" based converters.
        # Ideally converters should return values.

        capture = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = capture

        try:
            self.converter.convert(**kwargs)
            result = capture.getvalue()
            self.txt_output.delete("1.0", END)
            self.txt_output.insert(END, result)
        except Exception as e:
            self.txt_output.delete("1.0", END)
            self.txt_output.insert(END, f"Error: {str(e)}")
        finally:
            sys.stdout = original_stdout


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Universal Converter Platform")
        self.geometry("800x600")

        # Sidebar or Tabs? Tabs are easier for generic list
        tabs = tb.Notebook(self)
        tabs.pack(fill=BOTH, expand=True, padx=10, pady=10)

        from ..core.registry import ConverterRegistry
        # Import converters to ensure registration
        from ..converters import datetime_converter, number_converter, encoding_converter

        converters = ConverterRegistry.get_converters()

        for name, cls in converters.items():
            tab = ConverterTab(tabs, cls)
            tabs.add(tab, text=name.capitalize())

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
