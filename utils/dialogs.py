from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
import sqlite3

class NoteDialog(QDialog):
    def __init__(self, application_id, note_type="denial", parent=None):
        super().__init__(parent)
        self.application_id = application_id
        self.note_type = note_type  # "denial" or "additional_info"
        self.setWindowTitle(f"Add {self.note_type.replace('_', ' ').title()} Note")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Customize label based on note_type
        label_text = "Enter a note for denying this application:" if note_type == "denial" else "Enter a note for requesting additional information:"
        layout.addWidget(QLabel(label_text, styleSheet="color: #ffffff; font-size: 14px;"))
        self.note_text = QTextEdit()
        layout.addWidget(self.note_text)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 3px;")
        save_btn.clicked.connect(self.save_note)
        layout.addWidget(save_btn)

    def save_note(self):
        note = self.note_text.toPlainText().strip()
        if note:
            conn = sqlite3.connect('retirement.db')
            cursor = conn.cursor()
            if self.note_type == "denial":
                cursor.execute("UPDATE Applications SET denial_note = ?, status = 'Denied' WHERE application_id = ?", 
                               (note, self.application_id))
            else:  # additional_info
                cursor.execute("UPDATE Applications SET additional_info_note = ?, status = 'Needs Additional Info' WHERE application_id = ?", 
                               (note, self.application_id))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", f"{self.note_type.replace('_', ' ').title()} note saved successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a note before saving.")

class ViewNotesDialog(QDialog):
    def __init__(self, application_id, note_type="denial", parent=None):
        super().__init__(parent)
        self.application_id = application_id
        self.note_type = note_type  # "denial" or "additional_info"
        self.setWindowTitle(f"View {self.note_type.replace('_', ' ').title()} Notes for Application {application_id}")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        column = "denial_note" if note_type == "denial" else "additional_info_note"
        cursor.execute(f"SELECT {column} FROM Applications WHERE application_id = ?", (application_id,))
        note = cursor.fetchone()
        conn.close()

        if note and note[0]:
            layout.addWidget(QLabel(f"{self.note_type.replace('_', ' ').title()} Note:\n\n{note[0]}", styleSheet="color: #ffffff; font-size: 14px;"))
        else:
            layout.addWidget(QLabel(f"No {self.note_type.replace('_', ' ').title()} notes available.", styleSheet="color: #ffffff; font-size: 14px;"))

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #757575; color: white; padding: 5px; border-radius: 3px;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)