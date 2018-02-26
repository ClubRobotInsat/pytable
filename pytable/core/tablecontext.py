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
        Changes the value of the specified property for the specified element

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

        if isinstance(previous_value, int):
            new_value = int(new_value)
        elif isinstance(previous_value, float):
            new_value = float(new_value)
        elif isinstance(previous_value, str):
            new_value = str(new_value)

        prop_parent[final_name] = new_value
