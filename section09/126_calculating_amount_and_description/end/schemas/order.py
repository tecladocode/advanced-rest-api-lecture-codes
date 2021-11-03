from ma import ma
from models.order import OrderModel


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        load_instance = True
        load_only = ("token",)
        dump_only = ("id", "status",)
