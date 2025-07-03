#!/usr/bin/env python3
"""
FULLZ HAVEN Bot - Complete Version with Full Product Catalogs
Runs continuously with proper error handling and reconnection
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
        logging.FileHandler('fullz_haven_bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Bot configuration
API_KEY = os.getenv('TELEGRAM_BOT_TOKEN', '7984635760:AAGS7eDpCnK_EgnqYEMXgJk72avYAQe9pWI')
ADMIN_ID = int(os.getenv('ADMIN_ID', '123456789'))  # Replace with your actual user ID
GROUP_ID = int(os.getenv('GROUP_ID', '-1002563927894'))

class FullzHavenBot:
    def __init__(self):
        self.bot = telebot.TeleBot(API_KEY)
        self.running = True
        self.wallet_addresses = {}  # Store addresses for copying
        self.log_group_id = LOG_GROUP_ID
        self.user_balances = {}  # Store user wallet balances
        self.pending_purchases = {}  # Store pending purchase data
        
        # Clear webhook and pending updates to prevent conflicts
        try:
            # Delete webhook if exists
            self.bot.delete_webhook()
            logger.info("Webhook cleared successfully")
            
            # Clear pending updates
            updates = self.bot.get_updates(timeout=1, offset=-1)
            if updates:
                last_update_id = updates[-1].update_id
                self.bot.get_updates(offset=last_update_id + 1, timeout=1)
                logger.info("Pending updates cleared successfully")
                
        except Exception as e:
            logger.warning(f"Webhook/updates clearing failed (normal if none exist): {e}")
        
        self.setup_handlers()
        
        # Test logging system on startup
        self.test_logging_system()
    
    def test_logging_system(self):
        """Test if logging system is working"""
        try:
            test_message = "🚀 **LOGGING SYSTEM ACTIVE**\n✅ FULLZ HAVEN Bot logging system initialized successfully"
            self.bot.send_message(
                chat_id=self.log_group_id,
                text=test_message,
                parse_mode='Markdown'
            )
            print("✅ Logging system test successful - messages will be sent to group")
        except Exception as e:
            print(f"❌ Logging system test failed: {e}")
            print("📝 Will use console logging as fallback")
    
    def log_user_activity(self, user_id, username, action, details=""):
        """Log all user activities directly to admin"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = f"@{username}" if username and username != f"User{user_id}" else f"ID:{user_id}"
        
        # Always send to admin
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
            # Fallback to console logging if group message fails
            print(f"📊 USER LOG | {timestamp} | {user_info} | {action} | {details}")
            logger.info(f"User activity: {user_info} - {action} - {details}")
    
    def log_menu_navigation(self, user_id, username, menu_name, details=""):
        """Log menu navigation specifically"""
        self.log_user_activity(user_id, username, f"Menu: {menu_name}", details)
    
    def log_purchase_attempt(self, user_id, username, product, price, category):
        """Log purchase attempts"""
        details = f"Product: {product} | Price: {price} | Category: {category}"
        self.log_user_activity(user_id, username, "Purchase Attempt", details)
    
    def log_search_query(self, user_id, username, query, result_count):
        """Log search queries"""
        details = f"Query: {query} | Results: {result_count}"
        self.log_user_activity(user_id, username, "Search Query", details)
    
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
        # Generate a realistic looking address
        prefixes = ['bc1', '3', '1']
        prefix = random.choice(prefixes)
        
        if prefix == 'bc1':
            # Bech32 address
            chars = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
            length = random.randint(39, 59)
            address = prefix + ''.join(random.choice(chars) for _ in range(length))
        else:
            # Legacy or P2SH address
            chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789'
            length = random.randint(26, 35)
            address = prefix + ''.join(random.choice(chars) for _ in range(length))
        
        return address
    
    def handle_wallet_amount(self, call, amount_gbp):
        """Handle wallet amount selection and generate payment"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        # Log wallet amount selection
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
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='wallet'))
        
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
        btc_amount = btc_amounts.get(amount_gbp, amount_gbp * 0.000012856)
        
        payment_text = f"""💳 **Payment Instructions**

