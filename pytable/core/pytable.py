import json

from pytable.gui import (EditorWindow, ImageProvider)
from pytable.core import (Table, TableContext)


class PyTable:
    def __init__(self, *args):
        # TODO pas ouf sachant que la window a besoin de l'image provider pour ce créer
        self.image_provider = ImageProvider("images")
        self.window = EditorWindow(self)

        self.window.mainloop()

    def get_image_provider(self):
        return self.image_provider

    def create_default_ctx(self):
        return TableContext(Table())

    def load_ctx_from_file(self, filename):
        # Recuperation du fichier texte
        file_obj = open(filename, 'r')
        file_contents = file_obj.read()
        json_data = json.loads(file_contents)

        # Chargement de la Table
        table = Table.load_from_json(json_data)
        return TableContext(table)
