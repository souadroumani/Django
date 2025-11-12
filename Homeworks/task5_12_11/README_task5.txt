# 🗂️ File Upload API – Task 5

مشروع Django REST Framework لرفع الملفات (صور أو PDF) مع استخراج معلومات عنها :


---

##  المتطلبات

تثبيت المتطلبات التالية:

```bash
pip install django djangorestframework python-magic Pillow
```

> **ملاحظات مهمة**
> - مكتبة `python-magic` تستخدم لتحليل نوع الملف MIME.
> - مكتبة `Pillow` ضرورية لاكتشاف الصور والتحقق منها.
> - إذا واجهت مشكلة في `magic` على Windows، ثبّت:
>   ```bash
>   pip install python-magic-bin
>   ```

---

##  خطوات التشغيل محليًا

1. **استنساخ المشروع** أو انسخ الملفات لمجلدك المحلي.
2. من داخل مجلد المشروع (الذي يحتوي على `manage.py`)، نفّذ الأوامر التالية:

```bash
# إنشاء قاعدة البيانات
python manage.py makemigrations
python manage.py migrate

# إنشاء مستخدم إداري لتسجيل الدخول للوحة الإدارة
python manage.py createsuperuser

# تشغيل الخادم المحلي
python manage.py runserver
```

3. افتح المتصفح على:
   - **واجهة الإدارة:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - **الصفحة الرئيسية (Home):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **API الرفع:** [http://127.0.0.1:8000/uploads/new/](http://127.0.0.1:8000/uploads/new/)

---

##  المتطلبات الأمنية

رفع الملفات عبر واجهة API يتطلب تسجيل الدخول (`IsAuthenticated`).  
لذلك قبل الرفع، يجب إنشاء مستخدم وتسجيل الدخول باستخدام توكن أو عبر واجهة تسجيل الدخول الافتراضية.

---

##  المميزات

- التحقق من حجم الملف (حتى 10 ميغابايت)
- دعم الامتدادات التالية: `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`
- استخراج:
  - الاسم الأصلي للملف  
  - نوع الامتداد  
  - MIME Type  
  - الحجم بالبايت  
  - SHA256 Hash  
  - هل الملف صورة أم لا  
- تخزين الملفات داخل مجلد `media/uploads/`

---

##  أمثلة CURL

### 1رفع ملف (مع مصادقة)

```bash
curl -X POST http://127.0.0.1:8000/uploads/new/   -H "Authorization: Basic <base64encoded_user:pass>"   -F "file=@C:/path/to/image.png"
```
(.venv) C:\Users\HP\Desktop\vs\Django\Tasks\task5_12_11>curl -X POST -u admin:1234 -F "file=@C:\Users\HP\Desktop\vs\Django\Session 9 - Authentication & Authorization.pdf" http://127.0.0.1:8000/api/uploads/new/ {"id":5,"file_url":"http://127.0.0.1:8000/media/uploads/Session9-AuthenticationAuthorization.pdf","original_name":"Session9-AuthenticationAuthorization.pdf","mime_type":"application/pdf","extension":".pdf","size_bytes":8690903,"sha256":"35a6778b9f86d25e7cedd7ec9992172e3bcbb40183f97933dc9102d7cbf3f7f0","is_image":false,"created_at":"2025-11-11T17:57:18.179243Z"}
---

### 2️ عرض جميع الملفات )
```bash
curl http://127.0.0.1:8000/uploads/
```
(.venv) C:\Users\HP\Desktop\vs\Django\Tasks\task5_12_11>curl -u admin:1234 http://127.0.0.1:8000/api/uploads/ [{"id":7,"file_url":"http://127.0.0.1:8000/media/uploads/download.jpg","original_name":"","mime_type":"","extension":"","size_bytes":12271,"sha256":"","is_image":false,"created_at":"2025-11-11T18:00:27.452607Z"},{"id":6,"file_url":"http://127.0.0.1:8000/media/uploads/photo_2025-09-17_13-29-09.jpg","original_name":"photo_2025-09-17_13-29-09.jpg","mime_type":"image/jpeg","extension":".jpg","size_bytes":87171,"sha256":"a4ae16dd82a9021d2297dc59fafa2a512fedffb8ec6ef3e20e950c9897de1831","is_image":true,"created_at":"2025-11-11T17:59:26.934396Z"},{"id":5,"file_url":"http://127.0.0.1:8000/media/uploads/Session9-AuthenticationAuthorization.pdf","original_name":"Session9-AuthenticationAuthorization.pdf","mime_type":"application/pdf","extension":".pdf","size_bytes":8690903,"sha256":"35a6778b9f86d25e7cedd7ec9992172e3bcbb40183f97933dc9102d7cbf3f7f0","is_image":false,"created_at":"2025-11-11T17:57:18.179243Z"},{"id":4,"file_url":"http://127.0.0.1:8000/media/uploads/%D8%A8%D8%A8%D8%A8%D8%A8%D8%A8%D8%A8.jpg","original_name":"","mime_type":"","extension":"","size_bytes":51649,"sha256":"","is_image":false,"created_at":"2025-11-11T12:33:02.190628Z"},{"id":3,"file_url":"http://127.0.0.1:8000/media/uploads/Gemini_Generated_Image_xu42j3xu42j3xu42.png","original_name":"","mime_type":"","extension":"","size_bytes":1126661,"sha256":"","is_image":false,"created_at":"2025-11-11T12:32:45.298200Z"},{"id":2,"file_url":"http://127.0.0.1:8000/media/uploads/Session_5_-_Databases_SeIqLO1.pdf","original_name":"","mime_type":"","extension":"","size_bytes":4004893,"sha256":"","is_image":false,"created_at":"2025-11-11T12:31:31.823631Z"},{"id":1,"file_url":"http://127.0.0.1:8000/media/uploads/Session_6_-_Django_1dMsfK4.pdf","original_name":"","mime_type":"","extension":"","size_bytes":2073034,"sha256":"","is_image":false,"created_at":"2025-11-11T12:21:45.437641Z"}]
---

### 3️ عرض تفاصيل ملف حسب المعرف (ID)
```bash
curl http://127.0.0.1:8000/uploads/1/
```
(.venv) C:\Users\HP\Desktop\vs\Django\Tasks\task5_12_11>curl -u admin:1234 http://127.0.0.1:8000/uploads/5/
{"id":5,"file_url":"http://127.0.0.1:8000/media/uploads/Session9-AuthenticationAuthorization.pdf","original_name":"Session9-AuthenticationAuthorization.pdf","mime_type":"application/pdf","extension":".pdf","size_bytes":8690903,"sha256":"35a6778b9f86d25e7cedd7ec9992172e3bcbb40183f97933dc9102d7cbf3f7f0","is_image":false,"created_at":"2025-11-11T17:57:18.179243Z"}
---

##  بنية المشروع

```
task5_12_11/
│
├── manage.py
├── task5/                ← التطبيق الأساسي
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── validators.py
│   ├── admin.py
│   └── ...
│
├── task5_12_11/          ← إعدادات المشروع
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── media/uploads/        ← ملفات الرفع
```

---

##  مثال بعد الرفع

عند رفع صورة عبر الـ API أو لوحة الإدارة، ستحصل على نتيجة مشابهة:

```json
{
  "id": 3,
  "file_url": "http://127.0.0.1:8000/media/uploads/cat1_UKey2Ej.png",
  "original_name": "cat1.png",
  "mime_type": "image/png",
  "extension": ".png",
  "size_bytes": 5908,
  "sha256": "8f5e1e7e8b2d5d3d9c1f...",
  "is_image": true,
  "created_at": "2025-11-12T19:23:00Z"
}
```

---

##  
- الملفات المرفوعة تُحفظ داخل `media/uploads/`.

---

##  المطور

مشروع تم إنشاؤه كجزء من **مهمة Django REST Framework - Task 5**  
بواسطة: **Soaud Roumane**
