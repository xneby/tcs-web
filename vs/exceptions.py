import sys

class ValidationError(Exception): pass

def failwith(message):
	print('FAIL: {}'.format(message))
	sys.exit(1)
