def generate_telegram_link(user_id):
    """Generate Telegram profile link from User ID"""
    return f"tg://user?id={user_id}"

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
