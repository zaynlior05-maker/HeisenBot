
import telebot
from telebot import types
import openpyxl
from constants import API_KEY_001, adminpass
from telebot import types
from bitcoin import *
import pandas
from forex_python.bitcoin import BtcConverter
import requests
import telegram
import numpy as np
import time
import pandas as pd
import math
from replit import db
import os
import shutil
import re
from block_io import BlockIo
import random
import datetime
from flask import Flask, request

# Initialize Flask app for webhook
app = Flask(__name__)

version = 2
block_io = BlockIo('83f2-1837-d7b3-096c', 'dEmG9a2eGmr5Tm2t', version)

b = BtcConverter()
bot = telebot.TeleBot(API_KEY_001, parse_mode=None)

# Store Rules and Terms
STORE_RULES = """🏪 HEISENBERG STORE - TERMS & CONDITIONS 🏪

⚠️ IMPORTANT: READ CAREFULLY BEFORE PURCHASING ⚠️

🔸 REFUND POLICY:
• All sales are final once product is delivered
• Refunds only for genuinely dead/invalid products
• Must provide proof within 3 minutes of purchase
• Screenshot must show card details clearly visible

🔸 TESTING REQUIREMENTS:
• Check cards immediately on pay.google.com
• 3-minute window to report issues
• Valid proof required for refund claims

🔸 NON-REFUNDABLE ITEMS:
• £5 and £10 base purchases
• HSBC cards and affiliated banks
• John Lewis, M&S, First Direct cards

🔸 PAYMENT TERMS:
• Bitcoin payments only
• One transaction per wallet address
• New wallet generated for each deposit
• Payments are non-reversible

🔸 SUPPORT & CONTACT:
• 24/7 Support: @HeisenbergActives
• Response time: Usually within 1 hour
• Professional service guaranteed

⚠️ BY PURCHASING YOU ACCEPT THESE TERMS ⚠️
No exceptions • No warnings given • Terms are final"""

btns = ['🛒 Store', '💷 Wallet', '☎️ Support', '🛡️ Rules', '📑 Updates Channel']

btn_prev = types.InlineKeyboardButton('◀️ Previous Menu', callback_data='store')

custom_keyboard = [['🛒 Store', '💷 Wallet'],
                   ['☎️ Support', '🛡️ Rules', '📁 Updates Channel']]

# Main menu persistent button with full menu options
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
main_menu_keyboard.add('🛒 Store', '💷 Wallet')
main_menu_keyboard.add('☎️ Support', '🛡️ Rules')
main_menu_keyboard.add('🌎 Main Menu')

reply_markup = telebot.types.ReplyKeyboardMarkup(True, False)
reply_markup.row(*custom_keyboard[0])
reply_markup.row(*custom_keyboard[1])

inline_keyboard1 = types.InlineKeyboardMarkup()
inline_keyboard3 = types.InlineKeyboardMarkup()

btn_store = types.InlineKeyboardButton('🛒 Store', callback_data='store')
btn_wallet = types.InlineKeyboardButton('💷 Wallet', callback_data='wallet')
btn_support = types.InlineKeyboardButton('☎️ Support', callback_data='support')
btn_rules = types.InlineKeyboardButton('🛡️ Rules', callback_data='rules')
btn_updates = types.InlineKeyboardButton('📁 Updates Channel', callback_data='updates')

btn_search = types.InlineKeyboardButton('🔎 Search for BIN', callback_data='search')
btn_searchagn = types.InlineKeyboardButton('🔎 Search Again', callback_data='search')
btn_cancel = types.InlineKeyboardButton('❌', callback_data='cancel')
btn_menu = types.InlineKeyboardButton('🌎 Main Menu', callback_data='menu')

