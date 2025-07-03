#!/usr/bin/env python3
"""
Configuration Setup Script for ExcelYard Bot
Run this script to easily update all your personal details
"""

import os
import sys

def update_config():
    """Interactive configuration updater"""
    
    print("🤖 ExcelYard Bot Configuration Setup")
    print("=" * 50)
    
    # Get user inputs
    bot_token = input("Enter your Telegram Bot Token: ").strip()
    admin_id = input("Enter your Telegram User ID (admin): ").strip()
    group_chat_id = input("Enter your Group Chat ID (for notifications): ").strip()
    log_group_id = input("Enter your Log Group ID (can be same as above): ").strip()
    
    bot_name = input("Enter your Bot Name (e.g., 'MyAwesome Bot'): ").strip()
    support_username = input("Enter your Support Username (e.g., '@MySupport'): ").strip()
    channel_username = input("Enter your Channel Username (e.g., '@MyChannel'): ").strip()
    
    admin_username = input("Enter Admin Web Interface Username: ").strip()
    admin_password = input("Enter Admin Web Interface Password: ").strip()
    
    website_url = input("Enter your Website URL (e.g., 'https://mysite.com'): ").strip()
    
    # Validate inputs
    if not all([bot_token, admin_id, group_chat_id, bot_name]):
        print("❌ Error: All fields are required!")
        return False
    
    try:
        int(admin_id)
        int(group_chat_id)
        if log_group_id:
            int(log_group_id)
    except ValueError:
        print("❌ Error: User IDs and Group IDs must be numbers!")
        return False
    
    # Update environment variables in a .env file
    env_content = f"""# ExcelYard Bot Configuration
TELEGRAM_BOT_TOKEN={bot_token}
ADMIN_ID={admin_id}
GROUP_CHAT_ID={group_chat_id}
LOG_GROUP_ID={log_group_id or group_chat_id}
ADMIN_USERNAME={admin_username}
ADMIN_PASSWORD={admin_password}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    # Update constants.py file
    constants_content = f'''"""
Constants and configuration for {bot_name}
"""

import os

# Bot API Configuration
API_KEY_001 = os.getenv('TELEGRAM_BOT_TOKEN', '{bot_token}')

# Admin Configuration
ADMIN_ID = int(os.getenv('ADMIN_ID', '{admin_id}'))
adminpass = os.getenv('ADMIN_PASSWORD', '{admin_password}')

# Group Chat Configuration
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID', '{group_chat_id}'))
LOG_GROUP_ID = int(os.getenv('LOG_GROUP_ID', '{log_group_id or group_chat_id}'))

# Payment Configuration
BITCOIN_RATES = {{
    70: 0.000899,
    100: 0.001285,
    150: 0.001928,
    200: 0.002571,
    250: 0.003214,
    300: 0.003857,
    400: 0.005142,
    500: 0.006428,
    1000: 0.012856
}}

# Product Categories
PRODUCT_CATEGORIES = {{
    'fullz': {{
        'name': '🗓 Fullz',
        'description': 'Complete personal information packages',
        'countries': ['us', 'uk', 'ca', 'au']
    }},
    'cvv': {{
        'name': '💳 CVV',
        'description': 'Credit card verification values',
        'types': ['standard', 'premium', 'vip', 'fresh']
    }},
    'dumps': {{
        'name': '💾 Dumps',
        'description': 'Magnetic stripe data',
        'types': ['track12', 'fresh', 'premium', 'vip']
    }}
}}

# Pricing Configuration
PRICING = {{
    'fullz': {{
        'us': {{'min': 15, 'max': 25}},
        'uk': {{'min': 12, 'max': 20}},
        'ca': {{'min': 18, 'max': 28}},
        'au': {{'min': 20, 'max': 30}}
    }},
    'cvv': {{
        'standard': {{'min': 5, 'max': 8}},
        'premium': {{'min': 10, 'max': 15}},
        'vip': {{'min': 15, 'max': 25}},
        'fresh': {{'min': 20, 'max': 30}}
    }},
    'dumps': {{
        'track12': {{'min': 25, 'max': 40}},
        'fresh': {{'min': 35, 'max': 50}},
        'premium': {{'min': 45, 'max': 65}},
        'vip': {{'min': 55, 'max': 80}}
    }}
}}

# Bot Messages
MESSAGES = {{
    'welcome': """🏪 **Welcome to {bot_name}**

Your trusted marketplace for digital services.

💰 **Current Balance:** £{{balance:.2f}}

Choose a category to explore our products:""",
    
    'help': """🆘 **{bot_name} Help**

