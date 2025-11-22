import sqlite3

# Check login DB
conn = sqlite3.connect('logindata.db')
cur = conn.cursor()
print("📘 Tables in logindata.db:")
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

cur.execute("PRAGMA table_info(users)")
print("🧩 Columns in users table:")
print([col[1] for col in cur.fetchall()])
conn.close()


# Check attendance DB
conn = sqlite3.connect("attendance.db")
cur = conn.cursor()
print("\n📗 Tables in attendance.db:")
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

cur.execute("PRAGMA table_info(attendance)")
print("🧩 Columns in attendance table:")
print([col[1] for col in cur.fetchall()])
conn.close()

print("\n✅ Database structure verified successfully!")
