import auth
from app import db
from models import Cart

@auth.token_precheck
def add_to_cart(user, product_id, params):
    if not params:
        params= {}
    amount = params.get("amount", 1)
    cart_item = Cart.query.filter_by(user_id=user["
    id"], product_id=product_id)

    if not cart_item.count():
        cart_item = Cart(user["id"], product_id, amount)
        db.session.add(cart_item)
    else:
        cart_item = cart_item.one()
        cart_item.amount = amount
    
    db.session.commit()

    return cart_item.serialize()


@auth.token_precheck
@auth.admin_precheck
def add_product(user, params):
    # TODO: add products
    return "add stuff here"