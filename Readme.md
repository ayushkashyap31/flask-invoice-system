# Invoice Management System

A Flask-based Invoice Management System for managing customers, items, invoices, payments, and notifications.

## Features

* Customer Management (Add, Edit, Delete)
* Item Management
* Invoice Creation
* Invoice Search
* Invoice Details Page
* PDF Invoice Generation
* Payment Status Tracking
* Dashboard Analytics
* Redis Caching
* Automated Notifications using APScheduler
* Responsive UI with Bulma CSS

## Tech Stack

* Python
* Flask
* Peewee ORM
* SQLite
* Redis
* APScheduler
* WeasyPrint
* Bulma CSS

## Run Locally

```bash
git clone https://github.com/ayushkashyap31/flask-invoice-system.git

cd flask-invoice-system

pip install -r requirements.txt

redis-server

python app.py
```

## Dashboard

The application provides:

* Total Customers
* Total Items
* Total Invoices
* Unpaid Invoices
* Revenue Analytics

## Author

Ayush Kumar Kashyap
