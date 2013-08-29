from django.db import models
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class Vote(models.Model):
	user = models.ForeignKey(User)
	value = models.IntegerField()
	bucket = models.ForeignKey("tcs.VotingBucket")

	class Meta:
		app_label = 'tcs'

class VotingBucket(models.Model):
	class Meta:
		app_label = 'tcs'

	def get_object(self):
		for i in ('solution_coolness', 'solution_difficulty', 'problem_coolness'):
			try:
				return getattr(self, i)
			except ObjectDoesNotExist:
				continue
		return None

	def get_url(self):
		return self.get_object().get_url()

	def get_competition(self):
		return self.get_object().get_competition()

	def get_votes(self):
		return self.vote_set.order_by('-value')

	def get_average(self):
		return self.vote_set.aggregate(Avg('value'))['value__avg']

	def __str__(self):
		return "VotingBucket {}".format(self.pk)
