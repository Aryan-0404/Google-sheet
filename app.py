from flask import Flask, jsonify
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Function to initialize Google Sheets
def initialize_google_sheets(credentials_file, sheet_url):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet

# API route to fetch a random comment
@app.route('/random_comment', methods=['GET'])
def get_random_comment():
    try:
        # Update these paths with your credentials and sheet URL
        credentials_file = "credentials.json"  # Path to your JSON key file
        sheet_url = "https://docs.google.com/spreadsheets/d/your_sheet_id/edit"  # Your sheet URL
        
        # Initialize the sheet
        sheet = initialize_google_sheets(credentials_file, sheet_url)
        
        # Get all comments from the sheet (assuming comments are in the first column)
        comments = sheet.col_values(1)  # Replace '1' with the correct column index for comments
        
        if not comments:
            return jsonify({"status": "No comments available"}), 404

        # Pick a random comment
        random_comment = random.choice(comments)
        return jsonify({"random_comment": random_comment}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
