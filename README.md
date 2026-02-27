# 🎯 ASTU Smart Complaint & Issue Tracking System

A professional, secure, and AI-enhanced platform for students at Adama Science and Technology University to report and track facility issues.

## 🚀 Core Features
- **Role-Based Access Control (RBAC):** Distinct workflows for Students, Staff, and Admins.
- **Smart Ticket Management:** Status tracking from 'Open' to 'Resolved' with a full audit trail.
- **AI Chatbot:** Context-aware assistant that suggests solutions before tickets are created.
- **Live Analytics:** Admin dashboard for resolution rates and common issue hotspots.
- **Security First:** Built-in protection against SQLi, XSS, and unauthorized data access.

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** SQLite (Development) / PostgreSQL (Production ready)
- **Auth:** JWT (SimpleJWT)
- **AI:** Custom Knowledge-Base matching logic

## 🔧 Installation & Setup
1. Clone the repo: `git clone <your-repo-link>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## 🔒 Cyber Security Features
- **Data Isolation:** Students can only access their own data via `get_queryset` overrides.
- **Audit Logs:** Every suspicious unauthorized access attempt is logged in the `SecurityLog` table.
- **File Validation:** Strict extension and size checking for attachments.