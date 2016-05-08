def get_asd_asd(data, model, field_name):
    field = getattr(model, field_name, None)
    if isinstance(field.info, dict) and field.info.has_key('verbose_name'):
        return field.info["verbose_name"]
    return field_name.capitalize()


def display_value(data, obj, field_name):
    if hasattr(obj, field_name):
        result = getattr(obj, field_name)
        if callable(result):
            result = unicode(result())
        return result
    raise ValueError("Has not attribute")