
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
btn_70 = types.InlineKeyboardButton('🔶 £70 🔶', callback_data='btc70')
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

btn_tools = types.InlineKeyboardButton('🧰 Tools', callback_data='tools')

inline_keyboard1.add(btn_store)
inline_keyboard1.add(btn_tools)
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
        inline_keyboard2.add(btn_70)  # Featured amount
        inline_keyboard2.add(btn_100, btn_150)
        inline_keyboard2.add(btn_200, btn_250)
        inline_keyboard2.add(btn_300, btn_400)
        inline_keyboard2.add(btn_500, btn_1000)
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
    
    # Special handling for base11 (Skippers&Meth) with comprehensive BIN + Method menu
    if base == "11":
        inline_keyboard2 = types.InlineKeyboardMarkup()
        
        # Create product buttons with buy option
        products = [
            ("Domino's BIN + Method – £145 (Skips £250 ×3)", "skipper_1_145"),
            ("Just Eat BIN + Method – £145 (Skips £200 ×4)", "skipper_2_145"),
            ("Odeon BIN + Method – £250 (Skips £750 ×2)", "skipper_3_250"),
            ("Nike BIN + Method – £300 (Skips £950 ×2)", "skipper_4_300"),
            ("Foodhub BIN + Method – £145 (Skips £290 ×2)", "skipper_5_145"),
            ("Pets at Home BIN + Method – £250 (Skips £350 ×2)", "skipper_6_250"),
            ("Ola Cab App BIN + Method – £350 (Skips £850 ×2)", "skipper_7_350"),
            ("Studio BIN + Method – £280 (Skips £350 ×5)", "skipper_8_280"),
            ("Offspring BIN + Method – £300 (Skips £450 ×4)", "skipper_9_300"),
            ("JD BIN + Method – £300 (Skips £550 ×3)", "skipper_10_300"),
            ("Vans BIN + Method – £300 (Skips £950 ×2)", "skipper_11_300"),
            ("Selfridges e-Gift BIN + Method – £250 (Skips £550 ×4)", "skipper_12_250"),
            ("CDKeys BIN + Method – £350 (Skips £650 ×4)", "skipper_13_350"),
            ("Co-op Grocery BIN + Method – £200 (Skips £750 ×2)", "skipper_14_200"),
            ("Vue BIN + Method – £145", "skipper_15_145"),
            ("PLT BIN + Method – £150", "skipper_16_150"),
            ("Bolt BIN + Method – £300 (Skips £200–£300 ×6)", "skipper_17_300"),
            ("Premier Inn BIN + Method – £300 (Skips £650–£700 ×3)", "skipper_18_300"),
            ("Booking.com BIN + Method – £300 (Skips £650–£700 ×3)", "skipper_19_300"),
            ("Footlocker BIN + Method – £350 (Skips £850 ×3)", "skipper_20_350"),
            ("Adidas BIN + Method – £300 (Skips £500 ×4)", "skipper_21_300"),
            ("Argos BIN + Method – £300 (Skips £550 ×4)", "skipper_22_300")
        ]
        
        for product_name, callback_data in products:
            btn = types.InlineKeyboardButton(f"🔸 {product_name}", callback_data=callback_data)
            inline_keyboard2.add(btn)
        
        inline_keyboard2.add(btn_prev)
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="💳 **Skippers&Meth - BIN + Method Products**\n\n🧾 **Auto Add – No OTP Needed**\n✅ All tested and verified\n\n**Select a product to purchase:**",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
    elif base == "2":
        # Special handling for base2 (Heisen_Uk_Fresh_Base) with £30 pricing and pagination
        open_uk_fresh_page(message, 1)  # Start with page 1
    elif base == "3":
        # Special handling for base3 (Heisen_Aus_Fresh_Base) with £30 pricing and pagination
        open_aus_fresh_page(message, 1)  # Start with page 1
    elif base == "5":
        # Special handling for base5 (Heisen_10_Base) with £10 pricing and pagination
        open_10gbp_fresh_page(message, 1)  # Start with page 1
    elif base == "6":
        # Special handling for base6 (Heisen_Unspoofed_Base) with bulk pricing options
        open_unspoofed_menu(message)
    else:
        # Original handling for other bases
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
    inline_keyboard2.add(btn_70)  # Featured amount
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

