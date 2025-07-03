#!/usr/bin/env python3
"""
ExcelYard Bot - Complete Telegram Bot with Product Catalog and Payment Processing
"""

import telebot
from telebot import types
import time
import threading
import logging
import sys
import os
import random
import requests
import json
from datetime import datetime
from bin_data_loader import create_fullz_bases, get_base_records, search_bin_records, generate_fullz_name
from constants import API_KEY_001, adminpass, GROUP_CHAT_ID, LOG_GROUP_ID

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('excelyard_bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Bot configuration - CHANGE THESE TO YOUR VALUES
API_KEY = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_ID = int(os.getenv('ADMIN_ID', 'YOUR_ADMIN_USER_ID'))
GROUP_ID = int(os.getenv('GROUP_ID', 'YOUR_GROUP_CHAT_ID'))

class ExcelYardBot:
    def __init__(self):
        self.bot = telebot.TeleBot(API_KEY)
        self.running = True
        self.wallet_addresses = {}
        self.log_group_id = LOG_GROUP_ID
        self.user_balances = {}
        self.pending_purchases = {}
        
        # Clear webhook and pending updates
        try:
            self.bot.delete_webhook()
            logger.info("Webhook cleared successfully")
            
            updates = self.bot.get_updates(timeout=1, offset=-1)
            if updates:
                last_update_id = updates[-1].update_id
                self.bot.get_updates(offset=last_update_id + 1, timeout=1)
                logger.info("Pending updates cleared successfully")
                
        except Exception as e:
            logger.warning(f"Webhook/updates clearing failed: {e}")
        
        self.setup_handlers()
        self.test_logging_system()
    
    def test_logging_system(self):
        """Test if logging system is working"""
        try:
            test_message = "🚀 **LOGGING SYSTEM ACTIVE**\n✅ ExcelYard Bot logging system initialized successfully"
            self.bot.send_message(
                chat_id=self.log_group_id,
                text=test_message,
                parse_mode='Markdown'
            )
            print("✅ Logging system test successful")
        except Exception as e:
            print(f"❌ Logging system test failed: {e}")
    
    def log_user_activity(self, user_id, username, action, details=""):
        """Log all user activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = f"@{username}" if username and username != f"User{user_id}" else f"ID:{user_id}"
        
        try:
            log_message = f"📊 **USER LOG**\n⏰ {timestamp}\n👤 {user_info}\n🎯 {action}\n📝 {details}"
            
            self.bot.send_message(
                chat_id=self.log_group_id,
                text=log_message,
                parse_mode='Markdown',
                disable_web_page_preview=True,
                disable_notification=True
            )
            
        except Exception as e:
            print(f"📊 USER LOG | {timestamp} | {user_info} | {action} | {details}")
            logger.info(f"User activity: {user_info} - {action} - {details}")
    
    def get_user_balance(self, user_id):
        """Get user's wallet balance"""
        return self.user_balances.get(user_id, 0.0)
    
    def add_user_balance(self, user_id, amount):
        """Add to user's wallet balance"""
        current_balance = self.get_user_balance(user_id)
        self.user_balances[user_id] = current_balance + amount
        return self.user_balances[user_id]
    
    def deduct_user_balance(self, user_id, amount):
        """Deduct from user's wallet balance"""
        current_balance = self.get_user_balance(user_id)
        if current_balance >= amount:
            self.user_balances[user_id] = current_balance - amount
            return True
        return False
    
    def generate_btc_address(self, amount_gbp):
        """Generate Bitcoin address for payment"""
        try:
            prefixes = ['bc1', '3', '1']
            prefix = random.choice(prefixes)
            
            if prefix == 'bc1':
                chars = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
                length = random.randint(39, 59)
                address = prefix + ''.join(random.choice(chars) for _ in range(length))
            else:
                chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789'
                length = random.randint(26, 35)
                address = prefix + ''.join(random.choice(chars) for _ in range(length))
            
            return address
            
        except Exception as e:
            logger.error(f"Address generation error: {e}")
            return "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    
    def create_main_menu(self):
        """Create main menu with all service categories"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton('🗓 Fullz', callback_data='fullz'),
            types.InlineKeyboardButton('💳 CVV', callback_data='cvv')
        )
        keyboard.add(
            types.InlineKeyboardButton('💾 Dumps', callback_data='dumps'),
            types.InlineKeyboardButton('🔍 Search', callback_data='search')
        )
        keyboard.add(
            types.InlineKeyboardButton('💰 Wallet', callback_data='wallet'),
            types.InlineKeyboardButton('ℹ️ Info', callback_data='info')
        )
        
        return keyboard
    
    def create_wallet_menu(self):
        """Create wallet menu with deposit options"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton('💳 £70', callback_data='wallet_70'),
            types.InlineKeyboardButton('💳 £100', callback_data='wallet_100')
        )
        keyboard.add(
            types.InlineKeyboardButton('💳 £150', callback_data='wallet_150'),
            types.InlineKeyboardButton('💳 £200', callback_data='wallet_200')
        )
        keyboard.add(
            types.InlineKeyboardButton('💳 £250', callback_data='wallet_250'),
            types.InlineKeyboardButton('💳 £300', callback_data='wallet_300')
        )
        keyboard.add(
            types.InlineKeyboardButton('💳 £400', callback_data='wallet_400'),
            types.InlineKeyboardButton('💳 £500', callback_data='wallet_500')
        )
        keyboard.add(
            types.InlineKeyboardButton('💳 £1000', callback_data='wallet_1000')
        )
        keyboard.add(
            types.InlineKeyboardButton('🔙 Back', callback_data='start')
        )
        
        return keyboard
    
    def create_fullz_menu(self):
        """Create fullz category menu"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton('🇺🇸 US Fullz', callback_data='fullz_us'),
            types.InlineKeyboardButton('🇬🇧 UK Fullz', callback_data='fullz_uk')
        )
        keyboard.add(
            types.InlineKeyboardButton('🇨🇦 CA Fullz', callback_data='fullz_ca'),
            types.InlineKeyboardButton('🇦🇺 AU Fullz', callback_data='fullz_au')
        )
        keyboard.add(
            types.InlineKeyboardButton('🔙 Back', callback_data='start')
        )
        
        return keyboard
    
    def create_cvv_menu(self):
        """Create CVV category menu"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton('💳 Standard CVV', callback_data='cvv_standard'),
            types.InlineKeyboardButton('💎 Premium CVV', callback_data='cvv_premium')
        )
        keyboard.add(
            types.InlineKeyboardButton('🏆 VIP CVV', callback_data='cvv_vip'),
            types.InlineKeyboardButton('🔥 Fresh CVV', callback_data='cvv_fresh')
        )
        keyboard.add(
            types.InlineKeyboardButton('🔙 Back', callback_data='start')
        )
        
        return keyboard
    
    def setup_handlers(self):
        """Setup all message and callback handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            
            self.log_user_activity(user_id, username, "Bot Started", "Used /start command")
            
            welcome_text = """🏪 **Welcome to YOUR_BOT_NAME**

