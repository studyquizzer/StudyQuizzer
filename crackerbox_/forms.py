from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import Form, NumberInput, Textarea, TextInput

from crackerbox_.helpers import generate_unique_id

from .models import Document


class DocumentForm(Form):
    docText = forms.CharField(
        widget=Textarea(attrs={"class": "form-control"}), required=False
    )

    docTitle = forms.CharField(
        help_text="Title of the document.",
        widget=TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    numberOfQuestions = forms.IntegerField(
        help_text="Number of questions",
        widget=NumberInput(attrs={"class": "form-control"}),
        required=True,
        min_value=1,
    )

    def clean(self):
        cleaned_data = super(DocumentForm, self).clean()
        upText = cleaned_data.get("docText")
        title_ = cleaned_data.get("docTitle")
        if not title_:
            raise ValidationError("Empty Title")
        if not upText:
            raise ValidationError("Empty input.")
        if len(upText.encode("utf-8")) < 500:
            raise ValidationError("Not enough words.")

    def generateDocumentObject(self, user):
        doc = Document()
        doc.title = self.cleaned_data.get("docTitle")
        doc.unique_id = generate_unique_id()
        fpath = default_storage.get_available_name(f"{doc.title}_{user}.txt")
        savedDoc = default_storage.save(
            fpath, ContentFile(self.cleaned_data.get("docText"))
        )
        doc.docfile = savedDoc
        return doc
