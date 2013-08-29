from django import forms
from tcs.models import Comment
from datetime import datetime

def CommentAddForm(view):
	class _CommentAddForm(forms.ModelForm):
		title = forms.CharField(max_length = 100, label = "Tytuł")
		text = forms.CharField(widget = forms.Textarea, label = "Treść")

		class Meta:
			model = Comment
			fields = ('title', 'text')

		def save(self, *args, **kwargs):
			obj = super().save(commit = False, *args, **kwargs)
			obj.user = view.request.user
			obj.bucket = view.bucket
			obj.date = datetime.now()
			obj.save()
			return obj

	return _CommentAddForm
