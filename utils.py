def generate_telegram_link(user_id):
    """Generate Telegram profile link from User ID"""
    return f"https://web.telegram.org/a/#{user_id}"

def generate_explorer_link(network, tx_hash):
    """Generate blockchain explorer link based on network"""
    explorers = {
        "BSC (BEP20)": f"https://bscscan.com/tx/{tx_hash}",
        "Ethereum (ERC20)": f"https://etherscan.io/tx/{tx_hash}",
        "Polygon": f"https://polygonscan.com/tx/{tx_hash}",
        "Arbitrum": f"https://arbiscan.io/tx/{tx_hash}",
        "Optimism": f"https://optimistic.etherscan.io/tx/{tx_hash}"
    }
    
    return explorers.get(network, f"https://etherscan.io/tx/{tx_hash}")

def format_currency(amount):
    """Format currency with USDT symbol"""
    return f"${amount:,.2f} USDT"

def calculate_expiry_date(start_date_str, package):
    """Calculate expiry date based on start date and package"""
    from datetime import datetime, timedelta
    
    try:
        # Parse start date (format: YYYY-MM-DD)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        
        # Calculate duration based on package
        if package == "Monthly":
            expiry_date = start_date + timedelta(days=30)
        elif package == "Quarterly":
            expiry_date = start_date + timedelta(days=90)
        elif package == "Lifetime":
            return None  # Lifetime has no expiry
        else:
            return None
        
        return expiry_date
    except:
        return None

def get_days_remaining(expiry_date):
    """Calculate days remaining until expiry"""
    from datetime import datetime
    
    if expiry_date is None:
        return None
    
    today = datetime.now()
    delta = expiry_date - today
    
    return delta.days

def get_status_color(days_remaining):
    """Get status color based on days remaining"""
    if days_remaining is None:
        return "🟢"  # Lifetime
    elif days_remaining < 0:
        return "🔴"  # Expired
    elif days_remaining <= 7:
        return "🟠"  # Expiring soon
    else:
        return "🟢"  # Active
