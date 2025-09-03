from django.db import models

class ReactionType(models.IntegerChoices):
    LIKE = 1, 'Like'
    DISLIKE = 2, 'Dislike'