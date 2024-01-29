from django.apps import AppConfig
import os
from datetime import datetime
import uuid

class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"


def user_directory_path(instance, filename):
    date = datetime.now()
    name = date.strftime('%H:%M')
    path = "images/"

    # Check if the file is an InMemoryUploadedFile
    if hasattr(filename, 'name'):
        original_filename = filename.name
        extension = os.path.splitext(original_filename)[-1]
    else:
        original_filename = filename
        extension = "." + original_filename.split('.')[-1]

    # Filename reformat
    filename_reformat = f'scrap{name}{extension}'

    return os.path.join(path, filename_reformat)
