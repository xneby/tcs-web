from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.db.models import Sum, F
from datetime import datetime

class Comment(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 100)
	text = models.TextField()
	date = models.DateTimeField()

	bucket = models.ForeignKey("tcs.CommentBucket")

	def save(self, *args, **kwargs):
		if self.pk:
			return super().save(*args, **kwargs)
		else:
			retval = super().save(*args, **kwargs)

			self.bucket.commentalert_set.all().update(count = F('count') + 1)
			return retval

	def delete(self, *args, **kwargs):
		bucket = self.bucket
		retval = super().delete(*args, **kwargs)
		for i in bucket.commentalert_set.all():
			i.count = bucket.comment_set.filter(date__gt = i.date).count()
			i.save()
		return retval

	class Meta:
		app_label = 'tcs'

class CommentBucket(models.Model):
	class Meta:
		app_label = 'tcs'

	def get_alert(self, u):
		return self.commentalert_set.filter(user = u).aggregate(Sum('count'))['count__sum'] or 0
			
	def count_comment(self):
		return self.comment_set.count()

	def get_object(self):
		for i in ('news', 'problem', 'solution'):
			try:
				return getattr(self, i)
			except ObjectDoesNotExist:
				continue
		return None

	def get_url(self):
		return self.get_object().get_url()

	def get_competition(self):
		return self.get_object().get_competition()

	def form(self):
		from tcs.forms import CommentAddForm
		return CommentAddForm(None)()

	def get_comments(self):
		return self.comment_set.order_by('-date')

	def __str__(self):
		return "CommentBucket {}".format(self.pk)

	def save(self, *args, **kwargs):
		retval = super().save(*args, **kwargs)
		to_create = []
		for u in User.objects.all():
			to_create.append(CommentAlert(bucket = self, user = u, count = 0))
		CommentAlert.objects.bulk_create(to_create)
		return retval

class CommentAlert(models.Model):
	bucket = models.ForeignKey('tcs.CommentBucket')
	user = models.ForeignKey('auth.User')
	count = models.IntegerField()
	date = models.DateTimeField(default = datetime(1970, 1, 1, 0, 0))

	class Meta:
		app_label = 'tcs'

def create_alerts(sender, **kwargs):
	if isinstance(sender, User):
		to_create = []
		for bucket in CommentBucket.objects.all():
			to_create.append(CommentAlert(bucket = bucket, user = sender, count = bucket.count_comment()))
		CommentAlert.objects.bulk_create(to_create)

post_save.connect(create_alerts)