Send **exactly** {btc_amount:.8f} BTC to receive **£{amount_gbp}** credits

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
                text=payment_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Payment message error: {e}")
    
    def handle_copy_address(self, call, amount_gbp):
        """Handle copying wallet address to clipboard"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        address_key = f"{user_id}_{amount_gbp}"
        btc_address = self.wallet_addresses.get(address_key, "Address not found")
        
        self.log_user_activity(user_id, username, "Address Copy", f"£{amount_gbp} BTC address copied")
        
        try:
            self.bot.answer_callback_query(call.id, f"📋 Address copied: {btc_address}")
        except:
            pass
    
    def notify_admin(self, message):
        """Send notification to admin and group"""
        try:
            self.bot.send_message(
                chat_id=ADMIN_ID,
                text=message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Admin notification error: {e}")
    
    def create_main_menu(self):
        """Create main menu with all service categories"""
        keyboard = types.InlineKeyboardMarkup()
        
        # Row 1: Main categories
        keyboard.add(
            types.InlineKeyboardButton('🗓 Fullz', callback_data='fullz'),
            types.InlineKeyboardButton('🎯 Call Center', callback_data='call_center')
        )
        
        # Row 2: More categories
        keyboard.add(
            types.InlineKeyboardButton('💎 Crypto Leads', callback_data='crypto_leads'),
            types.InlineKeyboardButton('📧 Spam Tools', callback_data='spam_tools')
        )
        
        # Row 3: BIN services
        keyboard.add(
            types.InlineKeyboardButton('🔍 BIN Skipper', callback_data='skipper_bin'),
            types.InlineKeyboardButton('🌐 BIN Lookup', callback_data='bin_lookup')
        )
        
        # Row 4: Wallet and support
        keyboard.add(
            types.InlineKeyboardButton('💰 Wallet', callback_data='wallet'),
            types.InlineKeyboardButton('📋 Rules', callback_data='rules')
        )
        
        # Row 5: Support
        keyboard.add(
            types.InlineKeyboardButton('🆘 Support', callback_data='support'),
            types.InlineKeyboardButton('ℹ️ Info', callback_data='info')
        )
        
        return keyboard
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        
        @self.bot.message_handler(commands=['wallet'])
        def wallet_command(message):
            """Handle /wallet command"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            
            self.log_user_activity(user_id, username, "Wallet Command", "Used /wallet command")
            
            balance = self.get_user_balance(user_id)
            keyboard = self.create_wallet_menu()
            
            wallet_text = f"""💰 **Wallet Management**

💳 **Current Balance:** £{balance:.2f}

**Deposit Options:**
Choose an amount to deposit via Bitcoin:"""
            
            try:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=wallet_text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Wallet command error: {e}")
        
        @self.bot.message_handler(commands=['balance'])
        def balance_command(message):
            """Handle /balance command"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            
            self.log_user_activity(user_id, username, "Balance Check", "Used /balance command")
            
            balance = self.get_user_balance(user_id)
            balance_text = f"""💰 **Your Wallet Balance**

💳 **Current Balance:** £{balance:.2f}

