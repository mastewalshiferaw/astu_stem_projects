# 🛡 Security Audit Report - ASTU Smart Issue System

## 1. Identified Risks & Mitigations
- **Broken Access Control:** Prevented by overriding `get_queryset` so users only see their own data.
- **Injection Attacks:** Prevented by using Django ORM (parameterized queries).
- **Spam/DoS:** Implemented `Rate Limiting` (10 requests/min) on the AI Chatbot.
- **Sensitive Data Exposure:** Used JWT with short-lived access tokens and stored passwords using Argon2 hashing (Django default).

## 2. Testing Approach
- **Manual Pentesting:** Attempted to access staff endpoints using a student token; verified 403 Forbidden.
- **Validation Testing:** Attempted to upload `.exe` files to tickets; verified rejection by custom file validators.
- **Audit Logs:** Verified that every 403 error is logged in the `SecurityLog` table with IP address tracking.

## 3. Preventive Measures
- **Security Headers:** Implemented X-Frame-Options and Content-Type-Options via middleware.
- **Role Enforcement:** Custom permissions `IsStaffOrReadOnly` used for all ticket updates.