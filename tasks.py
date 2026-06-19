from celery_app import celery
from models import *
from datetime import datetime


@celery.task
def notify_unpaid_invoices():

    invoices = Invoice.select()

    count = 0

    for invoice in invoices:

        if invoice.payment_status == "UNPAID":

            Notification.create(
                invoice=invoice,
                message=f"Invoice #{invoice.id} is unpaid"
            )

            count += 1

    return f"{count} notifications created"