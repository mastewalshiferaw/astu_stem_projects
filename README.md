# 🎯 ASTU Smart Complaint & Issue Tracking System

A secure, full-stack issue management platform designed for Adama Science and Technology University.

## 🚀 Core Features
- **AI Chatbot:** Knowledge-base driven assistant for instant campus solutions.
- **RBAC (Role-Based Access Control):** Dedicated views for Students, Staff, and Admins.
- **Smart Workflow:** Automated notifications and audit trails for every ticket.
- **Security Monitoring:** Real-time logging of unauthorized access attempts.

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Auth:** JWT (SimpleJWT)
- **Documentation:** Swagger UI / OpenAPI 3.0
- **Deployment:** Render (Python 3.12)

## 🔧 Setup Instructions
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py seed_data`  <-- Important for the demo!
4. `python manage.py runserver`

## 🔗 Live API Documentation
Visit: `https://your-app-name.onrender.com/` to view the interactive Swagger docs.