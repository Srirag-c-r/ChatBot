@echo off
echo 🌍 Starting Multi-Language AI Chatbot...
echo.
echo 📦 Installing core dependencies first...
pip install streamlit pandas numpy requests langdetect googletrans==4.0.0rc1
echo.
echo 📦 Installing AI/ML dependencies (this may take a few minutes)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers sentencepiece protobuf accelerate
echo.
echo ✅ All dependencies installed!
echo.
echo 🚀 Launching application...
streamlit run app.py
pause
