from datetime import datetime

def calculate_age(dob):
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return age

def is_eligible(age, years_service):
    # Simplified FERS rules
    return (age >= 62 and years_service >= 5) or (age >= 55 and years_service >= 30)

def calculate_annuity(years_service, high_three, age):
    multiplier = 0.011 if (age >= 62 and years_service >= 20) else 0.01
    return multiplier * high_three * years_service