Use /start to add funds or make purchases."""
            
            try:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=balance_text,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Balance command error: {e}")
        
        @self.bot.message_handler(commands=['add100'])
        def add_balance_command(message):
            """Handle /add100 command for testing"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            
            if user_id == ADMIN_ID:
                self.add_user_balance(user_id, 100.0)
                new_balance = self.get_user_balance(user_id)
                self.log_user_activity(user_id, username, "Admin Balance Added", "Added £100 for testing")
                
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=f"✅ Added £100 to your balance!\n💰 New balance: £{new_balance:.2f}",
                    parse_mode='Markdown'
                )
            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="❌ Admin command only"
                )
        
        @self.bot.message_handler(commands=['userbal'])
        def userbal_command(message):
            """Handle admin balance management"""
            user_id = message.from_user.id
            
            if user_id == ADMIN_ID:
                if len(message.text.split()) >= 3:
                    try:
                        target_user = int(message.text.split()[1])
                        amount = float(message.text.split()[2])
                        
                        self.add_user_balance(target_user, amount)
                        new_balance = self.get_user_balance(target_user)
                        
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=f"✅ Added £{amount} to user {target_user}\n💰 New balance: £{new_balance:.2f}"
                        )
                    except:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text="❌ Usage: /userbal [user_id] [amount]"
                        )
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text="❌ Usage: /userbal [user_id] [amount]"
                    )
            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="❌ Admin command only"
                )
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            """Handle /start command"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            
            self.log_user_activity(user_id, username, "Bot Started", "Used /start command")
            
            welcome_text = """🏪 **Welcome to FULLZ HAVEN**

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
                    text="🏪 Welcome to FULLZ HAVEN\n\nChoose a category:",
                    reply_markup=self.create_main_menu()
                )
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callbacks(call):
            """Handle all callback queries"""
            user_id = call.from_user.id
            username = call.from_user.username or f"User{user_id}"
            
            try:
                if call.data == 'start':
                    self.log_user_activity(user_id, username, "Main Menu", "Returned to main menu")
                    
                    welcome_text = """🏪 **Welcome to FULLZ HAVEN**

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
                    self.handle_wallet_menu(call)
                
                elif call.data.startswith('wallet_'):
                    amount = int(call.data.split('_')[1])
                    self.handle_wallet_amount(call, amount)
                
                elif call.data.startswith('copy_address_'):
                    amount = int(call.data.split('_')[2])
                    self.handle_copy_address(call, amount)
                
                elif call.data == 'fullz':
                    self.handle_fullz_menu(call)
                
                elif call.data == 'call_center':
                    self.handle_call_center_menu(call)
                
                elif call.data == 'crypto_leads':
                    self.handle_crypto_leads_menu(call)
                
                elif call.data == 'spam_tools':
                    self.handle_spam_tools_menu(call)
                
                elif call.data == 'skipper_bin':
                    self.handle_skipper_bin_menu(call)
                
                elif call.data == 'bin_lookup':
                    self.handle_bin_lookup_menu(call)
                
                elif call.data == 'rules':
                    self.handle_rules_menu(call)
                
                elif call.data == 'support':
                    self.handle_support_menu(call)
                
                elif call.data == 'info':
                    self.handle_info_menu(call)
                
                else:
                    # Handle other callbacks
                    self.handle_product_purchase(call)
                    
            except Exception as e:
                logger.error(f"Callback handler error: {e}")
                try:
                    self.bot.answer_callback_query(call.id, "❌ Error occurred")
                except:
                    pass
        
        @self.bot.message_handler(content_types=['text'])
        def handle_text_messages(message):
            """Handle all text messages"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            text = message.text.strip()
            
            # Check if it's a BIN search
            if text.isdigit() and len(text) >= 6:
                self.handle_bin_analysis(message)
            else:
                # Log the message
                self.log_user_activity(user_id, username, "Text Message", f"Message: {text}")
                
                # Send default response
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="🏪 Welcome to FULLZ HAVEN\n\nChoose a category:",
                    reply_markup=self.create_main_menu()
                )
    
    def handle_main_menu(self, call):
        """Handle main menu display"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Main Menu", "Accessed main menu")
        
        welcome_text = """🏪 **Welcome to FULLZ HAVEN**

Your trusted marketplace for digital services.

💰 **Current Balance:** £{balance:.2f}

