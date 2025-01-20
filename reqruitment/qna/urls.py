from django.urls import path
from .views import QuestionView, AnswerView

urlpatterns = [
    path('question/', QuestionView.as_view({'get':'list', 'post':'create'}), name = 'question'),
    path('answer/', AnswerView.as_view({'get':'list'}), name='answer_list'),
    path('answer/reply/<int:question_id>/', AnswerView.as_view({'post':'create'}), name='answer_create'),
    path('answer/manage/<int:answer_id>/', AnswerView.as_view({'patch':'update', 'delete':'destroy'}), name='answer_edit')
]