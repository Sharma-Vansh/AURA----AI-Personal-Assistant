import os
from dotenv import load_dotenv
import google.generativeai as genai

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
            print("WARNING: GEMINI_API_KEY not found.")
            return

        try:
            genai.configure(api_key=GEMINI_API_KEY)

            # ⭐ CORRECT MODEL NAME for google-generativeai==0.5.2
            self.model = genai.GenerativeModel("models/gemini-1.5-flash")

            print("Gemini model loaded successfully.")
        except Exception as e:
            print("Error loading Gemini model:", e)
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

        except Exception as e:
            print("Gemini API Error:", e)
            reply = "Gemini se response nahi mila."

        self.speak(reply)
        return reply
