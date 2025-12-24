import streamlit as st
from datetime import datetime
import pandas as pd
from google_services import GoogleServices
from utils import generate_telegram_link, generate_explorer_link, format_currency, calculate_expiry_date, get_days_remaining, get_status_color

# Page config
st.set_page_config(
    page_title="LuxQuant User Registration",
    page_icon="📊",
    layout="wide"
)

# Initialize Google Services
@st.cache_resource
def init_google_services():
    return GoogleServices()

gs = init_google_services()

# Sidebar navigation
page = st.sidebar.selectbox("Menu", ["📝 Registration Form", "📊 User Dashboard", "⏰ User Expiry"])

# ==================== REGISTRATION FORM ====================
if page == "📝 Registration Form":
    st.title("📝 LuxQuant User Registration")
    st.markdown("---")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("Nama User *", placeholder="John Doe")
            telegram_user_id = st.text_input("Telegram User ID *", placeholder="7058728559")
            package = st.selectbox("Paket *", ["Monthly", "Quarterly", "Lifetime"])
            price = st.number_input("Harga (USDT) *", min_value=0.0, step=0.01, format="%.2f")
        
        with col2:
            start_date = st.date_input("Tanggal Mulai *", value=datetime.now())
            blockchain_network = st.selectbox("Blockchain Network *", 
                ["BSC (BEP20)", "Ethereum (ERC20)", "Polygon", "Arbitrum", "Optimism"])
            tx_hash = st.text_input("Transaction Hash *", placeholder="0x...")
            
        # Image upload
        st.markdown("### Upload Bukti Transfer")
        uploaded_image = st.file_uploader("Upload gambar bukti pembayaran *", 
                                         type=['png', 'jpg', 'jpeg', 'webp'])
        
        # Submit button
        submitted = st.form_submit_button("✅ Submit Registration", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([user_name, telegram_user_id, price, tx_hash, uploaded_image]):
                st.error("❌ Semua field wajib diisi!")
            elif not telegram_user_id.isdigit():
                st.error("❌ Telegram User ID harus berupa angka!")
            elif not tx_hash.startswith("0x"):
                st.error("❌ Transaction Hash harus diawali dengan '0x'")
            else:
                with st.spinner("⏳ Uploading data..."):
                    try:
                        # Upload image to Google Cloud Storage
                        image_url = gs.upload_image_to_gcs(uploaded_image, user_name)
                        
                        # Generate links
                        telegram_link = generate_telegram_link(telegram_user_id)
                        explorer_link = generate_explorer_link(blockchain_network, tx_hash)
                        
                        # Prepare data
                        user_data = {
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Nama User": user_name,
                            "Telegram User ID": telegram_user_id,
                            "Telegram Link": telegram_link,
                            "Paket": package,
                            "Harga (USDT)": price,
                            "Tanggal Mulai": start_date.strftime("%Y-%m-%d"),
                            "Blockchain Network": blockchain_network,
                            "Transaction Hash": tx_hash,
                            "Explorer Link": explorer_link,
                            "Bukti Transfer": image_url
                        }
                        
                        # Save to Google Sheets
                        gs.append_to_sheet(user_data)
                        
                        st.success("✅ Registrasi berhasil disimpan!")
                        st.balloons()
                        
                        # Show summary
                        st.markdown("### 📋 Summary")
                        st.info(f"""
                        **User:** {user_name}  
                        **Paket:** {package}  
                        **Harga:** {format_currency(price)}  
                        **Telegram:** [Profile Link]({telegram_link})  
                        **Transaction:** [View on Explorer]({explorer_link})
                        """)
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# ==================== USER DASHBOARD ====================
elif page == "📊 User Dashboard":
    st.title("📊 LuxQuant User Dashboard")
    st.markdown("---")
    
    try:
        # Load data from Google Sheets
        df = gs.get_all_users()
        
        if df.empty:
            st.info("Belum ada data user terdaftar.")
        else:
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Users", len(df))
            with col2:
                st.metric("Monthly", len(df[df['Paket'] == 'Monthly']))
            with col3:
                st.metric("Quarterly", len(df[df['Paket'] == 'Quarterly']))
            with col4:
                st.metric("Lifetime", len(df[df['Paket'] == 'Lifetime']))
            
            st.markdown("---")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                package_filter = st.multiselect("Filter by Paket", 
                                               options=["Monthly", "Quarterly", "Lifetime"],
                                               default=["Monthly", "Quarterly", "Lifetime"])
            with col2:
                search = st.text_input("🔍 Search User", placeholder="Cari nama user...")
            
            # Apply filters
            filtered_df = df[df['Paket'].isin(package_filter)]
            if search:
                filtered_df = filtered_df[filtered_df['Nama User'].str.contains(search, case=False, na=False)]
            
            # Display table
            st.markdown(f"### Showing {len(filtered_df)} users")
            
            # Format display
            display_df = filtered_df.copy()
            display_df['Harga (USDT)'] = display_df['Harga (USDT)'].apply(format_currency)
            
            # Make links clickable
            for idx, row in display_df.iterrows():
                with st.expander(f"👤 {row['Nama User']} - {row['Paket']} ({row['Harga (USDT)']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Telegram ID:** {row['Telegram User ID']}  
                        **Telegram:** [Open Profile]({row['Telegram Link']})  
                        **Paket:** {row['Paket']}  
                        **Harga:** {row['Harga (USDT)']}  
                        **Tanggal Mulai:** {row['Tanggal Mulai']}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Network:** {row['Blockchain Network']}  
                        **TX Hash:** `{row['Transaction Hash'][:20]}...`  
                        **Explorer:** [View Transaction]({row['Explorer Link']})  
                        **Bukti Transfer:** [View Image]({row['Bukti Transfer']})
                        """)
                        
                        # Display image
                        try:
                            st.image(row['Bukti Transfer'], width=300)
                        except:
                            st.warning("Image preview not available")
            
            # Download as CSV
            st.markdown("---")
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Data (CSV)",
                data=csv,
                file_name=f"luxquant_users_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")

# ==================== USER EXPIRY PAGE ====================
elif page == "⏰ User Expiry":
    st.title("⏰ User Expiry Management")
    st.markdown("---")
    
    try:
        # Load data from Google Sheets
        df = gs.get_all_users()
        
        if df.empty:
            st.info("Belum ada data user terdaftar.")
        else:
            # Calculate expiry for each user
            df['Expiry Date'] = df.apply(
                lambda row: calculate_expiry_date(row['Tanggal Mulai'], row['Paket']), 
                axis=1
            )
            df['Days Remaining'] = df['Expiry Date'].apply(get_days_remaining)
            df['Status'] = df['Days Remaining'].apply(get_status_color)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            active_users = len(df[(df['Days Remaining'].notna()) & (df['Days Remaining'] >= 0)])
            expired_users = len(df[(df['Days Remaining'].notna()) & (df['Days Remaining'] < 0)])
            expiring_soon = len(df[(df['Days Remaining'].notna()) & (df['Days Remaining'] >= 0) & (df['Days Remaining'] <= 7)])
            lifetime_users = len(df[df['Paket'] == 'Lifetime'])
            
            with col1:
                st.metric("🟢 Active", active_users)
            with col2:
                st.metric("🔴 Expired", expired_users)
            with col3:
                st.metric("🟠 Expiring Soon (≤7d)", expiring_soon)
            with col4:
                st.metric("♾️ Lifetime", lifetime_users)
            
            st.markdown("---")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=["Active", "Expired", "Expiring Soon", "Lifetime"],
                    default=["Active", "Expiring Soon", "Lifetime"]
                )
            with col2:
                search = st.text_input("🔍 Search User", placeholder="Cari nama user...")
            
            # Apply filters
            filtered_df = df.copy()
            
            # Status filter
            if "Active" not in status_filter:
                filtered_df = filtered_df[~((filtered_df['Days Remaining'].notna()) & 
                                           (filtered_df['Days Remaining'] >= 8))]
            if "Expired" not in status_filter:
                filtered_df = filtered_df[~((filtered_df['Days Remaining'].notna()) & 
                                           (filtered_df['Days Remaining'] < 0))]
            if "Expiring Soon" not in status_filter:
                filtered_df = filtered_df[~((filtered_df['Days Remaining'].notna()) & 
                                           (filtered_df['Days Remaining'] >= 0) & 
                                           (filtered_df['Days Remaining'] <= 7))]
            if "Lifetime" not in status_filter:
                filtered_df = filtered_df[filtered_df['Paket'] != 'Lifetime']
            
            # Search filter
            if search:
                filtered_df = filtered_df[filtered_df['Nama User'].str.contains(search, case=False, na=False)]
            
            # Sort by expiry date (soonest first, but put expired at end)
            filtered_df['Sort Key'] = filtered_df['Days Remaining'].apply(
                lambda x: 999999 if x is None else (1000000 + abs(x) if x < 0 else x)
            )
            filtered_df = filtered_df.sort_values('Sort Key')
            
            # Display users
            st.markdown(f"### Showing {len(filtered_df)} users")
            
            for idx, row in filtered_df.iterrows():
                expiry_date = row['Expiry Date']
                days_remaining = row['Days Remaining']
                status = row['Status']
                
                # Determine status text
                if row['Paket'] == 'Lifetime':
                    status_text = "♾️ Lifetime (No Expiry)"
                    expiry_display = "Never"
                elif days_remaining is None:
                    status_text = "❓ Unknown"
                    expiry_display = "N/A"
                elif days_remaining < 0:
                    status_text = f"🔴 Expired ({abs(days_remaining)} days ago)"
                    expiry_display = expiry_date.strftime("%Y-%m-%d")
                elif days_remaining == 0:
                    status_text = "🟠 Expires Today"
                    expiry_display = expiry_date.strftime("%Y-%m-%d")
                elif days_remaining <= 7:
                    status_text = f"🟠 Expiring in {days_remaining} days"
                    expiry_display = expiry_date.strftime("%Y-%m-%d")
                else:
                    status_text = f"🟢 Active ({days_remaining} days left)"
                    expiry_display = expiry_date.strftime("%Y-%m-%d")
                
                with st.expander(f"{status} {row['Nama User']} - {row['Paket']} - {status_text}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **User Info:**
                        - Name: {row['Nama User']}
                        - Package: {row['Paket']}
                        - Price: {format_currency(row['Harga (USDT)'])}
                        - Telegram: [Open Profile]({row['Telegram Link']})
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Subscription Info:**
                        - Start Date: {row['Tanggal Mulai']}
                        - Expiry Date: {expiry_display}
                        - Status: {status_text}
                        """)
            
            # Export
            st.markdown("---")
            
            # Prepare export data
            export_df = filtered_df.copy()
            export_df['Expiry Date'] = export_df['Expiry Date'].apply(
                lambda x: x.strftime("%Y-%m-%d") if x is not None else "Never"
            )
            export_df['Days Remaining'] = export_df['Days Remaining'].apply(
                lambda x: str(x) if x is not None else "N/A"
            )
            export_df = export_df[['Nama User', 'Paket', 'Harga (USDT)', 'Tanggal Mulai', 
                                   'Expiry Date', 'Days Remaining', 'Status']]
            
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Expiry Report (CSV)",
                data=csv,
                file_name=f"luxquant_expiry_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for LuxQuant | Powered by Streamlit")
