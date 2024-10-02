import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials to access the Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Define the mapping between sheet names and text file names
sheet_file_mapping = {
    'sheet1': 'domain/sheet1.txt',
    'sheet2': 'domain/sheet2.txt',
    'sheet3': 'domain/sheet3.txt',
    'sheet4': 'domain/sheet4.txt',
    'sheet5': 'domain/sheet5.txt',
    'sheet6': 'domain/sheet6.txt'
}

# Function to fetch data from Google Sheets and write to text files
def fetch_and_write_data():
    # Open the Google Sheets file by its ID
    sheet = client.open_by_key('replace with your google sheet file ID')

    for sheet_name, file_name in sheet_file_mapping.items():
        # Open the specific sheet by name
        worksheet = sheet.worksheet(sheet_name)

        # Fetch values from the range 
        values = worksheet.get('replace with your sheet range')

        # Write values to the corresponding text file
        with open(file_name, 'w') as file:
            for row in values:
                file.write(row[0] + '\n')  # Each row contains a single value in column B

# Call the function to fetch and write data
fetch_and_write_data()
