from django.contrib import admin

from . import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "doc",
        "text",
        "option1",
        "option2",
        "option3",
        "answer",
        "question_type",
    )


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "created_time", "modified_time")


@admin.register(models.Pdf)
class PdfAdmin(admin.ModelAdmin):
    list_display = ("owner", "title", "created_time", "modified_time")


admin.site.register(models.AllDocumentCount)
admin.site.register(models.QuizzerRecord)
admin.site.register(models.DocumentError)
