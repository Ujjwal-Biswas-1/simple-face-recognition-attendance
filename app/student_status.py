import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QScrollArea, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from db__initializer import init_databases


class StudentStatusWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Status - Teacher Panel")
        self.setGeometry(250, 80, 800, 700)

        # Ensure DBs are initialized
        init_databases()

        # Fetch or sync data
        self.sync_students()
        self.students = self.fetch_student_status()

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e8f0fe, stop:1 #bbdefb
                );
                font-family: 'Segoe UI';
            }
            QLabel {
                color: #0d47a1;
            }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                padding: 10px;
                border-radius: 8px;
                border: none;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
            QCheckBox {
                font-size: 15px;
                color: #212529;
                padding: 4px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QWidget#scrollCard {
                background: white;
                border-radius: 12px;
                border: 1px solid #ccc;
                padding: 15px;
            }
        """)

        self.initUI()

    # -------------------- SYNC STUDENTS --------------------
    def sync_students(self):
        """Ensure every student from logindata.db exists in studentstatus.db."""
        try:
            conn_main = sqlite3.connect("logindata.db")
            cur_main = conn_main.cursor()
            cur_main.execute("SELECT username FROM users WHERE role='Student'")
            students = [s[0] for s in cur_main.fetchall()]
            conn_main.close()

            conn_status = sqlite3.connect("studentstatus.db")
            cur_status = conn_status.cursor()

            for name in students:
                cur_status.execute("SELECT id FROM student_status WHERE student_name=?", (name,))
                if not cur_status.fetchone():
                    cur_status.execute(
                        "INSERT INTO student_status (student_name) VALUES (?)", (name,)
                    )

            conn_status.commit()
            conn_status.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to sync students:\n{str(e)}")

    # -------------------- FETCH DATA --------------------
    def fetch_student_status(self):
        try:
            conn = sqlite3.connect("studentstatus.db")
            cur = conn.cursor()
            cur.execute("SELECT student_name, got_books, got_uniform, fees_paid FROM student_status")
            data = cur.fetchall()
            conn.close()
            return data
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
            return []

    # -------------------- UI SETUP --------------------
    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        title = QLabel("🎓 Student Resource & Fee Status")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Scrollable card area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_card = QWidget()
        scroll_card.setObjectName("scrollCard")
        scroll_layout = QVBoxLayout(scroll_card)
        scroll_layout.setSpacing(10)

        self.checkboxes = {}

        if not self.students:
            scroll_layout.addWidget(QLabel("❌ No student data found."))
        else:
            for student_name, got_books, got_uniform, fees_paid in self.students:
                box_layout = QHBoxLayout()
                box_layout.setSpacing(30)

                name_label = QLabel(f"👤 {student_name}")
                name_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
                name_label.setFixedWidth(200)

                book_cb = QCheckBox("Books Acquired")
                uniform_cb = QCheckBox("Uniform Acquired")
                fees_cb = QCheckBox("Fees Paid")

                # Set checkbox states
                book_cb.setChecked(bool(got_books))
                uniform_cb.setChecked(bool(got_uniform))
                fees_cb.setChecked(bool(fees_paid))

                self.checkboxes[student_name] = (book_cb, uniform_cb, fees_cb)

                box_layout.addWidget(name_label)
                box_layout.addWidget(book_cb)
                box_layout.addWidget(uniform_cb)
                box_layout.addWidget(fees_cb)

                scroll_layout.addLayout(box_layout)

        scroll.setWidget(scroll_card)

        # Update button
        update_btn = QPushButton("💾 Update Student Status")
        update_btn.clicked.connect(self.update_status)
        update_btn.setFixedHeight(45)

        main_layout.addWidget(title)
        main_layout.addWidget(scroll)
        main_layout.addWidget(update_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    # -------------------- UPDATE STATUS --------------------
    def update_status(self):
        try:
            conn = sqlite3.connect("studentstatus.db")
            cur = conn.cursor()

            for student_name, (book_cb, uniform_cb, fees_cb) in self.checkboxes.items():
                cur.execute("""
                    UPDATE student_status
                    SET got_books=?, got_uniform=?, fees_paid=?
                    WHERE student_name=?
                """, (
                    int(book_cb.isChecked()),
                    int(uniform_cb.isChecked()),
                    int(fees_cb.isChecked()),
                    student_name
                ))

            conn.commit()
            conn.close()
            QMessageBox.information(self, "Updated", "✅ Student statuses updated successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update:\n{str(e)}")


# -------------------- Run Directly --------------------
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = StudentStatusWindow()
    window.show()
    sys.exit(app.exec_())
