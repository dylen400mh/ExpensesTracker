from app import db
from passlib.hash import pbkdf2_sha256

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, password_hash={self.password_hash})>"

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    category = db.Column(db.String)
    date = db.Column(db.Date)

    def __init__(self, amount, description=None, category=None, date=None):
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date

    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, description={self.description}, category={self.category}, date={self.date})>"