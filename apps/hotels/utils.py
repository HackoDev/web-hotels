def get_int_or_none(value):
	"""
	:param value: str or any
	:return: int or None
	"""
	try:
		return int(value)
	except:
		return None


def get_float_or_none(value):
	"""
	:param value: str or any
	:return: int or None
	"""
	try:
		return float(value)
	except:
		return None
