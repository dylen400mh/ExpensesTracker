import os
import secrets

# Flask configuration
DEBUG = True  # Set to False in production
SECRET_KEY = secrets.token_hex(16)  # Generate a secure random value

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CORS configuration (if needed)
# CORS_ALLOW_HEADERS = 'Content-Type'
# CORS_RESOURCES = {r'/api/*': {'origins': 'https://your-frontend-domain.com'}}