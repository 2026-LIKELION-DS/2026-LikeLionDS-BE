from django.contrib import admin
from .models import Application, CommonAnswer, PartSpecificAnswer

# Inline으로 공통 답변 표시
class CommonAnswerInline(admin.TabularInline):
    model = CommonAnswer
    extra = 0  # 빈 폼 안 보이게 
    fields = ['question_number', 'answer']
    readonly_fields = ['question_number', 'answer']  # 수정 방지
    can_delete = False

# Inline으로 파트별 답변 표시
class PartSpecificAnswerInline(admin.TabularInline):
    model = PartSpecificAnswer
    extra = 0
    fields = ['question_number', 'answer']
    readonly_fields = ['question_number', 'answer']
    can_delete = False

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'student_id', 'part', 'created_at']
    list_filter = ['part', 'academic_status']
    search_fields = ['name', 'email', 'student_id']
    ordering = ['created_at']
    
    # Inline 추가!
    inlines = [CommonAnswerInline, PartSpecificAnswerInline]
    
    # 상세 페이지 필드 정리
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'phone_number', 'email', 'student_id', 'department', 'academic_status', 'part')
        }),
        ('제출 시간', {
            'fields': ('created_at',),
        }),
    )
    readonly_fields = ['created_at']
