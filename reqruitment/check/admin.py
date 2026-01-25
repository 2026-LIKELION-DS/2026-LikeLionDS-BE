from django.contrib import admin
from .models import Applicant, InterviewTimeSlot, ApplicantTimeSlot

# Register your models here.
admin.site.register(Applicant)
admin.site.register(InterviewTimeSlot)
admin.site.register(ApplicantTimeSlot)