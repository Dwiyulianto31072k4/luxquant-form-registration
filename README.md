# LuxQuant User Registration System

Streamlit application untuk registrasi dan manajemen user LuxQuant dengan integrasi Google Sheets dan Google Drive.

## 🚀 Features

- ✅ Form registrasi user dengan validasi
- 📊 Dashboard untuk melihat semua user terdaftar
- 🖼️ Upload bukti transfer ke Google Drive
- 🔗 Auto-generate Telegram profile links dan blockchain explorer links
- 📈 Filter dan search functionality
- 💾 Export data ke CSV
- 🔒 Secure credentials management dengan Streamlit Secrets

## 📁 Project Structure

```
luxquant-registration/
├── app.py                      # Main Streamlit application
├── google_services.py          # Google Sheets & Drive integration
├── utils.py                    # Helper functions
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml           # Configuration & credentials (local)
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Secrets

File `.streamlit/secrets.toml` sudah berisi credentials lengkap dari:
- Google Service Account
- Google Sheet ID: `1XPcxjUYZMn4NLd6pVOPDdeHR3s-YdeDPZ1X26INeWg0`
- Google Drive Folder ID: `1L5nHnGlItPIjGriqE_JN16UECTEpOsT8`

**IMPORTANT:** File ini sudah di-exclude dari Git via `.gitignore`

### 3. Verify Google Services Access

Pastikan service account email sudah memiliki akses Editor ke:
- ✅ Google Sheet: https://docs.google.com/spreadsheets/d/1XPcxjUYZMn4NLd6pVOPDdeHR3s-YdeDPZ1X26INeWg0
- ✅ Google Drive Folder: https://drive.google.com/drive/folders/1L5nHnGlItPIjGriqE_JN16UECTEpOsT8

Service Account Email: `luxquant-form-registration@luxquant-user-registration.iam.gserviceaccount.com`

### 4. Run Locally

```bash
streamlit run app.py
```

App akan terbuka di: `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

**Note:** File `secrets.toml` tidak akan ter-push karena ada di `.gitignore`

### Step 2: Deploy di Streamlit Cloud

1. Buka https://share.streamlit.io/
2. Login dengan GitHub
3. Click **"New app"**
4. Pilih repository dan branch
5. Main file: `app.py`
6. Click **"Advanced settings"** → **"Secrets"**
7. Copy-paste isi file `.streamlit/secrets.toml` ke field Secrets
8. Click **"Deploy"**

### Step 3: Verify Deployment

Setelah deploy berhasil, test:
- ✅ Form submission
- ✅ Image upload ke Drive
- ✅ Data tersimpan di Sheets
- ✅ Dashboard menampilkan data

## 📊 Data Fields

### Form Input:
- **Nama User** - Display name
- **Telegram User ID** - Permanent numeric ID
- **Paket** - Monthly / Quarterly / Lifetime
- **Harga (USDT)** - Payment amount
- **Tanggal Mulai** - Start date
- **Blockchain Network** - BSC / Ethereum / Polygon / Arbitrum / Optimism
- **Transaction Hash** - Blockchain TX hash
- **Bukti Transfer** - Payment proof image

### Auto-Generated:
- **Timestamp** - Submission time
- **Telegram Link** - `tg://user?id={user_id}`
- **Explorer Link** - Network-specific blockchain explorer
- **Image URL** - Google Drive direct link

## 🔐 Security Notes

- ✅ Credentials disimpan di Streamlit Secrets
- ✅ File `secrets.toml` di-exclude dari Git
- ✅ Service account dengan permissions minimal
- ✅ Drive images dengan public read access
- ✅ No hardcoded credentials di code

## 📝 Usage

### Registration Flow:
1. User mengisi form
2. Upload bukti transfer
3. Submit → Image upload ke Drive
4. Data tersimpan di Google Sheets
5. Success notification dengan summary

### Dashboard Features:
- View all registered users
- Filter by package type
- Search by user name
- View payment proofs
- Click links (Telegram, Explorer, Images)
- Export to CSV

## 🆘 Troubleshooting

### Error: "Permission denied"
- Pastikan service account email sudah di-share ke Sheet & Drive

### Error: "Invalid credentials"
- Cek format `secrets.toml` sudah benar
- Pastikan private key tidak ada extra spaces/newlines

### Error: "Module not found"
- Run: `pip install -r requirements.txt`

### Images tidak muncul di Dashboard
- Cek folder permission sudah public atau di-share
- Verify direct link format: `drive.google.com/uc?export=view&id=...`

## 📞 Support

Untuk issue atau pertanyaan, hubungi developer.

---

Made with ❤️ for LuxQuant | Powered by Streamlit
