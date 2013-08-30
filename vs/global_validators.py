from interfaces import register_global_validator
from exceptions import ValidationError

@register_global_validator
def unique(seq):
	s = sorted(seq)
	for i, j in zip(s, s[1:]):
		if i == j:
			raise ValidationError('not a permutation')
