from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "invoice_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)



'''
this wala part is for the 
3rd of the month at 9:00 AM
'''

celery.conf.beat_schedule = {
    "check-unpaid-invoices": {
        "task": "tasks.notify_unpaid_invoices",
        "schedule": crontab(
            day_of_month=3,
            hour=9,
            minute=0
        ),
    }
}

'''
this is for the t
esting of 60seconds
'''
# celery.conf.beat_schedule = {

#     "check-unpaid-invoices": {

#         "task": "tasks.notify_unpaid_invoices",

#         "schedule": 60.0

#     }

# }