from collections import Counter
from flask import request
from flask_restful import Resource

from libs.strings import gettext
from models.item import ItemModel
from models.order import OrderModel, ItemsInOrder


class Order(Resource):

    @classmethod
    def post(cls):
        """
        Expect a token and a list of item ids from the request body.
        Construct an order and talk to the Strip API to make a charge.
        """
        data = request.get_json()  # token + list of item ids  [1, 2, 3, 5, 5, 5]
        items = []
        item_id_quantities = Counter(data["item_ids"])

        # Iterate over items and retrieve them from the database
        for _id, count in item_id_quantities.most_common():
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message": gettext("order_item_by_id_not_found").format(_id)}, 404

            items.append(ItemsInOrder(item_id=_id, quantity=count))

        order = OrderModel(items=items, status="pending")
        order.save_to_db()  # this does not submit to Stripe

        order.set_status("something")