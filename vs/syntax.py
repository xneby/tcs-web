# This file contains syntax objects
from exceptions import *
from values import save_value, arg_eval, get_value, limits_add_validator
import re

class SyntaxObject(object):
	pass

class Syntax(SyntaxObject):
	def __init__(self,syntax):
		if syntax.count('\n')>0:
			syntax=syntax.split('\n')
			self.syntax=[]
			for line in syntax:
				self.syntax.append(Syntax(line))
				self.syntax.append(Whitespace('\n'))

			# Ucinam nadmiarowe \n z końca listy
			self.syntax.pop()

		elif syntax.count('(')>0 or syntax.count('[')>0 or syntax.count('{')>0:
			def par_pair(c):
				if c=='(': return ')'
				if c==')': return '('
				if c=='[': return ']'
				if c==']': return '['
				if c=='{': return '}'
				if c=='}': return '{'
				return None
			par_open='([{'
			par_close=')]}'
			self.syntax=[]
			token=''
			par_stack=[]
			for c in syntax:
				if c in par_open:
					if not par_stack:
						if token:
							self.syntax.append(Syntax(token))
							token=''
					token+=c
					par_stack.append(c)
				elif c in par_close:
					if not par_stack or par_stack[-1] != par_pair(c):
						raise UserSyntaxError("Tried to close not opened parenthese.")
					token+=c
					par_stack.pop()
					if not par_stack:
						if c==')': self.syntax.append(SpaceSequence(token))
						elif c==']': self.syntax.append(LineSequence(token))
						elif c=='}': self.syntax.append(EmptySequence(token))
						token=''
				else:
					token+=c
			if token:
				if par_stack:
					raise UserSyntaxError("Not closed parenthese left.")
				self.syntax.append(Syntax(token))

		else:
			self.syntax=[]
			token=''
			for c in syntax:
				if c.isspace():
					if token:
						self.syntax.append(Variable(token))
						token=''
					self.syntax.append(Whitespace(c))
				else:
					token+=c
			if token:
				self.syntax.append(Variable(token))

		self.syntax=tuple(self.syntax)

	def __repr__(self):
		return str(self.syntax)
		
	def read(self,stream,variables=None):
		if variables is None:
			variables = dict()
		for syntax in self.syntax:
			syntax.read(stream,variables)

class Sequence(SyntaxObject):
	def __init__(self,line):
		if self.delimiters=='{}':
			match=re.match(r'^{(?P<times>[^|]+?)[|](?P<counter>[a-z])[|](?P<body>.*)}$',line)
		elif self.delimiters=='[]':
			match=re.match(r'^\[(?P<times>[^|]+?)[|](?P<counter>[a-z])[|](?P<body>.*)\]$',line)
		elif self.delimiters=='()':
			match=re.match(r'^[(](?P<times>[^|]+?)[|](?P<counter>[a-z])[|](?P<body>.*)[)]$',line)
		else:
			raise VSError("Unknown type of parentheses - '{}'".format(self.delimiters))

		if match is None:
			raise UserSyntaxError("The body syntax in the sequence is invalid - should be {}times|counter|body{}.".format(self.delimiters[0],self.delimiters[1]))

		match=match.groupdict()
		self.times=match['times']
		self.counter=match['counter']
		self.body=Syntax(match['body'])

	def __repr__(self):
		return "Sequence{}{}/{}/{}{}".format(self.delimiters[0],self.times,self.counter,self.body,self.delimiters[1])
		
	def read(self,stream,variables=dict()):
		n=self.times
		for i in range(len(n)-2,-1,-1):
			if n[i]=='_' and n[i+1] in 'qwertyuiopasdfghjklzxcvbnm':
				n=n[:i+1]+variables[n[i+1]]+n[i+2:]
		try:
			n=arg_eval(n)
		except TypeError:
			raise UserSyntaxError("Type error in the first parameter of the sequence (perhaps something is still a string)")
		white=Whitespace(self.whitespace)
		v=dict(variables)
		try:
			for i in range(n):
				if i:
					white.read(stream)
				v[self.counter]=str(i)
				self.body.read(stream,v)
		except TypeError:
			raise UserSyntaxError("The first parameter of the sequence must be an integer")

class SpaceSequence(Sequence):
	def __init__(self,line):
		self.delimiters='()'
		self.whitespace=' '
		super().__init__(line)

class LineSequence(Sequence):
	def __init__(self,line):
		self.delimiters='[]'
		self.whitespace='\n'
		super().__init__(line)

class EmptySequence(Sequence):
	def __init__(self,line):
		self.delimiters='{}'
		self.whitespace=''
		super().__init__(line)

class Variable(SyntaxObject):
	def __init__(self,name):
		if not re.match(r'^[a-z](_[a-z])*$',name):
			raise UserSyntaxError("Variable name is invalid (should match '^[a-z](_[a-z])*$')")
		name=name.split('_')
		self.name=name[0]
		self.args=name[1:]
	def __repr__(self):
		return 'Variable('+'_'.join([self.name]+self.args)+')'
	def read(self,stream,variables=None):
		if variables is None:
			variables = dict()
		save_value('_'.join([self.name]+[variables[i] for i in self.args]),stream.read_token())

class Whitespace(SyntaxObject):

	def __init__(self,white):
		if len(white)>1 or white not in ' \n':
			raise UserSyntaxError("{} is not not acceptable as a whitespace".format(white))

		self.char=white

	def __repr__(self):
		if self.char==' ':
			return 'White(SPACE)'
		elif self.char=='\n':
			return 'White(NEWLINE)'
		elif not self.char:
			return 'White(EMPTY)'
		else:
			raise VSError("Whitespace not in {SPACE,NEWLINE,EMPTY}")

	def read(self,stream,variables=None):
		if variables is None:
			variables = dict()
		if self.char:
			stream.read_chars(self.char)
