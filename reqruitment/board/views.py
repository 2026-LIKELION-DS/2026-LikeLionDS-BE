from .models import Board
from .serializers import BoardListSerializer, BoardDetailSerializer, BoardSerializer
from rest_framework import viewsets
from django.conf import settings

import boto3

class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardListSerializer
        elif self.action == 'retrieve':
            return BoardDetailSerializer
        else:
            return BoardSerializer
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        s3_client = boto3.client(
            's3', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        for image in instance.images.all():
            try:
                s3_client.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=image.image.name
                )
            except Exception as e:
                print(f"S3 이미지 삭제 실패: {e}")

        instance.delete()