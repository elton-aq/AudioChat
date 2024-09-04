from gtts import gTTS
import os

def speak(text, file_path):
    tts = gTTS(text=text, lang='pt')
    tts.save(file_path)