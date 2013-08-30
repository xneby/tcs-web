from interfaces import register_local_validator
from exceptions import ValidationError

@register_local_validator
def range(min_val, max_val, n):
	if n < min_val or n > max_val:
		raise ValidationError('not in range [{}; {}]'.format(min_val, max_val))

@register_local_validator
def int(value):
	try:
		n = __builtins__['int'](value)
	except ValueError:
		raise ValidationError('not an integer')
	return n

@register_local_validator
def prime(value):
	i = 2
	while i*i <= value:
		if value % i == 0:
			raise ValidationError('not a prime')
		i += 1
