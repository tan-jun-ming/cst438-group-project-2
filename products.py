import json
import sqlalchemy

import auth
import api
from app import db
from models import Product, Cart


@auth.token_precheck
def add_to_cart(user, product_id, params):
    if not params:
        params= {}
    amount = params.get("amount", 1)
    cart_item = Cart.query.filter_by(user_id=user["id"], product_id=product_id)

    if not cart_item.count():
        cart_item = Cart(product_id, user["id"], amount)
        db.session.add(cart_item)

    else:
        cart_item = cart_item.one()
        cart_item.amount = amount
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return api.error_400("There is no product by that ID.")

    return cart_item.serialize()

@auth.token_precheck
def checkout(user):
    items = Cart.query.filter_by(user_id=user["id"])
    ret = json.dumps([i.serialize() for i in items.all()])
    
    db.session.delete(items).first()

    return ret


@auth.token_precheck
def get_cart(user):
    items = Cart.query.filter_by(user_id=user["id"]).all()

    return json.dumps([i.serialize() for i in items])


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
        return Response(utils.get_traceback(e),status=500, mimetype="text/plain")
        

    return json.dumps(new_product.serialize())