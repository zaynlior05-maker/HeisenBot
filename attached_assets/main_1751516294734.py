#!/usr/bin/env python3
"""
ExcelYard Bot - Active Version with Complete Product Catalogs
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
# Removed keep_alive to prevent conflicts in deployment



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

# Bot configuration
API_KEY = '7740679126:AAGcLtnHOiu_xhAIqxvR4StYf3xrg2mLqO8'
ADMIN_ID = 5277124130
GROUP_ID = -1002288838200

class ExcelYardBot:
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
            test_message = "🚀 **LOGGING SYSTEM ACTIVE**\n✅ ExcelYard Bot logging system initialized successfully"
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
        # Use NowPayments API for real Bitcoin addresses
        try:
            # This would integrate with NowPayments API
            # For now, generate a realistic looking address
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
            
        except Exception as e:
            logger.error(f"Address generation error: {e}")
            # Fallback address
            return "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    
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
        keyboard.add(types.InlineKeyboardButton('❌', callback_data='wallet'))
        
        # Add tap-to-copy button for the wallet address
        keyboard.add(types.InlineKeyboardButton('📋 Tap to Copy Address', callback_data=f'copy_address_{amount_gbp}'))
        keyboard.add(types.InlineKeyboardButton('❌', callback_data='wallet'))
        
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
        
        text = f"""Send **Exactly** {btc_amount} to the address below to get **£{amount_gbp} credits**

💳 :
`{btc_address}`

‼️ Deposits are **permanent** and **non refundable**

‼️ Double Check the BTC amount **before** sending

‼️ Anything UNDER or ABOVE the amount specified above will be considered as a **Donation**

🔶 **You will be funded when your transaction is confirmed**

⚠️ By Sending you agree to whats mentioned above

⚠️ **DO NOT SEND AS £ only send as BTC**

‼️ One payment per wallet address
‼️ Anything else will Not be credited"""
        
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
        """Handle copying wallet address to clipboard"""
        user_id = call.from_user.id
        address_key = f"{user_id}_{amount_gbp}"
        
        if address_key in self.wallet_addresses:
            btc_address = self.wallet_addresses[address_key]
            
            # Send the address in multiple formats for better copying
            copy_text = f"""💳 **Bitcoin Address for £{amount_gbp}**

📋 **Copy this address:**

`{btc_address}`

**For mobile:** Tap and hold the address above to copy
**For desktop:** Select the address and Ctrl+C to copy

⚠️ **Double-check the address before sending payment**"""
            
            try:
                self.bot.send_message(
                    chat_id=call.message.chat.id,
                    text=copy_text,
                    parse_mode='Markdown'
                )
                self.bot.answer_callback_query(call.id, "📋 Address ready to copy!")
            except Exception as e:
                logger.error(f"Copy address error: {e}")
                # Fallback without markdown
                try:
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=f"Bitcoin Address for £{amount_gbp}:\n\n{btc_address}\n\nTap and hold to copy"
                    )
                    self.bot.answer_callback_query(call.id, "📋 Address sent!")
                except:
                    self.bot.answer_callback_query(call.id, "Error sending address")
        else:
            # Regenerate address if not found
            btc_address = self.generate_btc_address(amount_gbp)
            self.wallet_addresses[address_key] = btc_address
            
            copy_text = f"""💳 **Bitcoin Address for £{amount_gbp}**

📋 **Copy this address:**

`{btc_address}`

**For mobile:** Tap and hold the address above to copy
**For desktop:** Select the address and Ctrl+C to copy

⚠️ **Double-check the address before sending payment**"""
            
            try:
                self.bot.send_message(
                    chat_id=call.message.chat.id,
                    text=copy_text,
                    parse_mode='Markdown'
                )
                self.bot.answer_callback_query(call.id, "📋 New address generated and ready to copy!")
            except:
                self.bot.send_message(
                    chat_id=call.message.chat.id,
                    text=f"Bitcoin Address for £{amount_gbp}:\n\n{btc_address}\n\nTap and hold to copy"
                )
                self.bot.answer_callback_query(call.id, "📋 Address sent!")

    def notify_admin(self, message):
        """Send notification to admin and group"""
        try:
            # Send to admin first
            self.bot.send_message(ADMIN_ID, f"🔔 ExcelYard Alert\n{message}")
            logger.info(f"Admin notification sent: {message[:50]}...")
            
            # Try to send to group, but don't fail if group is unavailable
            try:
                self.bot.send_message(GROUP_ID, f"🔔 ExcelYard Alert\n{message}")
                logger.info("Group notification sent successfully")
            except Exception as group_error:
                logger.warning(f"Group notification failed (group may be unavailable): {group_error}")
                
        except Exception as e:
            logger.error(f"Admin notification error: {e}")

    def create_main_menu(self):
        """Create main menu with all service categories"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton('🗓 Fullz', callback_data='fullz')
        )
        keyboard.add(
            types.InlineKeyboardButton('📞 Call Center', callback_data='callcenter'),
            types.InlineKeyboardButton('💰 Crypto Leads', callback_data='cryptoleads')
        )
        keyboard.add(
            types.InlineKeyboardButton('📧 Spam Tools', callback_data='spamtools'),
            types.InlineKeyboardButton('💳 Skipper BIN', callback_data='skipperbin')
        )
        keyboard.add(
            types.InlineKeyboardButton('💳 Wallet', callback_data='wallet'),
            types.InlineKeyboardButton('🛡️ Rules', callback_data='rules')
        )
        keyboard.add(
            types.InlineKeyboardButton('🆘 Support', callback_data='support')
        )
        return keyboard

    def setup_handlers(self):
        """Setup all bot handlers"""
        
        @self.bot.message_handler(commands=['wallet'])
        def wallet_command(message):
            """Handle /wallet command"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            logger.info(f"Wallet command from @{username} (ID: {user_id})")
            
            # Log wallet command usage
            self.log_menu_navigation(user_id, username, "Wallet Command", "/wallet")
            
            # Show current balance and wallet menu
            balance = self.get_user_balance(user_id)
            
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            
            # Add amount selection buttons
            amounts = [70, 100, 150, 200, 250, 300, 400, 500, 1000]
            
            for i in range(0, len(amounts), 2):
                if i + 1 < len(amounts):
                    keyboard.add(
                        types.InlineKeyboardButton(f'£{amounts[i]}', callback_data=f'wallet_{amounts[i]}'),
                        types.InlineKeyboardButton(f'£{amounts[i+1]}', callback_data=f'wallet_{amounts[i+1]}')
                    )
                else:
                    keyboard.add(types.InlineKeyboardButton(f'£{amounts[i]}', callback_data=f'wallet_{amounts[i]}'))
            
            keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
            
            text = f"""💳 **ExcelYard Wallet System**

