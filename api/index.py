"""
Entry point for Vercel deployment.
This file serves as the main handler for all requests in the Vercel environment.
"""
import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')

# Import Django and setup
import django
django.setup()

# Import the WSGI application
from wesolar.wsgi import application

# This is the entry point for Vercel
app = application