Your trusted marketplace for digital services.

💰 **Current Balance:** £{balance:.2f}

Choose a category to explore our products:""".format(balance=self.get_user_balance(user_id))
            
            try:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=welcome_text,
                    reply_markup=self.create_main_menu(),
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Start message error: {e}")
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="🏪 Welcome to YOUR_BOT_NAME\n\nChoose a category:",
                    reply_markup=self.create_main_menu()
                )
        
        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            
            self.log_user_activity(user_id, username, "Help Requested", "Used /help command")
            
            help_text = """🆘 **ExcelYard Help**

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
Contact @ExcelYardSupport for assistance"""
            
            try:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=help_text,
                    parse_mode='Markdown'
                )
            except:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="ExcelYard Help\n\nUse /start for main menu\nContact support for assistance"
                )
        
        @self.bot.message_handler(commands=['balance'])
        def handle_balance(message):
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            balance = self.get_user_balance(user_id)
            
            self.log_user_activity(user_id, username, "Balance Check", f"Balance: £{balance:.2f}")
            
            balance_text = f"💰 **Your Wallet Balance**\n\n💳 **Current Balance:** £{balance:.2f}\n\nUse /start to add funds or make purchases."
            
            try:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=balance_text,
                    parse_mode='Markdown'
                )
            except:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=f"💰 Your Balance: £{balance:.2f}"
                )
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            user_id = call.from_user.id
            username = call.from_user.username or f"User{user_id}"
            
            try:
                if call.data == 'start':
                    self.log_user_activity(user_id, username, "Main Menu", "Returned to main menu")
                    
                    welcome_text = """🏪 **Welcome to YOUR_BOT_NAME**

