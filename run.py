#!/usr/bin/env python3
"""
MindSeek Startup Script
Quick way to start your MindSeek app
"""

import os
import sys
import subprocess

def main():
    """Start the MindSeek app"""
    print("🧠 Starting MindSeek...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your GOOGLE_API_KEY")
        print("Example:")
        print("GOOGLE_API_KEY=your_actual_api_key_here")
        return
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("❌ config.py not found!")
        return
    
    print("✅ Configuration found!")
    print("🚀 Starting Streamlit app...")
    print("📱 Open your browser to http://localhost:8502")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 MindSeek stopped!")

if __name__ == "__main__":
    main()
