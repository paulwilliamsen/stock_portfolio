from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    symbol = db.Column(db.String(256), index=True, unique=True)


    def __repr__(self):
        return '<Company {}-{}>'.format(self.name, self.symbol)

class Portfolio(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)

    company = db.relationship('Company', backref='category', lazy=True)


    def __repr__(self):
        return '<Category {}>'.format(self.name)