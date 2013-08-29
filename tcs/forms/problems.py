from django import forms
from tcs.models import Solution, Problem
from datetime import datetime

def ProblemAddForm(view):
	class _ProblemAddForm(forms.ModelForm):
		name = forms.CharField(max_length = 100, label = "Tytuł")
		slug = forms.SlugField(max_length = 100, label = "Skrót")
		description = forms.CharField(widget = forms.Textarea, label = "Treść", help_text = 'Tutaj wpisujemy opis problemu algorytmicznego; nie treść!')

		class Meta:
			model = Problem
			fields = ('name', 'slug', 'description')

		def save(self, *args, **kwargs):
			obj = super().save(commit = False, *args, **kwargs)
			obj.author = view.request.user
			obj.competition = view.competition
			if not obj.date:
				obj.date = datetime.now()
			obj.save()
			return obj

	return _ProblemAddForm
