import os
from dotenv import load_dotenv
import google.generativeai as genai
import pyttsx3

from system_commands import handle_system_command

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class AuraAssistant:
    def __init__(self, tts):
        self.tts = tts
        self.model = None
        self._setup_gemini()

    # ----------------------------
    # SETUP GEMINI MODEL (FIXED)
    # ----------------------------
    def _setup_gemini(self):
        if not GEMINI_API_KEY:
            print("WARNING: GEMINI_API_KEY not found in .env file.")
            return

        try:
            genai.configure(api_key=GEMINI_API_KEY)

            # ⭐ CORRECT MODEL NAME for latest google-generativeai API
            self.model = genai.GenerativeModel("gemini-2.0-flash")

            print("✓ Gemini model loaded successfully.")
        except ValueError as e:
            print(f"❌ Invalid API Key: {e}")
            self.model = None
        except Exception as e:
            print(f"❌ Error loading Gemini model: {type(e).__name__}: {e}")
            self.model = None

    # ----------------------------
    # TEXT TO SPEECH
    # ----------------------------
    def speak(self, text: str):
        print("AURA:", text)
        try:
            if self.tts:
                self.tts.say(text)
        except Exception as e:
            print("TTS error:", e)


    
    # ----------------------------
    # MAIN PROCESS FUNCTION
    # ----------------------------
    def process_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.strip()
        print("USER:", text)

        # -----------------------------------------
        # 1️⃣ Try System Commands first
        # -----------------------------------------
        handled, response = handle_system_command(text)
        if handled:
            if response:
                self.speak(response)
            return response or ""

        # -----------------------------------------
        # 2️⃣ Gemini AI Response
        # -----------------------------------------
        if not self.model:
            reply = "AI mode available nahi hai."
            self.speak(reply)
            return reply

        try:
            result = self.model.generate_content(
                f"You are Aura, a Hinglish desktop assistant. "
                f"Reply short.\nUser: {text}\nAura:"
            )

            reply = (result.text or "").strip()
            if not reply:
                reply = "Gemini se response nahi mila."

        except ValueError as e:
            print(f"❌ Gemini API ValueError: {e}")
            reply = "API key mein problem hai."
        except Exception as e:
            print(f"❌ Gemini API Error: {type(e).__name__}: {e}")
            reply = "Gemini se response nahi mila."

        self.speak(reply)
        return reply


def test_all_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("[TTS] Testing all voices...")
    for v in voices:
        print(f"Trying voice: {v.name} ({v.id})")
        engine.setProperty('voice', voices[0].id)  # or try other voices
        engine.setProperty('volume', 1.0)

        engine.say(f"Testing voice: {v.name}")
        engine.runAndWait()
    print("[TTS] Done testing all voices.")
import pyttsx3


class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()

        rate = self.engine.getProperty("rate")
        self.engine.setProperty("rate", rate - 20)

        voices = self.engine.getProperty('voices')
        print(f"[TTS] Available voices:")
        for v in voices:
            print(f"ID: {v.id}, Name: {v.name}, Lang: {v.languages}")

        if voices:
            self.engine.setProperty('voice', voices[0].id)

    def say(self, text: str):
        if not text:
            print("[TTS] Empty text, skipping.")
            return

        print(f"[TTS] Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print("TTS Error:", e)
import speech_recognition as sr