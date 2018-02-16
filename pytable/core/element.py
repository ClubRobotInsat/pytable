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

    def set_property_value(self, full_path, new_value):
        """
        Changes the value of the indicated property

        Arguments:
        full_name -- the complete path of the property, with each name separed
            by a dot
        str_value -- the new value of the property. The type of the provided
            value doesn't matter, the value is casted to the previous value type
        """
        names = full_path.split(".")  # FIXME probleme si la prop contient un .
        prop_parent = self.json_data

        for name in names[:-1]:
            prop_parent = prop_parent[name]  # TODO name check, range check etc

        final_name = names[-1]

        # type checking
        previous_value = prop_parent[final_name]

        if isinstance(previous_value, (dict, list)):
            raise TypeError("Can't replace a compound value")

        if isinstance(previous_value, int):
            new_value = int(new_value)
        elif isinstance(previous_value, float):
            new_value = float(new_value)
        elif isinstance(previous_value, str):
            new_value = str(new_value)

        prop_parent[final_name] = new_value

    @property
    def position(self):
        jsonutils.check_vector_key(self.json_data, "position")
        return self.json_data["position"]["x"], self.json_data["position"]["y"]

    @position.setter
    def position(self, xy):
        jsonutils.check_vector_key(self.json_data, "position")
        self.json_data["position"]["x"] = xy[0]
        self.json_data["position"]["y"] = xy[1]

    @property
    def angle(self):
        jsonutils.check_key(self.json_data, "angle", 0)
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
