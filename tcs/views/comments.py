from tcs.shortcuts import login_required, render, redirect, PermissionDenied, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tcs.models import Competition, Comment, CommentBucket
from tcs.forms import CommentAddForm
from django.http import HttpResponse
from datetime import datetime

class CommentAdd(CreateView):
	model = Comment

	def get_success_url(self):
		return self.bucket.get_url()
	
	def get_form_class(self):
		self.bucket = get_object_or_404(CommentBucket, pk = self.kwargs['pk'])
		self.competition = self.bucket.get_competition()
		return CommentAddForm(self)

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		c['bucket'] = self.bucket
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()
		return c

comment_add = login_required(CommentAdd.as_view())

class CommentModify(UpdateView):
	model = Comment

	def get_success_url(self):
		return self.bucket.get_url()
	
	def get_form_class(self):
		self.competition = self.bucket.get_competition()
		return CommentAddForm(self)

	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		self.competition = obj.bucket.get_competition()
		if not self.competition.has_permission(self.request.user) or obj.user != self.request.user:
			raise PermissionDenied()
		self.bucket = obj.bucket
		return obj

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		c['bucket'] = self.bucket
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()
		return c

comment_modify = login_required(CommentModify.as_view())

class CommentDelete(DeleteView):
	model = Comment

	def get_success_url(self):
		return self.bucket.get_url()
	
	def get_object(self, *args, **kwargs):
		obj = super().get_object(*args, **kwargs)
		self.competition = obj.bucket.get_competition()
		if not self.competition.has_permission(self.request.user) or obj.user != self.request.user:
			raise PermissionDenied()
		self.bucket = obj.bucket
		return obj

	def get_context_data(self, **kwargs):
		c = super().get_context_data(**kwargs)
		c['competition'] = self.competition
		c['bucket'] = self.bucket
		if not self.competition.has_permission(self.request.user):
			raise PermissionDenied()
		return c

comment_delete = login_required(CommentDelete.as_view())

class CommentAlert(View, SingleObjectMixin):
	model = CommentBucket
	def get(self, *args, **kwargs):
		bucket = self.get_object()
		self.request.user.commentalert_set.filter(bucket = bucket).update(count = 0, date=datetime.now())

		return HttpResponse('OK')

comment_alert = login_required(CommentAlert.as_view())
