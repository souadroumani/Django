
# Create your views here.
from django.shortcuts import render
from rest_framework import generics, permissions, throttling , pagination
from .models import Upload
from .serializers import UploadSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Task5 API")

#  Throttling settings
class AnonRateThrottle(throttling.AnonRateThrottle):
    rate = '10/min'

class UserRateThrottle(throttling.UserRateThrottle):
    rate = '60/min'


#  POST
class UploadCreateView(generics.CreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]


# GET
class UploadListView(generics.ListAPIView):
    queryset = Upload.objects.all().order_by('-id')
    serializer_class = UploadSerializer
    pagination_class = pagination

# GET /api/uploads/<id>/
class UploadDetailView(generics.RetrieveAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
