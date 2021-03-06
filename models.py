from app import db
from sqlalchemy.orm import backref

class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    password_hash = db.Column(db.LargeBinary())
    password_salt = db.Column(db.LargeBinary())
    oldest_valid_timestamp = db.Column(db.TIMESTAMP())
    is_admin = db.Column(db.Boolean())

    # cart = db.relationship("Cart", cascade='all, delete-orphan', backref='user')

    def __init__(self, username, first_name, last_name, password_hash, password_salt, oldest_valid_timestamp):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.password_salt = password_salt
        self.oldest_valid_timestamp = oldest_valid_timestamp
        self.is_admin = False

    def __repr__(self):
        return '<id {}>'.format(self.user_id)    

    def serialize(self):
        return {
            'id': self.user_id, 
            'username': self.username,
            'first_name': self.first_name,
            'last_name':self.last_name, 
            'oldest_valid_timestamp': self.oldest_valid_timestamp.timestamp(),
            'is_admin': self.is_admin
        }

class Product(db.Model):
    __tablename__ = "product"

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    details = db.Column(db.String())
    image_url = db.Column(db.String())
    price = db.Column(db.Float())

    # cart = db.relationship("Cart", cascade='all, delete-orphan', backref='product')

    def __init__(self, name, details, image_url, price):
        self.name = name
        self.details = details
        self.image_url = image_url
        self.price = price

    def __repr__(self):
        return '<id {}>'.format(self.product_id)    

    def serialize(self):
        return {
            'id': self.product_id, 
            'name': self.name,
            'details': self.details,
            'image_url':self.image_url, 
            'price': self.price
        }

class Cart(db.Model):
    __tablename__ = "cart"

    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    amount = db.Column(db.Integer)

    product = db.relationship("Product", backref=backref("cart", cascade="all,delete"))
    user = db.relationship("User", backref=backref("cart", cascade="all,delete"))

    def __init__(self, product_id, user_id, amount):
        self.product_id = product_id
        self.user_id = user_id
        self.amount = amount 

    def serialize(self):
        return {
            'product': self.product.serialize(),
            'amount': self.amount
        }





