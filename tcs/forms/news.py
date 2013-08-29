from django import forms
from tcs.models import News
from datetime import datetime

def NewsAddForm(view):
	class _NewsAddForm(forms.ModelForm):
		title = forms.CharField(max_length = 100, label = "Tytuł")
		text = forms.CharField(widget = forms.Textarea, label = "Treść")

		class Meta:
			model = News
			fields = ('title', 'text')

		def save(self, *args, **kwargs):
			obj = super().save(commit = False, *args, **kwargs)
			obj.author = view.request.user
			obj.competition = view.competition
			obj.time = datetime.now()
			obj.save()
			return obj

	return _NewsAddForm
