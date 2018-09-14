from django.conf import settings

from celery import shared_task
import json
import os

from files_app.utils import search_documents
from files_app.admin import DocumentResource


# Function that saves documents to local storage
@shared_task
def export_documents(search_str):
    # small fix, since in queue empty string is converted to undefined
    search_str = search_str if search_str != 'undefined' else ''

    object_list = search_documents(search_str)
    data = DocumentResource().export(object_list)
    file_name = os.path.join(settings.BASE_DIR, 'export/Documents.json')
    with open(file_name, mode='w', encoding='utf-8') as f:
        json.dump(data.json, f)
