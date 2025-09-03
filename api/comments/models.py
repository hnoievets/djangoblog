from django.db import models

from api.libs.base.base_model import BaseModel
from api.libs.resources.comments.validation_rule import CommentsValidationRule
from api.posts import Post
from api.users import User


class Comment(BaseModel):
    class Meta:
        db_table = 'comments'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(null=True, max_length=CommentsValidationRule.TEXT_MAX_LENGTH)

