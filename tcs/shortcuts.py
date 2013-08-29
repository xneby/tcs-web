from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def make_alert(*def_args):
	def get_alert(self, user, *args):
		count = 0
		if not args or args[0] == 'self':
			try:
				count += self.bucket.get_alert(user)
			except AttributeError:
				pass
			if args and args[0] == 'self':
				args = []
			else:
				args = def_args
		for x in args:
			for o in getattr(self, x + '_set').all():
				count += o.get_alert(user)
		return count
	return get_alert
