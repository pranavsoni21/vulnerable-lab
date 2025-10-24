# vulnerable-lab

This project is a deliberately vulnerable web application built with **Flask** and **SQLite**.  
It is designed for practicing **SQL Injection** attacks in a safe environment.  

⚠️ Disclaimer: This is for **educational purposes only**. Do not deploy it to the internet.  

---

## Features
- Login form vulnerable to SQL Injection
- Preloaded database with a test user (`admin:password`)
- Minimal setup with Docker

---

## Setup

### Local Run
```bash
git clone https://github.com/pranavsoni21/vulnerable-lab.git
cd vulnerable-lab/web
pip install -r requirements.txt
python db_init.py
python app.py
