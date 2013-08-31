from django import forms
from tcs.models import Solution, Implementation
from datetime import datetime
from django.contrib.auth.models import User

def ImplementationForm(view):
	class _ImplementationForm(forms.ModelForm):
		language = forms.CharField(label = "Język", help_text = "cpp/c/pascal/caml")
		code = forms.CharField(widget = forms.Textarea, label = "Kod")

		class Meta:
			model = Implementation
			fields = ('language', 'code')

		def save(self, *args, **kwargs):
			obj = super().save(commit = False, *args, **kwargs)
			try:
				obj.author
			except User.DoesNotExist:
				obj.author = view.request.user
			obj.solution = view.solution
			obj.date = datetime.now()
			if obj.author != view.problem.author:
				if obj.accepted:
					obj.bucket.comment_set.create(title = 'Cofnięto akceptację', date = obj.date, user = view.problem.author, text = '<p>Powód: zmiana implementacji.</p>')
					obj.accepted = None
			obj.save()
			return obj

	return _ImplementationForm
