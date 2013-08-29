from django import forms
from tcs.models import Solution
from datetime import datetime
from django.contrib.auth.models import User

def SolutionForm(view):
	class _SolutionForm(forms.ModelForm):
		name = forms.CharField(max_length = 100, label = "Tytuł")
		expected_score = forms.IntegerField(label = "Oczekiwana punktacja")
		text = forms.CharField(widget = forms.Textarea, label = "Treść", help_text = 'Tutaj wpisujemy opis algorytmu; nie kod!')

		class Meta:
			model = Solution
			fields = ('name', 'expected_score', 'text')

		def save(self, *args, **kwargs):
			obj = super().save(commit = False, *args, **kwargs)
			try:
				obj.author
			except User.DoesNotExist:
				obj.author = view.request.user
			obj.problem = view.problem
			obj.date = datetime.now()
			if obj.author != view.problem.author:
				if obj.accepted:
					obj.bucket.comment_set.create(title = 'Cofnięto akceptację', date = obj.date, user = view.problem.author, text = '<p>Powód: zmiana treści rozwiązania.</p>')
					obj.accepted = None
			obj.save()
			return obj

	return _SolutionForm
