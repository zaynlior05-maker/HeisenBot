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
import time  #Ovo je
import pandas as pd
import math
from replit import db
import arg
import os
import shutil
import re
from block_io import BlockIo
import random
import datetime

version = 2  # API version
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

reply_markup = telebot.types.ReplyKeyboardMarkup(True, False)
reply_markup.row(*custom_keyboard[0])
reply_markup.row(*custom_keyboard[1])

inline_keyboard1 = types.InlineKeyboardMarkup()
inline_keyboard3 = types.InlineKeyboardMarkup()

btn_store = types.InlineKeyboardButton('🛒 Store', callback_data='store')
btn_wallet = types.InlineKeyboardButton('💷 Wallet', callback_data='wallet')
btn_support = types.InlineKeyboardButton('☎️ Support', callback_data='support')
btn_rules = types.InlineKeyboardButton('🛡️ Rules', callback_data='rules')
btn_updates = types.InlineKeyboardButton('📁 Updates Channel',
                                         callback_data='updates')


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




btn_base2 = types.InlineKeyboardButton('🔸Australia', callback_data='base2')

dat1 = datetime.date.today()
month_1 = dat1.strftime("%B")
day_1 = dat1.strftime("%d")

dat2 = dat1 - datetime.timedelta(days=1)
month_2 = dat2.strftime("%B")
day_2 = dat2.strftime("%d")

dat3 = dat2 - datetime.timedelta(days=1)
month_3 = dat3.strftime("%B")
day_3 = dat3.strftime("%d")

btn_base3 = types.InlineKeyboardButton('🔸' + month_3 + '-Heisen-V' + day_3 + '-1', callback_data='base3')
btn_base4 = types.InlineKeyboardButton('🔸' + month_3 + '-Heisen-V' + day_3 + '-2', callback_data='base4')
btn_base5 = types.InlineKeyboardButton('🔸' + month_2 + '-Heisen-V' + day_2, callback_data='base5')
btn_base6 = types.InlineKeyboardButton('🔸' + month_1 + '-Heisen-V' + day_1 + '-1', callback_data='base6')
btn_base7 = types.InlineKeyboardButton('🔸' + month_1 + '-Heisen-V' + day_1 + '-2', callback_data='base7')
btn_base11 = types.InlineKeyboardButton('🔸Skiper & Meth', callback_data='base11')
btn_base10 = types.InlineKeyboardButton('🔸USA', callback_data='base10')


inline_keyboard1.add(btn_store)
inline_keyboard1.add(btn_wallet, btn_support)
inline_keyboard1.add(btn_rules, btn_updates)

inline_keyboard3.add(btn_base11)
inline_keyboard3.add(btn_base2)
inline_keyboard3.add(btn_base3)
inline_keyboard3.add(btn_base4)
inline_keyboard3.add(btn_base5)
inline_keyboard3.add(btn_base6)
inline_keyboard3.add(btn_base7)

inline_keyboard3.add(btn_base10)

#inline_keyboard3.add(btn_base2)
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
        bot.send_message(id, text = msg, 
      parse_mode="Markdown")
      except:
        print("error")

@bot.message_handler(commands=['sendall'])
def send_announcement(message):
    msg = str(extract_arg2(message.text)[0])
    password = str(extract_arg2(message.text)[1])

    print(msg)
    print(password)
  
    if adminpass == password:
      keys = db. keys()
      for i in keys: # or whatever variable.
        time.sleep(0.5)
        if str(i)[0:3] == "bal":
          print
          try:
            bot.send_message(str(i)[3:], text = msg, 
      parse_mode="Markdown")
          except Exception as e:
            print(e)
            
            

@bot.message_handler(commands=['userbal'])
def userbal(message):
  id = int(extract_arg1(message.text)[0])
  credit = int(extract_arg1(message.text)[1])
  password = str(extract_arg1(message.text)[2])
  if adminpass == password:
    bot.send_message(int(id), text = "✅£"+ str(credit-int(db["bal" + str(id)])) + " has been added to your wallet.✅", 
    parse_mode="Markdown")
    bot.send_message(message.chat.id, text = "£"+ str(credit) + " has been set to: " + str(id), 
    parse_mode="Markdown")
  db["bal" + str(id)] = credit

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  # Notification for admin tracking
  requests.post(
    'https://api.telegram.org/bot7984635760:AAGS7eDpCnK_EgnqYEMXgJk72avYAQe9pWI/sendMessage?chat_id=-1002563927894&text=@'
    + str(message.chat.username)  + " (" + str(message.chat.id) + ') just started the bot')

  try:
    value = db["bal" + str(message.chat.id)]
  except:
    db["bal" + str(message.chat.id)] = 0

  bot.send_message(
    message.chat.id,
    text=STORE_RULES,
    parse_mode="Markdown")
  msg = bot.send_message(
    message.chat.id,
    "Welcome to Heisenberg Store\n\nMade/Coded by @HeisenbergActives\n\nManaged by @HeisenbergActives\n\nUsername : <code>"
    + str(message.chat.username) + "</code>\nID: <code>" +
    str(message.chat.id) + "</code>",
    reply_markup=inline_keyboard1,
    parse_mode="HTML")


