import pyttsx3


class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Thoda slow pace
        rate = self.engine.getProperty("rate")
        self.engine.setProperty("rate", rate - 20)

    def say(self, text: str):
        if not text:
            return
        self.engine.say(text)
        self.engine.runAndWait()
