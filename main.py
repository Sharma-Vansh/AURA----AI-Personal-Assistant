import sys
from PySide6.QtWidgets import QApplication

from tts_engine import TTSEngine
from stt_engine import STTEngine
from assistant_core import AuraAssistant
from gui import AuraWindow


def main():
    app = QApplication(sys.argv)

    tts = TTSEngine()
    stt = STTEngine()
    assistant = AuraAssistant(tts)

    window = AuraWindow(assistant=assistant, stt_engine=stt)
    window.show()

    assistant.speak("Hello Vansh, I am Aura What can I do for you")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
