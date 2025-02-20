from PyQt6.QtWidgets import QMessageBox

def notify_employee(parent, app_id, benefits):
    QMessageBox.information(parent, "Notification", 
                            f"Application {app_id} Approved\nAnnual Benefits: ${benefits:,.2f}")