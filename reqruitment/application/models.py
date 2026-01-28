from django.db import models

class Application(models.Model):
    PART_CHOICES = [
        ('FE', '프론트엔드'),
        ('BE', '백엔드'),
        ('PD', '기획/디자인'),
    ]

    name = models.CharField(max_length=100)  # 이름
    phone_number = models.CharField(max_length=20)  # 전화번호
    email = models.EmailField(unique=True)  # 이메일
    student_id = models.CharField(max_length=20)  # 학번
    department = models.CharField(max_length=100)  # 학과
    academic_status = models.CharField(max_length=20) #학년/재학여부
    part = models.CharField(max_length=2, choices=PART_CHOICES)  # 지원 파트
    created_at = models.DateTimeField(auto_now_add=True)  # 제출일시

    def __str__(self):
        return f"{self.name} - {self.get_part_display()}"

class CommonAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='common_answers')
    question_number = models.IntegerField()  # 문항 번호 (1~7)
    answer = models.TextField()  # 답변

    class Meta:
        unique_together = ['application', 'question_number']

    def __str__(self):
        return f"{self.application.name} - 공통문항 {self.question_number}"

class PartSpecificAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='part_answers')
    question_number = models.IntegerField()  # 문항 번호
    answer = models.TextField()  # 답변

    class Meta:
        unique_together = ['application', 'question_number']

    def __str__(self):
        return f"{self.application.name} - 파트문항 {self.question_number}"
