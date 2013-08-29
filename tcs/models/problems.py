from django.db import models
from tcs.interfaces import Commentable, Voteable
from tcs.shortcuts import make_alert
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Problem(Commentable, Voteable('coolness', related='problem')):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(unique = True)
	date = models.DateTimeField()

	competition = models.ForeignKey('tcs.Competition')

	author = models.ForeignKey(User)
	description = models.TextField()

	get_alert = make_alert('solution')

	def get_competition(self):
		return self.competition
	
	def get_absolute_url(self):
		return reverse('problem-details', args = (self.slug, ))

	def get_url(self):
		return self.get_absolute_url()

	class Meta:
		app_label = 'tcs'

class Solution(Commentable, Voteable('coolness', related = 'solution'), Voteable('difficulty', related = 'solution')):
	problem = models.ForeignKey('tcs.Problem')
	name = models.CharField(max_length = 100)

	text = models.TextField()
	expected_score = models.IntegerField(blank = True, null = True)
	author = models.ForeignKey(User)

	date = models.DateTimeField()
	accepted = models.NullBooleanField(blank = True, null = True)

	get_alert = make_alert('implementation')
	def get_competition(self):
		return self.problem.get_competition()

	def get_url(self):
		return self.get_absolute_url()

	def get_absolute_url(self):
		return reverse('solution-list', args = [self.problem.slug]) + '?solution={}'.format(self.pk)

	class Meta:
		app_label = 'tcs'

class Implementation(Commentable):
	solution = models.ForeignKey('tcs.Solution')
	language = models.CharField(max_length = 10)
	code = models.TextField()

	class Meta:
		app_label = 'tcs'

	def get_competition(self):
		return self.solution.get_competition()

	def get_url(self):
		return self.solution.get_url()

	get_alert = make_alert()
