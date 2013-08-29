from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from tcs.shortcuts import redirect, login_required, PermissionDenied

from tcs.models import VotingBucket, Vote

class VoteView(View,SingleObjectMixin):
	model = VotingBucket

	def post(self, *args, **kwargs):
		bucket = self.get_object()
		url = bucket.get_url()

		if not bucket.get_competition().has_permission(self.request.user):
			raise PermissionDenied()

		if 'vote' not in self.request.POST: return redirect(url)
		value = self.request.POST['vote']

		try:
			value = int(value)
		except ValueError:
			return redirect(url)

		try:
			vote = bucket.vote_set.get(user = self.request.user)
			vote.value = value
			vote.save()
		except Vote.DoesNotExist:
			vote = bucket.vote_set.create(user = self.request.user, value = value)

		if vote.value == 0:
			vote.delete()

		return redirect(url)


vote = login_required(VoteView.as_view())
