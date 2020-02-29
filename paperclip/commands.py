import click

from faker import Faker
from random import randint, choice, uniform, randrange
from datetime import timedelta, datetime
from flask.cli import with_appcontext
from sqlalchemy.sql import func

from .extensions import db
from .models import Category, Currency, Invoice, Payment, User

fake = Faker()


@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()


@click.command(name="create_currencies")
@with_appcontext
def create_currencies():
    pln = Currency(name="PLN")
    usd = Currency(name="USD")
    eur = Currency(name="EUR")

    db.session.add_all([pln, usd, eur])
    db.session.commit()


@click.command(name="create_payments")
@with_appcontext
def create_payments():
    credit_card = Payment(name="Credit Card")
    cash = Payment(name="Cash")
    own_resource = Payment(name="Own Resource")
    transfer = Payment(name="Transfer")
    other = Payment(name="Other")

    db.session.add_all([credit_card, cash, own_resource, transfer, other])
    db.session.commit()


@click.command(name="create_categories")
@with_appcontext
def create_categories():
    hotel_service = Category(name="Hotel Service")
    catering_service = Category(name="Catering Service")
    marketing_service = Category(name="Marketing Service")
    fuel = Category(name="Fuel")
    parking = Category(name="Parking")
    car_wash = Category(name="Car Wash")
    car_renovation = Category(name="Car Renovation")
    other = Category(name="Other")

    db.session.add_all(
        [
            hotel_service,
            catering_service,
            marketing_service,
            fuel,
            parking,
            car_wash,
            car_renovation,
            other,
        ]
    )
    db.session.commit()


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


@click.command(name="create_invoices")
@with_appcontext
def create_invoices():

    currencies = Currency.query.all()
    payments = Payment.query.all()
    categories = Category.query.all()

    for _ in range(100):

        random_value = round(uniform(0.00, 400.00), 2)

        # d1 = datetime.strptime("1/1/2018", "%d/%m/%Y")
        # d2 = datetime.strptime("28/2/2020", "%d/%m/%Y")
        # random_date_values = random_date(d1, d2)

        random_date = fake.date_time_between(start_date="-500d", end_date="now")

        random_name = (
            "FV/"
            + fake.credit_card_expire(start="-1000d", end="now", date_format="%y/%m/")
            + fake.numerify(text="###")
        )

        random_description = fake.catch_phrase()

        random_currency = choice(currencies)
        random_payment = choice(payments)
        random_category = choice(categories)

        invoice = Invoice(
            value=random_value,
            date=random_date,
            name=random_name,
            description=random_description,
            currency=1,
            payment=random_payment.id,
            category=random_category.id,
        )

        db.session.add(invoice)

    db.session.commit()


@click.command(name="test_query")
@with_appcontext
def test_query():
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
    print(costs_by_month)

    costs_this_year = (
        db.session.query(func.extract("year", Invoice.date), func.sum(Invoice.value),)
        .group_by(func.extract("year", Invoice.date))
        .all()
    )
    # print(costs_this_year)

    invoices_this_month = (
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
    # print(invoices_this_month)

    invoices_this_year = (
        db.session.query(func.extract("year", Invoice.date), func.count(),)
        .group_by(func.extract("year", Invoice.date))
        .all()
    )
    print(invoices_this_year)

    costs_by_month_req = (
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
    # for cost in costs_by_month_req:
    # print(cost)
