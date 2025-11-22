import sqlite3
from datetime import datetime
import subprocess
import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QCheckBox, QMessageBox, QScrollArea, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import global_state
from db__initializer import init_databases


class MarkAttendanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mark Attendance - Teacher Panel")
        self.setGeometry(200, 80, 900, 750)

        # Ensure databases exist
        init_databases()

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e3f2fd, stop: 1 #bbdefb
                );
                font-family: 'Segoe UI';
            }
            QLabel { color: #0d47a1; }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-size: 15px;
                min-width: 180px;
                border: none;
            }
            QPushButton:hover { background-color: #0d47a1; }
            QPushButton#faceBtn {
                background-color: #43a047;
            }
            QPushButton#faceBtn:hover {
                background-color: #2e7d32;
            }
            QPushButton#saveBtn { background-color: #1565c0; }
            QPushButton#refreshBtn { background-color: #039be5; }
            QPushButton#markAllBtn { background-color: #6c63ff; }
            QComboBox {
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #ced4da;
                background: white;
                font-size: 14px;
            }
            QScrollArea { background: transparent; border: none; }
            QWidget#scrollCard {
                background: white;
                border-radius: 12px;
                border: 1px solid #ccc;
                padding: 10px;
            }
            QCheckBox {
                font-size: 15px;
                color: #212529;
                padding: 4px;
            }
        """)

        self.known_students = self.fetch_students()
        self.initUI()

    # -------------------- UI SETUP --------------------
    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        title = QLabel("📸 Smart Attendance (Manual + Face Recognition)")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Subject + Date
        subject_layout = QHBoxLayout()
        subject_layout.setSpacing(20)
        subject_layout.setAlignment(Qt.AlignCenter)

        self.subject = QComboBox()
        self.subject.addItems([
            "Select Subject", "English", "Maths", "Computer Science",
            "Science", "Hindi", "Social Science"
        ])

        date_label = QLabel(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
        date_label.setFont(QFont("Segoe UI", 12, QFont.Bold))

        subject_layout.addWidget(QLabel("Subject:"))
        subject_layout.addWidget(self.subject)
        subject_layout.addStretch()
        subject_layout.addWidget(date_label)

        # Face Recognition Button
        face_btn = QPushButton("🤖 Open Face Recognition Window")
        face_btn.setObjectName("faceBtn")
        face_btn.clicked.connect(self.open_face_recognition)
        face_btn.setFixedHeight(45)

        # Scrollable Student List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_card = QWidget()
        scroll_card.setObjectName("scrollCard")
        scroll_layout = QVBoxLayout(scroll_card)
        scroll_layout.setSpacing(6)

        self.checkboxes = {}
        if not self.known_students:
            scroll_layout.addWidget(QLabel("❌ No students found in database."))
        else:
            for roll, student in enumerate(self.known_students, start=1):
                checkbox = QCheckBox(f"{roll:02d}. {student}")
                scroll_layout.addWidget(checkbox)
                self.checkboxes[student.lower()] = checkbox

        scroll.setWidget(scroll_card)
        scroll.setMinimumHeight(400)

        # Action Buttons (Save + Refresh + Mark All)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)

        save_btn = QPushButton("💾 Save Attendance")
        save_btn.setObjectName("saveBtn")
        save_btn.clicked.connect(self.save_attendance)

        refresh_btn = QPushButton("🔄 Refresh Attendance")
        refresh_btn.setObjectName("refreshBtn")
        refresh_btn.clicked.connect(self.refresh_attendance)

        mark_all_btn = QPushButton("✅ Mark All Present")
        mark_all_btn.setObjectName("markAllBtn")
        mark_all_btn.clicked.connect(self.mark_all_present)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(mark_all_btn)

        main_layout.addWidget(title)
        main_layout.addLayout(subject_layout)
        main_layout.addWidget(face_btn, alignment=Qt.AlignCenter)
        main_layout.addWidget(scroll)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # -------------------- FETCH STUDENTS --------------------
    def fetch_students(self):
        try:
            conn = sqlite3.connect("logindata.db")
            cur = conn.cursor()
            cur.execute("SELECT username FROM users WHERE role='Student'")
            students = [row[0] for row in cur.fetchall()]
            conn.close()
            return students
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
            return []

    # -------------------- OPEN FACE RECOGNITION --------------------
    def open_face_recognition(self):
        subject = self.subject.currentText()
        teacher_name = global_state.current_teacher or "Unknown Teacher"

        if subject == "Select Subject":
            QMessageBox.warning(self, "Invalid", "Please select a subject before starting face recognition.")
            return

        try:
            subprocess.Popen([sys.executable, "face_module.py", subject, teacher_name])
            QMessageBox.information(
                self, "Face Recognition",
                f"📷 Face recognition started for {subject}.\nClose it after marking attendance."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open face recognition window:\n{str(e)}")

    # -------------------- SAVE ATTENDANCE --------------------
    def save_attendance(self):
        subject = self.subject.currentText()
        if subject == "Select Subject":
            QMessageBox.warning(self, "Invalid", "Please select a subject before saving attendance.")
            return

        teacher_name = global_state.current_teacher or "Unknown Teacher"

        try:
            conn = sqlite3.connect("attendance.db")
            cur = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d')

            for roll, student_name in enumerate(self.known_students, start=1):
                checkbox = self.checkboxes.get(student_name.lower())
                if checkbox:
                    status = "Present" if checkbox.isChecked() else "Absent"
                    cur.execute("""
                        INSERT INTO attendance (student_name, roll_number, date, subject, teacher_name, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (student_name, roll, date, subject, teacher_name, status))

            conn.commit()
            conn.close()
            QMessageBox.information(self, "Saved", "✅ Attendance saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    # -------------------- REFRESH --------------------
    def refresh_attendance(self):
        subject = self.subject.currentText()
        if subject == "Select Subject":
            QMessageBox.warning(self, "Invalid", "Please select a subject first.")
            return

        date = datetime.now().strftime('%Y-%m-%d')
        try:
            conn = sqlite3.connect("attendance.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT student_name, status FROM attendance WHERE date=? AND subject=?",
                (date, subject)
            )
            records = cur.fetchall()
            conn.close()

            for name, status in records:
                name = name.lower()
                if name in self.checkboxes:
                    self.checkboxes[name].setChecked(status == "Present")

            QMessageBox.information(self, "Refreshed", f"🔄 Attendance loaded for {subject}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh:\n{str(e)}")

    # -------------------- MARK ALL PRESENT --------------------
    def mark_all_present(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)
        QMessageBox.information(self, "Marked", "✅ All students marked as Present.")
