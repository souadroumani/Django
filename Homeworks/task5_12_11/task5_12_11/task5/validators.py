# task5/validators.py
import re
import os
import hashlib
from io import BytesIO

import magic
from PIL import Image, UnidentifiedImageError

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.pdf'}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

EXT_TO_FAMILY = {
    '.jpg': 'image',
    '.jpeg': 'image',
    '.png': 'image',
    '.webp': 'image',
    '.pdf': 'application/pdf',
}

FILENAME_SAFE_RE = re.compile(r'[^A-Za-z0-9._-]')

def sanitize_filename(name: str) -> str:
    name = os.path.basename(name)  # drop any path
    name = FILENAME_SAFE_RE.sub('', name)
    return name[:200]

def get_extension(name: str) -> str:
    _, ext = os.path.splitext(name)
    return ext.lower()

def compute_sha256(file_obj) -> str:
    file_obj.seek(0)
    hasher = hashlib.sha256()
    for chunk in iter(lambda: file_obj.read(8192), b''):
        hasher.update(chunk)
    file_obj.seek(0)
    return hasher.hexdigest()

def detect_mime(file_obj) -> str:
    file_obj.seek(0)
    blob = file_obj.read(2048)
    file_obj.seek(0)
    m = magic.Magic(mime=True)
    return m.from_buffer(blob)

def is_pdf_valid(file_obj) -> bool:
    file_obj.seek(0)
    header = file_obj.read(5)
    file_obj.seek(0)
    return header.startswith(b'%PDF-')

def is_image_file(file_obj) -> bool:
    file_obj.seek(0)
    try:
        img = Image.open(file_obj)
        img.verify()
        file_obj.seek(0)
        return True
    except (UnidentifiedImageError, Exception):
        file_obj.seek(0)
        return False

def validate_file_upload(uploaded_file):
    """
    Raise ValueError with human-friendly message on invalid files.
    Returns metadata dict on success.
    """
    # size check
    uploaded_file.seek(0, os.SEEK_END)
    size = uploaded_file.tell()
    uploaded_file.seek(0)
    if size > MAX_SIZE_BYTES:
        raise ValueError(f"File too large. Max allowed is {MAX_SIZE_BYTES} bytes.")

    original_name = getattr(uploaded_file, 'name', 'uploaded')
    sanitized = sanitize_filename(original_name)
    ext = get_extension(sanitized)
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension '{ext}' not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}")

    mime = detect_mime(uploaded_file)
    expected = EXT_TO_FAMILY.get(ext)
    if expected == 'image':
        if not mime.startswith('image'):
            raise ValueError(f"MIME type '{mime}' does not match extension '{ext}'. Expected an image MIME.")
        if not is_image_file(uploaded_file):
            raise ValueError("Uploaded file is not a valid image.")
        is_image = True
    else:
        # pdf
        if not (mime == 'application/pdf' or mime.startswith('application')):
            raise ValueError(f"MIME type '{mime}' does not match PDF.")
        if not is_pdf_valid(uploaded_file):
            raise ValueError("Invalid PDF file (missing %PDF- header).")
        is_image = False

    sha = compute_sha256(uploaded_file)

    return {
        'sanitized_name': sanitized,
        'extension': ext,
        'mime_type': mime,
        'size_bytes': size,
        'sha256': sha,
        'is_image': is_image,
    }
