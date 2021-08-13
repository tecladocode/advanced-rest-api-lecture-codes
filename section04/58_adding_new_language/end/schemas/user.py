from marshmallow import pre_dump

from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")

        @pre_dump
        def _pre_dump(self, user: UserModel):
            user.confirmation = [user.most_recent_confirmation]
            return user
