# face_module.py
import cv2
import os
import sqlite3
import time
import sys
from datetime import datetime
from deepface import DeepFace

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Constants
STUDENT_IMAGES_DIR = "student_images"
DB_PATH = "attendance.db"
TEMP_IMAGE = "temp_face.jpg"


def mark_attendance(student_name, subject, teacher_name):
    """
    Mark attendance for a recognized student for the given subject and teacher.
    Only once per subject per day.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    # Check if already marked for this subject and date
    cursor.execute("""
        SELECT * FROM attendance
        WHERE student_name=? AND subject=? AND date=?
    """, (student_name, subject, today))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            INSERT INTO attendance (student_name, roll_number, date, subject, teacher_name, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_name, None, today, subject, teacher_name, "Present"))
        conn.commit()
        print(f"✅ {student_name} marked Present for {subject} by {teacher_name}.")
    else:
        print(f"ℹ️ {student_name} already marked for {subject} today.")

    conn.close()


def start_face_recognition(subject, teacher_name):
    """
    Start webcam and recognize multiple students for a given subject and teacher.
    Marks attendance per subject per day.
    """
    if not os.path.exists(STUDENT_IMAGES_DIR) or not os.listdir(STUDENT_IMAGES_DIR):
        print("❌ No student images found in 'student_images' folder.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    print(f"📷 Face recognition started for '{subject}' (Teacher: {teacher_name}) — press 'q' to quit.")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    last_marked = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_crop = frame[y:y + h, x:x + w]
            cv2.imwrite(TEMP_IMAGE, face_crop)

            try:
                result = DeepFace.find(
                    img_path=TEMP_IMAGE,
                    db_path=STUDENT_IMAGES_DIR,
                    enforce_detection=False,
                    silent=True
                )

                if len(result) > 0 and len(result[0]) > 0:
                    match_path = result[0].iloc[0]['identity']
                    name = os.path.basename(match_path).split('.')[0]

                    now = time.time()
                    if name not in last_marked or (now - last_marked[name]) > 30:
                        mark_attendance(name, subject, teacher_name)
                        last_marked[name] = now

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{name}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            except Exception as e:
                print(f"⚠️ Error: {str(e)}")

        window_title = f"Face Attendance - {subject} ({teacher_name})"
        cv2.imshow(window_title, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    if os.path.exists(TEMP_IMAGE):
        os.remove(TEMP_IMAGE)

    print("👋 Face recognition closed.")


# ------------------- ENTRY POINT -------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Usage: python face_module.py <subject> <teacher_name>")
    else:
        subject = sys.argv[1]
        teacher_name = sys.argv[2]
        start_face_recognition(subject, teacher_name)
