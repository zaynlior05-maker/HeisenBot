#!/usr/bin/env python3
"""
UptimeRobot-style External Monitoring Service
This script can be run separately to monitor and ping the bot service
"""

import requests
import time
import os
from datetime import datetime
import threading

class UptimeMonitor:
    def __init__(self):
        # Detect environment
        self.repl_slug = os.environ.get('REPL_SLUG')
        self.repl_owner = os.environ.get('REPL_OWNER')
        
        if self.repl_slug and self.repl_owner:
            self.base_url = f"https://{self.repl_slug}.{self.repl_owner}.repl.co"
        else:
            self.base_url = "http://localhost:5000"
        
        self.endpoints = [
            "/",
            "/status", 
            "/health",
            "/ping",
            "/keepalive"
        ]
        
        self.running = True
        
    def ping_endpoint(self, endpoint):
        """Ping a specific endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ {datetime.now().strftime('%H:%M:%S')} - {endpoint} - OK")
                return True
            else:
                print(f"⚠️ {datetime.now().strftime('%H:%M:%S')} - {endpoint} - Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ {datetime.now().strftime('%H:%M:%S')} - {endpoint} - Error: {e}")
            return False
    
    def monitor_cycle(self):
        """Run a complete monitoring cycle"""
        print(f"🔄 {datetime.now().strftime('%H:%M:%S')} - Starting monitoring cycle")
        
        successful_pings = 0
        total_endpoints = len(self.endpoints)
        
        for endpoint in self.endpoints:
            if self.ping_endpoint(endpoint):
                successful_pings += 1
            time.sleep(2)  # Small delay between pings
        
        success_rate = (successful_pings / total_endpoints) * 100
        print(f"📊 {datetime.now().strftime('%H:%M:%S')} - Cycle complete: {successful_pings}/{total_endpoints} ({success_rate:.1f}%) endpoints responding")
        
        return success_rate >= 80  # Consider healthy if 80%+ endpoints respond
    
    def continuous_monitoring(self):
        """Run continuous monitoring"""
        print("🚀 Starting UptimeRobot-style monitoring...")
        print(f"🎯 Monitoring: {self.base_url}")
        
        while self.running:
            try:
                is_healthy = self.monitor_cycle()
                
                if is_healthy:
                    # If healthy, wait 3 minutes
                    time.sleep(180)
                else:
                    # If unhealthy, ping more frequently
                    print("⚠️ Service appears unhealthy, increasing ping frequency")
                    time.sleep(60)  # Wait only 1 minute
                    
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped by user")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(30)  # Wait 30 seconds on error

# External monitoring functions for integration
def start_external_monitoring():
    """Start external monitoring in background thread"""
    monitor = UptimeMonitor()
    monitor_thread = threading.Thread(target=monitor.continuous_monitoring, daemon=True)
    monitor_thread.start()
    print("✅ External UptimeRobot-style monitoring started")
    return monitor

def ping_service_once():
    """Single ping for health check"""
    monitor = UptimeMonitor()
    return monitor.monitor_cycle()

if __name__ == "__main__":
    monitor = UptimeMonitor()
    monitor.continuous_monitoring()