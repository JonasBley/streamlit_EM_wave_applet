import toml
import gspread
from google.oauth2.service_account import Credentials

# 1. Manually load the Streamlit secrets file
secrets = toml.load(".streamlit/secrets.toml")
creds_dict = dict(secrets["connections"]["gsheets"])

# 2. Fix the newline characters
creds_dict["private_key"] = creds_dict["private_key"].replace('\\n', '\n')

# 3. Authenticate
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

try:
    # 4. Attempt to open the sheet (Make sure this is your actual URL!)
    SHEET_URL = "https://docs.google.com/spreadsheets/d/14u3OWvARHLNxXSSHllmBHj4wy5Lc7LTq0uMMVDFXkV0/edit"
    sheet = client.open_by_url(SHEET_URL).sheet1

    # 5. Attempt a blind append
    sheet.append_row(["Auth Test Successful!", "12345"])
    print("✅ SUCCESS! The robot successfully wrote to your Google Sheet.")

except Exception as e:
    print(f"❌ FAILED: {e}")