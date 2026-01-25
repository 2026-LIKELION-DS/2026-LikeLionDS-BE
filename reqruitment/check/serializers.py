from rest_framework import serializers
from .models import Applicant, InterviewTimeSlot

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['name', 'phone_number', 'email', 'is_passed']

class InterviewTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTimeSlot
        fields = ['id', 'date', 'start_time', 'end_time']