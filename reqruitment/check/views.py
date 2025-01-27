from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


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
                    SELECT * FROM applicant 
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