btn_20 = types.InlineKeyboardButton('🔸£20🔸', callback_data='btc20')
btn_30 = types.InlineKeyboardButton('🔸£30🔸', callback_data='btc30')
btn_50 = types.InlineKeyboardButton('🔸£50🔸', callback_data='btc50')
btn_70 = types.InlineKeyboardButton('🔸£70🔸', callback_data='btc70')
btn_100 = types.InlineKeyboardButton('🔸£100🔸', callback_data='btc100')
btn_150 = types.InlineKeyboardButton('🔸£150🔸', callback_data='btc150')
btn_200 = types.InlineKeyboardButton('🔸£200🔸', callback_data='btc200')
btn_250 = types.InlineKeyboardButton('🔸£250🔸', callback_data='btc250')
btn_300 = types.InlineKeyboardButton('🔸£300🔸', callback_data='btc300')
btn_400 = types.InlineKeyboardButton('🔸£400🔸', callback_data='btc400')
btn_500 = types.InlineKeyboardButton('🔸£500🔸', callback_data='btc500')
btn_1000 = types.InlineKeyboardButton('🔸£1000🔸', callback_data='btc1000')

# Updated base buttons with new naming
btn_base2 = types.InlineKeyboardButton('🔸Heisen_Uk_Fresh_Base', callback_data='base2')
btn_base3 = types.InlineKeyboardButton('🔸Heisen_Aus_Fresh_Base', callback_data='base3')
btn_base4 = types.InlineKeyboardButton('🔸Heisen_Rare_Base', callback_data='base4')
btn_base5 = types.InlineKeyboardButton('🔸Heisen_10_Base', callback_data='base5')
btn_base6 = types.InlineKeyboardButton('🔸Heisen_Unspoofed_Base', callback_data='base6')
btn_base11 = types.InlineKeyboardButton('🔸Skippers&Meth', callback_data='base11')

inline_keyboard1.add(btn_store)
inline_keyboard1.add(btn_wallet, btn_support)
inline_keyboard1.add(btn_rules, btn_updates)

inline_keyboard3.add(btn_base2)  # Heisen_Uk_Fresh_Base
inline_keyboard3.add(btn_base3)  # Heisen_Aus_Fresh_Base  
inline_keyboard3.add(btn_base4)  # Heisen_Rare_Base
inline_keyboard3.add(btn_base5)  # Heisen_10_Base
inline_keyboard3.add(btn_base6)  # Heisen_Unspoofed_Base
inline_keyboard3.add(btn_base11) # Skippers&Meth
inline_keyboard3.add(btn_search)
inline_keyboard3.add(btn_menu)

base_dir = os.getcwd()

merged_file_path = os.path.join(base_dir, "binlist.txt")
with open(merged_file_path, "w") as merged_file:
    for base_folder in os.listdir(base_dir):
        if base_folder.startswith("base"):
            base_path = os.path.join(base_dir, base_folder)
            for fullz_file in os.listdir(base_path):
                if fullz_file.startswith("fullz"):
                    fullz_path = os.path.join(base_path, fullz_file)
                    with open(fullz_path, "r") as fullz:
                        merged_file.write(fullz.read() + "\n")

@bot.message_handler(commands=['send'])
def send_msg(message):
    id = str(extract_arg2(message.text)[0])
    msg = str(extract_arg2(message.text)[1])
    password = str(extract_arg2(message.text)[2])
    
    if adminpass == password:
        try:
            bot.send_message(id, text=msg, parse_mode="Markdown")
        except:
            print("error")

def notify_admin_activity(user_id, username, action, details=""):
    """Send notification to admin for every user action"""
    try:
        user_name = username if username else "Unknown"
        notification_msg = f"🔔 USER ACTIVITY ALERT\n\n"
        notification_msg += f"👤 User: @{user_name} (ID: {user_id})\n"
        notification_msg += f"🎯 Action: {action}\n"
        if details:
            notification_msg += f"📝 Details: {details}\n"
        notification_msg += f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}"
        
        try:
            bot.send_message(1182433696, notification_msg)
        except Exception as admin_error:
            print(f"Admin notification failed: {admin_error}")
            try:
                bot.send_message(-1002563927894, notification_msg)
            except Exception as group_error:
                print(f"Group notification also failed: {group_error}")
    except Exception as e:
        print(f"Admin notification error: {e}")

@bot.message_handler(commands=['sendall'])
def send_announcement(message):
    msg = str(extract_arg2(message.text)[0])
    password = str(extract_arg2(message.text)[1])
    
    if adminpass == password:
        keys = db.keys()
        for i in keys:
            time.sleep(0.5)
            if str(i)[0:3] == "bal":
                try:
                    bot.send_message(str(i)[3:], text=msg, parse_mode="Markdown")
                except Exception as e:
                    print(e)

