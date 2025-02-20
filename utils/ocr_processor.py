import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def parse_ocr_text(text):
    data = {}
    lines = text.split('\n')
    for line in lines:
        if 'First Name:' in line:
            data['first_name'] = line.split(':')[1].strip()
        elif 'Last Name:' in line:
            data['last_name'] = line.split(':')[1].strip()
        elif 'Date of Birth:' in line:
            data['dob'] = line.split(':')[1].strip()
        elif 'Years of Service:' in line:
            data['years_service'] = line.split(':')[1].strip()
        elif 'Retirement Date:' in line:
            data['retirement_date'] = line.split(':')[1].strip()
        elif 'Salary:' in line:
            data['salary'] = line.split(':')[1].strip()
    return data