def handle_skipper_purchase(call):
    """Handle purchase of skipper BIN + Method products"""
    # Extract product info from callback data (skipper_X_price)
    parts = call.data.split("_")
    product_id = parts[1]
    price = int(parts[2])
    
    # Product mapping for names and details
    product_map = {
        "1": ("Domino's BIN + Method", "Skips £250 ×3"),
        "2": ("Just Eat BIN + Method", "Skips £200 ×4"),
        "3": ("Odeon BIN + Method", "Skips £750 ×2 till bala"),
        "4": ("Nike BIN + Method", "Skips £950 ×2 till bala"),
        "5": ("Foodhub BIN + Method", "Skips £290 ×2"),
        "6": ("Pets at Home BIN + Method", "Skips £350 ×2"),
        "7": ("Ola Cab App BIN + Method", "Skips £850 ×2"),
        "8": ("Studio BIN + Method", "Skips £350 ×5"),
        "9": ("Offspring BIN + Method", "Skips £450 ×4"),
        "10": ("JD BIN + Method", "Skips £550 ×3"),
        "11": ("Vans BIN + Method", "Skips £950 ×2"),
        "12": ("Selfridges e-Gift BIN + Method", "Skips £550 ×4"),
        "13": ("CDKeys BIN + Method", "Skips £650 ×4"),
        "14": ("Co-op Grocery BIN + Method", "Skips £750 ×2"),
        "15": ("Vue BIN + Method", "Standard product"),
        "16": ("PLT BIN + Method", "Standard product"),
        "17": ("Bolt BIN + Method", "Skips £200–£300 ×6"),
        "18": ("Premier Inn BIN + Method", "Skips £650–£700 ×3"),
        "19": ("Booking.com BIN + Method", "Skips £650–£700 ×3"),
        "20": ("Footlocker BIN + Method", "Skips £850 ×3"),
        "21": ("Adidas BIN + Method", "Skips £500 ×4"),
        "22": ("Argos BIN + Method", "Skips £550 ×4")
    }
    
    product_name, skip_info = product_map.get(product_id, ("Unknown Product", ""))
    user_id = call.message.chat.id
    username = call.message.chat.username or "No username"
    
    # Check user balance
    try:
        current_balance = db["bal" + str(user_id)]
    except:
        current_balance = 0
    
    # Process purchase
    if current_balance >= price:
        # Deduct amount from balance
        db["bal" + str(user_id)] = current_balance - price
        new_balance = current_balance - price
        
        # Notify user of successful purchase
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✅ **Purchase Successful!**\n\n🔸 **Product:** {product_name}\n💰 **Price:** £{price}\n📊 **Info:** {skip_info}\n💳 **New Balance:** £{new_balance}\n\n⏳ **Delivery:** Manual delivery in progress\n📞 **Admin notified** for immediate processing",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
        
        # Notify admin for manual delivery
        admin_message = f"🔔 **NEW SKIPPER PURCHASE**\n\n👤 **User:** @{username} (ID: {user_id})\n🔸 **Product:** {product_name}\n💰 **Price:** £{price}\n📊 **Skip Info:** {skip_info}\n\n⚠️ **ACTION REQUIRED:** Manual delivery needed"
        
        try:
            bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
            bot.send_message(GROUP_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to notify admin: {e}")
        
        # Log the purchase
        notify_admin_activity(user_id, username, "💳 Skipper Purchase", f"{product_name} - £{price}")
        
    else:
        # Insufficient balance
        needed = price - current_balance
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_wallet)
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"❌ **Insufficient Balance**\n\n🔸 **Product:** {product_name}\n💰 **Price:** £{price}\n💳 **Your Balance:** £{current_balance}\n💸 **Need:** £{needed} more\n\n**Please top up your wallet to continue.**",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )

def open_uk_fresh_page(message, page=1):
    """Display UK fresh base with pagination (25 items per page)"""
    inline_keyboard2 = types.InlineKeyboardMarkup()
    
    # Load real UK fresh base data
    all_uk_data = []
    try:
        with open("base2/fullz2.txt") as file:
            all_uk_data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        all_uk_data = ["No data available"]
    
    # Pagination logic
    items_per_page = 25
    total_items = len(all_uk_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    if page > total_pages:
        page = total_pages
    if page < 1:
        page = 1
    
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    page_items = all_uk_data[start_idx:end_idx]
    
    # Add product buttons for current page
    for idx, item in enumerate(page_items):
        item_id = start_idx + idx + 1  # Create unique item ID
        # Shorten button text to avoid callback data limits
        short_text = item[:40] + "..." if len(item) > 40 else item
        btn = types.InlineKeyboardButton(f"{short_text} - £30", callback_data=f'uk_{item_id}')
        inline_keyboard2.add(btn)
    
    # Add pagination buttons
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f'ukfresh_page_{page-1}'))
    if page < total_pages:
        pagination_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f'ukfresh_page_{page+1}'))
    
    if pagination_buttons:
        if len(pagination_buttons) == 2:
            inline_keyboard2.add(pagination_buttons[0], pagination_buttons[1])
        else:
            inline_keyboard2.add(pagination_buttons[0])
    
    # Add navigation buttons
    inline_keyboard2.add(btn_prev)
    inline_keyboard2.add(btn_menu)
    
    # Display message
    page_text = f"💳 **Heisen UK Fresh Base** (Page {page}/{total_pages})\n\n💰 **Price:** £30 per item\n✅ **Fresh UK BINs with PostCodes**\n📊 **Showing:** {len(page_items)} of {total_items} items\n\n**Select an item to purchase:**"
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=page_text,
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def open_aus_fresh_page(message, page=1):
    """Display Australian fresh base with pagination (25 items per page)"""
    inline_keyboard2 = types.InlineKeyboardMarkup()
    
    # Load real Australian fresh base data
    all_aus_data = []
    try:
        with open("base3/fullz3.txt") as file:
            all_aus_data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        all_aus_data = ["No data available"]
    
    # Pagination logic
    items_per_page = 25
    total_items = len(all_aus_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    if page > total_pages:
        page = total_pages
    if page < 1:
        page = 1
    
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    page_items = all_aus_data[start_idx:end_idx]
    
    # Add product buttons for current page
    for idx, item in enumerate(page_items):
        item_id = start_idx + idx + 1  # Create unique item ID
        # Shorten button text to avoid callback data limits
        short_text = item[:40] + "..." if len(item) > 40 else item
        btn = types.InlineKeyboardButton(f"{short_text} - £30", callback_data=f'aus_{item_id}')
        inline_keyboard2.add(btn)
    
    # Add pagination buttons
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f'ausfresh_page_{page-1}'))
    if page < total_pages:
        pagination_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f'ausfresh_page_{page+1}'))
    
    if pagination_buttons:
        if len(pagination_buttons) == 2:
            inline_keyboard2.add(pagination_buttons[0], pagination_buttons[1])
        else:
            inline_keyboard2.add(pagination_buttons[0])
    
    # Add navigation buttons
    inline_keyboard2.add(btn_prev)
    inline_keyboard2.add(btn_menu)
    
    # Display message
    page_text = f"🇦🇺 **Heisen Aus Fresh Base** (Page {page}/{total_pages})\n\n💰 **Price:** £30 per item\n✅ **Fresh Australian BINs with Postcodes**\n📊 **Showing:** {len(page_items)} of {total_items} items\n\n**Select an item to purchase:**"
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=page_text,
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def open_10gbp_fresh_page(message, page=1):
    """Display £10 fresh base with pagination (25 items per page)"""
    inline_keyboard2 = types.InlineKeyboardMarkup()
    
    # Load real £10 base data
    all_10gbp_data = []
    try:
        with open("base5/fullz5.txt") as file:
            all_10gbp_data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        all_10gbp_data = ["No data available"]
    
    # Pagination logic
    items_per_page = 25
    total_items = len(all_10gbp_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    if page > total_pages:
        page = total_pages
    if page < 1:
        page = 1
    
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    page_items = all_10gbp_data[start_idx:end_idx]
    
    # Add product buttons for current page
    for idx, item in enumerate(page_items):
        item_id = start_idx + idx + 1  # Create unique item ID
        # Shorten button text to avoid callback data limits
        short_text = item[:40] + "..." if len(item) > 40 else item
        btn = types.InlineKeyboardButton(f"{short_text} - £10", callback_data=f'gbp10_{item_id}')
        inline_keyboard2.add(btn)
    
    # Add pagination buttons
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f'gbp10_page_{page-1}'))
    if page < total_pages:
        pagination_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f'gbp10_page_{page+1}'))
    
    if pagination_buttons:
        if len(pagination_buttons) == 2:
            inline_keyboard2.add(pagination_buttons[0], pagination_buttons[1])
        else:
            inline_keyboard2.add(pagination_buttons[0])
    
    # Add navigation buttons
    inline_keyboard2.add(btn_prev)
    inline_keyboard2.add(btn_menu)
    
    # Display message
    page_text = f"💰 **Heisen 10 Base** (Page {page}/{total_pages})\n\n💰 **Price:** £10 per item\n✅ **Fresh UK BINs with Postcodes**\n📊 **Showing:** {len(page_items)} of {total_items} items\n\n**Select an item to purchase:**"
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=page_text,
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def open_unspoofed_menu(message):
    """Display Heisen Unspoofed Base menu with bulk pricing options"""
    inline_keyboard2 = types.InlineKeyboardMarkup()
    
    # Create menu buttons for different unspoofed options
    btn1 = types.InlineKeyboardButton("💳 Specific Unspoofed 50+ - £225", callback_data='unspoofed_specific_50')
    btn2 = types.InlineKeyboardButton("💳 Specific Unspoofed 100+ - £350", callback_data='unspoofed_specific_100') 
    btn3 = types.InlineKeyboardButton("🃏 Random Unspoofed 50+ - £100", callback_data='unspoofed_random_50')
    btn4 = types.InlineKeyboardButton("🃏 Random Unspoofed 100+ - £150", callback_data='unspoofed_random_100')
    
    inline_keyboard2.add(btn1)
    inline_keyboard2.add(btn2)
    inline_keyboard2.add(btn3)
    inline_keyboard2.add(btn4)
    
    # Add navigation buttons
    inline_keyboard2.add(btn_prev)
    inline_keyboard2.add(btn_menu)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="🔓 **Heisen Unspoofed Base**\n\n💳 **Specific Unspoofed Files:**\n• 50+ cards: £4 per card = £225 total\n• 100+ cards: £3.50 per card = £350 total\n\n🃏 **Random Unspoofed Files:**\n• 50+ cards: £2 per card = £100 total\n• 100+ cards: £1.50 per card = £150 total\n\n⏰ **Freshness:** Spam from 3 days - 2 weeks\n\n**Select your preferred package:**",
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def open_tools_menu(message):
    """Display Tools menu with all available services"""
    inline_keyboard2 = types.InlineKeyboardMarkup()
    
    # Create menu buttons for all tools
    btn1 = types.InlineKeyboardButton("📌 Call Centre With DID Number", callback_data='tool_callcentre')
    btn2 = types.InlineKeyboardButton("📌 Crypto Leads", callback_data='tool_cryptoleads')
    btn3 = types.InlineKeyboardButton("📌 Valid Mail Checkers", callback_data='tool_mailcheckers')
    btn4 = types.InlineKeyboardButton("📌 Mailer", callback_data='tool_mailer')
    btn5 = types.InlineKeyboardButton("📌 Autodoxers", callback_data='tool_autodoxers')
    btn6 = types.InlineKeyboardButton("📌 Live Panels", callback_data='tool_livepanels')
    btn7 = types.InlineKeyboardButton("📌 Bulk SMS Routes", callback_data='tool_bulksms')
    btn8 = types.InlineKeyboardButton("📌 Email Spamming", callback_data='tool_emailspam')
    btn9 = types.InlineKeyboardButton("📌 P1", callback_data='tool_p1')
    
    inline_keyboard2.add(btn1)
    inline_keyboard2.add(btn2)
    inline_keyboard2.add(btn3)
    inline_keyboard2.add(btn4)
    inline_keyboard2.add(btn5)
    inline_keyboard2.add(btn6)
    inline_keyboard2.add(btn7)
    inline_keyboard2.add(btn8)
    inline_keyboard2.add(btn9)
    
    # Add navigation buttons
    inline_keyboard2.add(btn_menu)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="🧰 **Tools Menu**\n\n🟢 **Active On All Tools:**\n\n📌 Call Centre With DID Number\n📌 Crypto Leads\n📌 Valid Mail Checkers\n📌 Mailer\n📌 Autodoxers\n📌 Live Panels\n📌 Bulk SMS Routes\n📌 Email Spamming\n📌 P1\n\n**Message @admin for price** 🧰\n\n*Select a tool to contact admin for pricing:*",
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )

