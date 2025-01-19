from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request):
        questions = self.get_queryset()
        result = []

        for question in questions:
            answers = question.question_id.all()
            result.append({
                "id": question.id,
                "question": question.question,
                "answers": [answer.answer for answer in answers] if answers.exists() else "운영진이 질문을 확인하고 답변을 달아줘요."
            })

        return Response(
            {"message": "질문 조회에 성공하였습니다.", "result": result},
            status=status.HTTP_200_OK
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "질문 생성에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "질문 생성에 실패했습니다.", "result": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    
    def list(self, request):
        questions = Question.objects.all().order_by('-id')
        result = []

        for question in questions:
            answers = question.question_id.all() 
            if answers.exists():
                for answer in answers:
                    result.append({
                        "id": answer.id,
                        "question": question.question,
                        "answer": answer.answer
                    })
            else:
                result.append({
                    "id": None,
                    "question": question.question,
                })

        return Response(
            {"message": "답변 조회에 성공하였습니다.", "result": result},
            status=status.HTTP_200_OK
        )

    def create(self, request, question_id=None):
        question = get_object_or_404(Question, pk=question_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response({"message": "답변 생성에 성공했습니다.", "result": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "답변 생성에 실패했습니다.", "result": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, answer_id=None):
        answer = get_object_or_404(Answer, pk=answer_id)
        serializer = AnswerSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "답변 수정에 성공했습니다.", "result": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "답변 수정에 실패했습니다.", "result": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, answer_id=None):
        answer = get_object_or_404(Answer, pk=answer_id)
        answer.delete()
        return Response({"message": "답변 삭제에 성공했습니다."}, status=status.HTTP_200_OK)
