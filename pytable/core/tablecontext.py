import copy

from pytable.core import Element
from pytable.utils import jsonutils


class TableContext:
    """
    The metadata about the table currently opened in the editor.
    The context also plays the role of controller in MVC pattern, i.e. the
    instance who checks the user actions
    """

    def __init__(self, table):
        self.table = table

    def set_property_value(self, element, property_path, new_value):
        """
        Change the value of the specified property for the specified element

        Arguments:
        property_path -- the complete path of the property, with each name
            separed by a dot
        str_value -- the new value of the property. The type of the provided
            value doesn't matter, the value is casted to the previous value type
        """
        names = property_path.split(
            ".")  # FIXME probleme si la prop contient un .
        prop_parent = element.json_data

        for name in names[:-1]:
            prop_parent = prop_parent[name]  # TODO name check, range check etc

        final_name = names[-1]

        # type checking
        previous_value = prop_parent[final_name]

        if isinstance(previous_value, (dict, list)):
            raise TypeError("Can't replace a compound value")

        if isinstance(previous_value, bool):
            new_value = True if new_value == "True" else False
        elif isinstance(previous_value, (int, float)):
            new_value = float(new_value)
        elif isinstance(previous_value, str):
            new_value = str(new_value)

        prop_parent[final_name] = new_value

    def create_element(self, position, **kwargs):
        """
        Create a new element and add it to the table
        """
        json_data = copy.deepcopy(
            kwargs["json_data"]) if "json_data" in kwargs else {}

        x, y, z = position
        json_data["position"] = {"x": x, "y": y, "z": z}

        # check keys
        jsonutils.ensure_keys(
            json_data, **{
                "A*": {
                    "enabled": False
                },
                "angle": 0,
                "simulateur": {
                    "color": {
                        "b": 1,
                        "g": 1,
                        "r": 1
                    },
                    "dynamic": False,
                    "enabled": False,
                    "mass": 0
                },
                "type": "cuboid"
            })

        elem = Element(json_data)
        self.table.add_element(elem)
        return elem

    def create_cuboid(self, position, dimensions, **kwargs):
        """
        Add a cuboid element to the table.
        """
        dx, dy, dz = dimensions

        # TODO json_data = copy.deepcopy(kwargs["json_data"])
        json_data = {
            "type": "cuboid",
            "dimensions": {
                "x": dx,
                "y": dy,
                "z": dz
            }
        }

        return self.create_element(position, json_data=json_data)

    def create_cylinder(self, position, radius, height, **kwargs):
        """
        Add a cylinder element to the table.
        """

        # TODO data check
        json_data = {"type": "cylinder", "radius": radius, "height": height}

        return self.create_element(position, json_data=json_data)

    def remove_element(self, elem):
        self.table.remove_element(elem)

    def translate_element(self, elem, dx, dy, dz=0):
        elem["position"]["x"] += dx
        elem["position"]["y"] += dy
        elem["position"]["z"] += dz