**Available Commands:**
• /start - Main menu
• /help - Show this help
• /balance - Check wallet balance
• /contact - Contact support

**How to use:**
1. Add funds to your wallet
2. Browse our product categories
3. Make purchases with your balance
4. Products delivered instantly

**Payment Methods:**
• Bitcoin (BTC) only
• Minimum deposit: £70

**Support:**
Contact {support_username} for assistance""",
    
    'balance': """💰 **Your Wallet Balance**

💳 **Current Balance:** £{{balance:.2f}}

Use /start to add funds or make purchases.""",
    
    'wallet': """💰 **Wallet Management**

💳 **Current Balance:** £{{balance:.2f}}

**Deposit Options:**
Choose an amount to deposit via Bitcoin:""",
    
    'payment_instructions': """💳 **Payment Instructions**

Send **exactly** {{btc_amount}} BTC to receive **£{{amount_gbp}}** credits

**Bitcoin Address:**
`{{btc_address}}`

⚠️ **Important:**
• Send exact amount only
• Deposits are permanent & non-refundable
• Double-check amount before sending
• One payment per address
• Credits added after confirmation

🔶 **You will be funded when transaction confirms**""",
    
    'info': """ℹ️ **{bot_name} Information**

**About Us:**
Trusted marketplace for digital services since 2020.

**Quality Guarantee:**
• Fresh data only
• Instant delivery
• 24/7 support
• Secure transactions

**Payment:**
• Bitcoin only
• Instant processing
• Secure addresses

**Support:**
Contact {support_username}

**Terms:**
By using this service, you agree to our terms of service."""
}}

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', '{bot_name.lower().replace(" ", "_")}_bot.log')

# Security Configuration
MAX_SEARCH_RESULTS = 10
MAX_QUERY_LENGTH = 100
RATE_LIMIT_SECONDS = 1

# Database Configuration
DATA_DIR = 'data'
USER_DATA_FILE = os.path.join(DATA_DIR, 'user_data.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')
ACTIVITY_LOG_FILE = os.path.join(DATA_DIR, 'activity_log.json')

# Feature Flags
ENABLE_SEARCH = True
ENABLE_PURCHASE = True
ENABLE_WALLET = True
ENABLE_LOGGING = True
ENABLE_ADMIN_NOTIFICATIONS = True

# Contact Information
SUPPORT_USERNAME = '{support_username}'
SUPPORT_CHANNEL = '{channel_username}'
TERMS_URL = '{website_url}/terms'
PRIVACY_URL = '{website_url}/privacy'
'''
    
    with open('constants.py', 'w') as f:
        f.write(constants_content)
    
    # Update main.py bot configuration
    with open('main.py', 'r') as f:
        main_content = f.read()
    
    # Replace bot configuration section
    main_content = main_content.replace(
        "API_KEY = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')",
        f"API_KEY = os.getenv('TELEGRAM_BOT_TOKEN', '{bot_token}')"
    )
    main_content = main_content.replace(
        "ADMIN_ID = int(os.getenv('ADMIN_ID', 'YOUR_ADMIN_USER_ID'))",
        f"ADMIN_ID = int(os.getenv('ADMIN_ID', '{admin_id}'))"
    )
    main_content = main_content.replace(
        "GROUP_ID = int(os.getenv('GROUP_ID', 'YOUR_GROUP_CHAT_ID'))",
        f"GROUP_ID = int(os.getenv('GROUP_ID', '{group_chat_id}'))"
    )
    
    # Replace bot name in messages
    main_content = main_content.replace('YOUR_BOT_NAME', bot_name)
    
    with open('main.py', 'w') as f:
        f.write(main_content)
    
    # Update web_interface.py
    with open('web_interface.py', 'r') as f:
        web_content = f.read()
    
    web_content = web_content.replace(
        "ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'your_admin_username')",
        f"ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', '{admin_username}')"
    )
    web_content = web_content.replace(
        "ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'your_admin_password')",
        f"ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '{admin_password}')"
    )
    
    with open('web_interface.py', 'w') as f:
        f.write(web_content)
    
    print("\n✅ Configuration Updated Successfully!")
    print(f"📝 .env file created with your settings")
    print(f"🔧 constants.py updated with your bot name: {bot_name}")
    print(f"🤖 main.py updated with your bot token and admin ID")
    print(f"🌐 web_interface.py updated with admin credentials")
    print(f"\n💡 Your bot is now ready to run with your personal settings!")
    print(f"🚀 Run: python main.py")
    
    return True

if __name__ == "__main__":
    try:
        update_config()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration cancelled.")
    except Exception as e:
        print(f"\n❌ Error during configuration: {e}")