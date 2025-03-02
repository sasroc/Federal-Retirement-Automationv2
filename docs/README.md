# Federal Retirement Automation

A Python application to automate the federal employee retirement process.

## Setup
1. Clone the repository: `git clone https://github.com/[your-username]/federal-retirement-automation.git`
2. Navigate to the directory: `cd federal-retirement-automation`
3. Install dependencies: `pip install -r requirements.txt`
   - Install Tesseract OCR and ensure it's in your PATH.
   - Install Poppler for PDF processing (e.g., `brew install poppler` on macOS or `apt-get install poppler-utils` on Ubuntu).
4. Run the application: `python main.py`

## Usage
- Login with role-based credentials (e.g., `employee`/`emp123`, `processor`/`proc123`, `supervisor`/`super123`).
- **Employee**: Enter personal info, service history, salary, and benefits elections; optionally upload a form (PDF/image) for OCR extraction. Submit for processing. Use exampletestdoc.txt to either upload as screenshot, or convert to .pdf and upload to test the program. 
- **Processor**: Review applications, verify eligibility and benefits, and submit to supervisors or request more info.
- **Supervisor**: Approve or deny applications, add denial notes, and view detailed records.

## Limitations
- No access to external databases (e.g., Social Security, OPM).
- Simplified annuity calculation for proof of concept.
- Hardcoded login credentials (demo only; use secure authentication in production).

## License
MIT License
