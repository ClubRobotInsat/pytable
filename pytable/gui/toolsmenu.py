import tkinter as tk

from pytable.gui import tools


class ToolsMenu(tk.LabelFrame):
    def __init__(self, parent, master):
        tk.LabelFrame.__init__(self, parent, text="Tools")

        self.master = master
        img_provider = master.get_image_provider()

        # ajout des boutons
        self.buttons = []

        def add_button(imgid, row, column, tool):
            b = tk.Button(self)
            photo = img_provider.get_image(imgid)
            b.config(
                image=photo,
                width=32,
                height=32,
                command=lambda *ignore: self.__activate_button(b))
            b.grid(row=row, column=column, padx=4, pady=4)
            b.pytable_tool = tool
            self.buttons.append(b)

        add_button("selection_32", 0, 0, tools.SelectionTool())
        add_button("rectangle_32", 0, 1,
                   tools.ShapeTool(tools.ShapeTool.create_cuboid))
        add_button("circle_32", 0, 2,
                   tools.ShapeTool(tools.ShapeTool.create_cylinder))
        add_button("move_32", 0, 3, tools.MoveTool())

    def on_window_ready(self):
        self.graphical_editor = self.master.get_graphical_editor()

        if self.buttons:
            self.__activate_button(self.buttons[0])

    def __activate_button(self, activated_button):
        if self.graphical_editor:
            self.graphical_editor.set_current_tool(
                activated_button.pytable_tool)

        for button in self.buttons:
            if button is activated_button:
                button.config(bg="#ffffff")
            else:
                button.config(bg="#e0e0e0")
