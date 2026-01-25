from django.db import connection, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Applicant, InterviewTimeSlot, ApplicantTimeSlot
from .serializers import InterviewTimeSlotSerializer

class ApplicantStatusView(APIView):
    def post(self, request):
        # 요청 데이터 받기 및 공백 제거
        name = request.data.get('name', "").strip()
        phone_number = request.data.get('phone_number', "").strip().replace("-", "")    # '-' 제거해서 '-' 유무 상관없이 조회가능
        email = request.data.get('email', "").strip()

        # 입력값 검증
        if not all([name, phone_number, email]):
            return Response({
                "status": "fail",
                "message": "이름, 전화번호, 이메일을 모두 입력해주세요.",
                "data": None
            }, status=200)

        # 데이터베이스 조회 - 직접 쿼리로 수행함
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT * FROM check_applicant
                    WHERE name = %s 
                    AND REPLACE(phone_number, '-', '') = %s 
                    AND BINARY email = %s
                """
                cursor.execute(query, [name, phone_number, email])
                result = cursor.fetchone()

            if not result:
                return Response({
                    "status": "fail",
                    "message": "지원자를 찾을 수 없습니다. 입력하신 정보가 맞는지 확인해주세요.",
                    "data": None
                }, status=200)

            # 합/불 반환
            applicant_data = {
                "name": result[1],  # 테이블에서 두 번째 필드 (name)
                "is_passed": result[4],  # 테이블에서 다섯 번째 필드 (is_passed)
                "message": "합격을 축하합니다!" if result[4] else "안타깝게도 불합격하셨습니다."
            }

            return Response({
                "status": "success",
                "message": "조회 성공",
                "data": applicant_data
            }, status=200)

        # 나타나면 안되는 서버오류
        except Exception as e:
            return Response({
                "status": "error",
                "message": "데이터베이스 조회 중 오류가 발생했습니다.",
                "data": None,
                "error": str(e)
            }, status=500)

# 면접 시간 목록 조회
class InterviewSlotListView(APIView):
    def get(self, request):
        slots = InterviewTimeSlot.objects.all().order_by('date', 'start_time')
        serializer = InterviewTimeSlotSerializer(slots, many=True)
        
        return Response({
            "status": "success",
            "message": "면접 시간 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# 면접 시간 선택 및 저장 
class SelectInterviewView(APIView):
    def post(self, request):
        email = request.data.get('email')
        slot_ids = request.data.get('slot_ids')

        if not email or not slot_ids:
            return Response({
                "status": "fail",
                "message": "이메일과 선택한 시간(ID)이 필요합니다.",
            }, status=status.HTTP_400_BAD_REQUEST)

        # 지원자 확인
        try:
            applicant = Applicant.objects.get(email=email)
        except Applicant.DoesNotExist:
            return Response({
                "status": "fail",
                "message": "존재하지 않는 지원자 이메일입니다.",
            }, status=status.HTTP_404_NOT_FOUND)

        # 합격 여부 체크
        if not applicant.is_passed:
            return Response({
                "status": "fail",
                "message": "합격자만 면접 시간을 선택할 수 있습니다.",
            }, status=status.HTTP_403_FORBIDDEN)

        # 수정 불가 체크
        if ApplicantTimeSlot.objects.filter(applicant=applicant).exists():
            return Response({
                "status": "fail",
                "message": "이미 면접 시간을 선택하셨습니다. 수정이 불가능합니다.",
            }, status=status.HTTP_409_CONFLICT)

        # 하나라도 실패하면 전부 취소됨
        try:
            with transaction.atomic():
                for slot_id in slot_ids:
                    slot = get_object_or_404(InterviewTimeSlot, id=slot_id)
                    ApplicantTimeSlot.objects.create(applicant=applicant, time_slot=slot)
                    
        except Exception as e:
            return Response({
                "status": "error",
                "message": "저장 중 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "success",
            "message": "면접 시간이 성공적으로 저장되었습니다."
        }, status=status.HTTP_200_OK)