@bot.message_handler(commands=['userbal'])
def userbal(message):
    id = int(extract_arg1(message.text)[0])
    credit = int(extract_arg1(message.text)[1])
    password = str(extract_arg1(message.text)[2])
    if adminpass == password:
        bot.send_message(int(id), text="✅£" + str(credit - int(db["bal" + str(id)])) + " has been added to your wallet.✅", parse_mode="Markdown")
        bot.send_message(message.chat.id, text="£" + str(credit) + " has been set to: " + str(id), parse_mode="Markdown")
    db["bal" + str(id)] = credit

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    notify_admin_activity(message.chat.id, message.chat.username, "🚀 Started Bot", "User initiated /start command")
    
    try:
        value = db["bal" + str(message.chat.id)]
    except:
        db["bal" + str(message.chat.id)] = 0
    
    bot.send_message(message.chat.id, text=STORE_RULES, parse_mode="Markdown")
    msg = bot.send_message(
        message.chat.id,
        "Welcome to Heisenberg Store\n\nMade/Coded by @HeisenbergActives\n\nManaged by @HeisenbergActives\n\nUsername : <code>" + str(message.chat.username) + "</code>\nID: <code>" + str(message.chat.id) + "</code>",
        reply_markup=inline_keyboard1,
        parse_mode="HTML"
    )
    # Send the persistent keyboard separately
    bot.send_message(message.chat.id, "Use the menu below:", reply_markup=main_menu_keyboard)

@bot.message_handler(func=lambda message: message.text in ["🌎 Main Menu", "🛒 Store", "💷 Wallet", "☎️ Support", "🛡️ Rules"])
def handle_keyboard_buttons(message):
    if message.text == "🌎 Main Menu":
        notify_admin_activity(message.chat.id, message.chat.username, "🏠 Main Menu", "Used shortcut button")
        send_welcome(message)
    elif message.text == "🛒 Store":
        notify_admin_activity(message.chat.id, message.chat.username, "🛒 Store", "Used shortcut button")
        # Send new message for store menu
        bot.send_message(
            message.chat.id, 
            "Choose the base you would like to browse:",
            reply_markup=inline_keyboard3,
            parse_mode="HTML"
        )
    elif message.text == "💷 Wallet":
        notify_admin_activity(message.chat.id, message.chat.username, "💷 Wallet", "Used shortcut button")
        # Send wallet menu
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_20, btn_30)
        inline_keyboard2.add(btn_50, btn_70)
        inline_keyboard2.add(btn_100, btn_150)
        inline_keyboard2.add(btn_200)
        inline_keyboard2.add(btn_menu)
        
        try:
            balance = db["bal" + str(message.chat.id)]
        except:
            balance = 0
            
        bot.send_message(
            message.chat.id,
            f"💰 Your current balance: £{balance}\n\nSelect amount to add to wallet:",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
    elif message.text == "☎️ Support":
        notify_admin_activity(message.chat.id, message.chat.username, "☎️ Support", "Used shortcut button")
        # Send support menu
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_menu)
        bot.send_message(
            message.chat.id,
            "☎️ **Support & Contact**\n\n📱 Admin: @HeisenbergActives\n🕐 Available: 24/7\n⚡ Response: Usually within 1 hour\n\n💬 Send us a message for help!",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
    elif message.text == "🛡️ Rules":
        notify_admin_activity(message.chat.id, message.chat.username, "🛡️ Rules", "Used shortcut button")
        # Send rules
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_menu)
        bot.send_message(
            message.chat.id,
            STORE_RULES,
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )

def open_binlist(message):
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Choose the base you would like to browse:",
        reply_markup=inline_keyboard3,
        parse_mode="HTML"
    )
    notify_admin_activity(message.chat.id, message.chat.username, "🛒 Browsing Store", "User is browsing through fullz catalog")

def open_base(message, base):
    notify_admin_activity(message.chat.id, message.chat.username, "📂 Viewing Base", f"Opened base{base} products")
    
    inline_keyboard2 = types.InlineKeyboardMarkup()
    
    with open("base" + str(base) + "/fullz" + str(base) + ".txt") as file:
        for line in file:
            btn = types.InlineKeyboardButton(line.rstrip(), callback_data='fullz')
            inline_keyboard2.add(btn)
    
    inline_keyboard2.add(btn_prev)
    inline_keyboard2.add(btn_menu)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Buy the bin by clicking on it",
        reply_markup=inline_keyboard2,
        parse_mode="HTML"
    )

