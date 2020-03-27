import json
import sqlalchemy

import auth
import api
from app import db
from models import Product, Cart


@auth.token_precheck
def add_to_cart(user, product_id, params):
    if not params:
        params = {}
    amount = params.get("amount", 1)
    cart_item = Cart.query.filter_by(user_id=user["id"], product_id=product_id)

    if not cart_item.count():
        if amount == 0:
            return api.error_400("There is no product by that ID.")

        cart_item = Cart(product_id, user["id"], amount)
        db.session.add(cart_item)

    else:
        cart_item = cart_item.one()

        if amount > 0:
            cart_item.amount = amount
        else:
            db.session.delete(cart_item)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return api.error_400("There is no product by that ID.")

    return api.success()


@auth.token_precheck
def checkout(user):
    items = Cart.query.filter_by(user_id=user["id"]).all()

    total_charged = 0
    total_items = 0
    for i in items:
        total_charged += i.product.price * i.amount
        total_items += i.amount
        db.session.delete(i)

    ret = json.dumps(
        {
            "total_charged": total_charged,
            "total_items": total_items,
            "purchased": [i.serialize() for i in items],
        }
    )

    db.session.commit()

    return ret


@auth.token_precheck
def get_cart(user):
    items = Cart.query.filter_by(user_id=user["id"]).all()

    return json.dumps([i.serialize() for i in items])


def get_random_products(amount=25):
    items = Product.query.order_by(sqlalchemy.func.random()).limit(25)

    return json.dumps([i.serialize() for i in items])


# Please set `client_encoding = utf8`
# in your postgresql.conf
def add_products_from_json(fp):
    with open(fp, encoding="utf8") as o:
        data = json.loads(o.read())

    for d in data.values():
        new_product = Product(
            d.get("name"), d.get("desc"), d.get("img"), d.get("price")
        )
        db.session.add(new_product)

    db.session.commit()


@auth.token_precheck
@auth.admin_precheck
def add_product(user, params):
    if not params:
        return api.error_400()

    name = params.get("name")
    details = params.get("details")
    image_url = params.get("image_url")
    price = params.get("price")

    if not name or not price:
        return api.error_400()

    try:
        new_product = Product(name, details, image_url, price)
        db.session.add(new_product)
        db.session.commit()

    except Exception as e:
        return Response(utils.get_traceback(e), status=500, mimetype="text/plain")

    return json.dumps(new_product.serialize())
