from tcs.shortcuts import login_required, render, redirect, PermissionDenied, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tcs.models import Competition, News
from tcs.forms import NewsAddForm

class CompetitionsList(ListView):
	model = Competition
	context_object_name = 'competitions'

	def get_queryset(self):
		return Competition.objects.filter(group__in = self.request.user.groups.all())

competitions_list = login_required(CompetitionsList.as_view())

class CompetitionDetails(DetailView):
	model = Competition
	context_object_name = 'competition'

	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		if not obj.has_permission(self.request.user):
			raise PermissionDenied()
		return obj

competition_details = login_required(CompetitionDetails.as_view())

class CompetitionNews(ListView):
	def get_queryset(self):
		self.competition = get_object_or_404(Competition, slug=self.kwargs['slug'])
		if self.competition.has_permission(self.request.user):
			return self.competition.news_set.order_by('-time')
		else:
			raise PermissionDenied()

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		return c

	paginate_by = 10
	context_object_name = 'news_list'

competition_news = login_required(CompetitionNews.as_view())

class CompetitionNewsAdd(CreateView):
	model = News

	def get_success_url(self):
		return reverse('competition-news', args=[self.competition.slug])
	
	def get_form_class(self):
		self.competition = get_object_or_404(Competition, slug = self.kwargs['slug'])
		return NewsAddForm(self)

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()
		return c

competition_news_add = login_required(CompetitionNewsAdd.as_view())

class CompetitionNewsModify(UpdateView):
	model = News

	def get_success_url(self):
		return reverse('competition-news', args=[self.competition.slug])
	
	def get_form_class(self):
		return NewsAddForm(self)

	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		if not obj.competition.has_permission(self.request.user) or obj.author != self.request.user:
			raise PermissionDenied()
		self.competition = obj.competition
		return obj

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()
		return c

competition_news_modify = login_required(CompetitionNewsModify.as_view())

class CompetitionNewsDelete(DeleteView):
	model = News

	def get_success_url(self):
		return reverse('competition-news', args=[self.competition.slug])
	
	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		if not obj.competition.has_permission(self.request.user) or obj.author != self.request.user:
			raise PermissionDenied()
		self.competition = obj.competition
		return obj

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()
		return c

competition_news_delete = login_required(CompetitionNewsDelete.as_view())

