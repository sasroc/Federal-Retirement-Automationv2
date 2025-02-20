from datetime import datetime

def calculate_age(dob):
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return age

def is_eligible(age, years_service):
    # FERS eligibility rules (simplified)
    return (age >= 62 and years_service >= 5) or (age >= 55 and years_service >= 30) or (years_service >= 20)

def calculate_annuity(years_service, high_three_salary, age):
    # FERS annuity formula: 1% of high-3 salary per year, or 1.1% if age >= 62 and years >= 20
    multiplier = 0.011 if (age >= 62 and years_service >= 20) else 0.01
    return multiplier * high_three_salary * years_service

def calculate_unused_sick_leave_bonus(years_service, sick_leave_hours):
    # Simplified: 174 hours of sick leave = 1 month (1/12 year) added to service
    months = sick_leave_hours // 174
    return years_service + (months / 12)