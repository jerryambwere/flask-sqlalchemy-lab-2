from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reviews = db.relationship('Review', back_populates='customer')

    # Use association proxy to get items directly
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def serialize(self):
        # Serializing the customer, including the associated items (via association proxy)
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.serialize() for item in self.items]  # Serialize the items
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def serialize(self):
        # Serializing the item, excluding reviews to prevent recursion
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.serialize() for review in self.reviews]  # Serialize the reviews
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.ForeignKey('customers.id'))
    item_id = db.Column(db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

    def serialize(self):
        # Serializing the review, excluding reverse relationships to prevent recursion
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'customer': self.customer.serialize() if self.customer else None,  # Avoid recursion
            'item': self.item.serialize() if self.item else None  # Avoid recursion
        }
