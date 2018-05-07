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
        self.tree = ttk.Treeview(self, columns=columns)

        for column in columns:
            self.tree.heading(column, text=column)

        self.tree.bind("<Button-1>", self.on_click)
        self.tree.pack(fill=tk.BOTH, expand=True)

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
        self.tree.delete(*self.tree.get_children())
        self.rows = {}

        # Adding properties for the new items
        for elem in self.elements:
            keys = elem.get_keys()

            for key in keys:
                self.__update_property_in_tree(key, elem[key])

    def __get_item_value(self, item_id):
        """
        Gets the corresponding value for the given item in the tree.
        """
        value = self.tree.item(item_id, "value")

        if value != "":
            value = value[0]

        return value

    def __set_property_in_tree(self, property_path, value):
        """
        Sets the value of this property in the tree. Unlike __update_property_in_tree,
        this method does not care of the current value of the property.
        It is useful when you don't want to rebuild the whole tree after making
        a slight change to the context.

        Does not work with dict values.
        """
        if isinstance(value, dict):
            raise TypeError(
                "__set_property_in_tree does not currently support compound properties"
            )

        self.tree.item(self.rows[property_path], value=str(value))

    def __update_property_in_tree(self, property_path, value):
        """
        Adapts the tree by including the given value to the tree. If the property
        already exists in the tree and has a different value, it will be changed
        to "...", indicating that this property has currently multiple values.
        """
        last_separator_index = property_path.rfind(".")
        parent_path = property_path[:max(last_separator_index, 0)]
        child_name = property_path[(last_separator_index + 1):]

        added_item_value = str(value) if not isinstance(value, dict) else ""

        if property_path in self.rows:
            item_id = self.rows[property_path]

            # Change the value to "multiple" if necessary
            current_item_value = self.__get_item_value(item_id)

            if current_item_value != added_item_value:
                self.tree.item(item_id, value="...")
        else:
            parent_row_id = self.rows[parent_path] if parent_path != '' else ''

            self.rows[property_path] = self.tree.insert(
                parent_row_id, "end", text=child_name, value=added_item_value)

        # Add children properties
        if isinstance(value, dict):
            for child_name in value:
                self.__update_property_in_tree(
                    property_path + "." + child_name, value[child_name])

    def get_full_property_path(self, rowid):
        return [name for name in self.rows if self.rows[name] == rowid][0]

    def edit_item(self, item_id):
        """
        Opens a popup to edit a property. Only one popup can be open at the same
        time, so if there is a previously opened popup it will be closed.
        This method is called when the user clicks on an item in the tree.
        If this method is called with an empty string as argument, the popup

        Arguments:
        item_id -- the TKinter id of the list item.
        """
        # Delete the previous popup
        if self.edit_popup:
            self.edit_popup.destroy()
            self.edit_popup = None

        # Create the new one
        if item_id != "":
            x, y, width, height = self.tree.bbox(item_id, "#1")
            value = self.__get_item_value(item_id)

            self.edit_popup = ttk.Entry(self.tree)
            self.edit_popup.focus_force()
            self.edit_popup.place(x=x, y=y, width=width, height=height)

            self.edit_popup.insert(0, value)

            self.edit_popup.bind(
                "<Return>", lambda *ignore: self.on_validate_edition(item_id))

    def on_validate_edition(self, item_id):
        """
        This method is called when the user enters a value in the "edit" popup
        and validate his choice. The popup is closed and the value is set for
        all the selected elements.
        """
        property_path = self.get_full_property_path(item_id)

        for elem in self.elements:
            self.table_ctx.set_property_value(elem, property_path,
                                              self.edit_popup.get())

        self.__set_property_in_tree(property_path, self.edit_popup.get())
        self.edit_item("")

        # on context changed
        self.graphical_editor.update_all_canvas_elements()

    def on_click(self, event):
        ex, ey = event.x, event.y
        rowid = self.tree.identify_row(ey)
        column = self.tree.identify_column(ex)

        if column == "#1":
            self.edit_item(rowid)
        else:
            self.edit_item("")
