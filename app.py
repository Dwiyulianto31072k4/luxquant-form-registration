import streamlit as st
from datetime import datetime
import pandas as pd
from google_services import GoogleServices
from utils import generate_telegram_link, generate_explorer_link, format_currency

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
page = st.sidebar.selectbox("Menu", ["📝 Registration Form", "📊 User Dashboard"])

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
                        # Upload image to Google Drive
                        image_url = gs.upload_image_to_drive(uploaded_image, user_name)
                        
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

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for LuxQuant | Powered by Streamlit")