def handle_tools_contact(call):
    """Handle tool selection and redirect to admin contact"""
    user_id = call.message.chat.id
    username = call.message.chat.username or "No username"
    
    # Define tool names
    tools = {
        'tool_callcentre': 'Call Centre With DID Number',
        'tool_cryptoleads': 'Crypto Leads',
        'tool_mailcheckers': 'Valid Mail Checkers',
        'tool_mailer': 'Mailer',
        'tool_autodoxers': 'Autodoxers',
        'tool_livepanels': 'Live Panels',
        'tool_bulksms': 'Bulk SMS Routes',
        'tool_emailspam': 'Email Spamming',
        'tool_p1': 'P1'
    }
    
    tool_name = tools.get(call.data, "Unknown Tool")
    
    # Display contact information
    inline_keyboard2 = types.InlineKeyboardMarkup()
    inline_keyboard2.add(btn_menu)
    
    bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=f"🧰 **Tool Inquiry: {tool_name}**\n\n💬 **Contact Admin for Pricing:**\n\n📱 **Admin:** @HeisenbergActives\n🕐 **Available:** 24/7\n⚡ **Response:** Usually within 1 hour\n\n📝 **Please mention:**\n• Tool: {tool_name}\n• Your requirements\n• Expected usage volume\n\n✅ Admin will provide custom pricing and setup details.",
        reply_markup=inline_keyboard2,
        parse_mode="Markdown"
    )
    
    # Log the tool inquiry
    notify_admin_activity(user_id, username, "🧰 Tool Inquiry", f"{tool_name} - User requested pricing information")
    
    # Notify admin about the inquiry
    import datetime
    admin_message = f"🧰 **NEW TOOL INQUIRY**\n\n👤 **User:** @{username} (ID: {user_id})\n🔧 **Tool:** {tool_name}\n⏰ **Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n💬 **User is interested in pricing for this tool**"
    
    try:
        bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
        bot.send_message(GROUP_CHAT_ID, admin_message, parse_mode="Markdown")
    except Exception as e:
        print(f"Failed to notify admin: {e}")