def open_binlist(message):

  bot.edit_message_text(chat_id=message.chat.id,
                        message_id=message.message_id,
                        text="Choose the base you would like to browse:",
                        reply_markup=inline_keyboard3,
                        parse_mode="HTML")
  # Notification enabled for activity tracking
  requests.post(
    'https://api.telegram.org/bot7984635760:AAGS7eDpCnK_EgnqYEMXgJk72avYAQe9pWI/sendMessage?chat_id=-1002563927894&text=@'
    + str(message.chat.username)  + " (" + str(message.chat.id) + ') is browsing through fullz')


def open_base(message, base):
  inline_keyboard2 = types.InlineKeyboardMarkup()

  binlist = ""
  text_file = open("binlist.txt", "r")
  binlist = text_file.read()
  text_file.close()
  with open("base" + str(base) + "/fullz" + str(base) + ".txt") as file:
    for line in file:

      btn = types.InlineKeyboardButton(line.rstrip(), callback_data='fullz')
      inline_keyboard2.add(btn)

  inline_keyboard2.add(btn_prev)
  inline_keyboard2.add(btn_menu)
  bot.edit_message_text(chat_id=message.chat.id,
                        message_id=message.message_id,
                        text="Buy the bin by clicking on it",
                        reply_markup=inline_keyboard2,
                        parse_mode="HTML")


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
    text='🆔ID: <code>' + str(message.chat.id) + '</code>\n🏦Balance: £' +
    str(db["bal" + str(message.chat.id)]) + "\n🔸Choose amount:",
    reply_markup=inline_keyboard2,
    parse_mode="HTML")

  # Notification enabled for activity tracking
  # requests.post(
  #   'https://api.telegram.org/botYOUR_NOTIFICATION_BOT_TOKEN/sendMessage?chat_id=YOUR_GROUP_ID&text=@'
  #   + str(message.chat.username)  + " (" + str(message.chat.id) + ') opened the wallet')


def open_topup(message, amount):

  inline_keyboard2 = types.InlineKeyboardMarkup()
  inline_keyboard2.add(btn_menu)
  
  # Use fixed BTC rates instead of API call
  btc_rates = {
    '20': '0.00025', '30': '0.00038', '50': '0.00063', '70': '0.00088',
    '100': '0.00126', '150': '0.00189', '200': '0.00252', '250': '0.00315',
    '300': '0.00378', '400': '0.00504', '500': '0.00630', '1000': '0.01260'
  }
  
  btc_amount = btc_rates.get(amount, '0.00100')

  bot.edit_message_text(
    chat_id=message.chat.id,
    message_id=message.message_id,
    text="Send <b>exactly</b> <code>" + btc_amount + "</code>" +
    " BTC to the following address: \n<code>bc1q64f2jfjpv2f7n4a2jryj08wklc0yrvsjles5wt</code>\n\n⚠️┇Deposits are non refundable\n⚠️┇Double check BTC amount\n⚠️┇Send as BTC not as £\n\nFunds will appear in your account after 3 confirmations.",
    reply_markup=inline_keyboard2,
    parse_mode="HTML")
  # Notification enabled for activity tracking
  # requests.post(
  #   'https://api.telegram.org/botYOUR_NOTIFICATION_BOT_TOKEN/sendMessage?chat_id=YOUR_GROUP_ID&text=@'
  #   + str(message.chat.username)  + " (" + str(message.chat.id) + ') opened the topup page for £' +
  #   str(amount))


def open_support(message):
  inline_keyboard2 = types.InlineKeyboardMarkup()
  inline_keyboard2.add(btn_menu)
  bot.edit_message_text(chat_id=message.chat.id,
                        message_id=message.message_id,
                        text='Support Account  : @HeisenbergActives',
                        reply_markup=inline_keyboard2,
                        parse_mode="Markdown")


def open_update(message):
  inline_keyboard2 = types.InlineKeyboardMarkup()
  inline_keyboard2.add(btn_menu)
  bot.edit_message_text(chat_id=message.chat.id,
                        message_id=message.message_id,
                        text='Invite Link  : https://t.me/HeisenbergStoreUk',
                        reply_markup=inline_keyboard2,
                        parse_mode="Markdown")


