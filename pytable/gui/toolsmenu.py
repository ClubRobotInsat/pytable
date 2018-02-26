import tkinter as tk


class ToolsMenu(tk.LabelFrame):
    def __init__(self, parent, master):
        tk.LabelFrame.__init__(self, parent, text="Tools")

        self.master = master
        img_provider = master.get_image_provider()

        # ajout des boutons
        def add_button(imgid, row, column):
            b = tk.Button(self)
            photo = img_provider.get_image(imgid)
            b.config(image=photo, width=32, height=32)
            b.grid(row=row, column=column, padx=4, pady=4)

        add_button("rectangle_32", 0, 0)
        add_button("circle_32", 0, 1)

    def on_window_ready(self):
        pass
