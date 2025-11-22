# teacher_dashboard.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPoint

# Import your other pages
from mark_attendence import MarkAttendanceWindow
from view_reports import ViewReportsWindow
from student_status import StudentStatusWindow


class TeacherDashboard(QWidget):
    def __init__(self, username, login_window=None):
        super().__init__()
        self.username = username
        self.login_window = login_window
        self.setWindowTitle(f"Teacher Dashboard - {username}")
        self.setGeometry(100, 80, 900, 600)  # shifted slightly toward top-left

        # Keep references for child windows
        self.mark_window = None
        self.reports_window = None
        self.status_window = None

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e3f2fd, stop: 1 #bbdefb
                );
                font-family: 'Segoe UI';
            }
            QLabel {
                color: #0d47a1;
            }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                padding: 14px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 500;
                border: none;

            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
            QPushButton#logoutBtn {
                background-color: #ef5350;
            }
            QPushButton#logoutBtn:hover {
                background-color: #c62828;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # ---- Title ----
        title = QLabel("Teacher Dashboard")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(f"Welcome, {self.username} 👋")
        subtitle.setFont(QFont("Segoe UI", 15))
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(40)

        # ---- Button Layout ----
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(35)
        btn_layout.setAlignment(Qt.AlignCenter)

        mark_attendance_btn = QPushButton("📷 Mark Attendance")
        mark_attendance_btn.clicked.connect(self.open_mark_attendance)

        view_reports_btn = QPushButton("📄 View Reports")
        view_reports_btn.clicked.connect(self.open_view_reports)

        student_status_btn = QPushButton("🎒 Student Status")
        student_status_btn.clicked.connect(self.open_student_status)

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setObjectName("logoutBtn")
        logout_btn.clicked.connect(self.logout)

        # Add buttons
        btn_layout.addWidget(mark_attendance_btn)
        btn_layout.addWidget(view_reports_btn)
        btn_layout.addWidget(student_status_btn)

        layout.addLayout(btn_layout)
        layout.addSpacing(60)
        layout.addWidget(logout_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    # -------------------------------
    # Open child windows
    # -------------------------------
    def open_mark_attendance(self):
        if self.mark_window is None or not self.mark_window.isVisible():
            try:
                self.mark_window = MarkAttendanceWindow()
                self.mark_window.setAttribute(Qt.WA_DeleteOnClose, False)
                self.mark_window.show()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Cannot open Mark Attendance window:\n{e}")
        else:
            self.mark_window.activateWindow()

    def open_view_reports(self):
        if self.reports_window is None or not self.reports_window.isVisible():
            try:
                self.reports_window = ViewReportsWindow()
                self.reports_window.setAttribute(Qt.WA_DeleteOnClose, False)
                self.reports_window.show()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Cannot open View Reports window:\n{e}")
        else:
            self.reports_window.activateWindow()

    def open_student_status(self):
        if self.status_window is None or not self.status_window.isVisible():
            try:
                self.status_window = StudentStatusWindow()
                self.status_window.setAttribute(Qt.WA_DeleteOnClose, False)
                self.status_window.show()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Cannot open Student Status window:\n{e}")
        else:
            self.status_window.activateWindow()

    # -------------------------------
    # Logout Function
    # -------------------------------
    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
            if self.login_window:
                self.login_window.show()


# -------------------------------
# Run Dashboard (for testing)
# -------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherDashboard("teacher1")
    window.show()
    sys.exit(app.exec_())