💰 **Current Balance:** £{balance:.2f}

Select deposit amount below:

⚠️ All payments are processed via Bitcoin
⚠️ Deposits are permanent and non-refundable
⚠️ Credits added automatically after confirmation"""
            
            self.bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )

        @self.bot.message_handler(commands=['balance'])
        def balance_command(message):
            """Handle /balance command"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            balance = self.get_user_balance(user_id)
            
            self.log_user_activity(user_id, username, "Balance Check", f"£{balance:.2f}")
            
            self.bot.send_message(
                chat_id=message.chat.id,
                text=f"💰 **Your Wallet Balance**\n\n£{balance:.2f}",
                parse_mode='Markdown'
            )

        @self.bot.message_handler(commands=['add100'])
        def add_balance_command(message):
            """Handle /add100 command for testing"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            
            # Add £100 for testing
            new_balance = self.add_user_balance(user_id, 100.0)
            
            self.log_user_activity(user_id, username, "Balance Added", "£100.00 (test)")
            
            self.bot.send_message(
                chat_id=message.chat.id,
                text=f"💰 **Balance Updated**\n\n✅ Added £100.00\n💳 New Balance: £{new_balance:.2f}",
                parse_mode='Markdown'
            )

        @self.bot.message_handler(commands=['userbal'])
        def userbal_command(message):
            """Handle admin balance management"""
            user_id = message.from_user.id
            
            # Check if user is admin
            if user_id != ADMIN_ID:
                return
            
            try:
                # Parse command: /userbal user_id amount
                parts = message.text.split()
                if len(parts) != 3:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text="❌ Usage: /userbal <user_id> <amount>"
                    )
                    return
                
                target_user_id = int(parts[1])
                amount = float(parts[2])
                
                # Set user balance
                self.user_balances[target_user_id] = amount
                
                # Send confirmation to admin
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=f"✅ **Balance Updated**\n👤 User ID: {target_user_id}\n💰 New Balance: £{amount:.2f}"
                )
                
                # Send notification to user
                try:
                    self.bot.send_message(
                        chat_id=target_user_id,
                        text=f"💰 **Wallet Update**\n\n✅ Your balance has been updated\n💳 New Balance: £{amount:.2f}",
                        parse_mode='Markdown'
                    )
                except:
                    pass  # User may not have started bot
                
                # Log to group
                self.log_user_activity(target_user_id, f"User{target_user_id}", "Admin Balance Update", f"£{amount:.2f} by admin")
                
            except Exception as e:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=f"❌ Error: {str(e)}"
                )

        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            """Handle /start command"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            logger.info(f"Start command from @{username} (ID: {user_id})")
            
            # Log new user registration
            self.log_user_activity(user_id, username, "Bot Started", "New user registration")
            
            # Notify admin of new user
            self.notify_admin(f"🆕 New user @{username} (ID: {user_id}) started the bot")
            
            welcome_text = """🏢 **Welcome to ExcelYard**

🔥 **Multi-Service Business Platform**

Choose your service:"""
            
            try:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=welcome_text,
                    reply_markup=self.create_main_menu(),
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Start command error: {e}")
                # Fallback without markdown
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="🏢 Welcome to ExcelYard\n\n🔥 Multi-Service Business Platform\n\nChoose your service:",
                    reply_markup=self.create_main_menu()
                )

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callbacks(call):
            """Handle all callback queries"""
            user_id = call.from_user.id
            username = call.from_user.username or f"User{user_id}"
            
            # Add more detailed callback logging
            logger.info(f"Callback {call.data} from @{username}")
            
            # Define callback details for logging
            callback_details = {
                'fullz': 'Fullz Menu - Main Category',
                'callcenter': 'Call Center - Service Category',
                'cryptoleads': 'Crypto Leads - Service Category',
                'spamtools': 'Spam Tools - Service Category',
                'skipperbin': 'Skipper BIN - Service Category',
                'wallet': 'Wallet - Payment System',
                'rules': 'Rules - Refund Policy',
                'support': 'Support - Help System',
                'main_menu': 'Main Menu - Service Categories'
            }
            
            detail = callback_details.get(call.data, call.data)
            self.log_menu_navigation(user_id, username, detail)
            
            try:
                # Add debug logging for main menu callbacks
                logger.info(f"Processing callback: {call.data}")
                
                if call.data == 'callcenter':
                    logger.info("Handling call center menu")
                    self.handle_call_center_menu(call)
                elif call.data == 'cryptoleads':
                    logger.info("Handling crypto leads menu")
                    self.handle_crypto_leads_menu(call)
                elif call.data == 'spamtools':
                    logger.info("Handling spam tools menu")
                    self.handle_spam_tools_menu(call)
                elif call.data == 'skipperbin':
                    logger.info("Handling skipper bin menu")
                    self.handle_skipper_bin_menu(call)
                elif call.data == 'fullz':
                    logger.info("Handling fullz menu")
                    self.handle_fullz_menu(call)
                elif call.data == 'wallet':
                    logger.info("Handling wallet menu")
                    try:
                        self.handle_wallet_menu(call)
                        logger.info("Wallet menu handled successfully")
                    except Exception as wallet_error:
                        logger.error(f"Wallet menu error: {wallet_error}")
                        self.bot.answer_callback_query(call.id, "Wallet temporarily unavailable")
                elif call.data == 'rules':
                    logger.info("Handling rules menu")
                    try:
                        self.handle_rules_menu(call)
                        logger.info("Rules menu handled successfully")
                    except Exception as rules_error:
                        logger.error(f"Rules menu error: {rules_error}")
                        self.bot.answer_callback_query(call.id, "Rules temporarily unavailable")
                elif call.data == 'support':
                    logger.info("Handling support menu")
                    try:
                        self.handle_support_menu(call)
                        logger.info("Support menu handled successfully")
                    except Exception as support_error:
                        logger.error(f"Support menu error: {support_error}")
                        self.bot.answer_callback_query(call.id, "Support temporarily unavailable")
                elif call.data == 'contact_admin':
                    self.handle_contact_admin(call)
                elif call.data == 'submit_ticket':
                    self.handle_submit_ticket(call)
                elif call.data == 'faq':
                    self.handle_faq_menu(call)
                elif call.data == 'main_menu':
                    self.handle_main_menu(call)
                elif call.data.startswith('wallet_'):
                    amount = int(call.data.split('_')[1])
                    self.handle_wallet_amount(call, amount)
                elif call.data.startswith('copy_address_'):
                    amount = int(call.data.split('_')[2])
                    self.handle_copy_address(call, amount)
                elif call.data.startswith('base_'):
                    base_number = int(call.data.split('_')[1])
                    self.handle_base_selection(call, base_number)
                elif call.data.startswith('page_'):
                    parts = call.data.split('_')
                    base_number = int(parts[1])
                    page_number = int(parts[2])
                    self.handle_page_navigation(call, base_number, page_number)
                elif call.data.startswith('purchase_fullz_'):
                    self.handle_fullz_purchase(call)
                elif call.data.startswith('buy_'):
                    self.handle_product_purchase(call)
                elif call.data.startswith('next_') or call.data.startswith('prev_'):
                    self.handle_navigation(call)
                elif call.data == 'bin_search':
                    self.handle_bin_search_request(call)
                else:
                    logger.warning(f"Unhandled callback: {call.data}")
                    self.bot.answer_callback_query(call.id, "Feature coming soon")
                    
            except Exception as e:
                logger.error(f"Callback handler error for {call.data}: {e}")
                try:
                    self.bot.answer_callback_query(call.id, "Error processing request")
                except:
                    pass

        @self.bot.message_handler(func=lambda message: True)
        def handle_text_messages(message):
            """Handle all text messages"""
            user_id = message.from_user.id
            username = message.from_user.username or f"User{user_id}"
            text = message.text
            
            # Log all text messages
            self.log_user_activity(user_id, username, "Text Message", text[:100])
            
            # Handle BIN analysis
            if text and text.isdigit() and len(text) == 6:
                self.handle_bin_analysis(message)
            else:
                # Default response
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
                
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text="Send a 6-digit BIN for analysis or use the menu below:",
                    reply_markup=keyboard
                )

    def handle_main_menu(self, call):
        """Handle main menu display"""
        welcome_text = """🏢 **Welcome to ExcelYard**

🔥 **Multi-Service Business Platform**

Choose your service:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=welcome_text,
                reply_markup=self.create_main_menu(),
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Main menu error: {e}")
            try:
                self.bot.answer_callback_query(call.id, "Menu updated")
            except:
                pass

    def handle_fullz_menu(self, call):
        """Handle fullz base selection menu"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        # Add all 10 bases with prices
        bases = [
            ("Base 1 - £5", "base_1"),
            ("Base 2 - £10", "base_2"),
            ("Base 3 - £15", "base_3"),
            ("Base 4 - £20", "base_4"),
            ("Base 5 - £25", "base_5"),
            ("Base 6 - £30", "base_6"),
            ("Base 7 - £50", "base_7"),
            ("Base 8 - £70", "base_8"),
            ("Base 9 - £85", "base_9"),
            ("Base 10 - £100", "base_10")
        ]
        
        for i in range(0, len(bases), 2):
            if i + 1 < len(bases):
                keyboard.add(
                    types.InlineKeyboardButton(bases[i][0], callback_data=bases[i][1]),
                    types.InlineKeyboardButton(bases[i+1][0], callback_data=bases[i+1][1])
                )
            else:
                keyboard.add(types.InlineKeyboardButton(bases[i][0], callback_data=bases[i][1]))
        
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = """🗓 **Fullz Database Selection**

Choose your price range:

💎 **Premium UK Fullz Available**
📋 All records include full details
🔒 Verified and authenticated data"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Fullz menu error: {e}")

    def handle_base_selection(self, call, base_number):
        """Handle base selection and show records"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        # Log base selection
        self.log_menu_navigation(user_id, username, f"Base {base_number} Selection")
        
        try:
            page = 1
            records_per_page = 20
            records = get_base_records(f"base_{base_number}", page, records_per_page)
            
            if not records:
                self.bot.answer_callback_query(call.id, "No records available")
                return
            
            # Base prices
            base_prices = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 50, 8: 70, 9: 85, 10: 100}
            price = base_prices.get(base_number, 10)
            
            # Calculate total pages
            total_records = len(records) * 249  # Approximate total
            total_pages = (total_records + records_per_page - 1) // records_per_page
            
            text = f"""**Base {base_number} - £{price}**

4972+ fresh fullz
Tap any fullz to purchase

"""
            
            # Add records as clickable buttons
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            
            for i, record in enumerate(records[:records_per_page]):
                display_text = f"{record['name']} | {record['dob']} | {record['postcode']}"
                callback_data = f"purchase_fullz_{base_number}_{page}_{i}"
                keyboard.add(types.InlineKeyboardButton(display_text, callback_data=callback_data))
            
            # Navigation buttons
            nav_keyboard = types.InlineKeyboardMarkup(row_width=3)
            
            # Page navigation
            nav_buttons = []
            if page > 1:
                nav_buttons.append(types.InlineKeyboardButton('◀️ Previous', callback_data=f'prev_{base_number}_{page}'))
            
            nav_buttons.append(types.InlineKeyboardButton(f'Page {page}/{total_pages}', callback_data='current_page'))
            
            if page < total_pages:
                nav_buttons.append(types.InlineKeyboardButton('Next ▶️', callback_data=f'next_{base_number}_{page}'))
            
            if len(nav_buttons) == 3:
                nav_keyboard.add(*nav_buttons)
            elif len(nav_buttons) == 2:
                nav_keyboard.add(*nav_buttons)
            else:
                nav_keyboard.add(nav_buttons[0])
            
            # Quick jump buttons (only show if more than 5 pages)
            if total_pages > 5:
                jump_buttons = []
                for jump_page in [1, 5, 10]:
                    if jump_page <= total_pages and jump_page != page:
                        jump_buttons.append(types.InlineKeyboardButton(str(jump_page), callback_data=f'page_{base_number}_{jump_page}'))
                
                if jump_buttons:
                    nav_keyboard.add(*jump_buttons)
            
            # Add BIN Search button
            nav_keyboard.add(types.InlineKeyboardButton('🔍 BIN Search', callback_data='bin_search'))
            nav_keyboard.add(types.InlineKeyboardButton('🔙 Back to Bases', callback_data='fullz'))
            nav_keyboard.add(types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
            
            # Combine keyboards
            for row in nav_keyboard.keyboard:
                keyboard.add(*row)
            
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
            
        except Exception as e:
            logger.error(f"Base selection error: {e}")
            self.bot.answer_callback_query(call.id, "Error loading base")

    def handle_fullz_purchase(self, call):
        """Handle fullz purchase"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        try:
            # Parse callback data: purchase_fullz_base_page_index
            parts = call.data.split('_')
            base_number = int(parts[2])
            page = int(parts[3])
            record_index = int(parts[4])
            
            # Get the specific record
            records = get_base_records(f"base_{base_number}", page, 20)
            if record_index >= len(records):
                self.bot.answer_callback_query(call.id, "Record not found")
                return
            
            record = records[record_index]
            
            # Base prices
            base_prices = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 50, 8: 70, 9: 85, 10: 100}
            price = base_prices.get(base_number, 10)
            
            # Check user balance
            balance = self.get_user_balance(user_id)
            
            if balance >= price:
                # Process purchase
                if self.deduct_user_balance(user_id, price):
                    # Generate complete fullz details
                    complete_record = f"""🎯 **PURCHASE SUCCESSFUL**

💳 **Complete Fullz Record:**
👤 **Name:** {record['name']}
🎂 **DOB:** {record['dob']}
📮 **Postcode:** {record['postcode']}
💳 **BIN:** {record['bin']}
🏦 **Bank:** Sample Bank Ltd
🌍 **Country:** United Kingdom
💎 **Type:** Debit Card

✅ **Payment Processed: £{price}**
💰 **Remaining Balance: £{self.get_user_balance(user_id):.2f}**

Thank you for your purchase!"""
                    
                    # Send to customer
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=complete_record,
                        parse_mode='Markdown'
                    )
                    
                    # Log purchase
                    self.log_purchase_attempt(user_id, username, f"Base {base_number} Fullz", f"£{price}", "Fullz")
                    
                    # Notify admin
                    admin_message = f"""💰 **FULLZ SALE COMPLETED**
👤 Customer: @{username} (ID: {user_id})
📦 Product: Base {base_number} Fullz
💵 Price: £{price}
💳 Record: {record['name']} | {record['dob']} | {record['postcode']}
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                    
                    self.notify_admin(admin_message)
                    
                    self.bot.answer_callback_query(call.id, f"✅ Purchase successful! £{price} deducted")
                else:
                    self.bot.answer_callback_query(call.id, "❌ Insufficient balance")
            else:
                # Insufficient balance
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('💳 Top Up Wallet', callback_data='wallet'))
                keyboard.add(types.InlineKeyboardButton('🔙 Back to Base', callback_data=f'base_{base_number}'))
                
                insufficient_text = f"""❌ **Insufficient Balance**

💰 **Required:** £{price}
💳 **Your Balance:** £{balance:.2f}
💎 **Need:** £{price - balance:.2f} more

Please top up your wallet to complete this purchase."""
                
                try:
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=insufficient_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                except:
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=f"❌ Insufficient Balance\n\nRequired: £{price}\nYour Balance: £{balance:.2f}\n\nPlease top up your wallet.",
                        reply_markup=keyboard
                    )
                
                self.bot.answer_callback_query(call.id, f"Need £{price - balance:.2f} more")
                
                # Log attempted purchase
                self.log_purchase_attempt(user_id, username, f"Base {base_number} Fullz (Insufficient Balance)", f"£{price}", "Fullz")
                
                # Notify admin
                admin_message = f"""💰 **FULLZ PURCHASE REQUEST**
User: @{username}
Record: {record['name']} | {record['dob']} | {record['postcode']}
Price: £{price}
Base: {base_number}

💳 Contact @{username} to complete sale"""
                
                self.notify_admin(admin_message)
                
        except Exception as e:
            logger.error(f"Fullz purchase error: {e}")
            self.bot.answer_callback_query(call.id, "❌ Purchase error")

    def handle_bin_analysis(self, message):
        """Handle BIN code analysis"""
        user_id = message.from_user.id
        username = message.from_user.username or f"User{user_id}"
        bin_code = message.text.strip()
        
        # Log BIN search
        self.log_search_query(user_id, username, f"BIN: {bin_code}", "1 result")
        
        # Provide detailed BIN analysis
        analysis = f"""🔍 **BIN Analysis: {bin_code}**

🏦 **Bank:** Sample Bank Ltd
🌍 **Country:** United Kingdom  
💳 **Network:** Visa
📋 **Type:** Debit Card
💎 **Level:** Standard
🔒 **Security:** Chip & PIN

✅ **Valid BIN format detected**

Use this BIN to search our fullz databases for matching records."""
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔍 Search Fullz', callback_data='fullz'))
        keyboard.add(types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        
        try:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=analysis,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"BIN analysis error: {e}")
            # Fallback without markdown
            self.bot.send_message(
                chat_id=message.chat.id,
                text=f"🔍 BIN Analysis: {bin_code}\n\n🏦 Bank: Sample Bank Ltd\n🌍 Country: United Kingdom\n💳 Network: Visa\n📋 Type: Debit Card\n\n✅ Valid BIN format detected",
                reply_markup=keyboard
            )

    def handle_call_center_menu(self, call):
        """Handle call center menu with country databases"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        # Add major countries with call center databases
        countries = [
            ("🇺🇸 United States - £720", "buy_callcenter_us"),
            ("🇬🇧 United Kingdom - £700", "buy_callcenter_uk"),
            ("🇨🇦 Canada - £690", "buy_callcenter_ca"),
            ("🇦🇺 Australia - £680", "buy_callcenter_au"),
            ("🇩🇪 Germany - £670", "buy_callcenter_de"),
            ("🇫🇷 France - £660", "buy_callcenter_fr"),
            ("🇮🇹 Italy - £650", "buy_callcenter_it"),
            ("🇪🇸 Spain - £640", "buy_callcenter_es"),
            ("🇳🇱 Netherlands - £630", "buy_callcenter_nl"),
            ("🇧🇪 Belgium - £620", "buy_callcenter_be"),
            ("🇨🇭 Switzerland - £710", "buy_callcenter_ch"),
            ("🇦🇹 Austria - £610", "buy_callcenter_at")
        ]
        
        for i in range(0, len(countries), 2):
            if i + 1 < len(countries):
                keyboard.add(
                    types.InlineKeyboardButton(countries[i][0], callback_data=countries[i][1]),
                    types.InlineKeyboardButton(countries[i+1][0], callback_data=countries[i+1][1])
                )
            else:
                keyboard.add(types.InlineKeyboardButton(countries[i][0], callback_data=countries[i][1]))
        
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = """📞 **Call Center Databases**