def handle_unspoofed_purchase(call):
    """Handle unspoofed base purchases with bulk pricing"""
    user_id = call.message.chat.id
    username = call.message.chat.username or "No username"
    
    # Define pricing and package details
    packages = {
        'unspoofed_specific_50': {
            'name': 'Specific Unspoofed 50+',
            'price': 225,
            'quantity': 50,
            'type': 'Specific',
            'rate': '£4 per card'
        },
        'unspoofed_specific_100': {
            'name': 'Specific Unspoofed 100+',
            'price': 350,
            'quantity': 100,
            'type': 'Specific',
            'rate': '£3.50 per card'
        },
        'unspoofed_random_50': {
            'name': 'Random Unspoofed 50+',
            'price': 100,
            'quantity': 50,
            'type': 'Random',
            'rate': '£2 per card'
        },
        'unspoofed_random_100': {
            'name': 'Random Unspoofed 100+',
            'price': 150,
            'quantity': 100,
            'type': 'Random',
            'rate': '£1.50 per card'
        }
    }
    
    package = packages.get(call.data)
    if not package:
        return
    
    price = package['price']
    
    # Check user balance
    try:
        current_balance = db["bal" + str(user_id)]
    except:
        current_balance = 0
    
    # Process purchase
    if current_balance >= price:
        # Deduct amount from balance
        db["bal" + str(user_id)] = current_balance - price
        new_balance = current_balance - price
        
        # Notify user of successful purchase
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✅ **Purchase Successful!**\n\n🔓 **Package:** {package['name']}\n💳 **Quantity:** {package['quantity']} cards\n💰 **Rate:** {package['rate']}\n💰 **Total Price:** £{price}\n🔓 **Type:** {package['type']} Unspoofed\n💳 **New Balance:** £{new_balance}\n\n⏳ **Delivery:** Manual delivery in progress\n📞 **Admin notified** for immediate processing\n⏰ **Freshness:** 3 days - 2 weeks",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
        
        # Notify admin for manual delivery
        admin_message = f"🔔 **NEW UNSPOOFED BASE PURCHASE**\n\n👤 **User:** @{username} (ID: {user_id})\n🔓 **Package:** {package['name']}\n💳 **Quantity:** {package['quantity']} cards\n💰 **Rate:** {package['rate']}\n💰 **Total Price:** £{price}\n🔓 **Type:** {package['type']} Unspoofed\n⏰ **Freshness:** 3 days - 2 weeks\n\n⚠️ **ACTION REQUIRED:** Manual delivery needed"
        
        try:
            bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
            bot.send_message(GROUP_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to notify admin: {e}")
        
        # Log the purchase
        notify_admin_activity(user_id, username, "🔓 Unspoofed Purchase", f"{package['name']} - £{price}")
        
    else:
        # Insufficient balance
        needed = price - current_balance
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_wallet)
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"❌ **Insufficient Balance**\n\n🔓 **Package:** {package['name']}\n💳 **Quantity:** {package['quantity']} cards\n💰 **Total Price:** £{price}\n💳 **Your Balance:** £{current_balance}\n💸 **Need:** £{needed} more\n\n**Please top up your wallet to continue.**",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )

