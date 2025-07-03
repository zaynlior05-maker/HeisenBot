"""
Web interface for ExcelYard Bot monitoring and administration
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configuration
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'excelyard2024')

class BotMonitor:
    def __init__(self):
        self.data_dir = 'data'
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_user_data(self):
        """Load user data from file"""
        try:
            with open(os.path.join(self.data_dir, 'user_data.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def load_activity_log(self):
        """Load activity log from file"""
        try:
            with open(os.path.join(self.data_dir, 'activity_log.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def load_transactions(self):
        """Load transactions from file"""
        try:
            with open(os.path.join(self.data_dir, 'transactions.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def get_stats(self):
        """Get bot statistics"""
        user_data = self.load_user_data()
        activity_log = self.load_activity_log()
        transactions = self.load_transactions()
        
        stats = {
            'total_users': len(user_data),
            'total_transactions': len(transactions),
            'total_activity': len(activity_log),
            'active_users_24h': self.count_active_users(activity_log, 24),
            'active_users_7d': self.count_active_users(activity_log, 24 * 7),
            'total_revenue': sum(t.get('amount', 0) for t in transactions),
            'pending_payments': len([t for t in transactions if t.get('status') == 'pending'])
        }
        
        return stats
    
    def count_active_users(self, activity_log, hours):
        """Count active users in the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        active_users = set()
        
        for activity in activity_log:
            try:
                activity_time = datetime.fromisoformat(activity.get('timestamp', ''))
                if activity_time > cutoff:
                    active_users.add(activity.get('user_id'))
            except:
                continue
        
        return len(active_users)
    
    def get_recent_activity(self, limit=50):
        """Get recent activity"""
        activity_log = self.load_activity_log()
        return activity_log[-limit:] if len(activity_log) > limit else activity_log
    
    def get_user_details(self, user_id):
        """Get details for a specific user"""
        user_data = self.load_user_data()
        activity_log = self.load_activity_log()
        transactions = self.load_transactions()
        
        user_info = user_data.get(str(user_id), {})
        user_activity = [a for a in activity_log if a.get('user_id') == user_id]
        user_transactions = [t for t in transactions if t.get('user_id') == user_id]
        
        return {
            'info': user_info,
            'activity': user_activity,
            'transactions': user_transactions
        }

monitor = BotMonitor()

@app.route('/')
def index():
    """Main dashboard"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    stats = monitor.get_stats()
    recent_activity = monitor.get_recent_activity(20)
    
    return render_template('index.html', stats=stats, recent_activity=recent_activity)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/users')
def users():
    """Users page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    user_data = monitor.load_user_data()
    return render_template('users.html', users=user_data)

@app.route('/activity')
def activity():
    """Activity log page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    activity_log = monitor.load_activity_log()
    total = len(activity_log)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    activities = activity_log[start:end] if start < total else []
    
    return render_template('activity.html', 
                         activities=activities, 
                         page=page, 
                         total=total, 
                         per_page=per_page)

@app.route('/transactions')
def transactions():
    """Transactions page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    transactions = monitor.load_transactions()
    return render_template('transactions.html', transactions=transactions)

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify(monitor.get_stats())

@app.route('/api/user/<int:user_id>')
def api_user(user_id):
    """API endpoint for user details"""
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify(monitor.get_user_details(user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
