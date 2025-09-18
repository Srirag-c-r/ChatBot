# 🌍 Multi-Language AI Chatbot

A **100% FREE** intelligent chatbot that can understand and respond in multiple languages using state-of-the-art NLP models.

## ✨ Features

- 🔍 **Automatic Language Detection** - Detects 50+ languages
- 🌐 **Real-time Translation** - Translate conversations on the fly
- 🤖 **Multiple AI Models** - Choose from DialoGPT, BlenderBot, or FLAN-T5
- 💬 **Context-Aware Responses** - Maintains conversation context
- 📚 **Chat History** - SQLite database stores all conversations
- 🎨 **Beautiful UI** - Modern Streamlit interface
- 🆓 **Completely FREE** - No API keys required!

## 🚀 Quick Start

### Option 1: Automatic Installation (Recommended)
```bash
# Run the installation script
python install_dependencies.py

# Test the installation
python test_installation.py

# Run the chatbot
streamlit run app.py
```

### Option 2: Manual Installation
```bash
# Install core dependencies
pip install streamlit pandas numpy requests langdetect googletrans==4.0.0rc1

# Install AI/ML dependencies (this may take a few minutes)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers sentencepiece protobuf accelerate

# Run the chatbot
streamlit run app.py
```

### Option 3: Windows Batch File
```bash
# Double-click run.bat or run in command prompt
run.bat
```

### 4. Open in Browser
The app will automatically open at `http://localhost:8501`

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Models**: Hugging Face Transformers
  - DialoGPT (Conversational AI)
  - BlenderBot (Multi-turn chat)
  - FLAN-T5 (Instruction following)
- **Translation**: Google Translate (free tier)
- **Language Detection**: langdetect
- **Database**: SQLite (chat history)

## 🌍 Supported Languages

The chatbot supports 50+ languages including:

- 🇺🇸 English
- 🇪🇸 Spanish  
- 🇫🇷 French
- 🇩🇪 German
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇷🇺 Russian
- 🇨🇳 Chinese
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇸🇦 Arabic
- 🇮🇳 Hindi
- And many more!

## 💡 How It Works

1. **Input**: Type a message in any language
2. **Detection**: Automatically detects your language
3. **Translation**: Translates to English for processing (if needed)
4. **AI Response**: Generates intelligent response using selected model
5. **Translation Back**: Translates response to your preferred language
6. **Storage**: Saves conversation to local database

## 🎯 Model Comparison

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| DialoGPT | ⚡ Fast | 🟢 Good | Quick conversations |
| BlenderBot | 🐌 Medium | 🟡 Better | Engaging chat |
| FLAN-T5 | 🐌 Medium | 🟢 Good | Instructions/Q&A |

## 📁 Project Structure

```
NLP_LLM/
├── app.py              # Main Streamlit application
├── chatbot.py          # Core chatbot logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── chat_history.db    # SQLite database (created automatically)
```

## 🔧 Configuration

### Model Selection
Choose your preferred AI model in the sidebar:
- **DialoGPT**: Fastest, good for quick responses
- **BlenderBot**: Better conversational quality
- **FLAN-T5**: Best for instructions and Q&A

### Language Settings
- **Auto-detect**: Automatically detects input language
- **Response Language**: Choose output language
- **Translation**: Enable/disable translation features

## 🚨 Troubleshooting

### Common Issues

**1. Model Download Errors**
```bash
# Clear Hugging Face cache
rm -rf ~/.cache/huggingface/
```

**2. Translation Errors**
- Check internet connection
- Try different text (some characters may cause issues)

**3. Slow Performance**
- Use DialoGPT model for faster responses
- Close other applications to free up RAM

### System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space (for models)
- **Internet**: Required for translation and initial model download

## 🔮 Future Enhancements

- [ ] Voice input/output
- [ ] Custom model fine-tuning
- [ ] Export chat history
- [ ] Dark/Light theme toggle
- [ ] Mobile responsive design
- [ ] Offline translation models

## 🤝 Contributing

Feel free to contribute! Areas for improvement:
- Add more language models
- Improve translation accuracy
- Enhance UI/UX
- Add new features

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Enjoy Chatting!

Start chatting in your native language and experience the magic of AI-powered multilingual conversations!

---

**Made with ❤️ using 100% FREE technologies**