def handle_10gbp_purchase(call):
    """Handle purchase of £10 base items"""
    # Extract item ID from callback data
    item_id = int(call.data.replace("gbp10_", ""))
    price = 10  # Fixed price for £10 base
    
    # Load the same real £10 base data
    all_10gbp_data = []
    try:
        with open("base5/fullz5.txt") as file:
            all_10gbp_data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        all_10gbp_data = []
    
    # Get the specific product data
    if 1 <= item_id <= len(all_10gbp_data):
        product_data = all_10gbp_data[item_id - 1]
    else:
        product_data = f"£10 Base Item #{item_id}"
    
    user_id = call.message.chat.id
    username = call.message.chat.username or "No username"
    
    # Check user balance
    try:
        current_balance = db["bal" + str(user_id)]
    except:
        current_balance = 0
    
    # Process purchase
    if current_balance >= price:
        # Deduct amount from balance
        db["bal" + str(user_id)] = current_balance - price
        new_balance = current_balance - price
        
        # Notify user of successful purchase
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✅ **Purchase Successful!**\n\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n💳 **Type:** Heisen 10 Base\n💳 **New Balance:** £{new_balance}\n\n⏳ **Delivery:** Manual delivery in progress\n📞 **Admin notified** for immediate processing",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
        
        # Notify admin for manual delivery
        admin_message = f"🔔 **NEW £10 BASE PURCHASE**\n\n👤 **User:** @{username} (ID: {user_id})\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n💳 **Type:** Heisen 10 Base\n\n⚠️ **ACTION REQUIRED:** Manual delivery needed"
        
        try:
            bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
            bot.send_message(GROUP_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to notify admin: {e}")
        
        # Log the purchase
        notify_admin_activity(user_id, username, "💳 £10 Base Purchase", f"{product_data} - £{price}")
        
    else:
        # Insufficient balance
        needed = price - current_balance
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_wallet)
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"❌ **Insufficient Balance**\n\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n💳 **Your Balance:** £{current_balance}\n💸 **Need:** £{needed} more\n\n**Please top up your wallet to continue.**",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )

