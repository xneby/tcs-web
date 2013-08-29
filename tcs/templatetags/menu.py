from django import template
from django.core.urlresolvers import reverse
register = template.Library()

@register.inclusion_tag('_base/menu.html', takes_context = True)
def menu(context):
	if not context['user'].is_authenticated(): return dict()
	menu = []

	request = context['request']
	def D(**kwargs):
		kwargs['active'] = kwargs.get('url', None) == request.path
		return kwargs

	menu.append(D( text = "Konkursy", icon = "th-large", url = reverse('competitions-list')))

	menu.append(D( spacer = True))
	if 'competition' in context:
		competition = context['competition']
		menu.append(D(text = competition.name, icon = 'home', url = reverse('competition-details', args = [competition.slug]), strong = True))
		menu.append(D(text = 'Wiadomości', icon = 'envelope', url = reverse('competition-news', args = [competition.slug]), alert = competition.get_alert(request.user, 'news')))
		menu.append(D(text = 'Zadania', icon = 'th', url = reverse('competition-problems', args = [competition.slug]), alert = competition.get_alert(request.user, 'problem')))
		menu.append(D(text = 'Kontesty', icon = 'list', url = '#'))
		menu.append(D( spacer = True))

	if 'problem' in context:
		problem = context['problem']
		menu.append(D(text = problem.name, icon = 'book', url = reverse('problem-details', args = [problem.slug]), strong = True, alert = problem.get_alert(request.user, 'self'))),
		menu.append(D(text = 'Rozwiązania', icon = 'cog', url = reverse('solution-list', args = [problem.slug]), alert = problem.get_alert(request.user, 'solution'))),
		menu.append(D(text = 'Treść zadania', icon = 'file', url = '#')),
		menu.append(D(text = 'Testy', icon = 'leaf', url = '#')),
		menu.append(D(text = 'Pliki', icon = 'tag', url = '#')),
		menu.append(D(text = 'Kontrprzykłady', icon = 'exclamation-sign', url = '#')),
		menu.append(D(text = 'Status zadania', icon = 'ok-sign', url = '#')),

		menu.append(D(spacer = True))

	if request.user.is_superuser:
		menu.append(D( text = 'Administracja', icon = 'star', url='/admin/'))
	menu.append(D( text = 'Ustawienia', icon = 'wrench', url=reverse('passwd')))

	return dict(menu = menu)


