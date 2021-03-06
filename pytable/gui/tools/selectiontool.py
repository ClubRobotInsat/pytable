from pytable.gui.tools import Tool


class SelectionTool(Tool):
    def activate(self, graphical_editor):
        Tool.activate(self, graphical_editor)
        self.selection_manager = graphical_editor.selection_manager

    def on_click(self, event):
        if not event.state & 0x4:  # TODO constantes (0x04 == CTRL)
            self.selection_manager.unselect_all()

        self.selection_manager.select_current_elem(toggle=True)

    def on_start_drag(self, event):
        self.selection_manager.unselect_all()

        xy = self.graphical_editor.event_canvas_coords(event)
        self.selection_manager.start_rectangle_selection(xy)

    def on_drag(self, event):
        xy = self.graphical_editor.event_canvas_coords(event)
        self.selection_manager.update_rectangle_selection(xy)

    def on_end_drag(self, event):
        self.selection_manager.terminate_selection()

    def deactivate(self, graphical_editor):
        Tool.deactivate(self, graphical_editor)
        self.selection_manager = None
