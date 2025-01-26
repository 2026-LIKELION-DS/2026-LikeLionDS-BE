from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class BoardImage(models.Model):
    board = models.ForeignKey(Board, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='board_images/')
    
    def __str__(self):
        return f"{self.board.title}"