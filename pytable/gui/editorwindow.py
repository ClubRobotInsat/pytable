import tkinter as tk
from tkinter import filedialog

from pytable.gui import (ImageProvider, EditorCanvas, ToolsMenu,
                         PropertyEditor)


class EditorWindow(tk.Tk):
    def __init__(self, app):
        tk.Tk.__init__(self)

        self.app = app

        # configuration
        self.title("PyTable Designer")

        # menu
        menu = tk.Menu(self)
        self.config(menu=menu)

        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New table", command=self.new_table)
        filemenu.add_command(label="Open...", command=self.open_table_dialog)

        # components
        self.left_panel = tk.Frame(self)
        self.left_panel.config(width=200)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.tools = ToolsMenu(self.left_panel, self.app)
        self.tools.pack(side=tk.TOP, fill=tk.X)

        self.propeditor = PropertyEditor(self.left_panel)
        self.propeditor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.editor = EditorCanvas(self, app.create_default_ctx())
        self.editor.pack(fill=tk.BOTH, expand=1)

        # bindings
        self.editor.set_property_editor(self.propeditor)

    def get_property_editor(self):
        return self.propeditor

    # Events

    def open_table_dialog(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select table file",
            filetypes=(("json files", "*.json"), ("all files", "*.*")))

        if filename != "":
            table_ctx = self.app.load_ctx_from_file(filename)
            self.editor.set_context(table_ctx)

    def new_table(self):
        table_ctx = self.app.create_default_ctx()
        self.editor.set_context(table_ctx)
