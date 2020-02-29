from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash

from .extensions import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    currency = db.Column(db.ForeignKey("currency.id"))
    payment = db.Column(db.ForeignKey("payment.id"))
    category = db.Column(db.ForeignKey("category.id"))

    @staticmethod
    def invoices_per_month():
        first_of_month = datetime.today().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        return (
            db.session.query(func.count())
            .filter(Invoice.date > first_of_month)
            .scalar()
        )

    @staticmethod
    def invoices_per_year():
        this_year = datetime.today().year

        return db.session.query(func.count()).filter(Invoice.date > this_year).scalar()

    @staticmethod
    def costs_per_month():
        first_of_month = datetime.today().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        return (
            db.session.query(func.sum(Invoice.value))
            .filter(Invoice.date > first_of_month)
            .scalar()
        )

    @staticmethod
    def costs_per_year():
        this_year = datetime.today().year

        return (
            db.session.query(func.sum(Invoice.value))
            .filter(Invoice.date > this_year)
            .scalar()
        )

    @staticmethod
    def get_costs_by_month():
        costs_by_month = (
            db.session.query(
                func.extract("year", Invoice.date),
                func.extract("month", Invoice.date),
                func.sum(Invoice.value),
            )
            .group_by(
                func.extract("year", Invoice.date), func.extract("month", Invoice.date)
            )
            .all()
        )
        return costs_by_month

    @staticmethod
    def get_costs_by_year():
        costs_by_year = (
            db.session.query(
                func.extract("year", Invoice.date), func.sum(Invoice.value),
            )
            .group_by(func.extract("year", Invoice.date))
            .all()
        )
        return costs_by_year

    @staticmethod
    def get_invoices_by_month():
        invoices_by_month = (
            db.session.query(
                func.extract("year", Invoice.date),
                func.extract("month", Invoice.date),
                func.count(),
            )
            .group_by(
                func.extract("year", Invoice.date), func.extract("month", Invoice.date)
            )
            .all()
        )
        return invoices_by_month

    @staticmethod
    def get_invoices_by_year():
        invoices_by_year = (
            db.session.query(func.extract("year", Invoice.date), func.count(),)
            .group_by(func.extract("year", Invoice.date))
            .all()
        )
        return invoices_by_year


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    email_address = db.Column(db.String(100))
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError("Cannot view password")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
