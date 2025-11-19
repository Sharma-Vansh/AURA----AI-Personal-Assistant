import pyttsx3
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


import pyttsx3

class TTSEngine:
    def say(self, text: str):
        if not text:
            return

        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 160)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print("TTS Error:", e)
