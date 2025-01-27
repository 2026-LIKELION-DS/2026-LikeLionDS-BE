from django.db import models

class Applicant(models.Model):
    name = models.CharField(max_length=100)  # 이름
    phone_number = models.CharField(max_length=20)  # 전화번호
    email = models.EmailField(max_length=255, unique=True)  # 이메일
    is_passed = models.BooleanField()  # 합격 여부 (True/False)

    def __str__(self):
        return f"{self.name} - {'합격' if self.is_passed else '불합격'}"
