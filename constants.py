"""
Constants and configuration for ExcelYard Bot
"""

import os

# Bot API Configuration - CHANGE THIS TO YOUR BOT TOKEN
API_KEY_001 = os.getenv('TELEGRAM_BOT_TOKEN', '7984635760:AAGS7eDpCnK_EgnqYEMXgJk72avYAQe9pWI')

# Admin Configuration - CHANGE THESE TO YOUR DETAILS
ADMIN_ID = int(os.getenv('ADMIN_ID', '1182433696'))  # Your actual user ID
adminpass = os.getenv('ADMIN_PASSWORD', 'heisenberg2024')

# Group Chat Configuration - CHANGE THESE TO YOUR GROUP IDs
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID', '-1002563927894'))  # HeisenbergStoreUk group
LOG_GROUP_ID = int(os.getenv('LOG_GROUP_ID', '-1002563927894'))    # HeisenbergStoreUk group

# Payment Configuration
BITCOIN_RATES = {
    70: 0.000899,
    100: 0.001285,
    150: 0.001928,
    200: 0.002571,
    250: 0.003214,
    300: 0.003857,
    400: 0.005142,
    500: 0.006428,
    1000: 0.012856
}

# Bitcoin Wallet Address - ADD YOUR WALLET HERE
BITCOIN_WALLET = "bc1q64f2jfjpv2f7n4a2jryj08wklc0yrvsjles5wt"

# Product Categories
PRODUCT_CATEGORIES = {
    'fullz': {
        'name': '🗓 Fullz',
        'description': 'Complete personal information packages',
        'countries': ['us', 'uk', 'ca', 'au']
    },
    'cvv': {
        'name': '💳 CVV',
        'description': 'Credit card verification values',
        'types': ['standard', 'premium', 'vip', 'fresh']
    },
    'dumps': {
        'name': '💾 Dumps',
        'description': 'Magnetic stripe data',
        'types': ['track12', 'fresh', 'premium', 'vip']
    }
}

# Pricing Configuration
PRICING = {
    'fullz': {
        'us': {'min': 15, 'max': 25},
        'uk': {'min': 12, 'max': 20},
        'ca': {'min': 18, 'max': 28},
        'au': {'min': 20, 'max': 30}
    },
    'cvv': {
        'standard': {'min': 5, 'max': 8},
        'premium': {'min': 10, 'max': 15},
        'vip': {'min': 15, 'max': 25},
        'fresh': {'min': 20, 'max': 30}
    },
    'dumps': {
        'track12': {'min': 25, 'max': 40},
        'fresh': {'min': 35, 'max': 50},
        'premium': {'min': 45, 'max': 65},
        'vip': {'min': 55, 'max': 80}
    }
}

# Bot Messages
MESSAGES = {
    'welcome': """🏪 **Welcome to YOUR_BOT_NAME**

Your trusted marketplace for digital services.

💰 **Current Balance:** £{balance:.2f}

Choose a category to explore our products:""",
    
    'help': """🆘 **YOUR_BOT_NAME Help**

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
Contact @HeisenbergActives for assistance""",
    
    'balance': """💰 **Your Wallet Balance**

💳 **Current Balance:** £{balance:.2f}

Use /start to add funds or make purchases.""",
    
    'wallet': """💰 **Wallet Management**

💳 **Current Balance:** £{balance:.2f}

**Deposit Options:**
Choose an amount to deposit via Bitcoin:""",
    
    'payment_instructions': """💳 **Payment Instructions**

Send **exactly** {btc_amount} BTC to receive **£{amount_gbp}** credits

**Bitcoin Address:**
`{btc_address}`

⚠️ **Important:**
• Send exact amount only
• Deposits are permanent & non-refundable
• Double-check amount before sending
• One payment per address
• Credits added after confirmation

🔶 **You will be funded when transaction confirms**""",
    
    'info': """ℹ️ **ExcelYard Information**

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
Contact @ExcelYardSupport

**Terms:**
By using this service, you agree to our terms of service."""
}

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'excelyard_bot.log')

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

# Contact Information - CHANGE THESE TO YOUR DETAILS
SUPPORT_USERNAME = '@HeisenbergActives'
SUPPORT_CHANNEL = 'https://t.me/HeisenbergStoreUk'
TERMS_URL = 'https://your-website.com/terms'
PRIVACY_URL = 'https://your-website.com/privacy'
