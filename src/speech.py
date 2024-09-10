import speech_recognition as sr

def capturaAudio(audio):
    recognizer = sr.Recognizer()
    print(f'Áudio recebido: {audio}')

    if audio is None:
        return "Nenhum áudio recebido.", False

    # Abre o arquivo de áudio recebido e ajusta para ruído ambiente
    with sr.AudioFile(audio) as source:
        print(f'Áudio aberto: {source}')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio_data = recognizer.record(source)
        print(f'Áudio gravado: {audio_data}')

    try:
        # Transcrição usando a API do Google para português
        text = recognizer.recognize_google(audio_data, language='pt-BR')
        return text, True
    except sr.UnknownValueError:
        return "Não foi possível reconhecer o áudio.", False
    except sr.RequestError as e:
        return f"Erro ao solicitar resultados da API: {e}", False
