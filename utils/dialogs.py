from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
import sqlite3
from datetime import datetime

class NoteDialog(QDialog):
    def __init__(self, application_id, note_type="denial", parent=None):
        super().__init__(parent)
        self.application_id = application_id
        self.note_type = note_type
        self.setWindowTitle(f"Add {self.note_type.replace('_', ' ').title()} Note")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

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
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Fetch current note_history
            cursor.execute("SELECT note_history FROM Applications WHERE application_id = ?", (self.application_id,))
            current_history = cursor.fetchone()[0] or ""
            
            if self.note_type == "denial":
                # Append denial note to history and set denial_note
                new_entry = f"{timestamp}: Denied - {note}"
                updated_history = f"{current_history}\n{new_entry}" if current_history else new_entry
                cursor.execute("UPDATE Applications SET denial_note = ?, note_history = ? WHERE application_id = ?", 
                               (note, updated_history, self.application_id))
            else:  # additional_info
                # Append additional info note to history and set additional_info_note
                new_entry = f"{timestamp}: Needs Info - {note}"
                updated_history = f"{current_history}\n{new_entry}" if current_history else new_entry
                cursor.execute("UPDATE Applications SET additional_info_note = ?, status = 'Needs Additional Info', note_history = ? WHERE application_id = ?", 
                               (note, updated_history, self.application_id))
            
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
        self.note_type = note_type
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

class NoteHistoryDialog(QDialog):
    def __init__(self, application_id, parent=None):
        super().__init__(parent)
        self.application_id = application_id
        self.setWindowTitle(f"Note History for Application {application_id}")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT note_history FROM Applications WHERE application_id = ?", (application_id,))
        history = cursor.fetchone()
        conn.close()

        if history and history[0]:
            layout.addWidget(QLabel(f"Note History:\n\n{history[0]}", styleSheet="color: #ffffff; font-size: 14px;"))
        else:
            layout.addWidget(QLabel("No note history available.", styleSheet="color: #ffffff; font-size: 14px;"))

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #757575; color: white; padding: 5px; border-radius: 3px;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)