Choose a category to explore our products:""".format(balance=self.get_user_balance(user_id))
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=welcome_text,
                reply_markup=self.create_main_menu(),
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Main menu error: {e}")
    
    def create_wallet_menu(self):
        """Create wallet menu with deposit options"""
        keyboard = types.InlineKeyboardMarkup()
        
        # Add wallet amounts
        amounts = [70, 100, 150, 200, 250, 300, 400, 500, 1000]
        
        for i in range(0, len(amounts), 3):
            row = []
            for j in range(3):
                if i + j < len(amounts):
                    amount = amounts[i + j]
                    row.append(types.InlineKeyboardButton(f'£{amount}', callback_data=f'wallet_{amount}'))
            keyboard.add(*row)
        
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        return keyboard
    
    def handle_wallet_menu(self, call):
        """Handle wallet menu with amount selection"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Wallet Menu", "Accessed wallet menu")
        
        balance = self.get_user_balance(user_id)
        keyboard = self.create_wallet_menu()
        
        wallet_text = f"""💰 **Wallet Management**

💳 **Current Balance:** £{balance:.2f}

**Deposit Options:**
Choose an amount to deposit via Bitcoin:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=wallet_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Wallet menu error: {e}")
    
    def handle_fullz_menu(self, call):
        """Handle fullz base selection menu"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Fullz Menu", "Accessed fullz category")
        
        keyboard = types.InlineKeyboardMarkup()
        
        # Add fullz bases
        bases = [
            ("🇺🇸 USA BASE", "fullz_usa"),
            ("🇬🇧 UK BASE", "fullz_uk"),
            ("🇨🇦 CANADA BASE", "fullz_ca"),
            ("🇦🇺 AUSTRALIA BASE", "fullz_au"),
            ("🇩🇪 GERMANY BASE", "fullz_de"),
            ("🇫🇷 FRANCE BASE", "fullz_fr")
        ]
        
        for name, callback in bases:
            keyboard.add(types.InlineKeyboardButton(name, callback_data=callback))
        
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        fullz_text = """🗓 **FULLZ BASES**

**Available Databases:**
• Complete personal information packages
• High-quality verified data
• Instant delivery
• Multiple country options

**Price Range:** £15-30 per record

Choose a country database:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=fullz_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Fullz menu error: {e}")
    
    def handle_call_center_menu(self, call):
        """Handle call center menu with country databases"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Call Center Menu", "Accessed call center databases")
        
        keyboard = types.InlineKeyboardMarkup()
        
        # Add country databases
        countries = [
            ("🇺🇸 USA Database", "cc_usa"),
            ("🇬🇧 UK Database", "cc_uk"),
            ("🇨🇦 Canada Database", "cc_ca"),
            ("🇦🇺 Australia Database", "cc_au"),
            ("🇩🇪 Germany Database", "cc_de"),
            ("🇫🇷 France Database", "cc_fr")
        ]
        
        for name, callback in countries:
            keyboard.add(types.InlineKeyboardButton(name, callback_data=callback))
        
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        cc_text = """🎯 **CALL CENTER DATABASES**

**Available Countries:**
• Fresh phone number databases
• Verified active numbers
• High conversion rates
• Multiple demographics

**Price Range:** £20-50 per database

Choose a country:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=cc_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Call center menu error: {e}")
    
    def handle_crypto_leads_menu(self, call):
        """Handle crypto leads menu"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Crypto Leads Menu", "Accessed crypto leads")
        
        keyboard = types.InlineKeyboardMarkup()
        
        # Add crypto lead types
        leads = [
            ("💎 Premium Crypto Leads", "crypto_premium"),
            ("🚀 Fresh Trader Leads", "crypto_fresh"),
            ("🔥 VIP Investor Leads", "crypto_vip"),
            ("💰 Whale Leads", "crypto_whale"),
            ("📈 Exchange Leads", "crypto_exchange")
        ]
        
        for name, callback in leads:
            keyboard.add(types.InlineKeyboardButton(name, callback_data=callback))
        
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        crypto_text = """💎 **CRYPTO LEADS**

**Available Lead Types:**
• Verified crypto investors
• Active trader databases
• High-value leads
• Fresh and updated

**Price Range:** £30-100 per package

Choose lead type:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=crypto_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Crypto leads menu error: {e}")
    
    def handle_spam_tools_menu(self, call):
        """Handle spam tools menu with 4 pages"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Spam Tools Menu", "Accessed spam tools")
        
        keyboard = types.InlineKeyboardMarkup()
        
        # Add spam tools
        tools = [
            ("📧 Email Blaster Pro", "spam_email"),
            ("📱 SMS Bomber", "spam_sms"),
            ("🎯 Lead Generator", "spam_leads"),
            ("🔗 Link Shortener", "spam_links"),
            ("📊 Campaign Manager", "spam_campaign"),
            ("🤖 Auto Responder", "spam_auto")
        ]
        
        for name, callback in tools:
            keyboard.add(types.InlineKeyboardButton(name, callback_data=callback))
        
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        spam_text = """📧 **SPAM TOOLS**

**Available Tools:**
• Professional email marketing
• SMS campaign tools
• Lead generation software
• Automation systems

**Price Range:** £25-75 per tool

Choose a tool:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=spam_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Spam tools menu error: {e}")
    
    def handle_skipper_bin_menu(self, call):
        """Handle skipper BIN menu with all 22 products"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Skipper BIN Menu", "Accessed BIN skipper tools")
        
        keyboard = types.InlineKeyboardMarkup()
        
        # Add BIN tools
        bins = [
            ("🔍 BIN Checker Pro", "bin_checker"),
            ("💳 Card Validator", "bin_validator"),
            ("🎯 BIN Generator", "bin_generator"),
            ("📊 BIN Analytics", "bin_analytics"),
            ("🔒 Security Scanner", "bin_security"),
            ("⚡ Fast Lookup", "bin_fast")
        ]
        
        for name, callback in bins:
            keyboard.add(types.InlineKeyboardButton(name, callback_data=callback))
        
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        bin_text = """🔍 **BIN SKIPPER TOOLS**

**Available Tools:**
• Professional BIN checking
• Card validation systems
• Advanced analytics
• Security scanning

**Price Range:** £15-40 per tool

Choose a tool:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=bin_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"BIN skipper menu error: {e}")
    
    def handle_bin_lookup_menu(self, call):
        """Handle BIN lookup menu"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "BIN Lookup Menu", "Accessed BIN lookup")
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        bin_text = """🌐 **BIN LOOKUP**

**How to use:**
1. Send any 6-digit BIN number
2. Get instant detailed information
3. Free lookups for all users

**Information provided:**
• Bank name and country
• Card type and level
• Network (Visa/Mastercard)
• Additional security details

**Send a BIN number to start lookup:**"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=bin_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"BIN lookup menu error: {e}")
    
    def handle_rules_menu(self, call):
        """Handle rules and refund policy"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Rules Menu", "Accessed rules and policies")
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        rules_text = """📋 **RULES & REFUND POLICY**

**Terms of Service:**
• No refunds on digital products
• All sales are final
• Products delivered instantly
• Quality guaranteed

**Payment Policy:**
• Bitcoin payments only
• Exact amounts required
• No chargebacks possible
• Credits added after confirmation

**Usage Rules:**
• Products for authorized use only
• No sharing or reselling
• Follow local laws
• Account suspension for violations

**Refund Policy:**
• Digital products are non-refundable
• Technical issues will be resolved
• Product replacements available
• Contact support for assistance

**Contact:** @HeisenbergActives"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=rules_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Rules menu error: {e}")
    
    def handle_support_menu(self, call):
        """Handle support menu with contact options"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Support Menu", "Accessed support options")
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton('👤 Contact Admin', callback_data='contact_admin'),
            types.InlineKeyboardButton('🎫 Submit Ticket', callback_data='submit_ticket')
        )
        keyboard.add(
            types.InlineKeyboardButton('❓ FAQ', callback_data='faq'),
            types.InlineKeyboardButton('📢 Channel', url='https://t.me/HeisenbergStoreUk')
        )
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        support_text = """🆘 **SUPPORT CENTER**

**Available Support Options:**
• Direct admin contact
• Ticket submission system
• FAQ section
• Official channel

**Response Time:**
• Admin contact: 1-6 hours
• Ticket system: 12-24 hours
• Channel updates: Real-time

**Support Hours:**
• 24/7 automated responses
• Live support: 8 AM - 11 PM UTC

Choose a support option:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=support_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Support menu error: {e}")
    
    def handle_info_menu(self, call):
        """Handle info menu"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        self.log_user_activity(user_id, username, "Info Menu", "Accessed bot information")
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        info_text = """ℹ️ **FULLZ HAVEN Information**

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
Contact @HeisenbergActives

**Channel:**
https://t.me/HeisenbergStoreUk

**Terms:**
By using this service, you agree to our terms of service."""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=info_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Info menu error: {e}")
    
    def handle_bin_analysis(self, message):
        """Handle BIN code analysis"""
        user_id = message.from_user.id
        username = message.from_user.username or f"User{user_id}"
        bin_code = message.text.strip()
        
        self.log_user_activity(user_id, username, "BIN Analysis", f"Analyzed BIN: {bin_code}")
        
        # Simulate BIN lookup
        bank_info = {
            "bin": bin_code,
            "bank": "Sample Bank",
            "country": "United States",
            "type": "CREDIT",
            "level": "STANDARD",
            "network": "VISA"
        }
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔍 Another Lookup', callback_data='bin_lookup'))
        keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
        
        result_text = f"""🔍 **BIN LOOKUP RESULT**

**BIN:** {bin_code}
**Bank:** {bank_info['bank']}
**Country:** {bank_info['country']}
**Type:** {bank_info['type']}
**Level:** {bank_info['level']}
**Network:** {bank_info['network']}

**Additional Info:**
• Active BIN
• No restrictions
• Standard processing"""
        
        try:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=result_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"BIN analysis error: {e}")
    
    def handle_product_purchase(self, call):
        """Handle autonomous product purchases across all categories"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        # Product pricing
        prices = {
            'fullz_usa': 25, 'fullz_uk': 20, 'fullz_ca': 28, 'fullz_au': 30,
            'cc_usa': 45, 'cc_uk': 40, 'cc_ca': 48, 'cc_au': 50,
            'crypto_premium': 75, 'crypto_fresh': 65, 'crypto_vip': 85,
            'spam_email': 35, 'spam_sms': 30, 'spam_leads': 40,
            'bin_checker': 25, 'bin_validator': 30, 'bin_generator': 35
        }
        
        product_name = call.data
        price = prices.get(product_name, 25)
        
        self.log_purchase_attempt(user_id, username, product_name, price, "Digital Product")
        
        # Check balance
        balance = self.get_user_balance(user_id)
        if balance >= price:
            # Process purchase
            self.deduct_user_balance(user_id, price)
            new_balance = self.get_user_balance(user_id)
            
            # Generate product content
            product_content = self.generate_product_content(product_name, price)
            
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton('🛒 Buy More', callback_data='start'))
            
            success_text = f"""✅ **PURCHASE SUCCESSFUL**

