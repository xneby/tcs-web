from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from tcs.shortcuts import PermissionDenied, login_required, get_object_or_404
from tcs.models import Problem ,Solution, Implementation
from tcs.forms import ImplementationForm
from tcs.shortcuts import redirect
from datetime import datetime

class ImplementationAdd(CreateView):
	model = Implementation

	def get_form_class(self):
		self.problem = get_object_or_404(Problem, slug = self.kwargs['slug'])
		self.solution = get_object_or_404(Solution, pk = self.kwargs['solution_id'])
		if self.problem != self.solution.problem:
			raise PermissionDenied()

		self.competition = self.problem.get_competition()
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()

		return ImplementationForm(self)

	def get_context_data(self, *args, **kwargs):
		c = super().get_context_data(*args, **kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem
		c['solution'] = self.solution

		return c


implementation_add = login_required(ImplementationAdd.as_view())

class ImplementationModify(UpdateView):
	model = Implementation

	def get_form_class(self):
		self.problem = get_object_or_404(Problem, slug = self.kwargs['slug'])
		self.solution = get_object_or_404(Solution, pk = self.kwargs['solution_id'])
		if self.problem != self.solution.problem:
			raise PermissionDenied()

		self.competition = self.problem.get_competition()
		if not self.competition.has_permission(self.request.user) or self.solution != self.get_object().solution or (self.request.user != self.get_object().author and self.request.user != self.problem.author):
			raise PermissionDenied()

		return ImplementationForm(self)

	def get_context_data(self, *args, **kwargs):
		c = super().get_context_data(*args, **kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem
		c['solution'] = self.solution

		return c

implementation_modify = login_required(ImplementationModify.as_view())


class ImplementationDelete(DeleteView):
	model = Implementation

	def get_success_url(self):
		return self.solution.get_url()

	def get_object(self, *args, **kwargs):
		self.implementation = super().get_object(*args, **kwargs)
		self.problem = get_object_or_404(Problem, slug = self.kwargs['slug'])
		self.solution = get_object_or_404(Solution, pk = self.kwargs['solution_id'])
		if self.problem != self.solution.problem:
			raise PermissionDenied()

		self.competition = self.problem.get_competition()
		if not self.competition.has_permission(self.request.user) or self.solution != self.implementation.solution or self.request.user != self.problem.author:
			raise PermissionDenied()

		return self.implementation

	def get_context_data(self, *args, **kwargs):
		c = super().get_context_data(*args, **kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem
		c['solution'] = self.solution

		return c

implementation_delete = login_required(ImplementationDelete.as_view())

class ImplementationAccept(View, SingleObjectMixin):
	model = Implementation

	def get(self, *args, **kwargs):
		implementation = self.get_object()
		competition = implementation.get_competition()
		if not competition.has_permission(self.request.user) or self.request.user != implementation.solution.problem.author:
			raise PermissionDenied
		if 'value' in kwargs:
			value = kwargs['value']
			if value == 'acc':
				if not implementation.accepted:
					implementation.bucket.comment_set.create(user = implementation.solution.problem.author, title = 'Zaakceptowano implementację', text = '', date = datetime.now())
				implementation.accepted = True
			elif value == 'rej':
				if implementation.accepted != False:
					implementation.bucket.comment_set.create(user = implementation.solution.problem.author, title = 'Odrzucono implementację', text = '', date = datetime.now())
				implementation.accepted = False
			elif implementation.accepted:
				implementation.bucket.comment_set.create(user = implementation.solution.problem.author, title = 'Cofnięto akceptację', text = '', date = datetime.now())
				implementation.accepted = None
			elif implementation.accepted == False:
				implementation.bucket.comment_set.create(user = implementation.problem.author, title = 'Cofnięto odrzucenie', text = '', date = datetime.now())
				implementation.accepted = None

			implementation.save()

		return redirect(implementation.get_url())

implementation_accept = login_required(ImplementationAccept.as_view())
