from django.db import models

class Question(models.Model):
    question = models.CharField(max_length=300)

    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey('qna.Question', on_delete=models.CASCADE, null=False, blank=False, related_name='question_id')
    answer = models.CharField(max_length=300)

    def __str__(self):
        return self.answer