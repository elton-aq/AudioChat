import pyttsx3

def speak(answer):   
    # Inicializa o motor TTS
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[83].id)  
    engine.say(answer)
    engine.runAndWait()
