# 🚀 Deployment Guide - LuxQuant Registration

## Deployment Options

### Option 1: Local Development (Recommended untuk testing)
### Option 2: Streamlit Cloud (Production)

---

## 📋 Pre-Deployment Checklist

Before deploying, verify:

- [ ] Google Cloud Project created
- [ ] Google Sheets API enabled
- [ ] Google Drive API enabled
- [ ] Service Account created with Editor role
- [ ] Google Sheet shared with service account email
- [ ] Google Drive folder shared with service account email
- [ ] `.streamlit/secrets.toml` file configured correctly
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Verification script passed (`python verify_setup.py`)

---

## 🏠 Option 1: Local Development

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Verify Setup

```bash
python verify_setup.py
```

Expected output:
```
✅ ALL CHECKS PASSED!
```

### Step 3: Run Application

```bash
streamlit run app.py
```

App akan buka di: `http://localhost:8501`

### Step 4: Test Features

1. **Test Registration Form:**
   - Fill all fields
   - Upload test image
   - Submit
   - Check Google Sheet untuk data baru
   - Check Google Drive untuk uploaded image

2. **Test Dashboard:**
   - Navigate to "User Dashboard"
   - Verify data ditampilkan
   - Test filter by package
   - Test search functionality
   - Test CSV export
   - Click Telegram & Explorer links

---

## ☁️ Option 2: Streamlit Cloud Deployment

### Step 1: Prepare Repository

#### 1.1 Initialize Git

```bash
cd luxquant-registration
git init
```

#### 1.2 Create GitHub Repository

1. Buka https://github.com
2. Click "New repository"
3. Nama: `luxquant-registration`
4. Privacy: **Private** (recommended untuk production)
5. Click "Create repository"

#### 1.3 Push to GitHub

```bash
git add .
git commit -m "Initial commit - LuxQuant Registration System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/luxquant-registration.git
git push -u origin main
```

**IMPORTANT:** File `secrets.toml` **TIDAK** akan di-push karena ada di `.gitignore`

### Step 2: Deploy to Streamlit Cloud

#### 2.1 Login to Streamlit Cloud

1. Buka https://share.streamlit.io/
2. Click "Sign in with GitHub"
3. Authorize Streamlit

#### 2.2 Create New App

1. Click **"New app"** button
2. Select:
   - **Repository:** YOUR_USERNAME/luxquant-registration
   - **Branch:** main
   - **Main file path:** app.py
3. Click **"Advanced settings..."**

#### 2.3 Configure Secrets

1. Di Advanced settings, scroll ke **"Secrets"**
2. Copy **SELURUH ISI** file `.streamlit/secrets.toml`
3. Paste ke field Secrets
4. Verify formatnya tetap sama (TOML format)

**Example:**
```toml
[gcp_service_account]
type = "service_account"
project_id = "luxquant-user-registration"
private_key_id = "6dd3d738fc127bfb51fca925370dd7df9932a888"
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwBF+D7EZJFgiY
...
-----END PRIVATE KEY-----"""
client_email = "luxquant-form-registration@..."
...

[google_config]
sheet_id = "1XPcxjUYZMn4NLd6pVOPDdeHR3s-YdeDPZ1X26INeWg0"
folder_id = "1L5nHnGlItPIjGriqE_JN16UECTEpOsT8"
```

#### 2.4 Deploy

1. Click **"Deploy!"**
2. Wait 2-5 minutes for deployment
3. App URL akan berupa: `https://YOUR_APP_NAME.streamlit.app`

### Step 3: Post-Deployment Verification

#### 3.1 Test Registration

1. Buka deployed app URL
2. Fill registration form dengan test data
3. Upload test image
4. Submit
5. Check:
   - [ ] Success message muncul
   - [ ] Data masuk ke Google Sheet
   - [ ] Image uploaded ke Google Drive

#### 3.2 Test Dashboard

1. Navigate ke User Dashboard
2. Verify:
   - [ ] Data ditampilkan correctly
   - [ ] Metrics (Total Users, Monthly, dll) benar
   - [ ] Filter working
   - [ ] Search working
   - [ ] Images preview working
   - [ ] Telegram links working (open Telegram)
   - [ ] Explorer links working (open blockchain explorer)
   - [ ] CSV export working

---

## 🔧 Post-Deployment Configuration

### Custom Domain (Optional)

Streamlit Cloud support custom domains:

1. Go to app settings
2. Click "Custom domain"
3. Add your domain (misal: `register.luxquant.com`)
4. Follow DNS configuration instructions

### App Settings

Configure di Streamlit Cloud dashboard:
- **App name:** LuxQuant User Registration
- **Privacy:** Private (hanya accessible via link)
- **Resources:** Default (upgrade jika needed)

---

## 📊 Monitoring & Maintenance

### 1. Monitor Google Sheets

Regularly check:
- Data integrity
- No duplicate entries
- Proper formatting

### 2. Monitor Google Drive

Check:
- Storage usage
- Image accessibility
- Folder organization

### 3. App Performance

Monitor di Streamlit Cloud:
- Load times
- Error logs
- Resource usage

### 4. Update Secrets (if needed)

If you need to update credentials:

1. Go to Streamlit Cloud app settings
2. Click "Secrets"
3. Update values
4. Click "Save"
5. App will auto-restart

---

## 🐛 Troubleshooting

### Issue: "Permission denied" error

**Solution:**
1. Verify service account email shared to Sheet & Drive
2. Check role is **Editor**, not Viewer
3. Try re-sharing with explicit email

### Issue: Images tidak muncul

**Solution:**
1. Check Drive folder permissions
2. Verify `webViewLink` permission set to "anyone with link"
3. Check image URL format correct

### Issue: "Module not found"

**Solution:**
1. Verify `requirements.txt` complete
2. Force rebuild di Streamlit Cloud:
   - Settings → "Reboot app"
   - Or push dummy commit

### Issue: Secrets tidak loaded

**Solution:**
1. Check TOML format benar (no syntax errors)
2. Verify indentation correct
3. Check private_key dalam triple quotes
4. No trailing spaces

---

## 🔄 Updating the App

### For Code Changes:

```bash
# Make changes to code
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud akan auto-deploy update.

### For Secrets Changes:

1. Go to Streamlit Cloud settings
2. Update secrets directly
3. Save → app auto-restarts

---

## 📞 Support Contacts

**Google Cloud Issues:**
- Console: https://console.cloud.google.com

**Streamlit Issues:**
- Docs: https://docs.streamlit.io
- Community: https://discuss.streamlit.io

**GitHub Issues:**
- Create issue di repository

---

## ✅ Success Criteria

Your deployment is successful when:

- ✅ App accessible via public URL
- ✅ Registration form works end-to-end
- ✅ Images upload to Drive successfully
- ✅ Data saves to Google Sheets
- ✅ Dashboard displays all data
- ✅ All links (Telegram, Explorer) working
- ✅ Export to CSV works
- ✅ No errors in logs

---

**Congratulations! Your LuxQuant Registration System is now live! 🎉**
