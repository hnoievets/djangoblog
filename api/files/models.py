from django.db import models

from api.libs.base.base_model import BaseModel


class File(BaseModel):
    class Meta:
        db_table = 'files'

    user = models.ForeignKey(
        'api.User',
        on_delete=models.CASCADE,
        related_name='files'
    )
    original_name = models.CharField(max_length=255, null=True)
    file_key = models.TextField(max_length=255, null=False)
    type = models.IntegerField(null=False, db_comment='1 - avatar')
    is_used = models.BooleanField(default=False, null=False)