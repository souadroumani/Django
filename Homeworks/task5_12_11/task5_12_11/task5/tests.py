from django.test import TestCase

# Create your tests here.
# task5/tests.py
import io
import hashlib
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Upload
from PIL import Image

User = get_user_model()

def make_pdf_bytes():
    return b"%PDF-1.4\n%...\n%%EOF\n"

def make_jpeg_bytes():
    buf = io.BytesIO()
    img = Image.new('RGB', (10, 10), color='red')
    img.save(buf, format='JPEG')
    buf.seek(0)
    return buf.read()

class UploadTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='pass')
        self.client = APIClient()

    def test_upload_requires_auth(self):
        url = reverse('upload-list')
        pdf = io.BytesIO(make_pdf_bytes())
        pdf.name = 'doc.pdf'
        resp = self.client.post(url, {'file': pdf}, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_pdf_success(self):
        self.client.force_authenticate(self.user)
        url = reverse('upload-list')
        pdf = io.BytesIO(make_pdf_bytes())
        pdf.name = 'doc.pdf'
        resp = self.client.post(url, {'file': pdf}, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertIn('sha256', data)
        pdf.seek(0)
        expected = hashlib.sha256(pdf.read()).hexdigest()
        self.assertEqual(data['sha256'], expected)

    def test_upload_image_success(self):
        self.client.force_authenticate(self.user)
        url = reverse('upload-list')
        img_bytes = make_jpeg_bytes()
        img = io.BytesIO(img_bytes)
        img.name = 'pic.jpg'
        resp = self.client.post(url, {'file': img}, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resp.json()['is_image'])

    def test_reject_large_file(self):
        self.client.force_authenticate(self.user)
        url = reverse('upload-list')
        big = io.BytesIO(b'0' * (10 * 1024 * 1024 + 1))
        big.name = 'big.pdf'
        resp = self.client.post(url, {'file': big}, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_extension(self):
        self.client.force_authenticate(self.user)
        url = reverse('upload-list')
        f = io.BytesIO(b'hello')
        f.name = 'bad.exe'
        resp = self.client.post(url, {'file': f}, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mime_mismatch(self):
        self.client.force_authenticate(self.user)
        url = reverse('upload-list')
        b = io.BytesIO(make_pdf_bytes())
        b.name = 'fake.jpg'
        resp = self.client.post(url, {'file': b}, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_pagination(self):
        self.client.force_authenticate(self.user)
        url = reverse('upload-list')
        for i in range(15):
            f = io.BytesIO(make_jpeg_bytes())
            f.name = f'img{i}.jpg'
            self.client.post(url, {'file': f}, format='multipart')
        resp = self.client.get(url + '?page=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json()
        self.assertIn('results', body)
