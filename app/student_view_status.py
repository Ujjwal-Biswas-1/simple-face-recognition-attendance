import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt


class StudentViewStatus(QWidget):
    def __init__(self, student_name):
        super().__init__()
        self.student_name = student_name
        self.setWindowTitle(f"📋 Status Overview - {student_name}")
        self.setGeometry(300, 100, 700, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f6ff;
                font-family: 'Segoe UI';
            }
            QLabel#title {
                font-size: 26px;
                font-weight: bold;
                color: #0d47a1;
                margin-bottom: 15px;
            }
            QLabel#statusLabel {
                font-size: 18px;
                font-weight: 600;
                color: #37474f;
            }
            QFrame#card {
                border-radius: 16px;
                padding: 30px;
                margin: 12px;
                color: white;
            }
        """)

        self.initUI()

    # ------------------- UI SETUP -------------------
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("🎒 Student Status Summary")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Fetch status data
        data = self.fetch_student_status()

        if data:
            got_books, got_uniform, fees_paid = data

            # Create a card for each status
            layout.addWidget(self.create_status_card(
                "📚 Books Received", got_books,
                "#4caf50", "#c8e6c9"
            ))

            layout.addWidget(self.create_status_card(
                "👕 Uniform Received", got_uniform,
                "#2196f3", "#bbdefb"
            ))

            layout.addWidget(self.create_status_card(
                "💰 Fees Paid", fees_paid,
                "#ff9800", "#ffe0b2"
            ))

        else:
            layout.addWidget(QLabel("❌ No status record found for this student."))

        self.setLayout(layout)

    # ------------------- Fetch Status Data -------------------
    def fetch_student_status(self):
        try:
            conn = sqlite3.connect("studentstatus.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT got_books, got_uniform, fees_paid
                FROM student_status
                WHERE student_name = ?
            """, (self.student_name,))
            row = cur.fetchone()
            conn.close()
            return row
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            return None

    # ------------------- Create Card -------------------
    def create_status_card(self, title, status_value, color_active, color_inactive):
        card = QFrame()
        card.setObjectName("card")

        palette = card.palette()
        bg_color = QColor(color_active if status_value else color_inactive)
        palette.setColor(QPalette.Window, bg_color)
        card.setAutoFillBackground(True)
        card.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(title)
        label.setObjectName("statusLabel")

        status_text = "✅ Completed" if status_value else "❌ Pending"
        status_display = QLabel(status_text)
        status_display.setFont(QFont("Segoe UI", 16, QFont.Bold))
        status_display.setAlignment(Qt.AlignCenter)
        status_display.setStyleSheet("color: white;" if status_value else "color: #263238;")

        layout.addWidget(label)
        layout.addWidget(status_display)
        card.setLayout(layout)

        return card


# ------------------- Run Standalone -------------------
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = StudentViewStatus("Ujjwal Biswas")  # Example name
    window.show()
    sys.exit(app.exec_())
