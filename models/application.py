# models/application.py
import sqlite3

class Application:
    def __init__(self, employee_id, years_service, retirement_date, salary, agency, position_title, 
                 survivor_benefit, fehb_continue, fegli_continue, bank_name, account_number, 
                 routing_number, served_military, military_retired_pay, waived_military_pay, 
                 sick_leave_hours, has_court_orders, hire_date=None):
        self.employee_id = employee_id
        self.years_service = float(years_service) if years_service else 0
        self.retirement_date = retirement_date
        self.salary = float(salary)
        self.agency = agency
        self.position_title = position_title
        self.survivor_benefit = survivor_benefit
        self.fehb_continue = fehb_continue
        self.fegli_continue = fegli_continue
        self.bank_name = bank_name
        self.account_number = account_number
        self.routing_number = routing_number
        self.served_military = served_military
        self.military_retired_pay = military_retired_pay
        self.waived_military_pay = waived_military_pay
        self.sick_leave_hours = float(sick_leave_hours) if sick_leave_hours else 0
        self.has_court_orders = has_court_orders
        self.hire_date = hire_date

    def save(self):
        conn = sqlite3.connect('retirement.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Applications (employee_id, years_service, retirement_date, salary, agency, position_title, 
                                     survivor_benefit, fehb_continue, fegli_continue, bank_name, account_number, 
                                     routing_number, served_military, military_retired_pay, waived_military_pay, 
                                     sick_leave_hours, has_court_orders, hire_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.employee_id, self.years_service, self.retirement_date, self.salary, self.agency, 
              self.position_title, self.survivor_benefit, self.fehb_continue, self.fegli_continue, 
              self.bank_name, self.account_number, self.routing_number, self.served_military, 
              self.military_retired_pay, self.waived_military_pay, self.sick_leave_hours, 
              self.has_court_orders, self.hire_date))
        conn.commit()
        conn.close()