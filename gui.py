import os

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


class AuraWindow(QMainWindow):
    def __init__(self, assistant, stt_engine):
        super().__init__()
        self.assistant = assistant
        self.stt = stt_engine

        self.setWindowTitle("Aura 2.0 - AI Voice Assistant")
        self.setMinimumSize(1000, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 10, 10)
        layout.setSpacing(10)

        # 🎥 Video background (top me chalega)
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget, stretch=3)

        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        video_path = os.path.join(assets_dir, "background.mp4")

        if os.path.exists(video_path):
            self.player.setSource(QUrl.fromLocalFile(video_path))
            self.player.play()
            # Loop video
            self.player.mediaStatusChanged.connect(self._handle_media_status)
        else:
            # Agar video nahi mila toh simple message
            self.video_widget.setStyleSheet("background-color: black;")
            lbl = QLabel("Place your background.mp4 in assets/")
            lbl.setStyleSheet("color: white; font-size: 16px;")
            lbl.setAlignment(Qt.AlignCenter)
            over_layout = QVBoxLayout(self.video_widget)
            over_layout.addWidget(lbl)

        # ℹ️ Info text
        self.info_label = QLabel(
            "Press 'Speak' and say your command ."
        )
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 16px; color: #00FFAA;")
        layout.addWidget(self.info_label)

        # 🎤 Speak button
        self.speak_button = QPushButton("🎤 Speak")
        self.speak_button.setFixedHeight(60)
        self.speak_button.setStyleSheet(
            """
            QPushButton {
                font-size: 20px;
                border-radius: 30px;
                padding: 10px 20px;
                background-color: #222244;
                color: white;
            }
            QPushButton:hover {
                background-color: #333366;
            }
            QPushButton:pressed {
                background-color: #111122;
            }
            """
        )
        self.speak_button.clicked.connect(self.on_speak_clicked)
        layout.addWidget(self.speak_button, alignment=Qt.AlignCenter)

        # Status label
        self.status_label = QLabel("Ready.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #CCCCCC;")
        layout.addWidget(self.status_label)

        self.setStyleSheet("background-color: #050816;")

    def _handle_media_status(self, status):
        # Loop karega jab video khatam ho
        from PySide6.QtMultimedia import QMediaPlayer

        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    def on_speak_clicked(self):
        self.speak_button.setEnabled(False)
        self.status_label.setText("Listening...")
        QApplication.processEvents()

        text = self.stt.listen_once()
        if not text:
            self.status_label.setText("Sorry, samajh nahi aaya. Phir se try karo.")
            self.speak_button.setEnabled(True)
            return

        self.status_label.setText(f"You said: {text}")
        QApplication.processEvents()

        # Assistant se process karwana
        reply = self.assistant.process_text(text)
        self.status_label.setText(f"Aura: {reply}")

        QTimer.singleShot(500, lambda: self.speak_button.setEnabled(True))
