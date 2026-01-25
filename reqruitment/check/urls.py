from django.urls import path
from .views import ApplicantStatusView, InterviewSlotListView, SelectInterviewView

urlpatterns = [
    path('babylions/', ApplicantStatusView.as_view(), name='applicant_status'),  # 합격 여부 조회
    path('slots/', InterviewSlotListView.as_view(), name='interview_slots'), # 면접 시간 목록 조회
    path('select/', SelectInterviewView.as_view(), name='select_interview'), # 면접 시간 저장
]