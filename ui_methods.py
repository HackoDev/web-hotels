def get_asd_asd(data, model, field_name):
    field = getattr(model, field_name, None)
    if hasattr(field, "info") and isinstance(field.info, dict) and 'verbose_name' in field.info:
        return field.info["verbose_name"]
    return field_name.capitalize()


def display_value(data, obj, field_name):
    if hasattr(obj, field_name):
        result = getattr(obj, field_name)
        if callable(result):
            result = str(result())
        return result
    raise ValueError("Has not attribute")