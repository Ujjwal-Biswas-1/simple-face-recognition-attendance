# view_reports.py
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLineEdit, QHBoxLayout, QComboBox, QFrame, QScrollArea
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import global_state


class ViewReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Attendance Reports - Teacher Panel")
        self.setGeometry(200, 80, 950, 750)

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

            QLineEdit, QComboBox {
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
                background-color: white;
                font-size: 14px;
            }

            QPushButton {
                background-color: #1e88e5;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 15px;
                border: none;
                min-width: 130px;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
            QPushButton#refreshBtn {
                background-color: #039be5;
            }
            QPushButton#refreshBtn:hover {
                background-color: #0277bd;
            }

            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f1f8ff;
                border: 1px solid #ccc;
                border-radius: 12px;
                gridline-color: #90caf9;
                font-size: 14px;
            }

            QHeaderView::section {
                background-color: #1565c0;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
                font-size: 15px;
            }
        """)

        self.initUI()

    # -------------------- UI SETUP --------------------
    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("📊 Attendance Reports")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("View attendance history, filter by subject or student, and analyze daily reports.")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #1a237e; margin-bottom: 10px;")

        # Filter Card
        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_card.setStyleSheet("""
            QFrame#filterCard {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #ddd;
                padding: 20px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            }
        """)

        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setSpacing(15)
        filter_layout.setAlignment(Qt.AlignCenter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by name or date (YYYY-MM-DD)")
        self.search_input.setFixedWidth(300)

        self.subject_filter = QComboBox()
        self.subject_filter.addItems([
            "All Subjects", "English", "Maths", "Computer Science",
            "Science", "Hindi", "Social Science"
        ])
        self.subject_filter.setFixedWidth(200)

        search_btn = QPushButton("Search")
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("refreshBtn")

        search_btn.clicked.connect(self.load_filtered_data)
        refresh_btn.clicked.connect(self.load_all_data)

        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.subject_filter)
        filter_layout.addWidget(search_btn)
        filter_layout.addWidget(refresh_btn)

        # Table Section
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Roll No", "Student Name", "Date", "Subject", "Teacher", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(450)

        # Add everything
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(filter_card)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        # Load all data initially
        self.load_all_data()

    # -------------------- LOAD ALL --------------------
    def load_all_data(self):
        """Load all attendance records for the current teacher."""
        try:
            conn = sqlite3.connect("attendance.db")
            cur = conn.cursor()

            teacher_name = global_state.current_teacher or "Unknown Teacher"

            cur.execute("""
                SELECT roll_number, student_name, date, subject, teacher_name, status
                FROM attendance
                WHERE teacher_name = ?
                ORDER BY date DESC
            """, (teacher_name,))

            data = cur.fetchall()
            conn.close()
            self.populate_table(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    # -------------------- LOAD FILTERED --------------------
    def load_filtered_data(self):
        """Filter attendance by name/date and subject."""
        keyword = self.search_input.text().strip()
        subject = self.subject_filter.currentText()
        teacher_name = global_state.current_teacher or "Unknown Teacher"

        query = """
            SELECT roll_number, student_name, date, subject, teacher_name, status
            FROM attendance
            WHERE teacher_name = ?
        """
        params = [teacher_name]

        if keyword:
            query += " AND (student_name LIKE ? OR date LIKE ?)"
            params += [f"%{keyword}%", f"%{keyword}%"]

        if subject != "All Subjects":
            query += " AND subject = ?"
            params.append(subject)

        query += " ORDER BY date DESC"

        try:
            conn = sqlite3.connect("attendance.db")
            cur = conn.cursor()
            cur.execute(query, tuple(params))
            data = cur.fetchall()
            conn.close()
            self.populate_table(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    # -------------------- POPULATE TABLE --------------------
    def populate_table(self, data):
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(data):
            self.table.insertRow(row_num)
            for col_num, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_num, col_num, item)


# -------------------- Run Directly --------------------
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    import global_state

    # For test
    global_state.current_teacher = "DemoTeacher"

    app = QApplication(sys.argv)
    window = ViewReportsWindow()
    window.show()
    sys.exit(app.exec_())
