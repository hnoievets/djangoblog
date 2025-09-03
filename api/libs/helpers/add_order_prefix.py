from api.libs.resources.common.order_type import OrderType

def add_order_prefix(filed: str, order_type: OrderType) -> str:
    if order_type == OrderType.ASC:
        return filed

    return '-' + filed