from datetime import datetime

def calculate_age(date_of_birth):
    dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def calculate_years_of_service(service_history):
    total_days = 0
    for start, end in service_history:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d') if end else datetime.now()
        total_days += (end_date - start_date).days
    return total_days / 365.25

def is_eligible(age, years_of_service):
    return (age >= 55 and years_of_service >= 10) or (years_of_service >= 20)

def calculate_annuity(years_of_service, high_salary):
    # Simplified FERS annuity: 1% of high-3 salary per year of service
    return (0.01 * high_salary) * years_of_service