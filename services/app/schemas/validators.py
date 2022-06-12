from re import search as re_search


def validate_value_alphabetical(cls, value):
    """
    Reusable validator for pydantic models
    """
    pattern = "[^a-z A-Z .]"
    if re_search(pattern, value):
        raise ValueError('Use only letters.')
    return value

