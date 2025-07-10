#!/usr/bin/env python3
"""
External Keep-Alive Service for Heisenberg Store Bot
This service ensures the bot never goes to sleep by continuous monitoring
"""

import time
import requests
import os
import threading
from datetime import datetime

class KeepAliveService:
    def __init__(self):
        self.repl_slug = os.environ.get('REPL_SLUG')
        self.repl_owner = os.environ.get('REPL_OWNER')
        self.base_url = f"https://{self.repl_slug}.{self.repl_owner}.repl.co" if self.repl_slug and self.repl_owner else "http://localhost:5000"
        self.running = True
        
    def ping_service(self):
        """Ping the service to keep it alive"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                print(f"🟢 {datetime.now().strftime('%H:%M:%S')} - Keep-alive ping successful")
                return True
            else:
                print(f"🟡 {datetime.now().strftime('%H:%M:%S')} - Keep-alive ping returned {response.status_code}")
                return False
        except Exception as e:
            print(f"🔴 {datetime.now().strftime('%H:%M:%S')} - Keep-alive ping failed: {e}")
            return False
    
    def check_bot_status(self):
        """Check if bot is responding"""
        try:
            response = requests.get(f"{self.base_url}/status", timeout=10)
            if response.status_code == 200:
                print(f"✓ {datetime.now().strftime('%H:%M:%S')} - Bot status check passed")
                return True
            else:
                print(f"⚠ {datetime.now().strftime('%H:%M:%S')} - Bot status check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {datetime.now().strftime('%H:%M:%S')} - Bot status check error: {e}")
            return False
    
    def monitor_continuously(self):
        """Continuous monitoring loop"""
        print("🚀 Starting continuous monitoring service...")
        
        while self.running:
            try:
                # Ping every 4 minutes to prevent sleep
                self.ping_service()
                time.sleep(240)  # 4 minutes
                
                # Status check every 8 minutes
                self.check_bot_status()
                time.sleep(240)  # Another 4 minutes (total 8 minutes)
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute before retry
    
    def start(self):
        """Start the keep-alive service"""
        monitor_thread = threading.Thread(target=self.monitor_continuously, daemon=True)
        monitor_thread.start()
        print("✓ Keep-alive monitoring service started")

# Global instance
keep_alive_service = KeepAliveService()

if __name__ == "__main__":
    keep_alive_service.start()
    keep_alive_service.monitor_continuously()