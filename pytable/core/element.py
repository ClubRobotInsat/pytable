from pytable.utils import jsonutils


class Element:
    """
    Represents one single element on a table.

    An element has a wide set of properties. Some are common
    to most of them (position, color, angle) but there are
    no rules. Each property corresponds to a json field in
    the file containing the table.

    This class has several methods to access to the most
    usual fields of an element.
    """

    def __init__(self, json_data):
        self.json_data = json_data

    def __getitem__(self, key):
        return self.json_data[key]

    def __setitem__(self, key, value):
        self.json_data[key] = value

    def get_keys(self):
        """
        Returns a list containing the name of each property this object has.
        """
        
        return list(self.json_data.keys())

    @property
    def position(self):
        jsonutils.ensure_vector_key(self.json_data, "position")
        return self.json_data["position"]["x"], self.json_data["position"]["y"]

    @position.setter
    def position(self, xy):
        jsonutils.ensure_vector_key(self.json_data, "position")
        self.json_data["position"]["x"] = xy[0]
        self.json_data["position"]["y"] = xy[1]

    @property
    def angle(self):
        jsonutils.ensure_key(self.json_data, "angle", 0)
        return self.json_data["angle"]

    @angle.setter
    def angle(self, angle):
        self.json_data["angle"] = angle

    @property
    def color(self):
        try:
            color = self.json_data["simulateur"]["color"]
            return (int(color["r"] * 255), int(color["g"] * 255),
                    int(color["b"] * 255))
        except (KeyError, TypeError):
            return 255, 255, 255
