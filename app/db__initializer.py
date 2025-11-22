import os
import sqlite3

def init_databases():
    # ---------- 1️⃣ LOGIN DATABASE ----------
    if not os.path.exists("logindata.db"):
        conn = sqlite3.connect("logindata.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('Student', 'Teacher')) NOT NULL,
                roll_number INTEGER
            )
        """)
        conn.commit()
        print("🟢 logindata.db created successfully.")
        conn.close()

    # ---------- 2️⃣ ATTENDANCE DATABASE ----------
        # ---------- 2️⃣ ATTENDANCE DATABASE ----------
    if not os.path.exists("attendance.db"):
        conn = sqlite3.connect("attendance.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                roll_number INTEGER,
                date TEXT NOT NULL,
                subject TEXT NOT NULL DEFAULT 'General',
                teacher_name TEXT,
                status TEXT CHECK(status IN ('Present', 'Absent')) NOT NULL
            )
        """)
        conn.commit()
        print("🟢 attendance.db created successfully with default subject column.")
        conn.close()

    # ---------- 3️⃣ STUDENT STATUS DATABASE ----------
    if not os.path.exists("studentstatus.db"):
        conn = sqlite3.connect("studentstatus.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                roll_number INTEGER,
                got_books INTEGER DEFAULT 0,
                got_uniform INTEGER DEFAULT 0,
                fees_paid INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        print("🟢 studentstatus.db created successfully.")
        conn.close()

# Run once when imported
init_databases()