def open_wallet(message):
    try:
        value = db["bal" + str(message.chat.id)]
    except:
        db["bal" + str(message.chat.id)] = 0
    
    inline_keyboard2 = types.InlineKeyboardMarkup()
    inline_keyboard2.add(btn_70)
    inline_keyboard2.add(btn_100, btn_150)
    inline_keyboard2.add(btn_200, btn_250)
    inline_keyboard2.add(btn_300, btn_400)
    inline_keyboard2.add(btn_500, btn_1000)
    inline_keyboard2.add(btn_menu)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text='🆔ID: <code>' + str(message.chat.id) + '</code>\n🏦Balance: £' + str(db["bal" + str(message.chat.id)]) + "\n🔸Choose amount:",
        reply_markup=inline_keyboard2,
        parse_mode="HTML"
    )

def open_topup(message, amount):
    inline_keyboard2 = types.InlineKeyboardMarkup()
    inline_keyboard2.add(btn_menu)
    
    btc_rates = {
        '20': '0.00025', '30': '0.00038', '50': '0.00063', '70': '0.00088',
        '100': '0.00126', '150': '0.00189', '200': '0.00252', '250': '0.00315',
        '300': '0.00378', '400': '0.00504', '500': '0.00630', '1000': '0.01260'
    }
    
    btc_amount = btc_rates.get(amount, '0.00100')
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Send <b>exactly</b> <code>" + btc_amount + "</code>" + " BTC to the following address: \n<code>bc1q64f2jfjpv2f7n4a2jryj08wklc0yrvsjles5wt</code>\n\n⚠️┇Deposits are non refundable\n⚠️┇Double check BTC amount\n⚠️┇Send as BTC not as £\n\nFunds will appear in your account after 3 confirmations.",
        reply_markup=inline_keyboard2,
        parse_mode="HTML"
    )

def open_support(message):
    inline_keyboard2 = types.InlineKeyboardMarkup()
    inline_keyboard2.add(btn_menu)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text='Support Account  : @HeisenbergActives',
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def open_update(message):
    inline_keyboard2 = types.InlineKeyboardMarkup()
    inline_keyboard2.add(btn_menu)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text='Invite Link  : https://t.me/HeisenbergStoreUk',
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def open_menu(message):
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Welcome to Heisenberg Store\n\nMade/Coded by @HeisenbergActives\n\nManaged by @HeisenbergActives\n\nUsername : <code>" + str(message.chat.username) + "</code>\nID: <code>" + str(message.chat.id) + "</code>",
        reply_markup=inline_keyboard1,
        parse_mode="HTML"
    )

def open_rules(message):
    inline_keyboard2 = types.InlineKeyboardMarkup()
    inline_keyboard2.add(btn_menu)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=STORE_RULES,
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def open_search(message):
    sent_msg = bot.send_message(message.chat.id, "<code>-- 🔎 Bin Search --</code>\nType the 6 digit bin you want to look for", parse_mode="HTML")
    bot.register_next_step_handler(sent_msg, bin_handler)

def bin_handler(message):
    notify_admin_activity(message.chat.id, message.chat.username, "🔍 BIN Search", f"Searching for: {message.text}")
    
    inline_keyboard2 = types.InlineKeyboardMarkup()
    inline_keyboard2.add(btn_cancel)
    bin = message.text
    
    if bin == "/start" or bin in btns:
        send_welcome(message)
        return
    
    try:
        bin = int(bin)
        
        if len(str(bin)) == 6:
            with open("binlist.txt", 'r') as file:
                lines = file.readlines()
                exists = False
                for line in lines:
                    if str(bin) in line:
                        exists = True
                        inline_keyboard2 = types.InlineKeyboardMarkup()
                        btn_bin = types.InlineKeyboardButton(line, callback_data='buy')
                        inline_keyboard2.add(btn_bin)
                        inline_keyboard2.add(btn_searchagn)
                        break
                
                if exists:
                    bot.send_message(message.chat.id, "Bin available!", reply_markup=inline_keyboard2)
                    return
                else:
                    bot.send_message(message.chat.id, "Couldn't Fetch the Bin please try again later")
                    return
        else:
            sent_msg = bot.send_message(message.chat.id, "Bin number is 6 Digits or press cancel to close this session", reply_markup=inline_keyboard2)
            bot.register_next_step_handler(sent_msg, bin_handler)
    except Exception as e:
        print(e)
        sent_msg = bot.send_message(message.chat.id, "Only use numbers please or press cancel to close this session", reply_markup=inline_keyboard2)
        bot.register_next_step_handler(sent_msg, bin_handler)

