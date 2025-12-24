"""
Setup Verification Script
Run this to verify all configurations are correct before deployment
"""

import sys

def verify_setup():
    print("=" * 60)
    print("LuxQuant Registration - Setup Verification")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Check Python version
    print("\n1. Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"   ✅ Python {sys.version.split()[0]} (OK)")
    else:
        errors.append("Python 3.8+ required")
        print(f"   ❌ Python {sys.version.split()[0]} (Too old)")
    
    # 2. Check dependencies
    print("\n2. Checking dependencies...")
    required_packages = [
        'streamlit',
        'gspread',
        'google.auth',
        'pandas',
        'PIL'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('.', '_') if '.' in package else package)
            print(f"   ✅ {package}")
        except ImportError:
            errors.append(f"Missing package: {package}")
            print(f"   ❌ {package}")
    
    # 3. Check secrets file
    print("\n3. Checking secrets configuration...")
    try:
        import streamlit as st
        
        # Check GCP credentials
        if "gcp_service_account" in st.secrets:
            required_keys = ['type', 'project_id', 'private_key', 'client_email']
            missing_keys = [k for k in required_keys if k not in st.secrets["gcp_service_account"]]
            
            if missing_keys:
                errors.append(f"Missing keys in gcp_service_account: {missing_keys}")
                print(f"   ❌ GCP credentials incomplete")
            else:
                print(f"   ✅ GCP service account credentials")
        else:
            errors.append("Missing gcp_service_account in secrets")
            print(f"   ❌ GCP credentials not found")
        
        # Check Google config
        if "google_config" in st.secrets:
            if "sheet_id" in st.secrets["google_config"] and "folder_id" in st.secrets["google_config"]:
                print(f"   ✅ Google Sheet & Drive configuration")
            else:
                errors.append("Missing sheet_id or folder_id in google_config")
                print(f"   ❌ Sheet/Drive IDs not configured")
        else:
            errors.append("Missing google_config in secrets")
            print(f"   ❌ Google config not found")
            
    except Exception as e:
        errors.append(f"Error reading secrets: {str(e)}")
        print(f"   ❌ Secrets file error: {str(e)}")
    
    # 4. Test Google Services connection
    print("\n4. Testing Google Services connection...")
    try:
        from google_services import GoogleServices
        gs = GoogleServices()
        print(f"   ✅ Google Sheets connection")
        print(f"   ✅ Google Drive connection")
        
        # Try to read sheet
        df = gs.get_all_users()
        print(f"   ✅ Sheet accessible (current rows: {len(df)})")
        
    except Exception as e:
        errors.append(f"Google Services error: {str(e)}")
        print(f"   ❌ Connection failed: {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if not errors and not warnings:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYou can now run the app with:")
        print("   streamlit run app.py")
        print("\nOr deploy to Streamlit Cloud!")
    else:
        if errors:
            print(f"\n❌ ERRORS FOUND ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"   {i}. {warning}")
        
        print("\nPlease fix the errors above before running the app.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    verify_setup()
