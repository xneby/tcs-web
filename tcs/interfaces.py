from django.db import models
from tcs.models import CommentBucket, VotingBucket

class Commentable(models.Model):
	bucket = models.OneToOneField(CommentBucket, blank = True)

	def save(self, *args, **kwargs):
		try:
			self.bucket
		except CommentBucket.DoesNotExist:
			new_bucket = CommentBucket()
			new_bucket.save()
			self.bucket = new_bucket

		return super().save(*args, **kwargs)

	class Meta:
		abstract = True

VOTING = {
	'difficulty': [
			dict(text = 'Very Easy', style = 'badge-warning'),
			dict(text = 'Easy', style = 'badge-info'),
			dict(text = 'Medium', style = 'badge-success'),
			dict(text = 'Hard', style = 'badge-important'),
			dict(text = 'Very Hard', style = 'badge-inverse'),
		],
	'coolness': [
			dict(text = 'Boring', style = 'badge-warning'),
			dict(text = 'Typical', style = 'badge-info'),
			dict(text = 'Not Bad', style = 'badge-success'),
			dict(text = 'Cool', style = 'badge-important'),
			dict(text = 'Awesome', style = 'badge-inverse'),
		],
}

def Voteable(field_name, related = '', category = None):
	if category is None: category = field_name
	assert category in VOTING

	def make_save(obj):
		def save(self, *args, **kwargs):
			try:
				getattr(self, field_name)
			except VotingBucket.DoesNotExist:
				new_bucket = VotingBucket()
				new_bucket.save()
				setattr(self, field_name,  new_bucket)

			return super(obj, self).save(*args, **kwargs)

		return save
	
	def make_voting(obj):
		@classmethod
		def get_voting(self, arg):
			if arg == category:
				return VOTING[arg]

			return super(obj, self).get_voting(arg)
	
		return get_voting

	class Meta:
		abstract = True
	
	_Voteable = type('_Voteable', (models.Model, ), {
			'__module__': Meta.__module__,
			field_name: models.OneToOneField(VotingBucket, blank = True, related_name = related + '_' + category),
			'Meta': Meta
		})

	_Voteable.save = make_save(_Voteable)
	_Voteable.get_voting = make_voting(_Voteable)

	return _Voteable
