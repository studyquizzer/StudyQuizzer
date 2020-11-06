from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone

from crackerbox_.model_exports import BOOK_CATEGORY_CHOICES
from utils import unique_slug_generator
from validators import validate_file_extension, validate_file_size


class AllDocumentCount(models.Model):
    name = models.CharField(max_length=50, default="Document_count")
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


IN_QUEUE = 0
PROCESSING = 1
COMPLETE = 2
ERROR = -1
STATUS_CHOICES = (
    (IN_QUEUE, "In Queue"),
    (PROCESSING, "Processing"),
    (COMPLETE, "Complete"),
    (ERROR, "Error"),
)


class Document(models.Model):
    # allow
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    docfile = models.FileField(upload_to="documents/")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    title = models.CharField(max_length=64, default="")
    created_time = models.DateTimeField(
        default=timezone.now, editable=False, blank=True
    )
    modified_time = models.DateTimeField(
        default=timezone.now, editable=False, blank=True
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    unique_id = models.CharField(max_length=64, default="")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # update modified date on save
        if kwargs.pop("update_modified", False):
            self.modified = timezone.now()
        return super(Document, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("document", args=[str(self.unique_id)])


def r_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(r_pre_save_receiver, sender=Document)


class Question(models.Model):
    TYPE_CHOICES = (
        ("TF", "True or False"),
        ("MCQ", "Multiple choice"),
    )
    doc = models.ForeignKey(
        Document, related_name="questions", on_delete=models.CASCADE
    )

    text = models.CharField(max_length=256)
    answer = models.CharField(max_length=100)
    question_type = models.CharField(choices=TYPE_CHOICES, max_length=3)
    option1 = models.CharField(max_length=64, default="")
    option2 = models.CharField(max_length=64, default="")
    option3 = models.CharField(max_length=64, default="")

    def __str__(self):
        return f"{self.doc.title} for {self.doc.owner}"


class Pdf(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="pdf_documents",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=64,
        default="",
        help_text="The title of the book",
        verbose_name="book title",
    )
    category = models.CharField(choices=BOOK_CATEGORY_CHOICES, max_length=3)
    created_time = models.DateTimeField(
        default=timezone.now, editable=False, blank=True
    )
    modified_time = models.DateTimeField(
        default=timezone.now, editable=False, blank=True
    )
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # update modified date on save
        if kwargs.pop("update_modified", False):
            self.modified = timezone.now()
        return super(Pdf, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pdf_detail", args=[str(self.slug)])


class AbstractRecord(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    score = models.IntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class QuizzerRecord(AbstractRecord):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["document", "owner"]

    def __str__(self):
        return f"{self.document} of {self.owner}"

    def get_absolute_url(self):
        return reverse("results", args=[str(self.document.unique_id)])


class DocumentError(models.Model):
    doc_id = models.UUIDField()
    error = models.TextField()
    source_text = models.TextField()

    def __str__(self):
        return f"error on object {self.doc_id}"
