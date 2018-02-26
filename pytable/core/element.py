from pytable.utils import jsonutils


class Element:
    def __init__(self, json_data):
        self.json_data = json_data

    def __getitem__(self, key):
        return self.json_data[key]

    def __setitem__(self, key, value):
        self.json_data[key] = value

    def get_keys(self):
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
