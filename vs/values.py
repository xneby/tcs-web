VALUES = {}

def save_value(name, value):
	VALUES[name] = value

def arg_eval(x):
	return eval(x, None, VALUES)