def handle_ausfresh_purchase(call):
    """Handle purchase of Australian fresh base items"""
    # Extract item ID from callback data
    item_id = int(call.data.replace("aus_", ""))
    price = 30  # Fixed price for Australian fresh base
    
    # Load the same real Australian fresh base data
    all_aus_data = []
    try:
        with open("base3/fullz3.txt") as file:
            all_aus_data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        all_aus_data = []
    
    # Get the specific product data
    if 1 <= item_id <= len(all_aus_data):
        product_data = all_aus_data[item_id - 1]
    else:
        product_data = f"Australian Fresh Item #{item_id}"
    
    user_id = call.message.chat.id
    username = call.message.chat.username or "No username"
    
    # Check user balance
    try:
        current_balance = db["bal" + str(user_id)]
    except:
        current_balance = 0
    
    # Process purchase
    if current_balance >= price:
        # Deduct amount from balance
        db["bal" + str(user_id)] = current_balance - price
        new_balance = current_balance - price
        
        # Notify user of successful purchase
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✅ **Purchase Successful!**\n\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n🇦🇺 **Type:** Australian Fresh Base\n💳 **New Balance:** £{new_balance}\n\n⏳ **Delivery:** Manual delivery in progress\n📞 **Admin notified** for immediate processing",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
        
        # Notify admin for manual delivery
        admin_message = f"🔔 **NEW AUSTRALIAN FRESH BASE PURCHASE**\n\n👤 **User:** @{username} (ID: {user_id})\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n🇦🇺 **Type:** Australian Fresh Base\n\n⚠️ **ACTION REQUIRED:** Manual delivery needed"
        
        try:
            bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
            bot.send_message(GROUP_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to notify admin: {e}")
        
        # Log the purchase
        notify_admin_activity(user_id, username, "💳 Australian Fresh Purchase", f"{product_data} - £{price}")
        
    else:
        # Insufficient balance
        needed = price - current_balance
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_wallet)
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"❌ **Insufficient Balance**\n\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n💳 **Your Balance:** £{current_balance}\n💸 **Need:** £{needed} more\n\n**Please top up your wallet to continue.**",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )

