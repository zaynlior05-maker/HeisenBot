#!/usr/bin/env python3
"""
Deployment startup script for Heisenberg Store Bot
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main bot
if __name__ == "__main__":
    try:
        from main import *
        print("🚀 Heisenberg Store Bot starting...")
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")
        sys.exit(1)