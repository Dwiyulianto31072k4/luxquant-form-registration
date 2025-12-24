import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import pandas as pd
from io import BytesIO
from datetime import datetime

class GoogleServices:
    def __init__(self):
        """Initialize Google Sheets and Drive services"""
        # Get credentials from Streamlit secrets
        self.credentials_dict = dict(st.secrets["gcp_service_account"])
        self.sheet_id = st.secrets["google_config"]["sheet_id"]
        self.folder_id = st.secrets["google_config"]["folder_id"]
        
        # Setup credentials
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        self.credentials = Credentials.from_service_account_info(
            self.credentials_dict,
            scopes=self.scopes
        )
        
        # Initialize services
        self.sheets_client = gspread.authorize(self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        
        # Open the sheet
        self.sheet = self.sheets_client.open_by_key(self.sheet_id).sheet1
        
        # Initialize headers if needed
        self._initialize_sheet()
    
    def _initialize_sheet(self):
        """Initialize sheet with headers if empty"""
        try:
            headers = self.sheet.row_values(1)
            if not headers:
                headers = [
                    "Timestamp",
                    "Nama User",
                    "Telegram User ID",
                    "Telegram Link",
                    "Paket",
                    "Harga (USDT)",
                    "Tanggal Mulai",
                    "Blockchain Network",
                    "Transaction Hash",
                    "Explorer Link",
                    "Bukti Transfer"
                ]
                self.sheet.append_row(headers)
        except Exception as e:
            st.error(f"Error initializing sheet: {str(e)}")
    
    def upload_image_to_drive(self, uploaded_file, user_name):
        """Upload image to Google Drive and return shareable link"""
        try:
            # Prepare file metadata
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{user_name.replace(' ', '_')}_{timestamp}.{uploaded_file.name.split('.')[-1]}"
            
            file_metadata = {
                'name': file_name,
                'parents': [self.folder_id]
            }
            
            # Upload file
            media = MediaIoBaseUpload(
                BytesIO(uploaded_file.read()),
                mimetype=uploaded_file.type,
                resumable=True
            )
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            # Make file publicly accessible
            self.drive_service.permissions().create(
                fileId=file['id'],
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()
            
            # Get direct image link
            file_id = file['id']
            direct_link = f"https://drive.google.com/uc?export=view&id={file_id}"
            
            return direct_link
            
        except Exception as e:
            raise Exception(f"Error uploading image: {str(e)}")
    
    def append_to_sheet(self, user_data):
        """Append user data to Google Sheets"""
        try:
            row = [
                user_data["Timestamp"],
                user_data["Nama User"],
                user_data["Telegram User ID"],
                user_data["Telegram Link"],
                user_data["Paket"],
                user_data["Harga (USDT)"],
                user_data["Tanggal Mulai"],
                user_data["Blockchain Network"],
                user_data["Transaction Hash"],
                user_data["Explorer Link"],
                user_data["Bukti Transfer"]
            ]
            
            self.sheet.append_row(row)
            
        except Exception as e:
            raise Exception(f"Error saving to sheet: {str(e)}")
    
    def get_all_users(self):
        """Get all users from Google Sheets as DataFrame"""
        try:
            data = self.sheet.get_all_records()
            df = pd.DataFrame(data)
            
            # Convert price to float
            if not df.empty and 'Harga (USDT)' in df.columns:
                df['Harga (USDT)'] = pd.to_numeric(df['Harga (USDT)'], errors='coerce')
            
            return df
            
        except Exception as e:
            raise Exception(f"Error reading sheet: {str(e)}")