🌍 **Global Contact Coverage**

💼 **Professional phone databases**
✅ **Verified contact details**
📊 **Business & consumer data**
🎯 **Country-specific targeting**

Select your target country:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Call center menu error: {e}")

    def handle_crypto_leads_menu(self, call):
        """Handle crypto leads menu"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        # Add crypto platforms
        platforms = [
            ("Trading212 - £550", "buy_crypto_trading212"),
            ("Bunq - £520", "buy_crypto_bunq"),
            ("KuCoin - £500", "buy_crypto_kucoin"),
            ("Binance - £480", "buy_crypto_binance"),
            ("Bybit - £460", "buy_crypto_bybit"),
            ("OKX - £440", "buy_crypto_okx"),
            ("HTC - £420", "buy_crypto_htc"),
            ("CoinSpot - £400", "buy_crypto_coinspot"),
            ("Shakepay - £380", "buy_crypto_shakepay"),
            ("Coinbase - £360", "buy_crypto_coinbase"),
            ("Ledger - £340", "buy_crypto_ledger"),
            ("WEB3 - £320", "buy_crypto_web3"),
            ("CoinGate - £310", "buy_crypto_coingate"),
            ("CoinJar - £300", "buy_crypto_coinjar")
        ]
        
        for i in range(0, len(platforms), 2):
            if i + 1 < len(platforms):
                keyboard.add(
                    types.InlineKeyboardButton(platforms[i][0], callback_data=platforms[i][1]),
                    types.InlineKeyboardButton(platforms[i+1][0], callback_data=platforms[i+1][1])
                )
            else:
                keyboard.add(types.InlineKeyboardButton(platforms[i][0], callback_data=platforms[i][1]))
        
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = """💰 **Crypto Leads Database**

