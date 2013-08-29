from tcs.interfaces import Commentable
from tcs.shortcuts import make_alert
from django.db import models

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class News(Commentable):
	author = models.ForeignKey(User)
	competition = models.ForeignKey('tcs.Competition')

	title = models.CharField(max_length = 100)
	text = models.TextField()
	time = models.DateTimeField()

	get_alert = make_alert()

	def get_url(self):
		return reverse('competition-news', args=[self.competition.slug])

	def get_competition(self):
		return self.competition

	class Meta:
		app_label = 'tcs'