**Product:** {product_name.replace('_', ' ').title()}
**Price:** £{price}
**New Balance:** £{new_balance:.2f}

**Product Content:**
{product_content}

**Transaction ID:** {random.randint(100000, 999999)}
**Delivery:** Instant

Thank you for your purchase!"""
            
            try:
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=success_text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Purchase success error: {e}")
        else:
            # Insufficient balance
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton('💰 Add Funds', callback_data='wallet'))
            keyboard.add(types.InlineKeyboardButton('❌ Back', callback_data='start'))
            
            insufficient_text = f"""❌ **INSUFFICIENT BALANCE**

**Product:** {product_name.replace('_', ' ').title()}
**Price:** £{price}
**Your Balance:** £{balance:.2f}
**Required:** £{price - balance:.2f} more

Add funds to your wallet to complete this purchase."""
            
            try:
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=insufficient_text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Insufficient balance error: {e}")
    
    def generate_product_content(self, category, product):
        """Generate product content for delivery"""
        
        content_templates = {
            'fullz_usa': """**USA FULLZ DATA**
Full Name: John Smith
SSN: 123-45-6789
DOB: 01/15/1985
Address: 123 Main St, New York, NY 10001
Phone: (555) 123-4567
Email: john.smith@email.com
Mother's Maiden: Johnson""",
            
            'crypto_premium': """**CRYPTO LEAD PACKAGE**
Total Records: 1,000 leads
Quality: Premium verified
Countries: USA, UK, Canada
Formats: CSV, Excel
Update: Fresh (this week)
Contact: Active traders only""",
            
            'bin_checker': """**BIN CHECKER TOOL**
Tool: Professional BIN Checker
Features: Real-time validation
Database: 500,000+ BINs
Updates: Daily
Access: 30 days
Login: binchecker.com"""
        }
        
        return content_templates.get(category, f"**{product.upper()} PRODUCT**\nContent delivered successfully!\nTransaction completed.")
    
    def run(self):
        """Start the bot"""
        logger.info("🚀 FULLZ HAVEN Bot starting...")
        
        # Notify admin
        self.notify_admin("🚀 **FULLZ HAVEN Bot Started**\n✅ All systems operational")
        
        try:
            logger.info("🔄 Starting bot polling...")
            self.bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            logger.error(f"Bot polling error: {e}")
            time.sleep(5)
            if self.running:
                self.run()

def main():
    """Main function to start the bot"""
    bot = FullzHavenBot()
    bot.run()

if __name__ == "__main__":
    main()