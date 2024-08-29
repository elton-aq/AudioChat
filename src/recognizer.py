import speech_recognition as sr

def capturaAudio():
    # Inicializa o reconhecedor de fala
    recognizer = sr.Recognizer()

    # Configura o microfone como fonte de entrada
    with sr.Microphone() as source:
        print("Ajustando ao ambiente... Aguarde um momento.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Você pode começar a falar.")

        # Captura o áudio até que o usuário pare de falar
        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)

    try:
        # Converte o áudio para texto usando o Google Web Speech API
        text = recognizer.recognize_google(audio, language='pt-BR')
    except sr.UnknownValueError:
        print("Google Web Speech API não conseguiu reconhecer o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço Google Web Speech API; {e}")
    
    return text