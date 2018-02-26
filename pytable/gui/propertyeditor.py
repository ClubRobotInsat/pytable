import tkinter as tk
import tkinter.ttk as ttk


class PropertyEditor(tk.LabelFrame):
    def __init__(self, parent, master):
        tk.LabelFrame.__init__(self, parent, width=200, text="Properties")

        self.master = master
        self.graphical_editor = None
        self.elements = []

        self.rows = {}
        self.edit_popup = None

        # Main view
        columns = ["value"]
        self.main_view = ttk.Treeview(self, columns=columns)

        for column in columns:
            self.main_view.heading(column, text=column)

        self.main_view.bind("<Button-1>", self.on_click)
        self.main_view.pack(fill=tk.BOTH, expand=True)

    def on_window_ready(self):
        self.graphical_editor = self.master.get_graphical_editor()

    def set_context(self, ctx):
        self.table_ctx = ctx

    def set_elements(self, *elems):
        self.elements = list(elems)
        self.rebuild_property_tree()

    def rebuild_property_tree(self):
        # delete popup
        self.edit_item("")

        # Delete all items
        self.main_view.delete(*self.main_view.get_children())
        self.rows = {}

        # Adding properties for the new items
        for elem in self.elements:
            keys = elem.get_keys()

            for key in keys:
                self.__update_property_in_tree(key, elem[key])

    def __get_item_value(self, item_id):
        value = self.main_view.item(item_id, "value")

        if isinstance(value, tuple):
            value = value[0]

        return value

    def __update_property_in_tree(self, name, value, parent_name=''):
        prop_full_name = parent_name + "." + name if parent_name != '' else name
        item_value = str(value) if not isinstance(value, dict) else ""

        if prop_full_name in self.rows:
            item_id = self.rows[prop_full_name]

            # Change the value to "multiple" if necessary
            current_value = self.__get_item_value(item_id)

            if current_value != item_value:
                self.main_view.item(item_id, value="...")
        else:
            parent_row_id = self.rows[parent_name] if parent_name != '' else ''

            self.rows[prop_full_name] = self.main_view.insert(
                parent_row_id, "end", text=name, value=item_value)

        # Add children properties
        if isinstance(value, dict):
            for child_name in value:
                self.__update_property_in_tree(child_name, value[child_name],
                                               prop_full_name)

    def get_full_property_path(self, rowid):
        return [name for name in self.rows if self.rows[name] == rowid][0]

    def edit_item(self, item_id):
        # Delete the previous popup
        if self.edit_popup:
            self.edit_popup.destroy()
            self.edit_popup = None

        # Create the new one
        if item_id != "":
            x, y, width, height = self.main_view.bbox(item_id, "#1")
            value = self.__get_item_value(item_id)

            self.edit_popup = ttk.Entry(self.main_view)
            self.edit_popup.focus_force()
            self.edit_popup.place(x=x, y=y, width=width, height=height)

            self.edit_popup.insert(0, value)

            self.edit_popup.bind(
                "<Return>", lambda *ignore: self.on_validate_edition(item_id))

    def on_validate_edition(self, item_id):
        """
        This method is called when the user enters a value in the "edit" popup
        and validate his choice. The popup is closed and the value is set for
        all the selected elements
        """
        property_path = self.get_full_property_path(item_id)

        for elem in self.elements:
            self.table_ctx.set_property_value(elem, property_path,
                                              self.edit_popup.get())

        self.rebuild_property_tree()
        self.graphical_editor.update_all_canvas_elements()

    def on_click(self, event):
        ex, ey = event.x, event.y
        rowid = self.main_view.identify_row(ey)
        column = self.main_view.identify_column(ex)

        if column == "#1":
            self.edit_item(rowid)
        else:
            self.edit_item("")
