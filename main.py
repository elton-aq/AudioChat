import gradio as gr
import src.chat as chat
import src.talking as talking
import speech_recognition as sr

# Função para capturar áudio e transcrevê-lo usando o speech_recognition
def capturaAudio(audio):
    recognizer = sr.Recognizer()
    print(f'Áudio recebido: {audio}')

    if audio is None:
        return 

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
    
# Função para processar o áudio e gerar a resposta
def process_audio(audio, chat_history):
    try:
        # Exibe a mensagem de processamento e transcreve o áudio
        yield [(f"Processando fala...", None)], None, "Aguarde um segundo e fale algo.", chat_history
        question, ret = capturaAudio(audio)
        if not ret:
            raise Exception(question)

        print(f'Texto reconhecido: {question}')
        chat_history.append({"role": "user", "content": f"{question}"})

        # Gera a resposta usando o modelo LLaMA
        yield None, None, "Gerando resposta...", chat_history
        answer = chat.generate_answer_llama(chat_history)
        print(f'Resposta Gerada: {answer}')

        chat_history.append({"role": "assistant", "content": f"{answer}"})

        # Processa o áudio da resposta
        yield None, None, "Processando áudio...", chat_history
        audio_file_path = "output.mp3"
        talking.speak(answer, audio_file_path)

        # Organiza o histórico do chat
        chat_display = [
            (msg['content'], None) if msg['role'] == 'user' else (None, msg['content'])
            for msg in chat_history
        ]

        # Exibe a resposta no chat e o áudio gerado
        yield chat_display, audio_file_path, "Processamento completo.", chat_history

    except Exception as e:
        # Em caso de erro, exibe uma mensagem
        yield [(f"Erro ao processar áudio: {e}", None)], None, f"Tente novamente", chat_history

# Interface Gradio
with gr.Blocks() as app:
    gr.Markdown("# Llama Chatbot\n### Chatbot de perguntas e respostas por voz")

    # Definição do chatbot e status
    chatbot = gr.Chatbot(
        label="Chat",
        layout="bubble",
        bubble_full_width=True,
        avatar_images=(
            "https://em-content.zobj.net/source/apple/391/bust-in-silhouette_1f464.png", 
            "https://em-content.zobj.net/source/apple/391/robot_1f916.png"
        )
    )

    status_display = gr.Textbox(
        label="Status",
        value="Por favor, clique no botão para começar a falar",
        interactive=False,
        lines=1
    )

    # Estado do histórico do chat
    chat_history_state = gr.State([])

    # Definição do botão de entrada do áudio e chamada para processar o áudio
    audio_input = gr.Audio(sources=["microphone"], type="filepath")

    # Conectando a função process_audio com a interface Gradio
    audio_input.change(
        fn=process_audio,
        inputs=[audio_input, chat_history_state],
        outputs=[chatbot, gr.Audio(type="filepath", autoplay=True, visible=False), status_display, chat_history_state],
    )

app.launch()
