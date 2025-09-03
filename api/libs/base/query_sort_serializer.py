from rest_framework import serializers

from api.libs.helpers import get_choices_from_enum
from api.libs.resources.common.order_type import OrderType


class QuerySortSerializer(serializers.Serializer):
    sort = serializers.ChoiceField(
        required=False,
        allow_null=False,
        choices=[('id', 'id')],
        default='id'
    )
    order = serializers.ChoiceField(
        required=False,
        allow_null=False,
        choices=get_choices_from_enum(OrderType),
        default=OrderType.DESC,
    )

    def __init__(self, *args, sort_choices=None, default_sort_field='id', default_order=OrderType.DESC, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['sort'].default = default_sort_field
        self.fields['order'].default = default_order

        if sort_choices:
            self.fields['sort'].choices = sort_choices