Your trusted marketplace for digital services.

💰 **Current Balance:** £{balance:.2f}

Choose a category to explore our products:""".format(balance=self.get_user_balance(user_id))
                    
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=welcome_text,
                        reply_markup=self.create_main_menu(),
                        parse_mode='Markdown'
                    )
                
                elif call.data == 'wallet':
                    self.log_user_activity(user_id, username, "Wallet Menu", "Accessed wallet menu")
                    
                    wallet_text = f"""💰 **Wallet Management**

💳 **Current Balance:** £{self.get_user_balance(user_id):.2f}

**Deposit Options:**
Choose an amount to deposit via Bitcoin:"""
                    
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=wallet_text,
                        reply_markup=self.create_wallet_menu(),
                        parse_mode='Markdown'
                    )
                
                elif call.data.startswith('wallet_'):
                    amount = int(call.data.split('_')[1])
                    self.handle_wallet_amount(call, amount)
                
                elif call.data.startswith('copy_address_'):
                    amount = int(call.data.split('_')[2])
                    self.handle_copy_address(call, amount)
                
                elif call.data == 'fullz':
                    self.log_user_activity(user_id, username, "Fullz Menu", "Accessed fullz category")
                    
                    fullz_text = """🗓 **Fullz Categories**

**Available Countries:**
Choose a country for fullz data:

🇺🇸 **US Fullz** - $15-25
🇬🇧 **UK Fullz** - £12-20
🇨🇦 **CA Fullz** - $18-28
🇦🇺 **AU Fullz** - $20-30

*Prices vary by quality and data completeness*"""
                    
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=fullz_text,
                        reply_markup=self.create_fullz_menu(),
                        parse_mode='Markdown'
                    )
                
                elif call.data == 'cvv':
                    self.log_user_activity(user_id, username, "CVV Menu", "Accessed CVV category")
                    
                    cvv_text = """💳 **CVV Categories**

**Available Types:**

💳 **Standard CVV** - £5-8
💎 **Premium CVV** - £10-15
🏆 **VIP CVV** - £15-25
🔥 **Fresh CVV** - £20-30

*All CVV come with full card details*"""
                    
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=cvv_text,
                        reply_markup=self.create_cvv_menu(),
                        parse_mode='Markdown'
                    )
                
                elif call.data == 'dumps':
                    self.log_user_activity(user_id, username, "Dumps Menu", "Accessed dumps category")
                    
                    dumps_text = """💾 **Dumps Categories**

**Available Types:**

💾 **Track 1 & 2** - £25-40
🔥 **Fresh Dumps** - £35-50
💎 **Premium Dumps** - £45-65
🏆 **VIP Dumps** - £55-80

*High balance dumps available*"""
                    
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton('🔙 Back', callback_data='start'))
                    
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=dumps_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                
                elif call.data == 'search':
                    self.log_user_activity(user_id, username, "Search Menu", "Accessed search function")
                    
                    search_text = """🔍 **Search Products**

**Search by:**
• BIN number
• Country
• Bank name
• Card type

**How to search:**
Type your search query after this message.

Example: "UK Visa" or "442387"

