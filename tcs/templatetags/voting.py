from django import template
register = template.Library()

@register.inclusion_tag('partials/voting.html', takes_context = True)
def voting(context, obj, name):
	bucket = getattr(obj, name)

	votes = bucket.get_votes()
	
	results = {}
	own_vote = 0

	for vote in votes:
		if vote.value not in results:
			results[vote.value] = 0
		results[vote.value] += 1
		if vote.user == context['user']:
			own_vote = vote.value

	choices = []
	for i, x in enumerate(obj.get_voting(name), 1):
		if i not in results:
			results[i] = 0
		x.update(dict( votes = results[i], own = own_vote == i ))
		choices.append(x)

	return dict(bucket = bucket, choices = choices, own_vote = own_vote)
