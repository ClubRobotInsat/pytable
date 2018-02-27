from pytable.gui.tools import Tool


class ShapeTool(Tool):
    def __init__(self, create_shape):
        self.create_shape = create_shape

    def activate(self, graphical_editor):
        Tool.activate(self, graphical_editor)
        self.context = graphical_editor.table_ctx

    def on_click(self, event):
        self.create_shape(self, event)

    @staticmethod
    def create_cuboid(tool, event):
        position = tool.graphical_editor.event_table_coords(event) + (0, )
        dimensions = (0.1, 0.1, 0.1)
        elem = tool.context.create_cuboid(position, dimensions)
        tool.graphical_editor.create_canvas_element(elem)

    @staticmethod
    def create_cylinder(tool, event):
        position = tool.graphical_editor.event_table_coords(event) + (0, )
        elem = tool.context.create_cylinder(position, 0.1, 0.2)
        tool.graphical_editor.create_canvas_element(elem)
