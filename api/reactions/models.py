from django.db import models

from api.libs.base.base_model import BaseModel
from api.libs.enums.reaction_type import ReactionType
from api.posts import Post
from api.users import User


class Reaction(BaseModel):
    class Meta:
        db_table = 'reactions'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reactions',
    )
    type = models.IntegerField(choices=ReactionType.choices, db_comment='1 - like, 2 - dislike')