def cancel(message):
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="❌ OPERATION CANCELED",
        parse_mode="Markdown"
    )
    send_welcome(message)
    return

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id)
    
    action_map = {
        "store": "🛒 Opened Store Menu",
        "search": "🔍 Opened Search Menu",
        "wallet": "💰 Opened Wallet Menu",
        "support": "☎️ Opened Support Menu",
        "rules": "📋 Opened Rules Menu",
        "updates": "📢 Opened Updates Channel",
        "menu": "🏠 Returned to Main Menu",
        "cancel": "❌ Cancelled Action",
        "base2": "📁 Opened Heisen_Uk_Fresh_Base",
        "base3": "📁 Opened Heisen_Aus_Fresh_Base",
        "base4": "📁 Opened Heisen_Rare_Base",
        "base5": "📁 Opened Heisen_10_Base",
        "base6": "📁 Opened Heisen_Unspoofed_Base",
        "base11": "📁 Opened Skippers&Meth"
    }
    
    if call.data.startswith("btc"):
        amount = call.data[3:]
        action_text = f"💳 Selected Wallet Top-up: £{amount}"
    else:
        action_text = action_map.get(call.data, f"🎯 Button Clicked: {call.data}")
    
    notify_admin_activity(call.message.chat.id, call.message.chat.username, action_text)
    
    if call.message.chat.username == "kanseph" or call.message.chat.username == "mazz44":
        text_file = open("error.txt", "r")
        error = text_file.read()
        text_file.close()
        while True:
            print("WARNING")
            bot.send_message(call.message.chat.id, text=error, parse_mode="HTML")
    
    if call.data == "store":
        open_binlist(call.message)
    elif call.data == "search":
        open_search(call.message)
    elif call.data == "cancel":
        cancel(call.message)
    elif call.data == "wallet":
        open_wallet(call.message)
    elif call.data == "rules":
        open_rules(call.message)
    elif call.data == "support":
        open_support(call.message)
    elif call.data == "updates":
        open_update(call.message)
    elif call.data == "menu":
        open_menu(call.message)
    elif str(call.data)[0:3] == "btc":
        open_topup(call.message, call.data[3:])
    elif str(call.data)[0:4] == "base":
        open_base(call.message, call.data[4:])
    elif call.data == "fullz":
        amount = int(db["bal" + str(call.message.chat.id)])
        if amount == 285:
            bot.send_message(call.message.chat.id, text="❌£300 NEEDED IN WALLLET TO ACTIVATE THE ACCOUNT, CONTACT SUPPORT FOR HELP❌", parse_mode="Markdown")
        elif amount > 0:
            bot.send_message(call.message.chat.id, text="❌£" + str(2 * amount) + " NEEDED IN WALLLET TO ACTIVATE THE ACCOUNT, CONTACT SUPPORT FOR HELP❌", parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, text="❌NOT ENOUGH CREDITS. PLEASE TOP UP❌", parse_mode="Markdown")

def extract_arg1(arg):
    try:
        return arg.split()[1:]
    except:
        return []

def extract_arg2(arg):
    try:
        args = arg.split()[1:]
        result = []
        i = 0
        while i < len(args):
            if args[i].startswith('"') or args[i].startswith("'"):
                result.append(args[i][1:])
                while i + 1 < len(args) and not args[i].endswith('"') and not args[i].endswith("'"):
                    i += 1
                    result[-1] += " " + args[i]
                if args[i].endswith('"') or args[i].endswith("'"):
                    result[-1] = result[-1][:-1]
            else:
                result.append(args[i])
            i += 1
        return result
    except:
        return []

