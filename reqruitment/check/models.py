from django.db import models

class Applicant(models.Model):
    name = models.CharField(max_length=100)  # 이름
    phone_number = models.CharField(max_length=20)  # 전화번호
    email = models.EmailField(max_length=255, unique=True)  # 이메일
    is_passed = models.BooleanField()  # 합격 여부 (True/False)

    def __str__(self):
        return f"{self.name} - {'합격' if self.is_passed else '불합격'}"

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