def open_menu(message):
  bot.edit_message_text(
    chat_id=message.chat.id,
    message_id=message.message_id,
    text=
    "Welcome to Heisenberg Store\n\nMade/Coded by @HeisenbergActives\n\nManaged by @HeisenbergActives\n\nUsername : <code>"
    + str(message.chat.username) + "</code>\nID: <code>" +
    str(message.chat.id) + "</code>",
    reply_markup=inline_keyboard1,
    parse_mode="HTML")





def open_rules(message):
  inline_keyboard2 = types.InlineKeyboardMarkup()
  inline_keyboard2.add(btn_menu)
  bot.edit_message_text(
    chat_id=message.chat.id,
    message_id=message.message_id,
    text=STORE_RULES,
    reply_markup=inline_keyboard2,
    parse_mode="Markdown")


def open_search(message):
    sent_msg = bot.send_message(message.chat.id, "<code>-- 🔎 Bin Search --</code>\nType the 6 digit bin you want to look for", parse_mode = "HTML")
    bot.register_next_step_handler(sent_msg, bin_handler)




def bin_handler(message):
  inline_keyboard2 = types.InlineKeyboardMarkup()
  inline_keyboard2.add(btn_cancel)
  bin = message.text
  
  if(bin == "/start" or bin in btns):
    send_welcome(message)
    return
  
  try:
    bin = int(bin)
    
    if (len(str(bin)) == 6):
      with open("binlist.txt", 'r') as file:
        lines = file.readlines()
        exists = False
        print("opened")
        for line in lines:
            if str(bin) in line:
                exists = True
                inline_keyboard2 = types.InlineKeyboardMarkup()
                btn_bin = types.InlineKeyboardButton(line, callback_data='buy')
                inline_keyboard2.add(btn_bin)
                inline_keyboard2.add(btn_searchagn)
                
                break
        if(exists):
          bot.send_message(message.chat.id, "Bin available!", reply_markup = inline_keyboard2)
          return
        elif(exists == False):
          bot.send_message(message.chat.id, "Couldn't Fetch the Bin please try again later")
          # Notification enabled for activity tracking
          # requests.post(
          #   'https://api.telegram.org/botYOUR_NOTIFICATION_BOT_TOKEN/sendMessage?chat_id=YOUR_GROUP_ID&text=@'
          #   + str(message.chat.username) + " (" + str(message.chat.id) + ') searched this bin, but it is not available: ' + str(bin))
          return
    else:
      sent_msg = bot.send_message(message.chat.id, "Bin number is 6 Digits or press cancel to close this session", reply_markup = inline_keyboard2)
      bot.register_next_step_handler(sent_msg, bin_handler)  
  except Exception as e:
    print(e)
    sent_msg = bot.send_message(message.chat.id, "Only use numbers please or press cancel to close this session", reply_markup = inline_keyboard2)
    bot.register_next_step_handler(sent_msg, bin_handler)  
    
    
def cancel(message):
  bot.edit_message_text(
    chat_id=message.chat.id,
    message_id=message.message_id,
    text=
    "❌ OPERATION CANCELED",
    parse_mode="Markdown")
  send_welcome(message)
  return    



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  bot.answer_callback_query(callback_query_id=call.id)
  if (call.message.chat.username == "kanseph"
      or call.message.chat.username == "mazz44"):
    text_file = open("error.txt", "r")

    #read whole file to a string
    error = text_file.read()

    #close file
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
    print(call.data[3:])
    open_topup(call.message, call.data[3:])
  elif str(call.data)[0:4] == "base":
    open_base(call.message, call.data[4:])
  elif call.data == "fullz":
    # Notification enabled for activity tracking
    # requests.post(
    #   'https://api.telegram.org/botYOUR_NOTIFICATION_BOT_TOKEN/sendMessage?chat_id=YOUR_GROUP_ID&text=@'
    #   + str(call.message.chat.username)  + " (" + str(call.message.chat.id) + ') tried to buy fullz, but no credits')
    amount = int(db["bal"+ str(call.message.chat.id)])
    if(amount == 285):
      bot.send_message(call.message.chat.id, text="❌£300 NEEDED IN WALLLET TO ACTIVATE THE ACCOUNT, CONTACT SUPPORT FOR HELP❌", parse_mode = "Markdown")
    elif(amount>0):
      
      bot.send_message(call.message.chat.id, text="❌£" + str(2*amount) + " NEEDED IN WALLLET TO ACTIVATE THE ACCOUNT, CONTACT SUPPORT FOR HELP❌", parse_mode = "Markdown")
    else:
      bot.send_message(call.message.chat.id, text="❌NOT ENOUGH CREDITS. PLEASE TOP UP❌", parse_mode = "Markdown")


def extract_arg1(arg):
  return arg.split()[1:]


def extract_arg2(arg):
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

  
bot.infinity_polling()