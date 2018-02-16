import math
import tkinter as tk

from pytable.gui import tools


class SelectionManager:
    def __init__(self, editor):
        self.editor = editor

        self.selection = set()
        self.anchor = None
        self.select_item = None

    def select_current_elem(self):
        elem_id = self.editor.find_withtag(tk.CURRENT)

        if elem_id:
            self.selection |= set(elem_id)

            self.__on_selection_change()

        return True if elem_id else False

    def select_elem(self, **kwargs):
        raise Exception("Not supported")

    def unselect_all(self):
        self.selection = set()

        self.__on_selection_change()

    def start_rectangle_selection(self, xy, **args):
        self.anchor = xy

        self.select_item = self.editor.create_rectangle(*xy, *xy)

    def update_rectangle_selection(self, xy):
        item_ids = self.editor.find_enclosed(*self.anchor, *xy)
        self.selection = set(item_ids)

        self.editor.coords(self.select_item, *self.anchor, *xy)

        self.__on_selection_change()

    def terminate_selection(self):
        self.editor.delete(self.select_item)
        self.select_item = None

        self.anchor = None

    def __on_selection_change(self):
        self.editor.update_canvas_elements()
        # TODO à voir par qui cette ligne est gérée
        self.editor.propeditor.set_elements(
            *self.editor.get_corresponding_elements(*self.selection))


class EditorCanvas(tk.Canvas):
    def __init__(self, parent, ctx):
        tk.Canvas.__init__(self, parent)

        # initialisation stuff (TODO refactor)
        self.propeditor = None
        self.selection_manager = SelectionManager(self)
        self.current_tool = tools.SelectionTool(self)

        self.table_elements = {}
        self.scale = 500

        self.is_dragging = False

        self.set_context(ctx)

        # tkinter setup
        self.config(background='#d0d0d0')

        self.bind("<Configure>", self.on_resize)
        self.bind("<ButtonPress-1>", self.on_mouse_press)
        self.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.bind("<B1-Motion>", self.on_mouse_drag)

    def set_property_editor(self, propeditor):
        self.propeditor = propeditor

    def set_context(self, ctx):
        self.table_ctx = ctx
        self.reset_elements()

    def reset_elements(self):
        # Delete all elements
        for elem_id in self.table_elements:
            self.delete(elem_id)

        self.table_elements = {}

        # Add all elements from the current table
        table = self.table_ctx.table

        for elem in table.elements:
            self.create_canvas_element(elem)

    def create_canvas_element(self, elem):
        elem_id = None
        scale = self.scale
        x, y = elem.position

        if elem["type"] == "cuboid":
            elem_id = self.create_polygon([0, 0, 0, 0], outline="black")
        elif elem["type"] in ["cylinder", "sphere"]:
            elem_id = self.create_oval(0, 0, 0, 0)

        if elem_id != None:
            self.table_elements[elem_id] = elem
            self.update_canvas_element(elem_id)

    def update_canvas_elements(self):
        for elem_id in self.table_elements:
            self.update_canvas_element(elem_id)

    def update_canvas_element(self, elem_id):
        elem = self.table_elements[elem_id]

        scale = self.scale
        x, y = elem.position

        # Position
        if elem["type"] == "cuboid":
            dims = elem["dimensions"]
            hx, hy = dims["x"] / 2.0, dims["y"] / 2.0
            angle = elem["angle"] / 180.0 * math.pi
            sin, cos = math.sin(angle), math.cos(angle)

            self.coords(elem_id, [(x - cos * hx + hy * sin) * scale,
                                  (y - sin * hx - cos * hy) * scale,
                                  (x - cos * hx - hy * sin) * scale,
                                  (y - sin * hx + cos * hy) * scale,
                                  (x + cos * hx - hy * sin) * scale,
                                  (y + sin * hx + cos * hy) * scale,
                                  (x + cos * hx + hy * sin) * scale,
                                  (y + sin * hx - cos * hy) * scale])

        elif elem["type"] in ["cylinder", "sphere"]:
            hr = elem["radius"] / 2.0
            self.coords(elem_id, (x - hr) * scale, (y - hr) * scale,
                        (x + hr) * scale, (y + hr) * scale)

        # Paramètres
        color = elem.color
        stipple = ""

        if elem_id in self.selection_manager.selection:
            stipple = "gray75"

        self.itemconfig(elem_id, fill="#%02x%02x%02x" % color, stipple=stipple)

    def get_corresponding_elements(self, *elem_ids):
        return [
            self.table_elements[elem_id] for elem_id in self.table_elements
            if elem_id in elem_ids
        ]

    # Events

    def on_mouse_press(self, event):
        self.press_event = event

    def on_mouse_drag(self, event):
        ox, oy = self.press_event.x, self.press_event.y
        ex, ey = event.x, event.y

        # Determine if we start dragging or not
        if not self.is_dragging:
            dist = max(abs(ox - ex), abs(oy - ey))

            if dist > 3:
                self.is_dragging = True

                if self.current_tool:
                    self.current_tool.on_start_drag(self.press_event)

        # Trigger normal event (only if dragging)
        if self.current_tool and self.is_dragging:
            self.current_tool.on_drag(event)

    def on_mouse_release(self, event):
        if self.is_dragging:
            self.is_dragging = False

            if self.current_tool:
                self.current_tool.on_end_drag(event)
        else:
            if self.current_tool:
                self.current_tool.on_click(event)

    def on_resize(self, event):
        pass
