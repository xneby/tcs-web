from django.contrib import admin
from .models import *

def adminize(model):
	class _admin(admin.ModelAdmin):
		pass
	admin.site.register(model, _admin)

adminize(Competition)
adminize(News)
adminize(Comment)
adminize(Problem)
adminize(Solution)
adminize(Vote)
adminize(Implementation)
