# Inventory Management System

A Django-based inventory and sales management system for managing products, stock, categories, and sales.

## Features

* User authentication
* Role-based permissions
* Product management
* Category management
* Stock restocking
* Sales recording
* Automatic stock updates
* Sales history
* Product search
* Form validation

## Tech Stack

* Python
* Django
* SQLite
* HTML/CSS
* Django Templates

## User Roles

The system uses Django's built-in Groups and Permissions to control staff access.

* **Manager:** Manage products, stock, sales, and categories.
* **Sales Staff:** View products and record sales.
* **Storekeeper:** View products and manage stock.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Project Purpose

This project was built to practice developing a real-world Django application, with particular focus on CRUD operations, database relationships, authentication, authorization, inventory management, and sales workflows.

## Future Improvements

* REST API with Django REST Framework
* Inventory reports
* Low-stock notifications
* Automated tests
* PostgreSQL
* Production deployment
