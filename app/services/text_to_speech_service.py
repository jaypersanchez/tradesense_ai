import pyttsx3

class TextToSpeechService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)  # Adjust speed here

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
