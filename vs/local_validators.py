from interfaces import register_local_validator
from exceptions import *

@register_local_validator
def validator_length(min_len, max_len, value):
	"""LENGTH(int min_len, int max_len) for string:
  checks whether given string's length is in the range [min_length, max_length]."""
	try:
		a=len(value)
		if a<int(min_len) or a>int(max_len):
			raise UserTestError('the length does not match')
	except:
		raise UserTestError('with LENGTH function you can only check strings')
	return value

@register_local_validator
def validator_range(min_val, max_val, n):
	"""RANGE(int min_val, int max_val) for integer:
  checks whether fiven integers is in the range [min_val, max_val]."""
	try:
		if n < int(min_val) or n > int(max_val):
			raise UserTestError('value not in range [{}; {}]'.format(min_val, max_val))
	except TypeError:
		raise UserSyntaxError('with RANGE function you can only check integers')
	return n

@register_local_validator
def validator_int(value):
	"""INT for token:
  casts the token into an integer."""
	try:
		n = int(value)
	except ValueError:
		raise UserTestError('{} is not an integer'.format(value))
	return n

@register_local_validator
def validator_string(value):
	"""STRING for token:
  casts the token into a string."""
	try:
		n = str(value)
	except ValueError:
		raise UserTestError('cannot convert {} to a string'.format(value))
	return n

@register_local_validator
def validator_word(value):
	"""WORD for string:
  checks whether the string contains only letters from the latin alphabet."""
	for i in value:
		if i not in 'qwertyuiopasdfghjklzxcvbnm':
			raise UserTestError('letters in string not from latin alphabet')
	return value

@register_local_validator
def validator_letters(letters,value):
	"""LETTERS(string x) for string:
  checks whether all letters in the string are also in x."""
	for i in value:
		if i not in letters:
			raise UserTestError('letters in string ({}) not from {}{}{}'.format(i,'{\'',letters,'\'}'))
	return value

@register_local_validator
def validator_prime(value):
	"""PRIME for integer:
  checks whether an integer is a prime number."""
	if type(value) is not int:
		raise UserTestError('PRIME function requires an integer')
	i = 2
	while i*i <= value:
		if value % i == 0:
			raise UserTestError('not a prime')
		i += 1
	return value

@register_local_validator
def validator_odd(value):
	"""ODD for integer:
  checks whether the integer is odd."""
	try:
		if value%2!=1:
			raise UserTestError('{} is not odd'.format(value))
	except TypeError as e:
		raise UserSyntaxError("ODD requires an integer")
	return value

@register_local_validator
def validator_even(value):
	"""EVEN for integer:
  checks whether the integer is even."""
	try:
		if value%2!=0:
			raise UserTestError('{} is not odd'.format(value))
	except TypeError as e:
		raise UserSyntaxError("EVEN requires an integer")
	return value
