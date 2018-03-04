import tkinter as tk

from pytable.gui.tools import Tool


class MoveTool(Tool):
    def __init__(self):
        Tool.__init__(self)

        self.moved = []
        self.origin = None
        self.last_point = None

    def activate(self, graphical_editor):
        Tool.activate(self, graphical_editor)
        self.selection_manager = graphical_editor.selection_manager

    def on_start_drag(self, event):
        elem_id = self.graphical_editor.find_withtag(tk.CURRENT)

        if elem_id and not self.selection_manager.selection:
            self.moved += elem_id
        else:
            self.moved += self.selection_manager.selection

        self.last_point = self.graphical_editor.event_canvas_coords(event)
        self.origin = self.last_point

    def on_drag(self, event):
        lx, ly = self.last_point
        cx, cy = self.graphical_editor.event_canvas_coords(event)

        for elem_id in self.moved:
            self.graphical_editor.move(elem_id, cx - lx, cy - ly)

        self.last_point = cx, cy

    def on_end_drag(self, event):
        ox, oy = self.graphical_editor.canvas_to_table_coords(self.origin)
        cx, cy = self.graphical_editor.event_table_coords(event)

        elems = self.graphical_editor.get_corresponding_elements(*self.moved)

        for elem in elems:
            self.graphical_editor.table_ctx.translate_element(
                elem, cx - ox, cy - oy)

        self.graphical_editor.update_all_canvas_elements()

        self.moved = []
        self.origin = None
        self.last_point = None

    def deactivate(self, graphical_editor):
        Tool.deactivate(self, graphical_editor)
        self.selection_manager = None
