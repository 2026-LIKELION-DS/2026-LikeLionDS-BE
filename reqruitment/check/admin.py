from django.contrib import admin
from .models import Applicant, InterviewTimeSlot, ApplicantTimeSlot

admin.site.register(Applicant)
admin.site.register(InterviewTimeSlot)


# 면접 시간 신청 현황 - 파트별 + 시간대별 필터링
@admin.register(ApplicantTimeSlot)
class ApplicantTimeSlotAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'time_slot', 'created_at']
    
    list_filter = [
        'applicant__application__part',  # 파트 필터 (FE/BE/PD)
        'time_slot',                      # 시간대 필터
    ]
    
    search_fields = ['applicant__application__name', 'applicant__application__email']
    ordering = ['time_slot__date', 'time_slot__start_time', 'applicant__application__name']