from values import arg_eval
import re

LOCAL_VALIDATORS = dict()

dummy_validator = lambda x: x

def register_local_validator(func):
	def _func(*args):
		def __func(value):
			arguments = list(map(arg_eval, args)) + [value]
			return func(*arguments)

		__func.__doc__ = func.__doc__

		return __func

	_func.__doc__=func.__doc__

	match=re.match(r'^validator_(?P<name>[a-zA-Z0-9_]+)$',func.__name__)
	match=match.groupdict()
	LOCAL_VALIDATORS[match['name'].upper()] = _func
	return func

def get_local_validator(name):
	return LOCAL_VALIDATORS.get(name)

GLOBAL_VALIDATORS = dict()

def register_global_validator(func):
	def _func(*args):
		#arguments = map(arg_eval, args)
		return func(*args)
	
	_func.__doc__=func.__doc__

	match=re.match(r'^validator_(?P<name>[a-zA-Z0-9_]+)$',func.__name__)
	match=match.groupdict()

	GLOBAL_VALIDATORS[match['name'].upper()] = _func
	return func

def get_global_validator(name):
	return GLOBAL_VALIDATORS.get(name)


def list_local_validators(pref):
	print("All variable validators:\n")
	for key, val in [i for i in sorted(LOCAL_VALIDATORS.items())]:
		if key.lower().startswith(pref.lower()) and val.__doc__:
			print(val.__doc__,'\n')

def list_global_validators(pref):
	print("All additional functions:\n")
	for key, val in [i for i in sorted(GLOBAL_VALIDATORS.items())]:
		if key.lower().startswith(pref.lower()) and val.__doc__:
			print(val.__doc__,'\n')

