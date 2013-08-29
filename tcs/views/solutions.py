from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from tcs.shortcuts import PermissionDenied, login_required, get_object_or_404
from tcs.models import Problem ,Solution
from tcs.forms import SolutionForm
from tcs.shortcuts import redirect
from datetime import datetime

class SolutionList(ListView):
	def get_queryset(self):
		self.problem = get_object_or_404(Problem, slug = self.kwargs['slug'])
		if not self.problem.get_competition().has_permission(self.request.user):
			raise PermissionDenied()
		return self.problem.solution_set.all()

	def get_context_data(self, *args, **kwargs):
		c = super().get_context_data(*args, **kwargs)
		c['competition'] = self.problem.get_competition()
		c['problem'] = self.problem
		try:
			show = int(self.request.GET.get('solution', '0'))
		except ValueError:
			show = 0
		c['show'] = show
		return c

solution_list = login_required(SolutionList.as_view())

class SolutionAdd(CreateView):
	model = Solution

	def get_form_class(self):
		self.problem = get_object_or_404(Problem, slug = self.kwargs['slug'])
		self.competition = self.problem.get_competition()
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()

		return SolutionForm(self)

	def get_context_data(self, *args, **kwargs):
		c = super().get_context_data(*args, **kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem

		return c


solution_add = login_required(SolutionAdd.as_view())

class SolutionModify(UpdateView):
	model = Solution

	def get_form_class(self):
		self.problem = get_object_or_404(Problem, slug = self.kwargs['slug'])
		self.competition = self.problem.get_competition()
		if not self.competition.has_permission(self.request.user) or self.problem != self.get_object().problem or (self.request.user != self.get_object().author and self.request.user != self.problem.author):
			raise PermissionDenied()

		return SolutionForm(self)

	def get_context_data(self, *args, **kwargs):
		c = super().get_context_data(*args, **kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem

		return c

solution_modify = login_required(SolutionModify.as_view())


class SolutionDelete(DeleteView):
	model = Solution

	def get_success_url(self):
		return self.problem.get_url()

	def get_object(self, *args, **kwargs):
		self.solution = super().get_object(*args, **kwargs)
		self.problem = get_object_or_404(Problem, slug = self.kwargs['slug'])
		self.competition = self.problem.get_competition()
		if not self.competition.has_permission(self.request.user) or self.problem != self.solution.problem or self.request.user != self.problem.author:
			raise PermissionDenied()

		return self.solution

	def get_context_data(self, *args, **kwargs):
		c = super().get_context_data(*args, **kwargs)
		c['competition'] = self.competition
		c['problem'] = self.problem

		return c


solution_delete = login_required(SolutionDelete.as_view())

class SolutionAccept(View, SingleObjectMixin):
	model = Solution

	def get(self, *args, **kwargs):
		solution = self.get_object()
		competition = solution.get_competition()
		if not competition.has_permission(self.request.user) or self.request.user != solution.problem.author:
			raise PermissionDenied
		if 'value' in kwargs:
			value = kwargs['value']
			if value == 'acc':
				if not solution.accepted:
					solution.bucket.comment_set.create(user = solution.problem.author, title = 'Zaakceptowano rozwiązanie', text = '', date = datetime.now())
				solution.accepted = True
			elif value == 'rej':
				if solution.accepted != False:
					solution.bucket.comment_set.create(user = solution.problem.author, title = 'Odrzucono rozwiązanie', text = '', date = datetime.now())
				solution.accepted = False
			elif solution.accepted:
				solution.bucket.comment_set.create(user = solution.problem.author, title = 'Cofnięto akceptację', text = '', date = datetime.now())
				solution.accepted = None
			elif solution.accepted == False:
				solution.bucket.comment_set.create(user = solution.problem.author, title = 'Cofnięto odrzucenie', text = '', date = datetime.now())
				solution.accepted = None

			solution.save()

		return redirect(solution.get_url())

solution_accept = login_required(SolutionAccept.as_view())