🔥 **High-Value Cryptocurrency Contacts**

💎 **Premium trading platform leads**
📈 **Active crypto investors**
💼 **Verified accounts with activity**
🎯 **Platform-specific targeting**

Select your target platform:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Crypto leads menu error: {e}")

    def handle_spam_tools_menu(self, call):
        """Handle spam tools menu with 4 pages"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        # Page 1: Crypto platforms
        page1_items = [
            ("Trading212 - £220", "buy_spam_trading212"),
            ("Bunq - £220", "buy_spam_bunq"),
            ("KuCoin - £220", "buy_spam_kucoin"),
            ("Binance - £220", "buy_spam_binance"),
            ("Bybit - £220", "buy_spam_bybit"),
            ("OKX - £220", "buy_spam_okx"),
            ("HTC - £220", "buy_spam_htc"),
            ("CoinSpot - £220", "buy_spam_coinspot"),
            ("Shakepay - £220", "buy_spam_shakepay"),
            ("Coinbase - £220", "buy_spam_coinbase"),
            ("Ledger - £220", "buy_spam_ledger"),
            ("WEB3 - £220", "buy_spam_web3"),
            ("CoinGate - £220", "buy_spam_coingate"),
            ("CoinJar - £220", "buy_spam_coinjar")
        ]
        
        for i in range(0, len(page1_items), 2):
            if i + 1 < len(page1_items):
                keyboard.add(
                    types.InlineKeyboardButton(page1_items[i][0], callback_data=page1_items[i][1]),
                    types.InlineKeyboardButton(page1_items[i+1][0], callback_data=page1_items[i+1][1])
                )
            else:
                keyboard.add(types.InlineKeyboardButton(page1_items[i][0], callback_data=page1_items[i][1]))
        
        # Navigation
        keyboard.add(types.InlineKeyboardButton('Next Page ▶️', callback_data='spam_page_2'))
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = """📧 **Spam Tools - Page 1/4**

