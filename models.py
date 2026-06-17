from peewee import *
import datetime


db = SqliteDatabase('task_invoices.db')

class BaseModel(Model):
    #for the common db base
    class Meta:
        database=db

class Customers(BaseModel):
    first_name = TextField()
    last_name = TextField()
    phone = TextField()

    
class Items(BaseModel):
    item_name=TextField()
    price = FloatField()

# class Invoices(BaseModel):
#     #customer foreign ki ayegi yaha pe look out for that

#     invoice_date=DateTimeField(default=datetime.datetime.now)
#     total_price = FloatField()


class Invoice(BaseModel):
    customer = ForeignKeyField(Customers)

    invoice_date = DateTimeField(
        default=datetime.datetime.now
    )

    subtotal = FloatField(default=0)

    tax_percentage = FloatField(default=18)

    tax_amount = FloatField(default=0)

    total_price = FloatField(default=0)

    payment_status = TextField(default="UNPAID")


    
class InvoiceItem(BaseModel):
    invoice = ForeignKeyField(Invoice, backref="items")
    item = ForeignKeyField(Items)

    quantity = IntegerField(default=1)

    line_total = FloatField()


class Notification(BaseModel):

    invoice = ForeignKeyField(
        Invoice,
        backref="notifications"
    )

    message = TextField()

    created_at = DateTimeField(
        default=datetime.datetime.now
    )
