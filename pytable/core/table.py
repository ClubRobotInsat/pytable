import json
import copy

from pytable.core.element import Element


class Table:
    """
    Object representation of a table with all its elements.
    """

    def __init__(self, json_data):
        self.metadata = copy.deepcopy(json_data)
        self.elements = []

        if "objects" in json_data:
            del self.metadata["objects"]

            for element_data in json_data["objects"]:
                self.elements.append(Element(element_data))

    def to_json(self):
        """
        Creates a dict containing all elements of the table. This
        dict can be serialized directly into a json file.
        """
        
        json_data = copy.deepcopy(self.metadata)
        json_data["objects"] = []

        for element in self.elements:
            json_data["objects"].append(copy.deepcopy(element.json_data))

        return json_data

    def add_element(self, elem):
        self.elements.append(elem)

    def remove_element(self, elem):
        self.elements.remove(elem)
