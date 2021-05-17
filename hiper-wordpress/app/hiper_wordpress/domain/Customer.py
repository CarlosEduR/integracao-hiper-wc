from app import db

class Customer(db.Model):
    id_customer = db.Column(db.Integer, db.Sequence('customer_id_customer_seq'), primary_key=True)
    site = db.Column(db.String(100))
    consumer_key = db.Column(db.String(100))
    consumer_secret = db.Column(db.String(100))
    token_hiper = db.Column(db.String(100))
