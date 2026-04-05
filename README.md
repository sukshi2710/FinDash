# Finance_dash
Role-Based Access Control is implemented in this Finance Dashboard for the roles Admin, Analyst, and Viewer. This Django project uses sophisticated backend programming for net balance/trends calculation, soft delete operations, and search operations. This application is built using the Python programming language with SQLite database management.

# Finance_dashboard
Role-Based Access Control is implemented in this Finance Dashboard for the roles Admin, Analyst, and Viewer. This Django project uses sophisticated backend programming for net balance/trends calculation, soft delete operations, and search operations. This application is built using the Python programming language with SQLite database management.

# 💹 Pro-Finance Dashboard: A Role-Based Analytics Application

This is a fully functional, production-level finance tracker application coded with Django. More than just basic CRUD operations, this application is meant to show high-level backend operations such as Data Aggregation, Database Truncation of Trends, and strict Security Guards.

---

## 📖 Project Introduction

The Pro-Finance Dashboard is an application for managing financial transactions with strict control measures such as security and performance. The system caters to three different roles within the corporation to guarantee data visualization and operations.

---

## 👥 Roles & Permissions (RBAC)

**Admin**
- Full rights
- Can create records, view analytics, search, and perform Soft Deletes

**Analyst**
- Read-only access
- Can view transactions, search categories, and analyze:
  - Monthly Trends
  - Category Summary

**Viewer**
- Limited access
- Can only view:
  - Net Balance
  - Total Income
  - Total Expense

---

## 🛠️ Technical Implementation and Design

### 1. Backend Service Logic (Aggregation)

- Uses Django ORM functions:
  - `Sum`
  - `aggregate`
  - `annotate`

**Features:**
- Net Analytics: Income − Expenses calculated dynamically
- Trend Logic: Uses `TruncMonth` to group transactions monthly

---

### 2. Access Control Logic (Security)

**UI Level**
```html
{% if user_role == 'Admin' %}
```

**Backend Level**
```python
@login_required
@user_passes_test
```

- Prevents unauthorized access (e.g., `/delete/1`)

---

### 3. Production Features

- **Soft Delete**
  - Uses `is_deleted = True` instead of deleting data

- **Search**
  - Implemented using Django `Q` objects

- **Pagination**
  - Uses `Paginator` (5 records per page)

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip

---

### 1. Clone & Setup

```bash
git clone <your-repository-url>
cd finance-dashboard

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install django
```

---

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4. Create Superuser & Roles

```bash
python manage.py createsuperuser
python manage.py runserver
```

Go to: http://127.0.0.1:8000/admin  
Create groups:
- Admin
- Analyst
- Viewer

---

## 📊 Assumptions

- Currency: Indian Rupee (₹)
- Database: SQLite (PostgreSQL recommended for production)
- Soft Delete is used instead of Hard Delete

---

## 📁 Project Structure

```
finance-dashboard/
├── core/
├── dashboard/
│   ├── models.py
│   ├── views.py
│   └── templates/
├── manage.py
└── db.sqlite3
```

---

## 👨‍💻 Developed By

Sukshith P | MCA Student | Atria Institute of Technology
