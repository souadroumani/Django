
# Register your models here.



# task5/admin.py
from django.contrib import admin
from .models import Upload


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_name', 'is_image', 'size_kb', 'created_at')
    readonly_fields = ('original_name', 'extension', 'mime_type', 'size_bytes', 'sha256', 'is_image', 'created_at')

    def size_kb(self, obj):
        return f"{obj.size_bytes / 1024:.2f} KB"
    size_kb.short_description = 'Size (KB)'
