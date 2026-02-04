from django.contrib import admin
from .models import Applicant, InterviewTimeSlot, ApplicantTimeSlot

admin.site.register(Applicant)
admin.site.register(ApplicantTimeSlot)

# 커스텀 필터: 파트별 필터링
class PartFilter(admin.SimpleListFilter):
    title = '파트'
    parameter_name = 'part'

    def lookups(self, request, model_admin):
        return [
            ('FE', '프론트엔드'),
            ('BE', '백엔드'),
            ('PD', '기획/디자인'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            # 해당 파트 지원자가 선택한 시간대만 필터링
            return queryset.filter(
                applicants__applicant__application__part=self.value()
            ).distinct()
        return queryset


# 면접 시간대 관리 - 파트별 + 시간대별 필터링
@admin.register(InterviewTimeSlot)
class InterviewTimeSlotAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'formatted_slot',
        'date',
        'start_time',
        'end_time',
        'applicant_count'
    ]
    
    # 파트 → 날짜 → 시간대 순서로 필터링
    list_filter = [
        PartFilter,           # 파트 필터 (커스텀)
        'date',               # 날짜 필터
        'start_time',         # 시간대 필터
    ]
    
    ordering = ['date', 'start_time']
    search_fields = ['date', 'start_time']
    
    def formatted_slot(self, obj):
        return f"{obj.date} {obj.start_time.strftime('%H:%M')}~{obj.end_time.strftime('%H:%M')}"
    formatted_slot.short_description = '시간대'
    
    def applicant_count(self, obj):
        return obj.applicants.count()
    applicant_count.short_description = '신청 인원'