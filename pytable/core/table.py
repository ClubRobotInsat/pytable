import json

from pytable.core.element import Element


class Table:
    def __init__(self):
        self.elements = []

    @staticmethod
    def load_from_json(json_data):
        table = Table()

        for element_data in json_data["objects"]:
            table.elements.append(Element(element_data))
        return table
