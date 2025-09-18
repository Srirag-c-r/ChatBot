import streamlit as st
import warnings
import logging

# Try to import dependencies with fallbacks
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, BlenderbotTokenizer, BlenderbotForConditionalGeneration
    from transformers import T5Tokenizer, T5ForConditionalGeneration
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    st.error(f"⚠️ Transformers not installed: {e}")
    st.info("Please install dependencies by running: pip install transformers torch")
    TRANSFORMERS_AVAILABLE = False

try:
    from langdetect import detect, DetectorFactory
    LANGDETECT_AVAILABLE = True
    DetectorFactory.seed = 0
except ImportError:
    st.error("⚠️ Language detection not available. Install with: pip install langdetect")
    LANGDETECT_AVAILABLE = False

try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    st.error("⚠️ Translation not available. Install with: pip install googletrans==4.0.0rc1")
    TRANSLATOR_AVAILABLE = False

# Suppress warnings
warnings.filterwarnings("ignore")
if TRANSFORMERS_AVAILABLE:
    logging.getLogger("transformers").setLevel(logging.ERROR)

class MultiLanguageChatbot:
    def __init__(self):
        self.translator = Translator() if TRANSLATOR_AVAILABLE else None
        self.models = {}
        self.tokenizers = {}
        
        # Language code mapping
        self.lang_codes = {
            'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de',
            'italian': 'it', 'portuguese': 'pt', 'russian': 'ru', 'chinese': 'zh',
            'japanese': 'ja', 'korean': 'ko', 'arabic': 'ar', 'hindi': 'hi'
        }
        
        # Check if all dependencies are available
        if not TRANSFORMERS_AVAILABLE:
            st.error("🚨 AI models not available. Please install transformers and torch.")
        if not LANGDETECT_AVAILABLE:
            st.warning("⚠️ Language detection not available.")
        if not TRANSLATOR_AVAILABLE:
            st.warning("⚠️ Translation not available.")
    
    def detect_language(self, text):
        """Detect the language of input text"""
        if not LANGDETECT_AVAILABLE:
            return "English (detection unavailable)"
        
        try:
            detected = detect(text)
            # Map common language codes to readable names
            lang_map = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
                'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh-cn': 'Chinese',
                'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi'
            }
            return lang_map.get(detected, detected.upper())
        except:
            return "Unknown"
    
    def translate_text(self, text, target_lang):
        """Translate text to target language"""
        if not TRANSLATOR_AVAILABLE or self.translator is None:
            return text  # Return original text if translation not available
        
        try:
            if target_lang in self.lang_codes:
                target_lang = self.lang_codes[target_lang]
            
            result = self.translator.translate(text, dest=target_lang)
            return result.text
        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            return text
    
    @st.cache_resource
    def load_dialogpt_model(_self):
        """Load DialoGPT model"""
        if not TRANSFORMERS_AVAILABLE:
            return None, None
            
        try:
            model_name = "microsoft/DialoGPT-medium"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            return tokenizer, model
        except Exception as e:
            st.error(f"Error loading DialoGPT: {str(e)}")
            return None, None
    
    @st.cache_resource
    def load_blenderbot_model(_self):
        """Load BlenderBot model"""
        if not TRANSFORMERS_AVAILABLE:
            return None, None
            
        try:
            model_name = "facebook/blenderbot-400M-distill"
            tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
            model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
            return tokenizer, model
        except Exception as e:
            st.error(f"Error loading BlenderBot: {str(e)}")
            return None, None
    
    @st.cache_resource
    def load_flan_t5_model(_self):
        """Load FLAN-T5 model"""
        if not TRANSFORMERS_AVAILABLE:
            return None, None
            
        try:
            model_name = "google/flan-t5-base"
            tokenizer = T5Tokenizer.from_pretrained(model_name)
            model = T5ForConditionalGeneration.from_pretrained(model_name)
            return tokenizer, model
        except Exception as e:
            st.error(f"Error loading FLAN-T5: {str(e)}")
            return None, None
    
    def generate_response_dialogpt(self, text, max_length=100):
        """Generate response using DialoGPT"""
        try:
            tokenizer, model = self.load_dialogpt_model()
            if tokenizer is None or model is None:
                return "Sorry, I'm having trouble loading the model. Please try again."
            
            # Encode input
            input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
            
            # Generate response
            with torch.no_grad():
                chat_history_ids = model.generate(
                    input_ids,
                    max_length=input_ids.shape[-1] + max_length,
                    num_beams=5,
                    no_repeat_ngram_size=2,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decode response
            response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
            return response.strip() if response.strip() else "I'm not sure how to respond to that. Could you try rephrasing?"
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def generate_response_blenderbot(self, text):
        """Generate response using BlenderBot"""
        try:
            tokenizer, model = self.load_blenderbot_model()
            if tokenizer is None or model is None:
                return "Sorry, I'm having trouble loading the model. Please try again."
            
            # Encode input
            inputs = tokenizer([text], return_tensors="pt")
            
            # Generate response
            with torch.no_grad():
                reply_ids = model.generate(**inputs, max_length=100, num_beams=5, temperature=0.7, do_sample=True)
            
            # Decode response
            response = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
            return response.strip() if response.strip() else "I'm not sure how to respond to that."
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def generate_response_flan_t5(self, text):
        """Generate response using FLAN-T5"""
        try:
            tokenizer, model = self.load_flan_t5_model()
            if tokenizer is None or model is None:
                return "Sorry, I'm having trouble loading the model. Please try again."
            
            # Format as instruction
            prompt = f"Answer this question or respond to this statement: {text}"
            
            # Encode input
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids
            
            # Generate response
            with torch.no_grad():
                outputs = model.generate(input_ids, max_length=100, num_beams=5, temperature=0.7, do_sample=True)
            
            # Decode response
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response.strip() if response.strip() else "I'm not sure how to respond to that."
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def generate_fallback_response(self, text):
        """Generate a simple fallback response when AI models are not available"""
        responses = [
            f"I understand you said: '{text}'. Unfortunately, AI models are not loaded yet.",
            f"Thank you for your message: '{text}'. Please install the required dependencies to enable AI responses.",
            f"I received your message: '{text}'. To get intelligent responses, please run the installation commands.",
            f"Your message '{text}' was received. Install transformers and torch to enable AI chat features."
        ]
        import random
        return random.choice(responses)
    
    def generate_response(self, text, model_choice="DialoGPT (Fast)"):
        """Generate response based on selected model"""
        if not TRANSFORMERS_AVAILABLE:
            return self.generate_fallback_response(text)
            
        if "DialoGPT" in model_choice:
            return self.generate_response_dialogpt(text)
        elif "BlenderBot" in model_choice:
            return self.generate_response_blenderbot(text)
        elif "FLAN-T5" in model_choice:
            return self.generate_response_flan_t5(text)
        else:
            return self.generate_response_dialogpt(text)  # Default fallback
