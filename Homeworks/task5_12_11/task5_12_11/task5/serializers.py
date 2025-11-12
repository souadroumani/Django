import os
from typing import re

from rest_framework import serializers
from .models import Upload

from .validators import validate_file_upload

def  sanitize_filename(value):
    name = os.path.basename(value)
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    return name[:200]
class UploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    file_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Upload
        fields = [
            'id', 'file', 'file_url', 'original_name', 'mime_type',
            'extension', 'size_bytes', 'sha256', 'is_image', 'created_at'
        ]
        read_only_fields = ['id', 'file_url', 'original_name', 'mime_type', 'extension',
                            'size_bytes', 'sha256', 'is_image', 'created_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

    def create(self, validated_data):
        uploaded_file = validated_data.pop('file')
        try:
            meta = validate_file_upload(uploaded_file)
        except ValueError as e:
            raise serializers.ValidationError({"file": str(e)})

        instance = Upload(
            original_name = meta['sanitized_name'],
            extension = meta['extension'],
            mime_type = meta['mime_type'],
            size_bytes = meta['size_bytes'],
            sha256 = meta['sha256'],
            is_image = meta['is_image'],
        )
        uploaded_file.name = meta['sanitized_name']
        instance.file.save(uploaded_file.name, uploaded_file, save=False)
        instance.save()
        return instance