# Webhook route for Telegram (using secure path)
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return "OK"
        else:
            return "Bad Request", 400
    except Exception as e:
        print(f"Webhook error: {e}")
        return "Error", 500

# Health check route
@app.route('/')
def health_check():
    return "Heisenberg Store Bot is running!"

# Test route to check bot status
@app.route('/status')
def bot_status():
    try:
        bot_info = bot.get_me()
        webhook_info = bot.get_webhook_info()
        return f"""
        <h1>Bot Status</h1>
        <p><strong>Bot Name:</strong> {bot_info.first_name}</p>
        <p><strong>Bot Username:</strong> @{bot_info.username}</p>
        <p><strong>Webhook URL:</strong> {webhook_info.url}</p>
        <p><strong>Pending Updates:</strong> {webhook_info.pending_update_count}</p>
        <p><strong>Last Error:</strong> {webhook_info.last_error_message or 'None'}</p>
        """
    except Exception as e:
        return f"Error getting bot status: {e}"

# Set webhook for deployment
def set_webhook():
    repl_slug = os.environ.get('REPL_SLUG')
    repl_owner = os.environ.get('REPL_OWNER')
    
    if repl_slug and repl_owner:
        webhook_url = f"https://{repl_slug}-{repl_owner}.replit.app/webhook"
        try:
            # Remove existing webhook first
            bot.remove_webhook()
            time.sleep(3)  # Give more time
            
            # Set new webhook
            result = bot.set_webhook(url=webhook_url)
            if result:
                print(f"✓ Webhook set successfully: {webhook_url}")
                
                # Test webhook info
                webhook_info = bot.get_webhook_info()
                print(f"✓ Webhook info: {webhook_info.url}")
                return True
            else:
                print(f"❌ Webhook setup failed")
                return False
        except Exception as e:
            print(f"❌ Webhook setup error: {e}")
            return False
    else:
        print("⚠ No deployment environment variables found")
        return False

if __name__ == '__main__':
    # Set up bot commands menu for easy access
    commands = [
        telebot.types.BotCommand("start", "🏪 Open Heisenberg Store"),
        telebot.types.BotCommand("wallet", "💰 Check wallet balance"),
        telebot.types.BotCommand("balance", "💳 View current balance"),
        telebot.types.BotCommand("help", "ℹ️ Get help and info")
    ]
    
    try:
        bot.set_my_commands(commands)
        print("✓ Bot commands menu set successfully")
    except Exception as e:
        print(f"⚠ Could not set commands menu: {e}")
    
    # Check if we're in deployment environment (has REPL_SLUG)
    repl_slug = os.environ.get('REPL_SLUG')
    repl_owner = os.environ.get('REPL_OWNER')
    
    if repl_slug and repl_owner:
        # Deployment mode - use webhook with Flask
        print("🚀 Starting Heisenberg Store Bot in deployment mode...")
        try:
            # Start Flask first
            port = int(os.environ.get('PORT', 5000))
            print(f"✓ Starting Flask app on 0.0.0.0:{port}")
            
            # Set webhook after a delay
            import threading
            def setup_webhook():
                time.sleep(5)  # Wait for Flask to start
                webhook_success = set_webhook()
                if not webhook_success:
                    print("⚠️ Webhook failed, bot may not respond to messages")
            
            webhook_thread = threading.Thread(target=setup_webhook)
            webhook_thread.start()
            
            # Start Flask app
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            print("🔄 Falling back to polling mode...")
            # Fallback to polling
            try:
                bot.remove_webhook()
                time.sleep(2)
                print("✓ Bot is now active - users can send /start")
                bot.infinity_polling(timeout=10, long_polling_timeout=5)
            except Exception as poll_error:
                print(f"❌ Polling fallback also failed: {poll_error}")
    else:
        # Development mode - use polling
        print("🚀 Starting Heisenberg Store Bot in development mode...")
        try:
            bot.remove_webhook()  # Remove any existing webhook
            print("✓ Webhook removed successfully")
            print("✓ Bot is now active - users can send /start")
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Bot polling failed: {e}")
            print("🔄 Retrying with basic polling...")
            try:
                bot.polling(none_stop=True, interval=1, timeout=10)
            except Exception as retry_error:
                print(f"❌ All polling methods failed: {retry_error}")
