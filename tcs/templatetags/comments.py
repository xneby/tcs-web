from django import template
register = template.Library()

from tcs.models import CommentBucket

@register.inclusion_tag('partials/comments.html', takes_context = True)
def comments(context, obj):
	bucket = obj.bucket

	return dict(bucket = bucket, request = context['request'])

@register.inclusion_tag('partials/alert.html', takes_context = True)
def alert(context, num):
	if hasattr(num, 'get_alert'):
		num = num.get_alert(context['user'])
	return dict(num = num)
	
