
# 📋 Priority Task Manager

A clean, minimal task management application designed to boost productivity by organizing your to-dos by priority level (Grades 1–3). It highlights urgent tasks with visual badges, strikes through completed items, and automatically cleans up finished tasks on your next login.

---

## ✨ Features

- **User Accounts:** Secure sign-up and authentication using Flask-Login and hashed passwords.
- **Priority Categorization:** Grade 1 (High), Grade 2 (Medium), and Grade 3 (Low) with distinct color badges.
- **Urgent Priority Alerts:** Persistent warning alert banner when Grade 1 tasks remain pending.
- **Instant Completion & Purge:** Strikethrough effect on check; completed tasks automatically purge on the user's next login.
- **Dual Database Support:** Local SQLite database for local development with automatic fallback, and PostgreSQL support (via Supabase) for remote deployment.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend:** Jinja2 Templates, Bootstrap 5.3, Bootstrap Icons
- **Database:** SQLite (local) / PostgreSQL (production)

---

### Installation
If you are cloning this repository or submitting a pull request, install the required dependencies:

```bash
pip install -r requirements.txt

