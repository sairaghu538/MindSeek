#!/usr/bin/env python3
"""
MindSeek Deployment Script
Helps you deploy your MindSeek app to various platforms
"""

import os
import sys
import subprocess
import json

def print_banner():
    """Print the MindSeek banner"""
    print("""
🧠 MindSeek - AI Chat Assistant
================================
Deployment Helper Script
""")

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please create a .env file with your GOOGLE_API_KEY")
        return False
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("❌ config.py not found!")
        return False
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    print("✅ All requirements met!")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_local():
    """Test the app locally"""
    print("\n🧪 Testing app locally...")
    print("   Starting Streamlit app...")
    print("   Press Ctrl+C to stop the test")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n✅ Local test completed!")

def deploy_streamlit_cloud():
    """Deploy to Streamlit Cloud"""
    print("\n☁️  Deploying to Streamlit Cloud...")
    print("""
Steps to deploy:
1. Push your code to GitHub:
   git add .
   git commit -m "Ready for deployment"
   git push origin main

2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. Click "New app"
5. Select your repository
6. Set main file path to: app.py
7. Add environment variable:
   GOOGLE_API_KEY = your_api_key_here
8. Click "Deploy"
""")

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n🚀 Deploying to Heroku...")
    print("""
Steps to deploy:
1. Install Heroku CLI
2. Login to Heroku:
   heroku login

3. Create Heroku app:
   heroku create your-app-name

4. Set environment variables:
   heroku config:set GOOGLE_API_KEY=your_api_key_here

5. Deploy:
   git push heroku main

6. Open your app:
   heroku open
""")

def deploy_railway():
    """Deploy to Railway"""
    print("\n🚂 Deploying to Railway...")
    print("""
Steps to deploy:
1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your repository
6. Add environment variable:
   GOOGLE_API_KEY = your_api_key_here
7. Railway will automatically deploy your app
""")

def main():
    """Main deployment function"""
    print_banner()
    
    if not check_requirements():
        print("\n❌ Please fix the issues above before proceeding.")
        return
    
    while True:
        print("\n" + "="*50)
        print("Choose an option:")
        print("1. Install dependencies")
        print("2. Test locally")
        print("3. Deploy to Streamlit Cloud")
        print("4. Deploy to Heroku")
        print("5. Deploy to Railway")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            install_dependencies()
        elif choice == "2":
            test_local()
        elif choice == "3":
            deploy_streamlit_cloud()
        elif choice == "4":
            deploy_heroku()
        elif choice == "5":
            deploy_railway()
        elif choice == "6":
            print("\n👋 Goodbye! Happy deploying!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
