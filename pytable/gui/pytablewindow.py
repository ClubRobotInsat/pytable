import tkinter as tk
from tkinter import filedialog

from pytable.gui import (ImageProvider, EditorCanvas, ToolsMenu,
                         PropertyEditor)


class PyTableWindow(tk.Tk):
    def __init__(self, app, **kwargs):
        tk.Tk.__init__(self)

        self.app = app
        self.current_filename = ""
        self.current_ctx = app.create_default_ctx()
        self.image_provider = self.image_provider = ImageProvider("images")

        # configuration
        self.title("PyTable Designer")

        # menu
        menu = tk.Menu(self)
        self.config(menu=menu)

        filemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New table", command=self.command_new_table)
        filemenu.add_command(
            label="Open table...", command=self.command_open_table)
        filemenu.add_separator()
        filemenu.add_command(
            label="Save table", command=self.command_save_table)
        filemenu.add_command(
            label="Save table as...", command=self.command_save_table_as)

        # components
        self.left_panel = tk.Frame(self)
        self.left_panel.config(width=200)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.tools = ToolsMenu(self.left_panel, self)
        self.tools.pack(side=tk.TOP, fill=tk.X)

        self.propeditor = PropertyEditor(self.left_panel, self)
        self.propeditor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.editor = EditorCanvas(self, self, self.current_ctx)
        self.editor.pack(fill=tk.BOTH, expand=1)

        # ready
        self.editor.on_window_ready()
        self.tools.on_window_ready()
        self.propeditor.on_window_ready()

    def get_app(self):
        return self.app

    def get_property_editor(self):
        return self.propeditor

    def get_image_provider(self):
        return self.image_provider

    # Miscellaneous

    def __select_filename_dialog(self):
        """
        Open a save dialog to select a filename for the current opened table
        returns -- The filename selected
        """
        filename = filedialog.asksaveasfilename(
            initialdir=".",
            title="Save table...",
            filetypes=(("json files", "*.json"), ("all files", "*.*")))

        return filename

    # Events

    def command_open_table(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select table file",
            filetypes=(("json files", "*.json"), ("all files", "*.*")))

        if filename:
            # TODO catch exceptions
            self.current_ctx = self.app.load_ctx_from_file(filename)
            self.editor.set_context(self.current_ctx)
            self.current_filename = filename

    def command_new_table(self):
        self.current_ctx = self.app.create_default_ctx()
        self.editor.set_context(self.current_ctx)

    def command_save_table(self):
        if not self.current_filename:
            self.command_save_table_as()
        else:
            self.app.save_ctx_to_file(self.current_filename, self.current_ctx)

    def command_save_table_as(self):
        filename = self.__select_filename_dialog()

        if filename:
            self.app.save_ctx_to_file(filename, self.current_ctx)
            self.current_filename = filename
