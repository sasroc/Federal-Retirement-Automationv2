from gui.application import RetirementApp
from utils.database import create_database

if __name__ == "__main__":
    create_database()  # Initialize the database
    app = RetirementApp()
    app.mainloop()