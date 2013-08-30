from values import arg_eval

LOCAL_VALIDATORS = dict()

dummy_validator = lambda x: x

def register_local_validator(func):
	def _func(*args):
		def __func(value):
			arguments = list(map(arg_eval, args)) + [value]
			return func(*arguments)

		return __func
	LOCAL_VALIDATORS[func.__name__.upper()] = _func
	return func

def get_local_validator(name):
	return LOCAL_VALIDATORS.get(name, dummy_validator)

GLOBAL_VALIDATORS = dict()

def register_global_validator(func):
	def _func(*args):
		arguments = map(arg_eval, args)
		return func(*arguments)

	GLOBAL_VALIDATORS[func.__name__.upper()] = _func
	return func

def get_global_validator(name):
	return GLOBAL_VALIDATORS.get(name)