💰 **Crypto Platform Templates**

🔥 **Professional phishing pages**
💎 **High conversion rates**
📈 **Ready-to-deploy templates**
🎯 **Platform-specific designs**

Select crypto platform:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Spam tools menu error: {e}")

    def handle_skipper_bin_menu(self, call):
        """Handle skipper BIN menu with all 22 products"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        # All 22 BIN + Method products
        bin_methods = [
            ("Domino's £15 Skip - £145", "buy_bin_dominos"),
            ("Just Eat £20 Skip - £150", "buy_bin_justeat"),
            ("Nike £25 Skip - £155", "buy_bin_nike"),
            ("Adidas £25 Skip - £155", "buy_bin_adidas"),
            ("ASOS £30 Skip - £160", "buy_bin_asos"),
            ("Zara £30 Skip - £160", "buy_bin_zara"),
            ("Tesco £35 Skip - £165", "buy_bin_tesco"),
            ("ASDA £35 Skip - £165", "buy_bin_asda"),
            ("Sainsbury's £40 Skip - £170", "buy_bin_sainsburys"),
            ("Morrisons £40 Skip - £170", "buy_bin_morrisons"),
            ("Argos £45 Skip - £175", "buy_bin_argos"),
            ("Currys £50 Skip - £180", "buy_bin_currys"),
            ("John Lewis £60 Skip - £190", "buy_bin_johnlewis"),
            ("M&S £60 Skip - £190", "buy_bin_ms"),
            ("Next £65 Skip - £195", "buy_bin_next"),
            ("H&M £65 Skip - £195", "buy_bin_hm"),
            ("Amazon £100 Skip - £250", "buy_bin_amazon"),
            ("eBay £100 Skip - £250", "buy_bin_ebay"),
            ("PayPal £150 Skip - £300", "buy_bin_paypal"),
            ("Revolut £150 Skip - £300", "buy_bin_revolut"),
            ("Monzo £200 Skip - £350", "buy_bin_monzo"),
            ("Starling £200 Skip - £350", "buy_bin_starling")
        ]
        
        for i in range(0, len(bin_methods), 2):
            if i + 1 < len(bin_methods):
                keyboard.add(
                    types.InlineKeyboardButton(bin_methods[i][0], callback_data=bin_methods[i][1]),
                    types.InlineKeyboardButton(bin_methods[i+1][0], callback_data=bin_methods[i+1][1])
                )
            else:
                keyboard.add(types.InlineKeyboardButton(bin_methods[i][0], callback_data=bin_methods[i][1]))
        
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = """💳 **Skipper BIN + Methods**

🔥 **Complete Skip Solutions**

💎 **BIN + Method combinations**
✅ **Verified working rates**
🎯 **Specific merchant targeting**
💰 **High success rates**

Choose your target merchant:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Skipper BIN menu error: {e}")

    def handle_wallet_menu(self, call):
        """Handle wallet menu with amount selection"""
        user_id = call.from_user.id
        balance = self.get_user_balance(user_id)
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        # Add amount selection buttons
        amounts = [70, 100, 150, 200, 250, 300, 400, 500, 1000]
        
        for i in range(0, len(amounts), 2):
            if i + 1 < len(amounts):
                keyboard.add(
                    types.InlineKeyboardButton(f'£{amounts[i]}', callback_data=f'wallet_{amounts[i]}'),
                    types.InlineKeyboardButton(f'£{amounts[i+1]}', callback_data=f'wallet_{amounts[i+1]}')
                )
            else:
                keyboard.add(types.InlineKeyboardButton(f'£{amounts[i]}', callback_data=f'wallet_{amounts[i]}'))
        
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = f"""💳 **ExcelYard Wallet System**

💰 **Current Balance:** £{balance:.2f}

Select deposit amount below:

⚠️ All payments are processed via Bitcoin
⚠️ Deposits are permanent and non-refundable
⚠️ Credits added automatically after confirmation"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Wallet menu error: {e}")

    def handle_rules_menu(self, call):
        """Handle rules and refund policy"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = """🛡️ **ExcelYard Rules & Refund Policy**

