class Tool:
    def activate(self, graphical_editor):
        self.graphical_editor = graphical_editor

    def deactivate(self, graphical_editor):
        self.graphical_editor = None

    def on_click(self, event):
        pass

    def on_start_drag(self, event):
        pass

    def on_drag(self, event):
        pass

    def on_end_drag(self, event):
        pass


from .dummytesttool import DummyTestTool
from .selectiontool import SelectionTool
from .shapetool import ShapeTool
