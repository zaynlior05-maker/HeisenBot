"""
Data loader for ExcelYard Bot - Handles product catalogs and search functionality
"""

import json
import os
import random
from datetime import datetime

def load_json_data(filename):
    """Load JSON data from file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_data(filename, data):
    """Save data to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def create_fullz_bases():
    """Create sample fullz database structure"""
    bases = {
        'us': {
            'count': 1250,
            'samples': [
                {'state': 'CA', 'zip': '90210', 'bank': 'Bank of America', 'quality': 'Premium'},
                {'state': 'NY', 'zip': '10001', 'bank': 'Chase', 'quality': 'Standard'},
                {'state': 'TX', 'zip': '75001', 'bank': 'Wells Fargo', 'quality': 'Premium'},
                {'state': 'FL', 'zip': '33101', 'bank': 'Citi', 'quality': 'VIP'},
                {'state': 'IL', 'zip': '60601', 'bank': 'US Bank', 'quality': 'Standard'}
            ]
        },
        'uk': {
            'count': 850,
            'samples': [
                {'region': 'London', 'postcode': 'SW1A', 'bank': 'Barclays', 'quality': 'Premium'},
                {'region': 'Manchester', 'postcode': 'M1', 'bank': 'HSBC', 'quality': 'Standard'},
                {'region': 'Birmingham', 'postcode': 'B1', 'bank': 'Lloyds', 'quality': 'VIP'},
                {'region': 'Leeds', 'postcode': 'LS1', 'bank': 'NatWest', 'quality': 'Premium'},
                {'region': 'Glasgow', 'postcode': 'G1', 'bank': 'RBS', 'quality': 'Standard'}
            ]
        },
        'ca': {
            'count': 650,
            'samples': [
                {'province': 'ON', 'postal': 'M5V', 'bank': 'TD Bank', 'quality': 'Premium'},
                {'province': 'BC', 'postal': 'V6B', 'bank': 'RBC', 'quality': 'Standard'},
                {'province': 'AB', 'postal': 'T2P', 'bank': 'BMO', 'quality': 'VIP'},
                {'province': 'QC', 'postal': 'H2Y', 'bank': 'Scotia', 'quality': 'Premium'},
                {'province': 'NS', 'postal': 'B3H', 'bank': 'CIBC', 'quality': 'Standard'}
            ]
        },
        'au': {
            'count': 450,
            'samples': [
                {'state': 'NSW', 'postcode': '2000', 'bank': 'CBA', 'quality': 'Premium'},
                {'state': 'VIC', 'postcode': '3000', 'bank': 'ANZ', 'quality': 'Standard'},
                {'state': 'QLD', 'postcode': '4000', 'bank': 'Westpac', 'quality': 'VIP'},
                {'state': 'WA', 'postcode': '6000', 'bank': 'NAB', 'quality': 'Premium'},
                {'state': 'SA', 'postcode': '5000', 'bank': 'Bendigo', 'quality': 'Standard'}
            ]
        }
    }
    
    save_json_data('data/fullz_bases.json', bases)
    return bases

def get_base_records(country):
    """Get sample records for a country"""
    data = load_json_data('data/fullz_bases.json')
    
    if not data:
        data = create_fullz_bases()
    
    country_data = data.get(country.lower(), {})
    samples = country_data.get('samples', [])
    
    if samples:
        # Return formatted sample records
        formatted_samples = []
        for sample in samples[:3]:  # Show first 3 samples
            if country.lower() == 'us':
                formatted_samples.append(f"• {sample['state']} {sample['zip']} - {sample['bank']} ({sample['quality']})")
            elif country.lower() == 'uk':
                formatted_samples.append(f"• {sample['region']} {sample['postcode']} - {sample['bank']} ({sample['quality']})")
            elif country.lower() == 'ca':
                formatted_samples.append(f"• {sample['province']} {sample['postal']} - {sample['bank']} ({sample['quality']})")
            elif country.lower() == 'au':
                formatted_samples.append(f"• {sample['state']} {sample['postcode']} - {sample['bank']} ({sample['quality']})")
        
        return '\n'.join(formatted_samples)
    
    return None

