import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance App - Register")
        self.setGeometry(200, 50, 850, 1000)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: Segoe UI;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ced4da;
                background: white;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size:16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QLabel {
                color: #212529;
            }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Create a New Account")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        self.role = QComboBox()
        self.role.addItems(["Select Role", "Student", "Teacher"])
        self.role.currentTextChanged.connect(self.update_id_placeholder)

        # 🔹 New field for Roll No / Teacher ID
        self.id_field = QLineEdit()
        self.id_field.setPlaceholderText("Enter Roll No / Teacher ID")

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)

        self.message = QLabel("")
        self.message.setStyleSheet("color: red; font-size: 12px;")
        self.message.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)
        layout.addWidget(self.role)
        layout.addWidget(self.id_field)
        layout.addSpacing(15)
        layout.addWidget(register_btn)
        layout.addSpacing(10)
        layout.addWidget(self.message)

        self.setLayout(layout)

    def update_id_placeholder(self):
        """Change placeholder dynamically based on role."""
        role = self.role.currentText()
        if role == "Student":
            self.id_field.setPlaceholderText("Enter Roll Number")
        elif role == "Teacher":
            self.id_field.setPlaceholderText("Enter Teacher ID")
        else:
            self.id_field.setPlaceholderText("Enter Roll No / Teacher ID")

    def handle_register(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        confirm_password = self.confirm_password.text().strip()
        role = self.role.currentText()
        user_id = self.id_field.text().strip()

        if not username or not password or not confirm_password or not user_id or role == "Select Role":
            self.message.setText("⚠️ Please fill in all fields.")
            return

        if password != confirm_password:
            self.message.setText("⚠️ Passwords do not match.")
            return

        try:
            conn = sqlite3.connect("logindata.db")
            cur = conn.cursor()

            # Ensure table has the new column before insert
            cur.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cur.fetchall()]
            if "user_id" not in columns:
                cur.execute("ALTER TABLE users ADD COLUMN user_id TEXT")

            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            if cur.fetchone():
                self.message.setText("⚠️ Username already exists.")
                conn.close()
                return

            cur.execute("INSERT INTO users (username, password, role, user_id) VALUES (?, ?, ?, ?)",
                        (username, password, role, user_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Registration Successful", "Account created successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())
