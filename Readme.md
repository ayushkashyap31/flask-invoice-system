# Invoice Management System

A Flask-based Invoice Management System for managing customers, items, invoices, payments, notifications, and PDF generation.

## Features

* Customer Management (Add, Edit, Delete)
* Item Management
* Invoice Creation
* Invoice Search
* Invoice Details Page
* PDF Invoice Generation
* Payment Status Tracking
* Dashboard Analytics
* Flash Messages
* Redis Caching
* Background Tasks using Celery
* Scheduled Notifications using Celery Beat
* Responsive UI with Bulma CSS

## Tech Stack

* Python
* Flask
* Peewee ORM
* SQLite
* Redis
* Celery
* Celery Beat
* WeasyPrint
* Bulma CSS

## Run the Project

### Start Redis

```bash
redis-server
```

### Start Celery Worker

```bash
celery -A tasks worker --loglevel=info
```

### Start Celery Beat

```bash
celery -A celery_app beat --loglevel=info
```

### Run Flask Application

```bash
python app.py
```

## Learning Outcomes

* Flask Routing
* CRUD Operations
* Template Rendering
* Database Management with Peewee ORM
* Redis Caching
* Background Task Processing with Celery
* Task Scheduling with Celery Beat
* PDF Generation
* Git & GitHub Workflow

## Author

Ayush Kumar Kashyap
