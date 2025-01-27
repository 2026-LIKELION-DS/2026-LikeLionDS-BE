from django.urls import path
from .views import ApplicantStatusView

urlpatterns = [
    path('babylions/', ApplicantStatusView.as_view(), name='applicant_status'),  # 합격 여부 조회
]