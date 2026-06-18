# import flask

from models import *

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    flash
)
from peewee import *
import datetime
from weasyprint import HTML
from apscheduler.schedulers.background import (
    BackgroundScheduler
)


import redis

import json





app = Flask(__name__)
app.secret_key = "invoice-secret-key"

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)




@app.route("/")
def home():

    customer_count = Customers.select().count()

    item_count = Items.select().count()

    invoice_count = Invoice.select().count()

    unpaid_count = (
        Invoice
        .select()
        .where(
            Invoice.payment_status == "UNPAID"
        )
        .count()
    )

    revenue = sum(
        invoice.total_price
        for invoice in Invoice.select()
    )

    return render_template(
        "index.html",
        customer_count=customer_count,
        item_count=item_count,
        invoice_count=invoice_count,
        unpaid_count=unpaid_count,
        revenue=revenue
    )

@app.route('/hello')
def hello():
    return "Hello, Flask is running!"

@app.route("/customers")
def customers_list():
    customers= Customers.select()
    return render_template('customers.html',customers=customers)


@app.route("/customers/add", methods=["GET", "POST"])
def customers_add():

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")
    

        if not phone.isdigit() or len(phone) != 10:

            flash(
                "Phone number must contain exactly 10 digits.",
                "danger"
            )

            return redirect(
                url_for("customers_add")
            )

        Customers.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        
        flash(
            "Customer added successfully!",
            "success"
        )

        return redirect(url_for("customers_list"))

    return render_template("customer_form.html")

@app.route("/items")
def items_list():
    items = Items.select()

    return render_template(
        "items.html",
        items=items
    )
@app.route("/items/add", methods=["GET", "POST"])
def items_add():

    if request.method == "POST":
        item_name = request.form.get("item_name")
        price = request.form.get("price")

        Items.create(
            item_name=item_name,
            price=price
        )

        flash(
        "Item added successfully!",
        "success"
        )

        return redirect(url_for("items_list"))

    return render_template("item_form.html")

@app.route("/invoices")
def invoices_list():
    invoices = Invoice.select()

    return render_template(
        "invoices.html",
        invoices=invoices
    )

@app.route("/invoices/add", methods=["GET", "POST"])
def invoices_add():

    if request.method == "POST":

        customer_id = request.form.get("customer")

        item_ids = request.form.getlist("item")
        quantities = request.form.getlist("quantity")

        customer = Customers.get_by_id(customer_id)

        invoice = Invoice.create(
            customer=customer,
            total_price=0
        )

        grand_total = 0

        for item_id, qty in zip(item_ids, quantities):

            item = Items.get_by_id(item_id)

            qty = int(qty)

            line_total = item.price * qty

            InvoiceItem.create(
                invoice=invoice,
                item=item,
                quantity=qty,
                line_total=line_total
            )

            grand_total += line_total

        subtotal = grand_total

        tax_percentage = 18

        tax_amount = (
            subtotal * tax_percentage
        ) / 100

        final_total = (
            subtotal + tax_amount
        )

        invoice.subtotal = subtotal

        invoice.tax_percentage = tax_percentage

        invoice.tax_amount = tax_amount

        invoice.total_price = final_total

        invoice.save()

        redis_client.delete(f"customer_{customer.id}_invoices")

        flash("Invoice created successfully!",
            "success"
        )

        return redirect(url_for("invoices_list"))

    customers = Customers.select()
    items = Items.select()
    tax_percentage = float(
    request.form.get(
        "tax_percentage",
        18
    )
)

    return render_template(
        "invoice_form.html",
        customers=customers,
        items=items
    )


@app.route("/invoices/pdf/<int:invoice_id>")
def invoice_pdf(invoice_id):

    invoice = Invoice.get_by_id(invoice_id)

    html = render_template(
        "invoice_pdf.html",
        invoice=invoice
    )

    pdf = HTML(
        string=html
    ).write_pdf()

    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"

    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename=invoice_{invoice.id}.pdf"

    return response

@app.route("/invoices/pay/<int:invoice_id>")
def mark_invoice_paid(invoice_id):

    invoice = Invoice.get_by_id(invoice_id)

    invoice.payment_status = "PAID"

    invoice.save()

    flash(
    "Invoice marked as paid!",
    "success"
    )

    return redirect(
        url_for("invoices_list")
    )

@app.route("/test-notifications")
def test_notifications():

    notify_unpaid_invoices()

    return "Notifications Created"


@app.route("/notifications")
def notifications():

    notifications = (
        Notification
        .select()
        .order_by(
            Notification.created_at.desc()
        )
    )

    return render_template(
        "notifications.html",
        notifications=notifications
    )







@app.route(
    "/customer/<int:customer_id>/invoices"
)
def customer_invoices(customer_id):

    cache_key = (
        f"customer_{customer_id}_invoices"
    )

    cached_data = redis_client.get(
        cache_key
    )

    if cached_data:

        return (
            "Fetched from Redis<br><br>"
            + cached_data
        )

    invoices = (
        Invoice
        .select()
        .where(
            Invoice.customer == customer_id
        )
    )

    invoice_list = []

    for invoice in invoices:

        invoice_list.append({

            "id": invoice.id,

            "total_price":
            invoice.total_price,

            "status":
            invoice.payment_status

        })

    redis_client.set(

        cache_key,

        json.dumps(
            invoice_list
        )

    )

    return (

        "Fetched from Database "
        "(Saved to Redis)<br><br>"

        + json.dumps(
            invoice_list,
            indent=4
        )

    )



























def notify_unpaid_invoices():

    invoices = Invoice.select()

    for invoice in invoices:

        if invoice.payment_status == "UNPAID":

            Notification.create(
                invoice=invoice,
                message=f"Invoice #{invoice.id} is unpaid"
            )

    print("Notifications generated")







db.connect()
db.create_tables([
    Customers,
    Items,
    Invoice,
    InvoiceItem,
    Notification
])
# Customers.create(
#     first_name="John",
#     last_name="Doe",
#     phone="9876543210"
# )

# Customers.create(
#     first_name="Jane",
#     last_name="Smith",
#     phone="9999999999"
# )



if __name__ == "__main__":



    # abhi 1 min h
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        notify_unpaid_invoices,
        trigger="interval",
        minutes=1

        # trigger="cron",
        # day=3,
        # hour=9,
        # minute=0
    )

    scheduler.start()

    app.run(debug=True)