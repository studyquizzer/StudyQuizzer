import uuid
from crackerbox_.models import Document
from annoying.functions import get_object_or_None


def generate_unique_id():
    id = uuid.uuid4()
    doc_with_id = get_object_or_None(Document, unique_id=id)

    while doc_with_id:
        id = uuid.uuid4()
        doc_with_id = get_object_or_None(Document, unique_id=id)

    return id
