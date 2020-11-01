from django.contrib import admin

# Register your models here.
from MultiChoice.models import Question, Comments, Category

admin.site.register(Question)

admin.site.register(Comments)

admin.site.register(Category)