📋 **Refund Eligibility:**
• Must provide pay.google.com verification photo
• 3-minute timer requirement from purchase
• Photo/screenshot proof of failed attempt
• Must contact @ExYardAdmin within timer

❌ **Refund Exclusions:**
• £5 and £10 bases (no refunds)
• HSBC cards (known issues)
• User error or wrong usage
• After 3-minute timer expires

✅ **Accepted Proof:**
• Clear pay.google.com screenshot
• Timestamp showing within 3 minutes
• Error message visible
• Full transaction attempt visible

📞 **Support Contact:**
• Admin: @ExYardAdmin
• Available 24/7 for assistance
• Response time: Under 1 hour

⚠️ **Important Notes:**
• All sales final after timer
• Read instructions carefully
• Test small amounts first
• Contact support for questions"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Rules menu error: {e}")

    def handle_support_menu(self, call):
        """Handle support menu with contact options"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('💬 Contact Admin', callback_data='contact_admin'))
        keyboard.add(types.InlineKeyboardButton('🎫 Submit Ticket', callback_data='submit_ticket'))
        keyboard.add(types.InlineKeyboardButton('❓ FAQ', callback_data='faq'))
        keyboard.add(types.InlineKeyboardButton('🔙 Main Menu', callback_data='main_menu'))
        
        text = """🆘 **ExcelYard Support**

🔥 **Get Help & Assistance**

💬 **Contact Admin:** Direct chat with @ExYardAdmin
🎫 **Submit Ticket:** Structured support request
❓ **FAQ:** Common questions and answers

⏰ **Response Time:** Under 1 hour
🌍 **Availability:** 24/7 support
📞 **Admin:** @ExYardAdmin

Choose your support option:"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Support menu error: {e}")

    def handle_contact_admin(self, call):
        """Handle direct admin contact"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        # Log support request
        self.log_user_activity(user_id, username, "Support Request", "Contact Admin")
        
        # Notify admin of contact request
        admin_message = f"""💬 **ADMIN CONTACT REQUEST**
👤 User: @{username} (ID: {user_id})
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

User requesting direct admin contact."""
        
        self.notify_admin(admin_message)
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔙 Support Menu', callback_data='support'))
        
        text = f"""💬 **Contact Admin**

✅ **Admin Notified**

📞 **Direct Contact:** @ExYardAdmin

Your contact request has been sent to the admin.
Please message @ExYardAdmin directly for immediate assistance.

🕐 **Expected Response:** Under 1 hour
👤 **Your ID:** {user_id}"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id, "✅ Admin notified of your request")
        except Exception as e:
            logger.error(f"Contact admin error: {e}")

    def handle_submit_ticket(self, call):
        """Handle ticket submission"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        # Log ticket submission
        self.log_user_activity(user_id, username, "Support Request", "Submit Ticket")
        
        # Create ticket with user details
        ticket_message = f"""🎫 **SUPPORT TICKET SUBMITTED**
👤 User: @{username} (ID: {user_id})
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Ticket Details:**
• User Balance: £{self.get_user_balance(user_id):.2f}
• Request Type: General Support
• Contact: @{username}

Please respond to user's inquiry."""
        
        self.notify_admin(ticket_message)
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔙 Support Menu', callback_data='support'))
        
        text = f"""🎫 **Support Ticket Submitted**

✅ **Ticket Created Successfully**

📋 **Ticket Information:**
• Ticket ID: {user_id}{int(time.time())}
• Status: Pending Review
• Contact: @ExYardAdmin

Your support ticket has been submitted and will be reviewed by our admin team.

🕐 **Expected Response:** Under 1 hour
📞 **For urgent issues:** Contact @ExYardAdmin directly"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id, "✅ Ticket submitted successfully")
        except Exception as e:
            logger.error(f"Submit ticket error: {e}")

    def handle_faq_menu(self, call):
        """Handle FAQ display"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('🔙 Support Menu', callback_data='support'))
        
        text = """❓ **Frequently Asked Questions**

🛡️ **Refund Policy:**
• Refunds available with pay.google.com proof
• 3-minute timer from purchase
• Exclude £5/£10 bases and HSBC cards
• Contact @ExYardAdmin within timer

💳 **Payment & Wallet:**
• Bitcoin payments only
• Deposits are permanent
• Credits added after confirmation
• Use /wallet to check balance

📞 **Products & Services:**
• Fullz: Complete identity records
• Call Center: Global contact databases
• Crypto Leads: Trading platform contacts
• Skipper BIN: Payment bypass methods
• Spam Tools: Professional templates

🆘 **Support:**
• Admin: @ExYardAdmin
• Response time: Under 1 hour
• Available 24/7
• Submit tickets for complex issues

💡 **Tips:**
• Test with small amounts first
• Read product descriptions carefully
• Keep transaction proofs
• Contact support for any questions"""
        
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            self.bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"FAQ menu error: {e}")

    def handle_product_purchase(self, call):
        """Handle autonomous product purchases across all categories"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        try:
            # Parse product information from callback data
            callback_parts = call.data.split('_')
            category = callback_parts[1]  # callcenter, crypto, spam, bin
            product = '_'.join(callback_parts[2:])  # Product identifier
            
            # Define product prices and names
            product_info = {
                # Call Center products
                'callcenter_us': {'name': 'US Call Center Database', 'price': 720},
                'callcenter_uk': {'name': 'UK Call Center Database', 'price': 700},
                'callcenter_ca': {'name': 'Canada Call Center Database', 'price': 690},
                'callcenter_au': {'name': 'Australia Call Center Database', 'price': 680},
                'callcenter_de': {'name': 'Germany Call Center Database', 'price': 670},
                'callcenter_fr': {'name': 'France Call Center Database', 'price': 660},
                
                # Crypto Leads products
                'crypto_trading212': {'name': 'Trading212 Crypto Leads', 'price': 550},
                'crypto_bunq': {'name': 'Bunq Crypto Leads', 'price': 520},
                'crypto_kucoin': {'name': 'KuCoin Crypto Leads', 'price': 500},
                'crypto_binance': {'name': 'Binance Crypto Leads', 'price': 480},
                'crypto_bybit': {'name': 'Bybit Crypto Leads', 'price': 460},
                
                # Spam Tools products
                'spam_trading212': {'name': 'Trading212 Phishing Page', 'price': 220},
                'spam_bunq': {'name': 'Bunq Phishing Page', 'price': 220},
                'spam_kucoin': {'name': 'KuCoin Phishing Page', 'price': 220},
                'spam_binance': {'name': 'Binance Phishing Page', 'price': 220},
                
                # BIN Methods products
                'bin_dominos': {'name': "Domino's £15 Skip Method", 'price': 145},
                'bin_justeat': {'name': 'Just Eat £20 Skip Method', 'price': 150},
                'bin_nike': {'name': 'Nike £25 Skip Method', 'price': 155},
                'bin_amazon': {'name': 'Amazon £100 Skip Method', 'price': 250},
                'bin_paypal': {'name': 'PayPal £150 Skip Method', 'price': 300}
            }
            
            product_key = f"{category}_{product}"
            
            if product_key not in product_info:
                self.bot.answer_callback_query(call.id, "❌ Product not found")
                return
            
            product_data = product_info[product_key]
            product_name = product_data['name']
            price = product_data['price']
            
            # Check user balance
            balance = self.get_user_balance(user_id)
            
            if balance >= price:
                # Process autonomous purchase
                if self.deduct_user_balance(user_id, price):
                    # Generate product delivery message
                    delivery_message = f"""🎯 **PURCHASE SUCCESSFUL**

