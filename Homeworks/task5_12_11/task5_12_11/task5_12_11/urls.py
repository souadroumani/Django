

#task5\urls.py

"""
URL configuration for task5_12_11 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from task5.views import UploadListView, UploadDetailView, UploadCreateView , home
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # POST to create, GET to list are under the /api/uploads/ and /api/uploads/new/
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('uploads/', UploadListView.as_view(), name='upload-list'),
    path('uploads/<int:pk>/', UploadDetailView.as_view(), name='upload-detail'),
    path('uploads/new/', UploadCreateView.as_view(), name='upload-create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
