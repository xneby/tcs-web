from exceptions import *
import re

VALUES = {}
VALUES_IDS = {}
LIMITS = dict()

check_id=re.compile(r'^[a-z](?:_([0-9]+|[?]))*$')

def INT(i):
	try: i=int(i)
	except ValueError: pass
	return i

def get_value_filter(l,name):
	c=INT(name[0])
	name=name[1:]
	if c=='?':
		r=sorted(l)
		l=[]
		last='$'
		for el in r:
			if not el[0]:
				continue
			elif el[0][0]==last:
				l[-1].append(el)
			else:
				l.append([el])
				last=el[0][0]
			el[0]=el[0][1:]

		if name:
			for i in range(len(l)):
				l[i]=get_value_filter(l[i],name)
		else:
			for f in l:
				for i in range(len(f)):
					f[i]=f[i][1]

	else:
		for pair in l:
			if pair[0] and pair[0][0]==c:
				pair[0]=pair[0][1:]
			else:
				pair[0]='{'
		l=sorted(l)
		while l and l[-1][0]=='{':
			l.pop()
		if name:
			l=get_value_filter(l,name)
		else:
			for i in range(len(l)):
				l[i]=l[i][1]

	return l

def get_value(name):
	if check_id.match(name) is None:
		try:
			return arg_eval(name)
		except (NameError, SyntaxError):
			raise UserSyntaxError("{} is not defined".format(name))
	try:
		return VALUES[name]
	except KeyError:
		l=[ [[INT(j) for j in i.split('_')],VALUES[i]] for i in VALUES_IDS[name.split('_')[0]] ]
		return get_value_filter(l,name.split('_'))
		if False:
			try:
				return ((i,VALUES[name])[0] for i in sorted(VALUES_IDS[name]) )
			except KeyError:
				raise UserSyntaxError("Unknown identifier: {}".format(name))

def save_value(name, value):
	path=name.split('_')
	
	for i in range(len(path)):
		pref='_'.join(path[:i+1])
		if not VALUES_IDS.get(pref,None):
			VALUES_IDS[pref]=[]
		VALUES_IDS[pref].append(name)
		VALUES[name] = LIMITS.get(pref,lambda x: x)(VALUES.get(name,value))

def arg_eval(x):
	#print('arg_eval({})'.format(x))
	try:
		return eval(x, None, VALUES)
	except NameError as e:
		raise UserSyntaxError(e)

def combine(f1,f2):
	"""Returns a composition of two functions - f1(f2())"""
	def _result(s):
		return f1(f2(s))

	return _result

def limits_add_validator(name,cmd):
	if name not in LIMITS:
		LIMITS[name] = cmd
	else:
		LIMITS[name] = combine(cmd,LIMITS[name])
