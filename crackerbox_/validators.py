from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 50485760:
        raise ValidationError(
            "The maximum file size that can be uploaded is 50MB"
        )
    else:
        return value


def validate_file_extension(value):
    if value.file.content_type != "application/pdf":
        raise ValidationError("Only Pdf Documents are accepted")
