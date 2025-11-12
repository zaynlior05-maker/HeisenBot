# 🤖 FULLZ HAVEN Bot - Final Setup Instructions

Your bot is **ALMOST READY**! Just need your actual User ID to complete the setup.

## ✅ What's Already Configured:
- ✅ Bot Token: `8371436909:AAHHtha3kC8b9mNfXk5jpuRW54wfJxtRMXw`
- ✅ Bot Name: **FULLZ HAVEN**
- ✅ Bot Username: `@FullzHavenUkBot`
- ✅ Group Chat: `HEISENBERG_CITY://🕹️` (-1003275412781)
- ✅ Support Username: `@HeisenbergActives`
- ✅ Web Admin: Username: `admin`, Password: `heisenberg2024`

## 🔧 What You Need to Do:

### Step 1: Get Your User ID
1. Start a chat with your bot: [@FullzHavenUkBot](https://t.me/FullzHavenUkBot)
2. Send `/start` to your bot
3. Or use [@userinfobot](https://t.me/userinfobot) - just send any message to it and it will reply with your User ID

### Step 2: Update Your User ID
Once you have your User ID (it's a number like `123456789`), update these files:

**In `constants.py` line 11:**
```python
ADMIN_ID = int(os.getenv('ADMIN_ID', 'YOUR_ACTUAL_USER_ID_HERE'))
```

**In `main.py` line 33:**
```python
ADMIN_ID = int(os.getenv('ADMIN_ID', 'YOUR_ACTUAL_USER_ID_HERE'))
```

**In `.env` file line 6:**
```
ADMIN_ID=YOUR_ACTUAL_USER_ID_HERE
```

### Step 3: Test Your Bot
1. Restart the bot: Stop and start the "Bot Test" workflow
2. Send `/start` to [@FullzHavenUkBot](https://t.me/FullzHavenUkBot)
3. You should see the welcome message with menu options

### Step 4: Access Admin Dashboard
1. Open: http://localhost:5000 (or the web interface URL)
2. Login with:
   - Username: `admin`
   - Password: `heisenberg2024`

## 🎯 Your Bot Features:

### For Users:
- 🏪 **Product Marketplace**: Fullz, CVV, and Dumps categories
- 💰 **Wallet System**: Bitcoin payment processing
- 🔍 **Search Function**: Find products quickly
- 📱 **User-Friendly Menus**: Easy navigation

### For Admin (You):
- 📊 **Web Dashboard**: Monitor all activity at http://localhost:5000
- 👥 **User Management**: See all registered users
- 💳 **Transaction Tracking**: Monitor all payments and purchases
- 📝 **Activity Logs**: Complete user interaction history
- 🔔 **Real-time Notifications**: Get alerts in your Telegram group

## 🚀 Bot Commands:
- `/start` - Main menu
- `/wallet` - Check balance and add funds
- `/balance` - Quick balance check
- `/help` - Show help information

## 📞 Support Integration:
- Support contact: @HeisenbergActives
- Group notifications: HeisenbergStoreUk
- All user activities are logged automatically

## ⚠️ Important Notes:
- Bot accepts Bitcoin payments only
- All transactions are logged in the admin dashboard
- Product data is stored in the `/data/` folder
- Keep your bot token secure and never share it

Once you update your User ID, your bot will be 100% ready to use!