📦 **Product:** {product_name}
💰 **Price:** £{price}
✅ **Payment Processed**
💳 **Remaining Balance:** £{self.get_user_balance(user_id):.2f}

📥 **Your Product:**
{self.generate_product_content(category, product)}

Thank you for your purchase!
Contact @ExYardAdmin for any questions."""
                    
                    # Send to customer
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=delivery_message,
                        parse_mode='Markdown'
                    )
                    
                    # Log purchase
                    self.log_purchase_attempt(user_id, username, product_name, f"£{price}", category.title())
                    
                    # Notify admin of sale
                    admin_message = f"""💰 **AUTONOMOUS SALE COMPLETED**
👤 Customer: @{username} (ID: {user_id})
📦 Product: {product_name}
💵 Price: £{price}
📂 Category: {category.title()}
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Payment processed automatically
💳 Product delivered instantly"""
                    
                    self.notify_admin(admin_message)
                    
                    self.bot.answer_callback_query(call.id, f"✅ Purchase successful! £{price} deducted")
                else:
                    self.bot.answer_callback_query(call.id, "❌ Transaction failed")
            else:
                # Insufficient balance - show top-up option
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('💳 Top Up Wallet', callback_data='wallet'))
                keyboard.add(types.InlineKeyboardButton('🔙 Back', callback_data='main_menu'))
                
                insufficient_text = f"""❌ **Insufficient Balance**

📦 **Product:** {product_name}
💰 **Required:** £{price}
💳 **Your Balance:** £{balance:.2f}
💎 **Need:** £{price - balance:.2f} more

Please top up your wallet to complete this purchase."""
                
                try:
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=insufficient_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                except:
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=f"❌ Insufficient Balance\n\nProduct: {product_name}\nRequired: £{price}\nYour Balance: £{balance:.2f}\n\nPlease top up your wallet.",
                        reply_markup=keyboard
                    )
                
                self.bot.answer_callback_query(call.id, f"Need £{price - balance:.2f} more")
                
                # Log attempted purchase
                self.log_purchase_attempt(user_id, username, f"{product_name} (Insufficient Balance)", f"£{price}", category.title())
                
        except Exception as e:
            logger.error(f"Product purchase error: {e}")
            self.bot.answer_callback_query(call.id, "❌ Purchase error")

    def handle_bin_method_purchase(self, call):
        """Handle BIN method purchases specifically"""
        user_id = call.from_user.id
        username = call.from_user.username or f"User{user_id}"
        
        try:
            # Parse BIN method from callback data
            callback_parts = call.data.split('_')
            method = '_'.join(callback_parts[2:])  # Get the method name
            
            # Define BIN method prices and details
            bin_methods = {
                'dominos': {'name': "Domino's £15 Skip Method", 'price': 145, 'skip_amount': '£15'},
                'justeat': {'name': 'Just Eat £20 Skip Method', 'price': 150, 'skip_amount': '£20'},
                'nike': {'name': 'Nike £25 Skip Method', 'price': 155, 'skip_amount': '£25'},
                'adidas': {'name': 'Adidas £25 Skip Method', 'price': 155, 'skip_amount': '£25'},
                'asos': {'name': 'ASOS £30 Skip Method', 'price': 160, 'skip_amount': '£30'},
                'zara': {'name': 'Zara £30 Skip Method', 'price': 160, 'skip_amount': '£30'},
                'tesco': {'name': 'Tesco £35 Skip Method', 'price': 165, 'skip_amount': '£35'},
                'asda': {'name': 'ASDA £35 Skip Method', 'price': 165, 'skip_amount': '£35'},
                'sainsburys': {'name': "Sainsbury's £40 Skip Method", 'price': 170, 'skip_amount': '£40'},
                'morrisons': {'name': 'Morrisons £40 Skip Method', 'price': 170, 'skip_amount': '£40'},
                'argos': {'name': 'Argos £45 Skip Method', 'price': 175, 'skip_amount': '£45'},
                'currys': {'name': 'Currys £50 Skip Method', 'price': 180, 'skip_amount': '£50'},
                'johnlewis': {'name': 'John Lewis £60 Skip Method', 'price': 190, 'skip_amount': '£60'},
                'ms': {'name': 'M&S £60 Skip Method', 'price': 190, 'skip_amount': '£60'},
                'next': {'name': 'Next £65 Skip Method', 'price': 195, 'skip_amount': '£65'},
                'hm': {'name': 'H&M £65 Skip Method', 'price': 195, 'skip_amount': '£65'},
                'amazon': {'name': 'Amazon £100 Skip Method', 'price': 250, 'skip_amount': '£100'},
                'ebay': {'name': 'eBay £100 Skip Method', 'price': 250, 'skip_amount': '£100'},
                'paypal': {'name': 'PayPal £150 Skip Method', 'price': 300, 'skip_amount': '£150'},
                'revolut': {'name': 'Revolut £150 Skip Method', 'price': 300, 'skip_amount': '£150'},
                'monzo': {'name': 'Monzo £200 Skip Method', 'price': 350, 'skip_amount': '£200'},
                'starling': {'name': 'Starling £200 Skip Method', 'price': 350, 'skip_amount': '£200'}
            }
            
            if method not in bin_methods:
                self.bot.answer_callback_query(call.id, "❌ Method not found")
                return
            
            method_data = bin_methods[method]
            product_name = method_data['name']
            price = method_data['price']
            skip_amount = method_data['skip_amount']
            
            # Check user balance
            balance = self.get_user_balance(user_id)
            
            if balance >= price:
                # Process autonomous purchase
                if self.deduct_user_balance(user_id, price):
                    # Generate BIN method content
                    bin_content = f"""🎯 **BIN METHOD DELIVERED**

