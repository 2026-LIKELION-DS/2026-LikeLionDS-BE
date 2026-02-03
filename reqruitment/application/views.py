from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Application
from .serializers import ApplicationSerializer , SubmissionCheckSerializer, DuplicateCheckSerializer, EmailDuplicateCheckSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_class = [AllowAny]  # 누구나 접근 가능


class SubmissionCheckView(generics.GenericAPIView):
    serializer_class = SubmissionCheckSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        if not serializer.is_valid():
            return Response({
                "status": "fail",
                "message": "입력값을 확인해주세요.",
                "errors": serializer.errors,
                "data": None
            }, status=status.HTTP_200_OK)

        name = serializer.validated_data["name"].strip()
        phone_number = serializer.validated_data["phone_number"].strip().replace("-", "")
        email = serializer.validated_data["email"].strip()

        app = Application.objects.filter(email=email).first()
        if not app:
            return Response({
                "status": "success",
                "message": "제출된 지원서가 없습니다.",
                "data": {"submitted": False}
            }, status=status.HTTP_200_OK)

        normalized_db_phone = (app.phone_number or "").replace("-", "").replace(" ", "")
        if app.name != name or normalized_db_phone != phone_number:
            return Response({
                "status": "success",
                "message": "제출된 지원서가 없습니다. 입력 정보를 확인해주세요.",
                "data": {"submitted": False}
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "success",
            "message": "제출이 완료되었습니다.",
            "data": {"submitted": True, "submitted_at": app.created_at}
        }, status=status.HTTP_200_OK)
        
class DuplicateCheckView(generics.GenericAPIView):
    serializer_class = DuplicateCheckSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "fail",
                "message": "입력값을 확인해주세요.",
                "errors": serializer.errors,
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        # 입력값 정규화
        name = serializer.validated_data["name"].strip()
        phone_number = serializer.validated_data["phone_number"].strip().replace("-", "").replace(" ", "")

        # 이름 + 전화번호로 기존 지원자 조회
        # DB에 저장된 전화번호도 하이픈 제거 후 비교
        applications = Application.objects.filter(name=name)
        
        for app in applications:
            db_phone = app.phone_number.replace("-", "").replace(" ", "")
            if db_phone == phone_number:
                # 중복 발견!
                return Response({
                    "status": "success",
                    "message": "이미 지원서를 제출한 지원자입니다.",
                    "data": {
                        "is_duplicate": True,
                        "applicant": {
                            "name": app.name,
                            "email": app.email,
                            "part": app.get_part_display(),
                            "submitted_at": app.created_at
                        }
                    }
                }, status=status.HTTP_200_OK)
        
        # 중복 없음
        return Response({
            "status": "success",
            "message": "신규 지원자입니다.",
            "data": {
                "is_duplicate": False
            }
        }, status=status.HTTP_200_OK)

class EmailDuplicateCheckView(generics.GenericAPIView):
    serializer_class = EmailDuplicateCheckSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "fail",
                "message": "입력값을 확인해주세요.",
                "errors": serializer.errors,
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data["email"].strip()
        
        # 이메일 중복 확인
        is_duplicate = Application.objects.filter(email=email).exists()
        
        return Response({
            "status": "success",
            "message": "이메일 중복 확인 완료",
            "data": {
                "is_duplicate": is_duplicate
            }
        }, status=status.HTTP_200_OK)