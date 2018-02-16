class DummyTestTool:
    def on_click(self, event):
        print("click")

    def on_start_drag(self, event):
        print("start drag")

    def on_drag(self, event):
        print("drag")

    def on_end_drag(self, event):
        print("end drag")


class SelectionTool:
    def __init__(self, editor):
        self.selector = editor.selection_manager

    def on_click(self, event):
        self.selector.unselect_all()
        self.selector.select_current_elem()

    def on_start_drag(self, event):
        self.selector.unselect_all()

        xy = event.x, event.y
        self.selector.start_rectangle_selection(xy)

    def on_drag(self, event):
        xy = event.x, event.y
        self.selector.update_rectangle_selection(xy)

    def on_end_drag(self, event):
        self.selector.terminate_selection()
