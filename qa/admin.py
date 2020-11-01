from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget

from qa.models import (
    Answer,
    AnswerComment,
    AnswerVote,
    Question,
    QuestionComment,
    Flag,
)

admin.site.register(Question)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
admin.site.register(AnswerVote)
admin.site.register(Flag)


class AnswerModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }


admin.site.register(Answer, AnswerModelAdmin)
