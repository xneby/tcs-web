from django.db import models
from django.contrib.auth.models import Group
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from tcs.shortcuts import make_alert
from .problems import Implementation, Solution

class Competition(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, blank = True)
	group = models.ForeignKey(Group)

	def __repr__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)

		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('competition-details', args=[self.slug])

	def has_permission(self, user):
		return self.group in user.groups.all()

	get_alert = make_alert('problem', 'news')

	class Meta:
		app_label = 'tcs'

	def get_latest_problems(self):
		return self.problem_set.order_by('-date')[:5]

	def get_latest_solutions(self):
		return Solution.objects.filter(problem__competition = self).order_by('-date')[:5]

	def get_latest_implementations(self):
		return Implementation.objects.filter(solution__problem__competition = self).order_by('-date')[:5]