Use /start to return to main menu."""
                    
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton('🔙 Back', callback_data='start'))
                    
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=search_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                
                elif call.data == 'info':
                    self.log_user_activity(user_id, username, "Info Menu", "Accessed info page")
                    
                    info_text = """ℹ️ **ExcelYard Information**

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
                    
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton('🔙 Back', callback_data='start'))
                    
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=info_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                
                # Handle specific product categories
                elif call.data.startswith('fullz_'):
                    country = call.data.split('_')[1].upper()
                    self.handle_fullz_country(call, country)
                
                elif call.data.startswith('cvv_'):
                    cvv_type = call.data.split('_')[1]
                    self.handle_cvv_type(call, cvv_type)
                
                try:
                    self.bot.answer_callback_query(call.id)
                except:
                    pass
                    
            except Exception as e:
                logger.error(f"Callback handler error: {e}")
                try:
                    self.bot.answer_callback_query(call.id, "Error processing request")
                except:
                    pass
        
        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            text = message.text.lower()
            
            # Handle search queries
            if len(text) > 2:
                self.log_user_activity(user_id, username, "Search Query", f"Query: {text}")
                
                # Perform search
                results = self.search_products(text)
                
                if results:
                    search_results = "🔍 **Search Results:**\n\n"
                    for i, result in enumerate(results[:5], 1):
                        search_results += f"{i}. {result}\n"
                    
                    search_results += f"\n*Showing {min(len(results), 5)} of {len(results)} results*"
                    
                    try:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=search_results,
                            parse_mode='Markdown'
                        )
                    except:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=f"🔍 Found {len(results)} results for '{text}'"
                        )
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text="🔍 No results found for your search query."
                    )
    
    def handle_wallet_amount(self, call, amount_gbp):
        """Handle wallet amount selection and generate payment"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, f"Wallet Amount Selected", f"£{amount_gbp}")
        
        try:
            self.bot.answer_callback_query(call.id, f"💳 Generating payment for £{amount_gbp}...")
        except:
            pass
        
        # Generate Bitcoin address
        address_key = f"{user_id}_{amount_gbp}"
        btc_address = self.generate_btc_address(amount_gbp)
        self.wallet_addresses[address_key] = btc_address
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('📋 Tap to Copy Address', callback_data=f'copy_address_{amount_gbp}'))
        keyboard.add(types.InlineKeyboardButton('🔙 Back', callback_data='wallet'))
        
        # Calculate BTC amount
        btc_amounts = {
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
        
        btc_amount = btc_amounts.get(amount_gbp, 0.000899)
        
        text = f"""💳 **Payment Instructions**

Send **exactly** {btc_amount} BTC to receive **£{amount_gbp}** credits

**Bitcoin Address:**
`{btc_address}`

⚠️ **Important:**
• Send exact amount only
• Deposits are permanent & non-refundable
• Double-check amount before sending
• One payment per address
• Credits added after confirmation

🔶 **You will be funded when transaction confirms**"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
    
    def handle_copy_address(self, call, amount_gbp):
        """Handle copying wallet address"""
        user_id = call.from_user.id
        address_key = f"{user_id}_{amount_gbp}"
        
        if address_key in self.wallet_addresses:
            btc_address = self.wallet_addresses[address_key]
        else:
            btc_address = self.generate_btc_address(amount_gbp)
            self.wallet_addresses[address_key] = btc_address
        
        copy_text = f"""📋 **Copy Bitcoin Address**

**Amount:** £{amount_gbp}

**Address:**
`{btc_address}`

**Instructions:**
• Tap and hold address to copy (mobile)
• Select address and Ctrl+C (desktop)
• Verify address before sending

⚠️ **Double-check address before payment**"""
        
        try:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=copy_text,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id, "📋 Address ready to copy!")
        except Exception as e:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=f"Bitcoin Address for £{amount_gbp}:\n\n{btc_address}"
            )
            self.bot.answer_callback_query(call.id, "📋 Address sent!")
    
    def handle_fullz_country(self, call, country):
        """Handle fullz country selection"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, f"Fullz Country", f"Selected {country}")
        
        # Get fullz data for country
        fullz_data = get_base_records(country.lower())
        
        if fullz_data:
            text = f"""🗓 **{country} Fullz Available**

**Sample Data:**
{fullz_data[:3]}

**Pricing:**
• Standard: £15
• Premium: £25
• Bulk (10+): £20 each

**Includes:**
• Full name, SSN/ID
• Address, phone
• DOB, email
• Bank details

💰 **Balance:** £{self.get_user_balance(user_id):.2f}"""
        else:
            text = f"""🗓 **{country} Fullz**

**Currently Restocking**

New stock arrives daily. Check back soon!

**Typical Pricing:**
• Standard: £15-20
• Premium: £25-35

