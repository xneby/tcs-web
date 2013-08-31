from django.db import models
from tcs.interfaces import Commentable, Voteable
from tcs.shortcuts import make_alert
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import math

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

	def get_solutions(self):
		return self.solution_set.order_by('-expected_score')

	def get_difficulty(self):
		sols = self.solution_set.filter(accepted = True).order_by('-expected_score')
		result = 0.0
		last_score = 100
		low_diff = 5.0
		for sol in sols:
			if sol.get_difficulty() == None: continue
			result += low_diff * (last_score - sol.expected_score)
			
			last_score = sol.expected_score
			low_diff = min(low_diff, sol.get_difficulty())
		return result + last_score * low_diff

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

	def get_implementation_difficulty(self):
		try:
			impl = self.implementation_set.filter(accepted = True).order_by('code_length')[:1].get().get_difficulty()
		except Implementation.DoesNotExist:
			impl = 5.0
		return impl

	def get_difficulty(self):
		conc = self.difficulty.get_average() or 5.0
		impl = self.get_implementation_difficulty()

		return math.sqrt((conc*conc + impl*impl)/2)

	def get_implementations(self):
		return self.implementation_set.all()

	class Meta:
		app_label = 'tcs'

class Implementation(Commentable):
	solution = models.ForeignKey('tcs.Solution')
	language = models.CharField(max_length = 10)
	code = models.TextField()
	code_length = models.IntegerField()
	date = models.DateTimeField()
	author = models.ForeignKey('auth.User')
	accepted = models.NullBooleanField(blank = True, null = True)

	class Meta:
		app_label = 'tcs'

	def get_difficulty(self):
		l = self.code_length
		if l <= 50: return 1.0
		if l >= 250: return 5.0
		return l/50.0

	def get_competition(self):
		return self.solution.get_competition()

	def get_url(self):
		return self.get_absolute_url()

	def get_absolute_url(self):
		return self.solution.get_url()

	def save(self, *args, **kwargs):
		self.code_length = self.code.count('\n')
		if not self.code.endswith('\n'):
			self.code_length += 1
		return super().save(*args, **kwargs)

	get_alert = make_alert()
