from rest_framework import serializers
from .models import Application, CommonAnswer, PartSpecificAnswer


class CommonAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonAnswer
        fields = ['question_number', 'answer']

class PartSpecificAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartSpecificAnswer
        fields = ['question_number', 'answer']

class ApplicationSerializer(serializers.ModelSerializer):
    common_answers = CommonAnswerSerializer(many=True)
    part_answers = PartSpecificAnswerSerializer(many=True)

    class Meta:
        model = Application
        fields = [
            'id', 'name', 'phone_number', 'email', 'student_id', 
            'department','academic_status', 'part', 'common_answers', 'part_answers'
        ]

    def create(self, validated_data):
        # 1. 답변 데이터를 따로 추출
        common_answers_data = validated_data.pop('common_answers')
        part_answers_data = validated_data.pop('part_answers')

        # 2. 지원서 본체 저장
        application = Application.objects.create(**validated_data)

        # 3. 추출한 데이터를 반복문으로 각각 저장
        for answer_data in common_answers_data:
            CommonAnswer.objects.create(application=application, **answer_data)
        
        for answer_data in part_answers_data:
            PartSpecificAnswer.objects.create(application=application, **answer_data)

        return application
    


class SubmissionCheckSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()

class DuplicateCheckSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=20)
    
class EmailDuplicateCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)