class Tool:
    """
    Base class for tools. Each tool corresponds to one of the squared buttons
    at the top of the window (Selection, Create a cuboid, Create a cylinder...)

    Tools specify what should be modified on the table and on the editor,
    when the user moves the mouse or clicks, for exemple. When a tool is activated,
    it gets attached to a graphical editor and obtains a reference to it.
    """

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
from .movetool import MoveTool
