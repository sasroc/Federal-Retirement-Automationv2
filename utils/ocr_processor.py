import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def parse_ocr_text(text):
    """
    Parse OCR-extracted text to extract retirement application fields.
    Assumes the paper form has labeled fields (e.g., "First Name:").
    """
    data = {}
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Personal Information
        if 'First Name:' in line:
            data['first_name'] = line.split('First Name:')[1].strip()
        elif 'Last Name:' in line:
            data['last_name'] = line.split('Last Name:')[1].strip()
        elif 'Date of Birth:' in line:
            data['dob'] = line.split('Date of Birth:')[1].strip()  # Expect YYYY-MM-DD
        elif 'Social Security Number:' in line:
            data['ssn'] = line.split('Social Security Number:')[1].strip()
        elif 'Address:' in line:
            data['address'] = line.split('Address:')[1].strip()
        elif 'City:' in line:
            data['city'] = line.split('City:')[1].strip()
        elif 'State:' in line:
            data['state'] = line.split('State:')[1].strip()
        elif 'Zip Code:' in line:
            data['zip_code'] = line.split('Zip Code:')[1].strip()
        elif 'Phone Number:' in line:
            data['phone'] = line.split('Phone Number:')[1].strip()
        elif 'Email Address:' in line:
            data['email'] = line.split('Email Address:')[1].strip()
        elif 'U.S. Citizen:' in line:
            data['is_us_citizen'] = 'Yes' in line or 'true' in line.lower()

        # Employment Details
        elif 'Agency:' in line:
            data['agency'] = line.split('Agency:')[1].strip()
        elif 'Position Title:' in line:
            data['position_title'] = line.split('Position Title:')[1].strip()
        elif 'Hire/Start Date:' in line:
            data['hire_date'] = line.split('Hire/Start Date:')[1].strip()  # Expect YYYY-MM-DD
        elif 'Retirement Date:' in line:
            data['retirement_date'] = line.split('Retirement Date:')[1].strip()  # Expect YYYY-MM-DD
        elif 'High-3 Salary:' in line:
            data['salary'] = line.split('High-3 Salary:')[1].strip().replace('$', '').replace(',', '')

        # Benefits Elections
        elif 'Survivor Benefit:' in line:
            data['survivor_benefit'] = line.split('Survivor Benefit:')[1].strip()
        elif 'Continue FEHB:' in line:
            data['fehb_continue'] = 'Yes' in line or 'true' in line.lower()
        elif 'Continue FEGLI:' in line:
            data['fegli_continue'] = 'Yes' in line or 'true' in line.lower()
        elif 'Bank Name:' in line:
            data['bank_name'] = line.split('Bank Name:')[1].strip()
        elif 'Account Number:' in line:
            data['account_number'] = line.split('Account Number:')[1].strip()
        elif 'Routing Number:' in line:
            data['routing_number'] = line.split('Routing Number:')[1].strip()

        # Military Service
        elif 'Served in Armed Forces:' in line:
            data['served_military'] = 'Yes' in line or 'true' in line.lower()
        elif 'Receiving Military Retired Pay:' in line:
            data['military_retired_pay'] = 'Yes' in line or 'true' in line.lower()
        elif 'Waived Military Pay for CSRS/FERS:' in line:
            data['waived_military_pay'] = 'Yes' in line or 'true' in line.lower()

        # Additional Information
        elif 'Unused Sick Leave Hours:' in line:
            data['sick_leave_hours'] = line.split('Unused Sick Leave Hours:')[1].strip()
        elif 'Court Orders for Former Spouses:' in line:
            data['has_court_orders'] = 'Yes' in line or 'true' in line.lower()

    # Default values or cleanup
    for key in ['salary', 'sick_leave_hours']:
        if key in data and data[key]:
            try:
                data[key] = float(data[key])
            except ValueError:
                data[key] = 0
    for key in ['is_us_citizen', 'fehb_continue', 'fegli_continue', 'served_military', 
                'military_retired_pay', 'waived_military_pay', 'has_court_orders']:
        if key in data:
            data[key] = bool(data[key])

    return data