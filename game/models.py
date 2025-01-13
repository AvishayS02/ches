from django.db import models
from users.models import User



class Game(models.Model):
    RESULT_CHOICES = [
        ('White', 'White wins'),
        ('Black', 'Black wins'),
        ('Draw', 'Draw'),
        ('Pending', 'Pending'),
    ]

    white_player = models.ForeignKey(User, related_name='white_games', on_delete=models.CASCADE)
    black_player = models.ForeignKey(User, related_name='black_games', on_delete=models.CASCADE, null=True, blank=True)
    moves = models.TextField(blank=True)  # Store moves in PGN format
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