def search_bin_records(query):
    """Search for BIN records based on query"""
    # Sample BIN data
    bin_data = {
        '442387': {'bank': 'Barclays', 'country': 'UK', 'type': 'Visa'},
        '424242': {'bank': 'Test Bank', 'country': 'US', 'type': 'Visa'},
        '545454': {'bank': 'Mastercard', 'country': 'US', 'type': 'Mastercard'},
        '378282': {'bank': 'American Express', 'country': 'US', 'type': 'Amex'},
        '411111': {'bank': 'Test Visa', 'country': 'US', 'type': 'Visa'},
        '552145': {'bank': 'HSBC', 'country': 'UK', 'type': 'Mastercard'},
        '453298': {'bank': 'Chase', 'country': 'US', 'type': 'Visa'},
        '478952': {'bank': 'TD Bank', 'country': 'CA', 'type': 'Visa'},
        '523456': {'bank': 'RBC', 'country': 'CA', 'type': 'Mastercard'},
        '456789': {'bank': 'CBA', 'country': 'AU', 'type': 'Visa'}
    }
    
    results = []
    query_lower = query.lower()
    
    for bin_num, details in bin_data.items():
        if (query_lower in bin_num.lower() or 
            query_lower in details['bank'].lower() or 
            query_lower in details['country'].lower() or 
            query_lower in details['type'].lower()):
            
            results.append(f"BIN {bin_num}: {details['bank']} ({details['country']}) - {details['type']}")
    
    return results

def generate_fullz_name(country='us'):
    """Generate realistic names for fullz based on country"""
    names = {
        'us': [
            'John Smith', 'Sarah Johnson', 'Michael Brown', 'Emily Davis', 'David Wilson',
            'Jennifer Miller', 'Robert Garcia', 'Lisa Rodriguez', 'William Martinez', 'Mary Anderson'
        ],
        'uk': [
            'James Wilson', 'Emma Thompson', 'Oliver Jones', 'Sophie Brown', 'Harry Davies',
            'Charlotte Evans', 'George Thomas', 'Amelia Roberts', 'Jack Johnson', 'Emily Williams'
        ],
        'ca': [
            'Connor MacDonald', 'Olivia Campbell', 'Liam Wilson', 'Ava Thompson', 'Noah Smith',
            'Emma Johnson', 'Lucas Brown', 'Sophia Davis', 'Mason Miller', 'Isabella Anderson'
        ],
        'au': [
            'Jackson Smith', 'Charlotte Brown', 'William Johnson', 'Mia Wilson', 'Oliver Davis',
            'Amelia Miller', 'Noah Thompson', 'Isla Anderson', 'Lucas Taylor', 'Zoe Martin'
        ]
    }
    
    country_names = names.get(country.lower(), names['us'])
    return random.choice(country_names)

def create_sample_data():
    """Create all sample data files"""
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Create fullz bases
    create_fullz_bases()
    
    # Create CVV data
    cvv_data = {
        'standard': {
            'price_range': '£5-8',
            'description': 'Basic CVV with card details',
            'features': ['Card number', 'Expiry', 'CVV', 'Name', 'Address'],
            'stock': 450
        },
        'premium': {
            'price_range': '£10-15',
            'description': 'Higher balance CVV',
            'features': ['Card number', 'Expiry', 'CVV', 'Name', 'Address', 'Phone'],
            'stock': 320
        },
        'vip': {
            'price_range': '£15-25',
            'description': 'Premium cards with high limits',
            'features': ['Card number', 'Expiry', 'CVV', 'Name', 'Address', 'Phone', 'Email'],
            'stock': 180
        },
        'fresh': {
            'price_range': '£20-30',
            'description': 'Recently obtained CVV data',
            'features': ['Card number', 'Expiry', 'CVV', 'Name', 'Address', 'Phone', 'Email', 'SSN'],
            'stock': 95
        }
    }
    
    save_json_data('data/cvv_data.json', cvv_data)
    
    # Create dumps data
    dumps_data = {
        'track12': {
            'price_range': '£25-40',
            'description': 'Track 1 & 2 dump data',
            'features': ['Track 1', 'Track 2', 'PIN (some)', 'Expiry'],
            'stock': 280
        },
        'fresh': {
            'price_range': '£35-50',
            'description': 'Fresh dump data',
            'features': ['Track 1', 'Track 2', 'PIN', 'Expiry', 'Balance info'],
            'stock': 150
        },
        'premium': {
            'price_range': '£45-65',
            'description': 'Premium dumps with high balance',
            'features': ['Track 1', 'Track 2', 'PIN', 'Expiry', 'Balance info', 'Bank info'],
            'stock': 85
        },
        'vip': {
            'price_range': '£55-80',
            'description': 'VIP dumps with verified high balance',
            'features': ['Track 1', 'Track 2', 'PIN', 'Expiry', 'Balance info', 'Bank info', 'Full profile'],
            'stock': 45
        }
    }
    
    save_json_data('data/dumps_data.json', dumps_data)
    
    print("✅ Sample data files created successfully")

if __name__ == "__main__":
    create_sample_data()
