# ExcelYard Bot

## Overview

ExcelYard Bot is a Telegram bot application designed for managing and selling digital products, specifically focusing on fullz (complete personal information packages), CVV data, and dumps. The bot includes a comprehensive product catalog system, user management, transaction processing, and a web-based administrative dashboard.

## System Architecture

### Backend Architecture
- **Bot Framework**: Python-based Telegram bot using `telebot` library
- **Web Interface**: Flask-based web dashboard for administration
- **Data Storage**: JSON file-based storage system for product catalogs, user data, and transactions
- **Core Components**:
  - `main.py`: Primary bot logic and message handling
  - `web_interface.py`: Flask web dashboard
  - `bin_data_loader.py`: Data loading and search functionality
  - `constants.py`: Configuration and API keys

### Frontend Architecture
- **Web Dashboard**: Bootstrap-based responsive interface
- **Real-time Updates**: JavaScript-based auto-refresh functionality
- **Administrative Tools**: User management, activity monitoring, and transaction tracking

## Key Components

### Bot Core (`main.py`)
- Handles Telegram bot interactions and message processing
- Manages user authentication and command routing
- Processes product catalog requests and search functionality
- Handles payment processing and transaction management
- Includes logging and error handling mechanisms

### Data Management (`bin_data_loader.py`)
- Loads and manages product catalog data from JSON files
- Provides search functionality for fullz bases
- Generates sample data and handles data persistence
- Manages product inventory and availability

### Web Dashboard (`web_interface.py`)
- Provides administrative interface for bot monitoring
- Displays user statistics, activity logs, and transaction history
- Implements session-based authentication
- Offers data export and management capabilities

### Product Catalog System
- **Fullz Bases**: Complete personal information packages organized by country
- **CVV Data**: Credit card information with different quality tiers
- **Dumps**: Magnetic stripe data with various feature sets
- JSON-based storage in `/data/` directory

## Data Flow

1. **User Interaction**: Users interact with the bot through Telegram messages
2. **Command Processing**: Bot processes commands and routes to appropriate handlers
3. **Data Retrieval**: Product information is loaded from JSON files
4. **Response Generation**: Bot generates responses with product catalogs and pricing
5. **Transaction Processing**: Payment requests are handled and logged
6. **Administrative Monitoring**: Web dashboard provides real-time monitoring and management

## External Dependencies

### Python Libraries
- `telebot`: Telegram Bot API wrapper
- `flask`: Web framework for dashboard
- `requests`: HTTP client for external API calls
- `json`: JSON data handling
- `datetime`: Date and time utilities
- `logging`: Application logging
- `threading`: Multi-threading support

### Frontend Dependencies
- **Bootstrap 5.1.3**: CSS framework for responsive design
- **Font Awesome 6.0.0**: Icon library
- **jQuery**: JavaScript utility library (implied by Bootstrap usage)

### External Services
- **Telegram Bot API**: Core bot functionality
- **Bitcoin Payment Processing**: Cryptocurrency payment handling

## Deployment Strategy

The application is designed for deployment on Replit with the following characteristics:

- **Environment Variables**: Sensitive configuration stored in environment variables
- **File-based Storage**: Uses JSON files for data persistence
- **Continuous Operation**: Bot runs continuously with error handling and reconnection logic
- **Web Interface**: Accessible via Flask development server
- **Logging**: Comprehensive logging to both console and file

### Configuration Management
- Bot tokens and API keys stored as environment variables
- Admin credentials configurable through environment variables
- Group chat IDs and payment addresses configurable
- Default values provided for development environment

## Changelog
- July 03, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.