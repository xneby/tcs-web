from interfaces import register_global_validator
from exceptions import *

@register_global_validator
def validator_unique(seq):
	"""UNIQUE(sequence seq):
  if given a simple sequence, checks whether all elements are unique
  if given a sequence of sequence of ... of sequence,
  it checks uniuqeness for every subsequence, which does not contain any other sequences"""
	if not seq: return
	if type(seq[0]) is tuple or type(seq[0]) is list:
		for i in seq:
			validator_unique(i)
	else:
		s = sorted(seq)
		for i, j in zip(s, s[1:]):
			if i == j:
				raise UserTestError('not unique')

@register_global_validator
def validator_print(*args):
	"""PRINT(*args):
  calls a print function with same arguments
  it separates arguments with a space"""
	print(*args)

@register_global_validator
def validator_println(*args):
	"""PRINT(*args):
  calls a print function with same arguments
  is separates arguments with a new line"""
	print(*args,sep='\n')

@register_global_validator
def validator_list(arg):
	"""LIST(argument):
  prints the argument - only for debug purposes"""
	print('=== arguments  ===\n{}\n=== end of arg ==='.format(list([arg])))
