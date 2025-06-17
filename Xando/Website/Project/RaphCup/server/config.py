import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'email': os.getenv('EMAIL_ADDRESS', 'your-email@gmail.com'),
    'password': os.getenv('EMAIL_PASSWORD', 'your-app-password'),
    'sender_name': os.getenv('SENDER_NAME', 'RaphCup Team')
}

# Database configuration
DATABASE_CONFIG = {
    'name': 'raphcup.db'
}

# Security configuration
SECURITY_CONFIG = {
    'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-change-in-production'),
    'password_reset_expiry_hours': 1,
    'verification_code_expiry_minutes': 15
}

# Server configuration
SERVER_CONFIG = {
    'host': os.getenv('HOST', '0.0.0.0'),
    'port': int(os.getenv('PORT', '5000')),
    'debug': os.getenv('DEBUG', 'False').lower() == 'true'
}
