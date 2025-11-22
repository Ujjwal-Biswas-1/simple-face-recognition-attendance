import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

from student_view_attendance import StudentViewAttendance
from student_view_status import StudentViewStatus


class StudentDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Student Dashboard - {username}")
        self.setGeometry(250, 80, 900, 700)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5f7fa, stop:1 #c3cfe2
                );
                font-family: 'Segoe UI';
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #0d47a1;
            }
            QLabel#welcome {
                font-size: 22px;
                color: #37474f;
            }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 500;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)

        # --- Header Section ---
        title = QLabel("🎓 Student Dashboard")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        welcome = QLabel(f"Welcome, {self.username}")
        welcome.setObjectName("welcome")
        welcome.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(welcome)

        # --- Buttons ---
        attendance_btn = QPushButton("📅 Attendance")
        status_btn = QPushButton("📘 Status")
        academics_btn = QPushButton("📚 Academics")
        logout_btn = QPushButton("🚪 Logout")

        # Connect buttons
        attendance_btn.clicked.connect(self.open_attendance)
        status_btn.clicked.connect(self.open_status)
        academics_btn.clicked.connect(self.open_academics)
        logout_btn.clicked.connect(self.logout)

        # --- Row Layouts ---
        row1 = QHBoxLayout()
        row1.setAlignment(Qt.AlignCenter)
        row1.setSpacing(40)
        row1.addWidget(attendance_btn)
        row1.addWidget(status_btn)

        row2 = QHBoxLayout()
        row2.setAlignment(Qt.AlignCenter)
        row2.setSpacing(40)
        row2.addWidget(academics_btn)
        row2.addWidget(logout_btn)

        layout.addLayout(row1)
        layout.addLayout(row2)

        self.setLayout(layout)

    # ---------------- BUTTON ACTIONS ----------------
    def open_attendance(self):
        self.attendance_window = StudentViewAttendance(self.username)
        self.attendance_window.show()

    def open_status(self):
        self.status_window = StudentViewStatus(self.username)
        self.status_window.show()

    def open_academics(self):
        QMessageBox.information(self, "Academics", "Academic records coming soon.")

    def logout(self):
        confirm = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.close()


# ---------------- RUN DIRECTLY ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentDashboard("Ujjwal")
    window.show()
    sys.exit(app.exec_())
