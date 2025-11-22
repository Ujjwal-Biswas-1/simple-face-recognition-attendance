import sqlite3

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QMessageBox, QCheckBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
from db__initializer import init_databases

from teacher_dashboard import TeacherDashboard
from student_dashboard import StudentDashboard
from register import RegisterWindow
import global_state


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance App - Login")
        self.setGeometry(200, 50, 850, 1000)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: Segoe UI;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #ced4da;
                background: white;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border-radius: 6px;
                border: none;
                font-size:16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                color: #212529;
            }
            QCheckBox {
                color: #212529;
            }
        """)
        self.initUI()

    def initUI(self):
        # Main outer layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(80, 100, 80, 100)

        # --- Card Widget (Container for the form) ---
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(15)
        card.setMaximumWidth(600)
        card.setMinimumSize(300, 600)

        # --- Title ---
        title = QLabel("Siksha+")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        title1 = QLabel("Login")
        title1.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title1.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Smart Attendance Portal")
        font = QFont("Segoe UI", 14, QFont.Bold)
        font.setUnderline(True)
        subtitle.setFont(font)
        subtitle.setAlignment(Qt.AlignCenter)

        # --- Input fields ---
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.show_password = QCheckBox("Show Password")
        self.show_password.stateChanged.connect(
            self.toggle_password_visibility)

        self.role = QComboBox()
        self.role.addItems(["Select Role", "Student", "Teacher"])

        # --- Buttons ---
        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")
        forgot_btn = QPushButton("Forgot Password")

        login_btn.clicked.connect(self.handle_login)
        register_btn.clicked.connect(self.handle_register)
        forgot_btn.clicked.connect(self.handle_forgot_password)

        # --- Message label ---
        self.message = QLabel("")
        self.message.setStyleSheet("color: red; font-size: 12px;")
        self.message.setAlignment(Qt.AlignCenter)

        # --- Add widgets to card layout ---
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(title1)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.show_password)
        card_layout.addWidget(self.role)
        card_layout.addSpacing(10)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(register_btn)
        card_layout.addWidget(forgot_btn)
        card_layout.addSpacing(15)
        card_layout.addWidget(self.message)

        card.setLayout(card_layout)
        card.setStyleSheet("""
            QWidget#card {
                background-color: white;
                border-radius: 15px;
                padding: 40px;
                border: 2px solid #ccc;
            }
        """)

        # --- Add card to main layout ---
        layout.addWidget(card)
        self.setLayout(layout)

    # ------------------------------
    #       Helper Functions
    # ------------------------------
    def toggle_password_visibility(self):
        if self.show_password.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText()

        if not username or not password or role == "Select Role":
            self.message.setText("⚠️ Please fill in all fields correctly.")
            return

        try:
            conn = sqlite3.connect("logindata.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username=? AND password=? AND role=?",
                (username, password, role)
            )
            result = cur.fetchone()
            conn.close()

            if result:
                QMessageBox.information(
                    self, "Login Success", f"Welcome {role} {username}!")
                self.hide()

                if role == "Teacher":
                    global_state.current_teacher = username
                    self.dashboard = TeacherDashboard(username)
                else:
                    self.dashboard = StudentDashboard(username)
                self.dashboard.show()
            else:
                QMessageBox.warning(self, "Login Failed",
                                    "Invalid username, password, or role!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def handle_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def handle_forgot_password(self):
        QMessageBox.information(self, "Forgot Password",
                                "Please contact your teacher/admin to reset your password..")


# ------------------------------
#          MAIN
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
