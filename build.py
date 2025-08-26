"""
Build script for Vercel deployment.
This script handles the build process and static file collection.
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set environment variables for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
os.environ.setdefault('DEVELOPMENT', 'False')
os.environ.setdefault('DEBUG', 'False')

def main():
    """Run build commands for deployment."""
    print("🚀 Starting build process...")
    
    # Setup Django
    django.setup()
    
    # Import Django management
    from django.core.management import execute_from_command_line
    
    try:
        # Collect static files
        print("📦 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
        
        # Run migrations
        print("🗄️ Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        print("✅ Build completed successfully!")
        
    except Exception as e:
        print(f"❌ Build failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
