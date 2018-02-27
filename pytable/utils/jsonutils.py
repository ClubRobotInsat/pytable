def ensure_key(json_data, key, default=None):
    """
    Ensure that the given key belongs to the given json_data. The key is added
    if not present, with the given default value.
    """
    if not isinstance(json_data, dict):
        raise TypeError("given data is not a json object")

    if key not in json_data:
        json_data[key] = default


def ensure_keys(json_data, **kv):
    """
    Ensure that all the keys given in parameters are in json_data. If not,
    they are added. The method processes recursively : if a compound value is
    found in the reference, then all the keys in this compound value will also
    be tested. TODO unit tests
    """
    for key in kv:
        if isinstance(kv[key], dict):
            ensure_compound_key(json_data, key)
            ensure_keys(json_data[key], **kv[key])
        else:
            ensure_key(json_data, key, default=kv[key])


def ensure_compound_key(json_data, key):
    """
    Ensure that the given key belongs to the given json_data and that the
    corresponding value has a dict type. If needed, this value can be modified
    in order to ensure its type.
    """
    ensure_key(json_data, key, default={})

    if not isinstance(json_data[key], dict):
        json_data[key] = {}


def ensure_vector_key(json_data, key):
    """
    Ensure that the given key belongs to the given json_data, and that the
    corresponding value has a vector structure. If needed, this value can be
    modified in order to ensure a vector structure.
    """
    ensure_compound_key(json_data, key)

    ensure_key(json_data[key], "x", default=0)
    ensure_key(json_data[key], "y", default=0)
    ensure_key(json_data[key], "z", default=0)
