from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_url(value):
	url_validator = URLValidator()
	url_invalid = False
	try:
		url_validator(value)
	except:
		url_invalid = True
		try:
			value = "http://"+value
			url_validator(value)
			url_invalid = False
		except:
			url_invalid = True

	if url_invalid:
		raise ValidationError("Invalid Data for this field")
	return value
