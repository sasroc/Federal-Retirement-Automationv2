import tkinter as tk
from tkinter import ttk, messagebox
from models.employee import Employee
from models.service_history import ServiceHistory
from models.salary_history import SalaryHistory
from models.leave_balances import LeaveBalances
from utils.calculations import calculate_age, calculate_years_of_service, is_eligible, calculate_annuity

class RetirementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Federal Retirement Automation")
        self.geometry("800x600")
        self.employee_data = {}
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        self.pages = {}
        self.entries = {}

        # Create pages
        for page_name in ["Personal", "Service", "Salary", "Leave", "Submit"]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=page_name)
            self.pages[page_name] = frame

        self.setup_personal_page()
        self.setup_service_page()
        self.setup_salary_page()
        self.setup_leave_page()
        self.setup_submit_page()

    def setup_personal_page(self):
        frame = self.pages["Personal"]
        labels = ["First Name", "Last Name", "Date of Birth (YYYY-MM-DD)", "Address", "City", "State", "Zip Code", "Email", "Phone Number", "SSN"]
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

    def setup_service_page(self):
        frame = self.pages["Service"]
        labels = ["Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)", "Position", "Agency"]
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

    def setup_salary_page(self):
        frame = self.pages["Salary"]
        labels = ["Effective Date (YYYY-MM-DD)", "Annual Salary"]
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

    def setup_leave_page(self):
        frame = self.pages["Leave"]
        labels = ["Annual Leave Hours", "Sick Leave Hours"]
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

    def setup_submit_page(self):
        frame = self.pages["Submit"]
        ttk.Button(frame, text="Submit Application", command=self.submit).grid(row=0, column=0, padx=5, pady=20)

    def submit(self):
        # Collect Personal Info
        emp = Employee(
            self.entries["First Name"].get(),
            self.entries["Last Name"].get(),
            self.entries["Date of Birth (YYYY-MM-DD)"].get(),
            self.entries["Address"].get(),
            self.entries["City"].get(),
            self.entries["State"].get(),
            self.entries["Zip Code"].get(),
            self.entries["Email"].get(),
            self.entries["Phone Number"].get(),
            self.entries["SSN"].get()
        )
        employee_id = emp.save()

        # Collect Service History
        svc = ServiceHistory(
            employee_id,
            self.entries["Start Date (YYYY-MM-DD)"].get(),
            self.entries["End Date (YYYY-MM-DD)"].get(),
            self.entries["Position"].get(),
            self.entries["Agency"].get()
        )
        svc.save()

        # Collect Salary History
        sal = SalaryHistory(
            employee_id,
            self.entries["Effective Date (YYYY-MM-DD)"].get(),
            float(self.entries["Annual Salary"].get())
        )
        sal.save()

        # Collect Leave Balances
        leave = LeaveBalances(
            employee_id,
            float(self.entries["Annual Leave Hours"].get()),
            float(self.entries["Sick Leave Hours"].get())
        )
        leave.save()

        # Process Application
        age = calculate_age(emp.date_of_birth)
        service_years = calculate_years_of_service([(svc.start_date, svc.end_date)])
        eligible = is_eligible(age, service_years)
        if eligible:
            annuity = calculate_annuity(service_years, sal.annual_salary)
            messagebox.showinfo("Result", f"Application approved!\nMonthly Annuity: ${annuity:.2f}")
        else:
            messagebox.showinfo("Result", "Application denied. Eligibility criteria not met.")