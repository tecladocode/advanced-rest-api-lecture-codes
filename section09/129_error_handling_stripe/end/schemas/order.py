from ma import ma
from models.order import OrderModel


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = OrderModel
        load_only = ("token",)
        dump_only = ("id", "status",)
