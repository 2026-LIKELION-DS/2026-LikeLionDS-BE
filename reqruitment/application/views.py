from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_class = [AllowAny]  # 누구나 접근 가능