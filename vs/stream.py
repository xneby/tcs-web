from exceptions import *

class Stream(object):
	"""Smartly reads from a string"""
	def __init__(self, s):
		"""Init stream with a string s"""
		self.s = s
		self.i = 0
		self.cinl = 0
		self.line = 0
		self.l = len(s)
	
	def position(self):
		return "line {}, char {}".format(self.line,self.cinl)
	
	def skip(self):
		if self.next() == '\n':
			self.line += 1
			self.cinl = -1
		self.i += 1
		self.cinl += 1

	def next(self):
		"""Returns a character under the pointer or None if EOF"""
		if self.i == self.l:
			return None
		return self.s[self.i]

	def read_chars(self, chars):
		"""Reads any character from set chars.
		chars is a string not a set actually."""
		if self.next() in chars:
			self.skip()
			return True
		raise UserTestError("read '{}' but expected [{}]".format(self.next(), chars))
	
	def read_eof(self):
		"""Tries to read EOF"""
		if self.next() is not None:
			raise UserTestError("read '{}' but expected EOF".format(self.next()))

	def read_token(self):
		"""Reads and returns a group of non-white characters"""
		s = ''
		while self.next() is not None and not self.next().isspace():
			s += self.next()
			self.skip()
		if not s:
			raise UserTestError('no token')
		return s

