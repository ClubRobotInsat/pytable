import json

from pytable.gui import PyTableWindow
from pytable.core import (Table, TableContext)


class PyTable:
    def __init__(self, *args):
        pass

    def run(self):
        window = PyTableWindow(self)
        window.mainloop()

    def set_current_file(self, filename):
        self.current_file = filename

    def create_default_ctx(self):
        return TableContext(Table({}))

    def load_ctx_from_file(self, filename, **kwargs):
        # Get file contents
        file_obj = open(filename, 'r')
        json_data = json.load(file_obj)
        file_obj.close()

        # Load the table
        table = Table(json_data)
        return TableContext(table)

    def save_ctx_to_file(self, filename, ctx):
        # Convert the table into json
        json_data = ctx.table.to_json()

        file_obj = open(filename, 'w')
        json.dump(json_data, file_obj, sort_keys=True, indent=4)
        file_obj.close()