def handle_ukfresh_purchase(call):
    """Handle purchase of UK fresh base items"""
    # Extract item ID from callback data
    item_id = int(call.data.replace("uk_", ""))
    price = 30  # Fixed price for UK fresh base
    
    # Load the same real UK fresh base data
    all_uk_data = []
    try:
        with open("base2/fullz2.txt") as file:
            all_uk_data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        all_uk_data = []
    
    # Get the specific product data
    if 1 <= item_id <= len(all_uk_data):
        product_data = all_uk_data[item_id - 1]
    else:
        product_data = f"UK Fresh Item #{item_id}"
    
    user_id = call.message.chat.id
    username = call.message.chat.username or "No username"
    
    # Check user balance
    try:
        current_balance = db["bal" + str(user_id)]
    except:
        current_balance = 0
    
    # Process purchase
    if current_balance >= price:
        # Deduct amount from balance
        db["bal" + str(user_id)] = current_balance - price
        new_balance = current_balance - price
        
        # Notify user of successful purchase
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✅ **Purchase Successful!**\n\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n🇬🇧 **Type:** UK Fresh Base\n💳 **New Balance:** £{new_balance}\n\n⏳ **Delivery:** Manual delivery in progress\n📞 **Admin notified** for immediate processing",
            reply_markup=inline_keyboard2,
            parse_mode="Markdown"
        )
        
        # Notify admin for manual delivery
        admin_message = f"🔔 **NEW UK FRESH BASE PURCHASE**\n\n👤 **User:** @{username} (ID: {user_id})\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n🇬🇧 **Type:** UK Fresh Base\n\n⚠️ **ACTION REQUIRED:** Manual delivery needed"
        
        try:
            bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")
            bot.send_message(GROUP_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to notify admin: {e}")
        
        # Log the purchase
        notify_admin_activity(user_id, username, "💳 UK Fresh Purchase", f"{product_data} - £{price}")
        
    else:
        # Insufficient balance
        needed = price - current_balance
        inline_keyboard2 = types.InlineKeyboardMarkup()
        inline_keyboard2.add(btn_wallet)
        inline_keyboard2.add(btn_menu)
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"❌ **Insufficient Balance**\n\n🔸 **Product:** {product_data}\n💰 **Price:** £{price}\n💳 **Your Balance:** £{current_balance}\n💸 **Need:** £{needed} more\n\n**Please top up your wallet to continue.**",
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
    elif call.data.startswith("skipper_"):
        # Handle skipper product purchases
        handle_skipper_purchase(call)
    elif call.data.startswith("ukfresh_page_"):
        # Handle UK fresh base pagination
        page = int(call.data.split("_")[-1])
        open_uk_fresh_page(call.message, page)
    elif call.data.startswith("ausfresh_page_"):
        # Handle Australian fresh base pagination
        page = int(call.data.split("_")[-1])
        open_aus_fresh_page(call.message, page)
    elif call.data.startswith("gbp10_page_"):
        # Handle £10 base pagination
        page = int(call.data.split("_")[-1])
        open_10gbp_fresh_page(call.message, page)
    elif call.data.startswith("uk_"):
        # Handle UK fresh base purchases
        handle_ukfresh_purchase(call)
    elif call.data.startswith("aus_"):
        # Handle Australian fresh base purchases
        handle_ausfresh_purchase(call)
    elif call.data.startswith("gbp10_"):
        # Handle £10 base purchases
        handle_10gbp_purchase(call)
    elif call.data.startswith("unspoofed_"):
        # Handle unspoofed base purchases
        handle_unspoofed_purchase(call)
    elif call.data == "tools":
        # Handle tools menu
        open_tools_menu(call.message)
    elif call.data.startswith("tool_"):
        # Handle tool contact requests
        handle_tools_contact(call)
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

# Webhook route for Telegram
@app.route(f'/{API_KEY_001}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK"

# Health check route
@app.route('/')
def health_check():
    return "Heisenberg Store Bot is running!"

# Set webhook
def set_webhook():
    # Only set webhook if REPL_SLUG and REPL_OWNER are available (deployment environment)
    repl_slug = os.environ.get('REPL_SLUG')
    repl_owner = os.environ.get('REPL_OWNER')
    
    if repl_slug and repl_owner:
        webhook_url = f"https://{repl_slug}.{repl_owner}.repl.co/{API_KEY_001}"
        try:
            bot.remove_webhook()
            time.sleep(1)
            bot.set_webhook(url=webhook_url)
            print(f"Webhook set to: {webhook_url}")
        except Exception as e:
            print(f"Webhook setup failed: {e}")
            print("Falling back to polling mode...")
            bot.remove_webhook()
    else:
        print("Development environment detected, using polling mode")
        bot.remove_webhook()

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
    
    # Force polling mode only - resolve conflicts
    print("🚀 Starting Heisenberg Store Bot in polling mode...")
    
    # Clean up any existing connections - force delete webhook
    try:
        bot.delete_webhook()
        print("✓ Webhook deleted successfully")
    except Exception as e:
        print(f"⚠️ Webhook deletion: {e}")
    
    # Additional cleanup attempt
    try:
        bot.remove_webhook()
        print("✓ Webhook removed successfully")
    except Exception as e:
        print(f"⚠️ Webhook removal: {e}")
    
    # Wait longer for Telegram API to clear
    time.sleep(5)
    
    # Start with robust error handling
    retry_attempts = 0
    max_retries = 3
    
    while retry_attempts < max_retries:
        try:
            print("✓ Bot is now active - users can send /start")
            bot.infinity_polling(
                timeout=20,
                long_polling_timeout=10,
                skip_pending=True,
                none_stop=True
            )
            break
        except Exception as e:
            retry_attempts += 1
            print(f"❌ Attempt {retry_attempts} failed: {e}")
            if retry_attempts < max_retries:
                wait_time = 10 * retry_attempts
                print(f"🔄 Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("❌ Starting basic polling as fallback...")
                try:
                    bot.polling(none_stop=True, interval=2, timeout=15)
                except Exception as final_error:
                    print(f"❌ All methods failed: {final_error}")
                    time.sleep(60)  # Wait before restart
            
# Remove Flask app startup to prevent deployment mode conflicts
