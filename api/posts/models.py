from django.db import models

from api.libs.base.base_model import BaseModel
from api.users import User


class Post(BaseModel):
    class Meta:
        db_table = 'posts'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(max_length=10000, null=False)
    views = models.PositiveIntegerField(default=0, null=False)

