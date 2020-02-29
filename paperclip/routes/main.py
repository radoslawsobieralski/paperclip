from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import asc, desc

from paperclip.models import Invoice, Currency, Payment, Category
from paperclip.extensions import db


main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@login_required
def index():

    this_month = datetime.today().month
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    last_12_months = months[this_month:] + months[:this_month]
    last_6_months = last_12_months[-6:]

    invoices = Invoice.query.all()
    invoices_newest_10_desc = Invoice.query.order_by(desc(Invoice.date)).limit(10).all()
    currencies = Currency.query.all()
    payments = Payment.query.all()
    categories = Category.query.all()

    costs_by_month = Invoice.get_costs_by_month()
    costs_by_year = Invoice.get_costs_by_year()
    invoices_by_month = Invoice.get_invoices_by_month()
    invoice_by_year = Invoice.get_invoices_by_year()

    costs_per_month = Invoice.costs_per_month()
    costs_per_year = Invoice.costs_per_year()
    invoices_per_month = Invoice.invoices_per_month()
    invoices_per_year = Invoice.invoices_per_year()

    invoices_monthly_array = [invoice[1] for invoice in invoices_by_month[-12:]]
    costs_monthly_array = [round(cost[2], 2) for cost in costs_by_month[-12:]]

    context = {
        "invoices": invoices,
        "currencies": currencies,
        "payments": payments,
        "categories": categories,
        "invoices_newest_10_desc": invoices_newest_10_desc,
        "costs_last_month": costs_by_month[-1][2],
        "costs_last_year": costs_by_year[-1][1],
        "invoices_last_month": invoices_by_month[-1][2],
        "invoices_last_year": invoice_by_year[-1][1],
        "current_user": current_user,
        "costs_per_month": costs_per_month,
        "costs_per_year": costs_per_year,
        "invoices_per_month": invoices_per_month,
        "invoices_per_year": invoices_per_year,
        "last_12_months": last_12_months,
        "last_6_months": last_6_months,
        "invoices_monthly_array": invoices_monthly_array[-6:],
        "costs_monthly_array": costs_monthly_array[-6:],
    }

    return render_template("index.html", **context)


@main.route("/invoices", methods=["GET", "POST"])
@login_required
def invoices():

    invoices = Invoice.query.order_by(desc(Invoice.id)).all()
    currencies = Currency.query.all()
    payments = Payment.query.all()
    categories = Category.query.all()

    context = {
        "invoices": invoices,
        "currencies": currencies,
        "payments": payments,
        "categories": categories,
    }

    return render_template("invoices.html", **context)


@main.route("/add_invoice", methods=["GET", "POST"])
@login_required
def add_invoice():

    if request.method == "POST":
        date = request.form["date"]
        name = request.form["name"]
        value = request.form["value"]
        currency = request.form["currency"]
        payment = request.form["payment"]
        category = request.form["category"]
        description = request.form["description"]

        invoice = Invoice(
            date=datetime.strptime(date, "%Y-%m-%d"),
            name=name,
            value=value,
            currency=currency,
            payment=payment,
            category=category,
            description=description,
        )

        db.session.add(invoice)
        db.session.commit()

        flash("Invoice added successfully!")

        return redirect(url_for("main.invoices"))


@main.route("/edit_invoice", methods=["GET", "POST"])
@login_required
def edit_invoice():

    if request.method == "POST":
        invoices = Invoice.query.get(request.form.get("id"))

        invoices.date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        invoices.name = request.form["name"]
        invoices.value = request.form["value"]
        invoices.currency = request.form["currency"]
        invoices.payment = request.form["payment"]
        invoices.category = request.form["category"]
        invoices.description = request.form["description"]

        db.session.commit()

        flash("Invoice edited successfully!")

        return redirect(url_for("main.invoices"))


@main.route("/delete_invoice", methods=["GET", "POST"])
@login_required
def delete_invoice():

    if request.method == "POST":
        invoices = Invoice.query.get(request.form.get("id"))
        db.session.delete(invoices)
        db.session.commit()

        flash("Invoice deleted successfully!")

        return redirect(url_for("main.invoices"))


@main.route("/reports")
@login_required
def reports():
    return render_template("reports.html")
