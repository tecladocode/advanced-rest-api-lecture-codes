from ma import ma
from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_instance = True
        load_only = ("user",)
        dump_only = ("id", "expired_at", "confirmed")
        include_fk = True
