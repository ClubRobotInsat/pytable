def check_key(json_data, key, default={}):
    """
    Ajoute la clé passée en paramètres à l'objet passé en paramètres,
    si elle n'y est pas.
    """
    if not isinstance(json_data, dict):
        raise TypeError("given data is not a json object")

    if key not in json_data:
        json_data[key] = default


def check_vector_key(json_data, key):
    """
    Ajoute la clé passée en paramètres à l'objet passé en paramètres,
    si elle n'y est pas.
    """
    check_key(json_data, key)

    if not isinstance(json_data[key], dict):
        json_data[key] = {}

    check_key(json_data[key], "x", 0)
    check_key(json_data[key], "y", 0)
    check_key(json_data[key], "z", 0)
