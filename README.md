# Cloud Attendance Management System
This is the actual Flask application source code, not only the report.

## Run locally
Install Python 3.10+, then in this directory:
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Features
Record student attendance, Present/Absent status, date-filtered report, duplicate-entry prevention, SQLite storage, and `/health` endpoint.

## Cloud demo
Push to GitHub and create a Render Web Service. Build command: `pip install -r requirements.txt`; start command: `gunicorn app:app`. SQLite is for demo; use managed persistent storage for production.

## 10-minute demo
Introduce objective; explain Flask/cloud; record entries; show duplicate validation; generate report; discuss deployment and limitations.

References: Flask, Python, SQLite, and Render documentation.
