class SelectionTool:
    def __init__(self):
        pass

    def activate(self, graphical_editor):
        self.selection_manager = graphical_editor.selection_manager

    def on_click(self, event):
        self.selection_manager.unselect_all()
        self.selection_manager.select_current_elem()

    def on_start_drag(self, event):
        self.selection_manager.unselect_all()

        xy = event.x, event.y
        self.selection_manager.start_rectangle_selection(xy)

    def on_drag(self, event):
        xy = event.x, event.y
        self.selection_manager.update_rectangle_selection(xy)

    def on_end_drag(self, event):
        self.selection_manager.terminate_selection()

    def deactivate(self, graphical_editor):
        self.selection_manager = None
