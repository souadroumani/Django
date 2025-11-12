from django.db import models
import os
from .validators import validate_file_upload

# Create your models here.

def upload_to(instance, filename):
    # use date-based folders optionally: "uploads/%Y/%m/%d/filename"
    return os.path.join("uploads", filename)

class Upload(models.Model):
    file = models.FileField(upload_to=upload_to)
    original_name = models.CharField(max_length=200)
    extension = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=100)
    size_bytes = models.IntegerField()
    sha256 = models.CharField(max_length=64)
    is_image = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and (not self.pk or not Upload.objects.filter(pk=self.pk, file=self.file).exists()):
            meta = validate_file_upload(self.file)
            self.original_name = meta['sanitized_name']
            self.extension = meta['extension']
            self.mime_type = meta['mime_type']
            self.size_bytes = meta['size_bytes']
            self.sha256 = meta['sha256']
            self.is_image = meta['is_image']

        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_name or "Unnamed Upload"