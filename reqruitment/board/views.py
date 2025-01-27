from .models import Board
from .serializers import BoardListSerializer, BoardDetailSerializer, BoardSerializer
from rest_framework import viewsets

class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardListSerializer
        elif self.action == 'retrieve':
            return BoardDetailSerializer
        else:
            return BoardSerializer
    
    def perform_create(self, serializer):
        print("Request Data:", self.request.data) 
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()