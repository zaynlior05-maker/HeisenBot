#!/usr/bin/env python3
"""
Personal Details Setup Script for your Telegram Bot
Run this script to easily customize all your personal information
"""

import os
import re

def update_personal_details():
    print("=== Personal Details Setup ===")
    print("This will update your bot with your personal information")
    print()
    
    # Get user inputs
    store_name = input("Enter your store name (e.g., 'John's Digital Store'): ")
    your_username = input("Enter your Telegram username (without @): ")
    admin_username = input("Enter your admin/manager username (without @): ")
    support_username = input("Enter your support account username (without @): ")
    bot_username = input("Enter your bot's username (without @): ")
    bitcoin_address = input("Enter your Bitcoin wallet address: ")
    
    # Optional notification settings
    print("\n--- Notification Settings (Optional) ---")
    use_notifications = input("Do you want to enable activity notifications? (y/n): ").lower() == 'y'
    
    notification_bot_token = ""
    notification_group_id = ""
    
    if use_notifications:
        notification_bot_token = input("Enter your notification bot token: ")
        notification_group_id = input("Enter your notification group/channel ID: ")
    
    print("\nUpdating your bot files...")
    
    # Read the main.py file
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Replace placeholders with actual values
    content = content.replace('YOUR_STORE_NAME', store_name)
    content = content.replace('YOUR_USERNAME', f'@{your_username}')
    content = content.replace('YOUR_ADMIN_USERNAME', f'@{admin_username}')
    content = content.replace('YOUR_SUPPORT_USERNAME', f'@{support_username}')
    content = content.replace('YOUR_BOT_USERNAME', bot_username)
    content = content.replace('bc1qsndr0eczpagjxenh8dus3x720zy8c5dkvfds8n', bitcoin_address)
    
    # Handle notifications
    if use_notifications:
        # Uncomment and update notification lines
        content = re.sub(
            r'  # Add your notification.*?\n  # requests\.post\(\n  #   \'https://api\.telegram\.org/botYOUR_NOTIFICATION_BOT_TOKEN/sendMessage\?chat_id=YOUR_GROUP_ID&text=@\'([^)]+)\)',
            f'  requests.post(\n    \'https://api.telegram.org/bot{notification_bot_token}/sendMessage?chat_id={notification_group_id}&text=@\'\\1)',
            content,
            flags=re.DOTALL
        )
    
    # Write the updated content back
    with open('main.py', 'w') as f:
        f.write(content)
    
    # Update constants.py
    with open('constants.py', 'r') as f:
        constants_content = f.read()
    
    # Update support username in constants
    constants_content = re.sub(
        r"SUPPORT_USERNAME = '@.*'",
        f"SUPPORT_USERNAME = '@{support_username}'",
        constants_content
    )
    
    with open('constants.py', 'w') as f:
        f.write(constants_content)
    
    print("\n✅ Personal details updated successfully!")
    print("\nNext steps:")
    print("1. Update your bot token in constants.py (API_KEY_001)")
    print("2. Update your admin password in constants.py (adminpass)")
    print("3. Test your bot by running: python main.py")
    print("\nYour bot is ready to use with your personal branding!")

if __name__ == "__main__":
    update_personal_details()