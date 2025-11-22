import sqlite3

# ----------------------------
#  LOGIN DATABASE SETUP
# ----------------------------
conn = sqlite3.connect("logindata.db")
cursor = conn.cursor()

# Create users table (with user_id)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('Student', 'Teacher')) NOT NULL,
    user_id TEXT
)
""")

# Sample data
users = [
    ("student1", "12345", "Student", "STU001"),
    ("teacher1", "12345", "Teacher", "TCH001")
]

for user in users:
    try:
        cursor.execute("INSERT INTO users (username, password, role, user_id) VALUES (?, ?, ?, ?)", user)
    except sqlite3.IntegrityError:
        pass


# ----------------------------
#  STUDENT INFO RELATED TABLES
# ----------------------------

cursor.execute('''CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    date TEXT,
    status TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS goods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    uniform_received TEXT,
    books_received TEXT,
    issue_year INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS academics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    subject TEXT,
    marks INTEGER,
    term TEXT
)''')

conn.commit()
conn.close()
print("✅ logindata.db initialized successfully with user_id support!")


# ----------------------------
#  ATTENDANCE DATABASE SETUP
# ----------------------------
conn = sqlite3.connect("attendance.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    roll_no TEXT,
    subject TEXT,
    teacher_name TEXT,
    date TEXT NOT NULL,
    time TEXT,
    status TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("✅ attendance.db initialized successfully with subject + teacher support!")
