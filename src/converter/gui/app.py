import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ..core.arguments import InterfaceBuilder, ArgumentType
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

        for group in self.groups:
            if group.exclusive:
                # Create a frame for the group
                frame = tb.Labelframe(self.parent, text="Select Mode", bootstyle="info")
                frame.pack(fill=X, padx=10, pady=5)

                self.mode_var = tk.StringVar()
                if group.arguments:
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
                    container = tb.Frame(self.parent)
                    # Don't pack immediately, _update_visibility will handle it

                    self.entries[arg.name] = {
                        'container': container,
                        'widget': None,
                        'var': None,
                        'arg': arg
                    }

                    # Only create input widget if it's NOT a flag
                    if arg.type != ArgumentType.FLAG:
                        self._create_widget(container, arg, self.entries[arg.name])

                self._update_visibility()
            else:
                # Normal group
                # Maybe put in a LabelFrame?
                frame = tb.Frame(self.parent)
                frame.pack(fill=X, padx=10, pady=5)
                # If we want a label for the group:
                # frame = tb.Labelframe(self.parent, text="Options")

                for arg in group.arguments:
                    self._create_field(arg, parent=frame)

        for arg in self.arguments:
            self._create_field(arg)

    def _create_field(self, arg, parent=None):
        if parent is None:
            parent = self.parent

        container = tb.Frame(parent)
        container.pack(fill=X, padx=10, pady=5)

        self.entries[arg.name] = {
            'container': container,
            'widget': None,
            'var': None,
            'arg': arg
        }
        self._create_widget(container, arg, self.entries[arg.name])

    def _create_widget(self, container, arg, entry_data):
        if arg.type == ArgumentType.FLAG:
            # Checkbox for non-exclusive flags
            var = tk.BooleanVar()
            entry_data['var'] = var
            entry_data['type'] = 'flag'
            chk = tb.Checkbutton(container, text=arg.help, variable=var)
            chk.pack(side=LEFT, anchor=W, padx=5)
            entry_data['widget'] = chk
            return

        # Label for other types
        lbl = tb.Label(container, text=f"{arg.metavar or arg.help}:")
        lbl.pack(side=TOP if arg.type == ArgumentType.TEXT else LEFT, anchor=W, padx=5)

        if arg.type == ArgumentType.TEXT:
            from tkinter.scrolledtext import ScrolledText
            txt = ScrolledText(container, height=5)
            txt.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            entry_data['widget'] = txt
            entry_data['type'] = 'text'

        elif arg.type == ArgumentType.FILE_SAVE:
            var = tk.StringVar()
            entry_data['var'] = var
            entry_data['type'] = 'file_save'

            frame_inner = tb.Frame(container)
            frame_inner.pack(side=LEFT, fill=X, expand=True)

            ent = tb.Entry(frame_inner, textvariable=var)
            ent.pack(side=LEFT, fill=X, expand=True, padx=5)

            btn = tb.Button(frame_inner, text="Browse", command=lambda: self._browse_save(var))
            btn.pack(side=LEFT, padx=5)

            entry_data['widget'] = ent

        else:
            # Default STRING
            var = tk.StringVar()
            entry_data['var'] = var
            entry_data['type'] = 'string'
            ent = tb.Entry(container, textvariable=var)
            ent.pack(side=LEFT, fill=X, expand=True, padx=5)
            entry_data['widget'] = ent

    def _browse_save(self, var):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if filename:
            var.set(filename)

    def _update_visibility(self):
        # For exclusive groups, show/enable only the selected input
        selected = getattr(self, 'mode_var', None)
        if selected:
            val = selected.get()
            for name, data in self.entries.items():
                # Re-check exclusive membership
                is_exclusive_arg = False
                for group in self.groups:
                    if group.exclusive:
                         for arg in group.arguments:
                             if arg.name == name:
                                 is_exclusive_arg = True
                                 break

                if is_exclusive_arg:
                    if name == val:
                        # Only pack if it has content (i.e. not a flag in exclusive mode which has no extra widget)
                        if data['arg'].type != ArgumentType.FLAG:
                            data['container'].pack(fill=X, padx=10, pady=5)
                        else:
                            data['container'].pack_forget() # Hide container for flag (radio button is enough)
                    else:
                        data['container'].pack_forget()

    def get_values(self):
        values = {}

        def get_val(name, data):
            if data['type'] == 'text':
                return data['widget'].get("1.0", END).strip()
            elif data['type'] == 'flag':
                return data['var'].get()
            else:
                return data['var'].get()

        selected = getattr(self, 'mode_var', None)

        exclusive_arg_names = []
        for group in self.groups:
            if group.exclusive:
                for arg in group.arguments:
                    exclusive_arg_names.append(arg.name)

        if selected:
            active_name = selected.get()
            # If the selected mode is a flag, set it to True
            # If it's a widget, get its value

            # Find the arg definition
            active_arg = None
            for group in self.groups:
                if group.exclusive:
                    for arg in group.arguments:
                        if arg.name == active_name:
                            active_arg = arg
                            break

            if active_arg and active_arg.type == ArgumentType.FLAG:
                values[active_name] = True
            elif active_name in self.entries:
                values[active_name] = get_val(active_name, self.entries[active_name])

        for name, data in self.entries.items():
            if name not in exclusive_arg_names:
                val = get_val(name, data)
                if val:
                    values[name] = val

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

        self.converter.configure_args(self.builder)
        self.builder.build_form()

        # Convert Button
        btn_convert = tb.Button(self, text="Convert / Execute", bootstyle="success", command=self.on_convert)
        btn_convert.pack(pady=20)

        # Output Area
        lbl_out = tb.Label(self, text="Output:", font=("Helvetica", 12, "bold"))
        lbl_out.pack(anchor=W, padx=10)

        self.txt_output = tb.Text(self, height=10)
        self.txt_output.pack(fill=BOTH, expand=True, padx=10, pady=5)

    def on_convert(self):
        kwargs = self.builder.get_values()

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
            import traceback
            traceback.print_exc()
        finally:
            sys.stdout = original_stdout


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Universal Converter Platform")
        self.geometry("900x700")

        tabs = tb.Notebook(self)
        tabs.pack(fill=BOTH, expand=True, padx=10, pady=10)

        from ..core.registry import ConverterRegistry
        from ..converters import datetime_converter, number_converter, csr_converter

        converters = ConverterRegistry.get_converters()

        for name, cls in converters.items():
            tab = ConverterTab(tabs, cls)
            tabs.add(tab, text=name.upper())

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
