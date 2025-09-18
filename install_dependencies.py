#!/usr/bin/env python3
"""
Installation script for Multi-Language Chatbot dependencies
Run this script to install all required packages step by step
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🌍 Multi-Language Chatbot - Dependency Installer")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return
    
    # List of dependencies to install
    dependencies = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install streamlit>=1.28.0", "Installing Streamlit"),
        ("pip install pandas>=1.3.0 numpy>=1.21.0", "Installing data processing libraries"),
        ("pip install requests>=2.25.0", "Installing requests"),
        ("pip install langdetect==1.0.9", "Installing language detection"),
        ("pip install googletrans==4.0.0rc1", "Installing Google Translate"),
        ("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu", "Installing PyTorch (CPU version)"),
        ("pip install transformers>=4.30.0", "Installing Transformers"),
        ("pip install sentencepiece>=0.1.96", "Installing SentencePiece"),
        ("pip install protobuf>=3.20.0", "Installing Protocol Buffers"),
        ("pip install accelerate>=0.20.0", "Installing Accelerate")
    ]
    
    # Install each dependency
    failed_installations = []
    
    for command, description in dependencies:
        success = run_command(command, description)
        if not success:
            failed_installations.append(description)
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 INSTALLATION SUMMARY")
    print("=" * 50)
    
    if not failed_installations:
        print("🎉 All dependencies installed successfully!")
        print("\n🚀 You can now run the chatbot with:")
        print("   streamlit run app.py")
    else:
        print(f"⚠️  {len(failed_installations)} installation(s) failed:")
        for failed in failed_installations:
            print(f"   - {failed}")
        print("\n💡 Try running the failed commands manually or check your internet connection.")
    
    print("\n📚 For help, check the README.md file")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
