def ensure_key(json_data, key, default=None):
    """
    Ensure that the given key belongs to the given json_data. The key is added
    if not present, with the given default value.
    """
    if not isinstance(json_data, dict):
        raise TypeError("given data is not a json object")

    if key not in json_data:
        json_data[key] = default

def ensure_compound_key(json_data, key):
    """
    Ensure that the given key belongs to the given json_data and that the
    corresponding value has a dict type. If needed, the value can be modified
    in order to ensure its type.
    """
    ensure_key(json_data, key, default={})

    if not isinstance(json_data[key], dict):
        json_data[key] = {}

def ensure_vector_key(json_data, key):
    """
    Ensure that the given key belongs to the given json_data, and that the
    corresponding value has a vector structure. If needed, the value can be
    modified in order to ensure a vector structure.
    """
    ensure_compound_key(json_data, key)

    ensure_key(json_data[key], "x", 0)
    ensure_key(json_data[key], "y", 0)
    ensure_key(json_data[key], "z", 0)