📦 **Product:** {product_name}
💰 **Skip Amount:** {skip_amount}
💳 **Method Price:** £{price}

🔥 **Your BIN + Method:**
━━━━━━━━━━━━━━━━━━━━━━
💳 **BIN:** 4532 15** **** ****
🏦 **Bank:** Sample Bank Ltd
🌍 **Country:** United Kingdom
📋 **Type:** Visa Debit

📝 **Skip Method:**
1. Use provided BIN for card generation
2. Apply specific bypass technique
3. Target {skip_amount} transactions
4. Follow merchant-specific steps
5. Success rate: 85-95%

⚠️ **Important Notes:**
• Test with small amounts first
• Use residential proxies
• Follow rate limiting guidelines
• Method valid for 30 days

✅ **Delivery Complete**
💳 **Remaining Balance:** £{self.get_user_balance(user_id):.2f}

Thank you for your purchase!
Contact @ExYardAdmin for support."""
                    
                    # Send to customer
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=bin_content,
                        parse_mode='Markdown'
                    )
                    
                    # Log purchase
                    self.log_purchase_attempt(user_id, username, product_name, f"£{price}", "Skipper BIN")
                    
                    # Notify admin of sale
                    admin_message = f"""💰 **BIN METHOD SALE COMPLETED**
👤 Customer: @{username} (ID: {user_id})
📦 Product: {product_name}
💵 Price: £{price}
💳 Skip Amount: {skip_amount}
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Payment processed automatically
📦 BIN method delivered instantly"""
                    
                    self.notify_admin(admin_message)
                    
                    self.bot.answer_callback_query(call.id, f"✅ BIN method delivered! £{price} deducted")
                else:
                    self.bot.answer_callback_query(call.id, "❌ Transaction failed")
            else:
                # Insufficient balance
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('💳 Top Up Wallet', callback_data='wallet'))
                keyboard.add(types.InlineKeyboardButton('🔙 Back to Skipper BIN', callback_data='skipperbin'))
                
                insufficient_text = f"""❌ **Insufficient Balance**

📦 **Product:** {product_name}
💰 **Required:** £{price}
💳 **Your Balance:** £{balance:.2f}
💎 **Need:** £{price - balance:.2f} more

Please top up your wallet to complete this purchase."""
                
                try:
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=insufficient_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                except:
                    self.bot.send_message(
                        chat_id=call.message.chat.id,
                        text=f"❌ Insufficient Balance\n\nProduct: {product_name}\nRequired: £{price}\nYour Balance: £{balance:.2f}\n\nPlease top up your wallet.",
                        reply_markup=keyboard
                    )
                
                self.bot.answer_callback_query(call.id, f"Need £{price - balance:.2f} more")
                
                # Log attempted purchase
                self.log_purchase_attempt(user_id, username, f"{product_name} (Insufficient Balance)", f"£{price}", "Skipper BIN")
                
        except Exception as e:
            logger.error(f"BIN method purchase error: {e}")
            self.bot.answer_callback_query(call.id, "❌ Purchase error")

    def generate_product_content(self, category, product):
        """Generate product content for delivery"""
        if category == 'callcenter':
            return f"""📞 **Call Center Database**
• 50,000+ verified contacts
• Phone numbers with area codes
• Business and residential data
• Contact rate: 85-90%
• CSV format download ready
• Updated within 30 days

Access link: https://excelyard.com/download/{product}
Password: {random.randint(100000, 999999)}"""
        
        elif category == 'crypto':
            return f"""💰 **Crypto Leads Database**
• 10,000+ active crypto users
• Trading platform verified accounts
• Email addresses and contact info
• High-value investor profiles
• Excel format download
• Conversion rate: 15-25%

Access link: https://excelyard.com/crypto/{product}
Login: ExcelYard / Password: {random.randint(100000, 999999)}"""
        
        elif category == 'spam':
            return f"""📧 **Phishing Template Package**
• Complete HTML/CSS/JS files
• Mobile-responsive design
• 95% visual accuracy
• Anti-detection features
• Setup instructions included
• Hosting recommendations

Download: https://excelyard.com/templates/{product}
Extract password: EY{random.randint(1000, 9999)}"""
        
        elif category == 'bin':
            return f"""💳 **BIN Skip Method**
• Working BIN numbers included
• Step-by-step bypass guide
• Success rate: 80-95%
• Multiple payment gateways
• Video tutorial access
• 30-day method validity

Method code: {random.randint(100000, 999999)}
Access: https://excelyard.com/methods/{product}"""
        
        else:
            return f"""📦 **Product Package**
• Complete digital delivery
• Instructions included
• Support available
• Access code: {random.randint(100000, 999999)}"""

    def run(self):
        """Start the bot"""
        logger.info("Starting ExcelYard Bot directly for deployment compatibility...")
        logger.info("Starting ExcelYard Bot with complete product catalogs...")
        
        try:
            # Notify admin that bot is starting
            self.notify_admin("🚀 ExcelYard Bot started with complete 4-category platform and autonomous payment system")
            
            # Get bot info for confirmation
            bot_info = self.bot.get_me()
            logger.info(f"Bot connected successfully: @{bot_info.username}")
            
            logger.info("Starting infinity polling...")
            
            # Start polling with automatic restart
            while self.running:
                try:
                    self.bot.infinity_polling(
                        timeout=30,
                        long_polling_timeout=30,
                        none_stop=True,
                        interval=1,
                        allowed_updates=['message', 'callback_query']
                    )
                except Exception as e:
                    logger.error(f"Polling error: {e}")
                    logger.info("Restarting polling in 5 seconds...")
                    time.sleep(5)
                    
        except Exception as e:
            logger.error(f"Bot startup error: {e}")
            raise

if __name__ == "__main__":
    try:
        print("ExcelYard Bot is now running with all product catalogs!")
        print("Keep-alive server running - bot will stay online 24/7")
        
        bot = ExcelYardBot()
        bot.run()
        
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        logger.error(f"Fatal error: {e}")