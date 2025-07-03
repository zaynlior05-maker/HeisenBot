# Telegram Bot - Customizable Digital Services Marketplace

A comprehensive Telegram bot for managing digital product sales with integrated payment processing, user management, and admin dashboard.

## Quick Setup Guide

### 1. Get Your Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Choose a name and username for your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your User ID
1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Copy your user ID number

### 3. Setup Group for Notifications (Optional)
1. Create a Telegram group
2. Add your bot to the group as admin
3. Get the group ID using [@userinfobot](https://t.me/userinfobot) (forward a message from the group)

### 4. Configure Your Bot

#### Option A: Use the Setup Script (Recommended)
```bash
python config_setup.py
```
Follow the prompts to enter all your details.

#### Option B: Manual Configuration
Edit these files with your details:

**constants.py:**
- Replace `YOUR_BOT_TOKEN_HERE` with your bot token
- Replace `YOUR_ADMIN_USER_ID` with your user ID
- Replace `YOUR_GROUP_CHAT_ID` with your group ID
- Replace `YOUR_BOT_NAME` with your bot's name
- Replace `@YOUR_SUPPORT_USERNAME` with your support username

**main.py:**
- Update the bot configuration section with your token and IDs
- Replace `YOUR_BOT_NAME` with your bot's name

**web_interface.py:**
- Replace `your_admin_username` and `your_admin_password` with your admin credentials

### 5. Run Your Bot
```bash
python main.py
```

### 6. Access Admin Dashboard
- Open your browser to `http://localhost:5000`
- Login with your admin credentials
- Monitor users, transactions, and activity

## Features

### Bot Features
- **Product Catalog Management**: Fullz, CVV, and Dumps categories
- **Payment Processing**: Bitcoin payment integration
- **User Wallet System**: Balance management and transactions
- **Search Functionality**: Product search across categories
- **Admin Notifications**: Real-time logging to admin and groups

### Admin Dashboard Features
- **User Management**: View registered users and their activity
- **Transaction Monitoring**: Track payments and purchases
- **Activity Logs**: Complete user interaction history
- **Real-time Stats**: User counts, revenue, and activity metrics

## File Structure

```
├── main.py                 # Main bot application
├── constants.py            # Configuration and settings
├── bin_data_loader.py      # Product data management
├── web_interface.py        # Admin dashboard
├── config_setup.py         # Easy configuration script
├── data/                   # Data storage directory
│   ├── fullz_bases.json    # Fullz product data
│   ├── cvv_data.json       # CVV product data
│   └── dumps_data.json     # Dumps product data
├── templates/              # Web interface templates
│   ├── index.html
│   ├── login.html
│   ├── users.html
│   ├── activity.html
│   └── transactions.html
└── static/                 # CSS and JavaScript files
    ├── style.css
    └── script.js
```

## Environment Variables (Optional)

You can also set these environment variables instead of editing the files:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export ADMIN_ID="your_user_id"
export GROUP_CHAT_ID="your_group_id"
export LOG_GROUP_ID="your_log_group_id"
export ADMIN_USERNAME="your_admin_username"
export ADMIN_PASSWORD="your_admin_password"
```

## Customization

### Changing Product Categories
Edit `constants.py` to modify:
- Product types and descriptions
- Pricing ranges
- Available countries/regions

### Updating Messages
Modify the `MESSAGES` dictionary in `constants.py` to change:
- Welcome messages
- Help text
- Payment instructions
- Bot information

### Adding New Features
- Add new handlers in `main.py`
- Update the web interface in `web_interface.py`
- Modify templates in `templates/` directory

## Security Notes

- Keep your bot token private
- Use strong admin passwords
- Only share group invite links with trusted users
- Regularly monitor the admin dashboard for suspicious activity

## Troubleshooting

### Bot Not Responding
1. Check your bot token is correct
2. Ensure the bot is not blocked by Telegram
3. Verify your user ID is correct

### Web Dashboard Not Loading
1. Check if port 5000 is available
2. Verify admin credentials
3. Ensure all template files are present

### Payment Issues
1. Verify Bitcoin address generation
2. Check payment processing logic
3. Monitor transaction logs in admin dashboard

## Support

- Check the admin dashboard for user activity and errors
- Review the bot logs for debugging information
- Test all features thoroughly before deploying

## License

This project is for educational and personal use. Ensure compliance with local laws and Telegram's Terms of Service.