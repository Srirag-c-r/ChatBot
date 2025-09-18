#!/usr/bin/env python3
"""
Test script to verify all dependencies are properly installed
"""

def test_imports():
    """Test if all required packages can be imported"""
    tests = []
    
    # Test Streamlit
    try:
        import streamlit as st
        tests.append(("✅ Streamlit", "OK"))
    except ImportError as e:
        tests.append(("❌ Streamlit", f"FAILED: {e}"))
    
    # Test basic packages
    try:
        import pandas as pd
        import numpy as np
        tests.append(("✅ Pandas & NumPy", "OK"))
    except ImportError as e:
        tests.append(("❌ Pandas & NumPy", f"FAILED: {e}"))
    
    # Test language detection
    try:
        from langdetect import detect
        test_text = "Hello world"
        result = detect(test_text)
        tests.append(("✅ Language Detection", f"OK (detected: {result})"))
    except ImportError as e:
        tests.append(("❌ Language Detection", f"FAILED: {e}"))
    except Exception as e:
        tests.append(("⚠️ Language Detection", f"Imported but error: {e}"))
    
    # Test translation
    try:
        from googletrans import Translator
        translator = Translator()
        tests.append(("✅ Google Translate", "OK"))
    except ImportError as e:
        tests.append(("❌ Google Translate", f"FAILED: {e}"))
    except Exception as e:
        tests.append(("⚠️ Google Translate", f"Imported but error: {e}"))
    
    # Test PyTorch
    try:
        import torch
        tests.append(("✅ PyTorch", f"OK (version: {torch.__version__})"))
    except ImportError as e:
        tests.append(("❌ PyTorch", f"FAILED: {e}"))
    
    # Test Transformers
    try:
        from transformers import AutoTokenizer
        tests.append(("✅ Transformers", "OK"))
    except ImportError as e:
        tests.append(("❌ Transformers", f"FAILED: {e}"))
    
    return tests

def main():
    print("🧪 Multi-Language Chatbot - Installation Test")
    print("=" * 50)
    
    results = test_imports()
    
    # Display results
    passed = 0
    failed = 0
    
    for test_name, result in results:
        print(f"{test_name}: {result}")
        if "✅" in test_name:
            passed += 1
        elif "❌" in test_name:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your installation is ready.")
        print("\n🚀 Run the chatbot with: streamlit run app.py")
    else:
        print("⚠️  Some dependencies are missing. Run install_dependencies.py")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
