from django.urls import path
from .views import ApplicationCreateView , SubmissionCheckView

urlpatterns = [
    path('', ApplicationCreateView.as_view(), name='application-create'),
    path("check-submission/", SubmissionCheckView.as_view(), name="check-submission"),
]