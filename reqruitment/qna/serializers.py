from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question']


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='question.question', read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True, source='question')
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_id','answer']