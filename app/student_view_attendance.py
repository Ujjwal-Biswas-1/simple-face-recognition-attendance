# student_view_attendance.py
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class StudentViewAttendance(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Attendance Record - {username}")
        self.setGeometry(250, 100, 850, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #f9fcff;
                font-family: 'Segoe UI';
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #0d47a1;
                margin-bottom: 10px;
            }
            QLabel#percentage {
                font-size: 18px;
                color: #2e7d32;
                margin-bottom: 15px;
            }
            QTableWidget {
                background: white;
                border-radius: 10px;
                border: 1px solid #ccc;
                font-size: 14px;
                selection-background-color: #bbdefb;
            }
            QHeaderView::section {
                background-color: #1e88e5;
                color: white;
                padding: 8px;
                border: none;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("📅 Your Attendance Report")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Attendance percentage label
        self.percentage_label = QLabel("Calculating your attendance...")
        self.percentage_label.setObjectName("percentage")
        self.percentage_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.percentage_label)

        # Table for attendance data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Subject", "Teacher", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Load student attendance data
        self.load_data()

    def load_data(self):
        """Load the attendance data for the current student."""
        try:
            conn = sqlite3.connect("attendance.db")
            cur = conn.cursor()

            cur.execute("""
                SELECT date, subject, teacher_name, status
                FROM attendance
                WHERE student_name = ?
                ORDER BY date DESC
            """, (self.username,))

            data = cur.fetchall()
            conn.close()

            if not data:
                self.percentage_label.setText("No attendance records found.")
                return

            # Populate table
            self.table.setRowCount(0)
            present_count = 0
            for row_num, row_data in enumerate(data):
                self.table.insertRow(row_num)
                for col_num, value in enumerate(row_data):
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(value)))
                if row_data[3] == "Present":
                    present_count += 1

            # Calculate percentage
            total_classes = len(data)
            percentage = (present_count / total_classes) * 100
            self.percentage_label.setText(
                f"✅ Attendance: {present_count}/{total_classes} classes ({percentage:.2f}%)"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
