import speech_recognition as sr


class STTEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_once(self, language: str = "en-IN") -> str | None:
        """Listen from microphone once and return recognized text (or None)."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio, language=language)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