💰 **Balance:** £{self.get_user_balance(user_id):.2f}"""
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔙 Back', callback_data='fullz'))
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"{country} Fullz - Check back for availability",
                reply_markup=keyboard
            )
    
    def handle_cvv_type(self, call, cvv_type):
        """Handle CVV type selection"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, f"CVV Type", f"Selected {cvv_type}")
        
        cvv_info = {
            'standard': {'price': '£5-8', 'desc': 'Basic CVV with card details'},
            'premium': {'price': '£10-15', 'desc': 'Higher balance CVV'},
            'vip': {'price': '£15-25', 'desc': 'Premium cards with high limits'},
            'fresh': {'price': '£20-30', 'desc': 'Recently obtained CVV data'}
        }
        
        info = cvv_info.get(cvv_type, {'price': '£5-10', 'desc': 'CVV with card details'})
        
        text = f"""💳 **{cvv_type.title()} CVV**

**Pricing:** {info['price']}
**Description:** {info['desc']}

**Includes:**
• Full card number
• Expiry date
• CVV code
• Cardholder name
• Billing address

**Current Stock:** Available
💰 **Your Balance:** £{self.get_user_balance(user_id):.2f}

*Contact support to purchase*"""
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔙 Back', callback_data='cvv'))
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"{cvv_type.title()} CVV - {info['price']}",
                reply_markup=keyboard
            )
    
    def search_products(self, query):
        """Search for products based on query"""
        results = []
        
        # Search in different categories
        if 'fullz' in query or 'ssn' in query:
            results.extend(['🗓 US Fullz - £15-25', '🗓 UK Fullz - £12-20', '🗓 CA Fullz - £18-28'])
        
        if 'cvv' in query or 'card' in query:
            results.extend(['💳 Standard CVV - £5-8', '💳 Premium CVV - £10-15', '💳 VIP CVV - £15-25'])
        
        if 'dump' in query:
            results.extend(['💾 Track 1&2 Dumps - £25-40', '💾 Fresh Dumps - £35-50'])
        
        # Search by country
        if 'us' in query or 'usa' in query or 'american' in query:
            results.extend(['🇺🇸 US Products Available'])
        
        if 'uk' in query or 'british' in query:
            results.extend(['🇬🇧 UK Products Available'])
        
        if 'ca' in query or 'canada' in query:
            results.extend(['🇨🇦 CA Products Available'])
        
        return list(set(results))
    
    def notify_admin(self, message):
        """Send notification to admin"""
        try:
            self.bot.send_message(ADMIN_ID, f"🔔 ExcelYard Alert\n{message}")
            logger.info(f"Admin notification sent: {message[:50]}...")
        except Exception as e:
            logger.error(f"Admin notification error: {e}")
    
    def run(self):
        """Main bot loop with error handling"""
        logger.info("🚀 ExcelYard Bot starting...")
        
        # Send startup notification
        try:
            self.notify_admin("🚀 ExcelYard Bot started successfully")
        except:
            pass
        
        while self.running:
            try:
                logger.info("🔄 Starting bot polling...")
                self.bot.polling(none_stop=True, interval=1, timeout=30)
            except Exception as e:
                logger.error(f"❌ Bot polling error: {e}")
                
                # Send error notification
                try:
                    self.notify_admin(f"❌ Bot Error: {str(e)[:100]}")
                except:
                    pass
                
                logger.info("⏳ Waiting 10 seconds before restart...")
                time.sleep(10)
                
                # Recreate bot instance
                try:
                    self.bot = telebot.TeleBot(API_KEY)
                    self.setup_handlers()
                    logger.info("✅ Bot instance recreated")
                except Exception as recreate_error:
                    logger.error(f"❌ Failed to recreate bot: {recreate_error}")
                    time.sleep(30)
        
        logger.info("🛑 ExcelYard Bot stopped")

def main():
    """Main function to start the bot"""
    bot = ExcelYardBot()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
        bot.running = False
    except Exception as e:
        logger.error(f"💥 Critical error: {e}")
        # Try to send final notification
        try:
            bot.notify_admin(f"💥 Critical Bot Error: {str(e)[:100]}")
        except:
            pass

if __name__ == "__main__":
    main()
