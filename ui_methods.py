def get_asd_asd(data, model, field_name):
	field = getattr(model, field_name, None)
	if isinstance(field.info, dict) and field.info.has_key('verbose_name'):
		return field.info["verbose_name"]
	return field_name.capitalize()


def display_value(data, obj, field_name):
	if hasattr(obj, field_name):
		return getattr(obj, field_name)
	raise ValueError("Has not attribute")