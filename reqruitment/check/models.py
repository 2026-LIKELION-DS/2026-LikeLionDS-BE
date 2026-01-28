from django.db import models
from application.models import Application

class Applicant(models.Model):
    application = models.OneToOneField(
        Application, 
        on_delete=models.CASCADE, 
        related_name='pass_status',
        verbose_name='지원서'
        )
    
    is_passed = models.BooleanField(default=False, verbose_name='합격 여부')
    
    @property
    def name(self):
        return self.application.name
    
    @property
    def email(self):
        return self.application.email

    def __str__(self):
        return f"{self.application.name}({self.application.get_part_display()}/{self.application.student_id}) - {'합격' if self.is_passed else '불합격'}"
    
class InterviewTimeSlot(models.Model):
    date = models.DateField()  # 면접 날짜
    start_time = models.TimeField()  # 시작 시간
    end_time = models.TimeField()  # 종료 시간

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.date} {self.start_time.strftime('%H:%M')}~{self.end_time.strftime('%H:%M')}"

class ApplicantTimeSlot(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='selected_times')
    time_slot = models.ForeignKey(InterviewTimeSlot, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(auto_now_add=True)  # 선택일시

    class Meta:
        unique_together = ['applicant', 'time_slot']

    def __str__(self):
        return f"{self.applicant.name} - {self.time_slot}"
