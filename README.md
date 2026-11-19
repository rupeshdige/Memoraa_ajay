# Memoraa Attendance System

Complete attendance + salary management system for **Memoraa Photography Studio**.

## Features

- Punch In / Punch Out with location
- Attendance Regularization (with manager approval)
- Holiday Management
- Employee Management (Admin)
- Salary Slip PDF generation
- Role-based access (Admin / Manager / Employee)

## Default Admin Login

- **Mobile**: `9324029311`
- **Password**: `Ajay@9311`

> Change the password after first login.

## Setup for Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/memoraa
SECRET_KEY=your-very-secret-key-here
```

4. Run the app:
```bash
python app.py
```

## Deploy on Vercel

1. Push this project to GitHub
2. Import the repository in Vercel
3. Add Environment Variables:
   - `DATABASE_URL` → Your PostgreSQL connection string (Neon / Supabase / etc.)
   - `SECRET_KEY` → A long random string
4. Deploy

## Tech Stack

- Flask
- Flask-Login
- SQLAlchemy + PostgreSQL (psycopg3)
- ReportLab (PDF generation)
- Bootstrap 5 (UI)
