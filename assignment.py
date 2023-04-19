import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Define the scopes and credentials to access the Google Sheets API
SCOPES = ['https://docs.google.com/spreadsheets/d/1CD_ZszagDlCrYEvKYuav_CxnARYHgVVODdgeHyvzFD4/edit?usp=sharing']
CREDS_FILE = 'manishadoosa-mail-com@cultivated-list-384215.iam.gserviceaccount.com'
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)

# Define the IDs of the input and output sheets
INPUT_SHEET_ID_1 = 'input_sheet_id_1'
INPUT_SHEET_ID_2 = 'input_sheet_id_2'
OUTPUT_SHEET_ID_1 = 'output_sheet_id_1'
OUTPUT_SHEET_ID_2 = 'output_sheet_id_2'

# Open the input sheets and read the data
client = gspread.authorize(creds)
input_sheet_1 = client.open_by_key(INPUT_SHEET_ID_1).sheet1
input_sheet_2 = client.open_by_key(INPUT_SHEET_ID_2).sheet1

input_data_1 = input_sheet_1.get_all_values()
input_data_2 = input_sheet_2.get_all_values()

# Convert the input data to a pandas dataframe and calculate the rankings
df = pd.DataFrame(input_data_1, columns=['Name', 'Sales'])
df['Sales'] = df['Sales'].astype(float)  # Convert the 'Sales' column to float
df['Rank'] = df['Sales'].rank(method='dense', ascending=False)  # Calculate the rankings

# Sort the data by rank and display the leaderboard
output_sheet_1 = client.open_by_key(OUTPUT_SHEET_ID_1).add_worksheet(title='Leaderboard', rows=100, cols=10)
output_sheet_1.update([['Name', 'Sales', 'Rank']] + df.sort_values(by='Rank').values.tolist())

print('Leaderboard created successfully')
