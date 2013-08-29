from tcs.shortcuts import login_required, render, redirect, PermissionDenied, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tcs.models import Competition, Problem
from tcs.forms import ProblemAddForm

class ProblemDetails(DetailView):
	model = Problem

	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		if not obj.competition.has_permission(self.request.user):
			raise PermissionDenied()
		self.competition = obj.competition
		self.problem = obj
		return obj

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem
		return c

problem_details = login_required(ProblemDetails.as_view())

class ProblemList(ListView):
	def get_queryset(self):
		self.competition = get_object_or_404(Competition, slug=self.kwargs['slug'])
		if self.competition.has_permission(self.request.user):
			return self.competition.problem_set.order_by('-pk')
		else:
			raise PermissionDenied()

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		return c

	paginate_by = 10
	context_object_name = 'problem_list'

problem_list = login_required(ProblemList.as_view())

class ProblemAdd(CreateView):
	model = Problem

	def get_form_class(self):
		self.competition = get_object_or_404(Competition, slug = self.kwargs['slug'])
		return ProblemAddForm(self)

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()
		return c

problem_add = login_required(ProblemAdd.as_view())

class ProblemModify(UpdateView):
	model = Problem

	def get_form_class(self):
		return ProblemAddForm(self)

	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		if not obj.competition.has_permission(self.request.user) or obj.author != self.request.user:
			raise PermissionDenied()
		self.competition = obj.competition
		self.problem = obj
		return obj

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem
		return c

problem_modify = login_required(ProblemModify.as_view())
