class DummyTestTool:
    def activate(self, graphical_editor):
        pass

    def on_click(self, event):
        print("click")

    def on_start_drag(self, event):
        print("start drag")

    def on_drag(self, event):
        print("drag")

    def on_end_drag(self, event):
        print("end drag")

    def deactivate(self, graphical_editor):
        pass
