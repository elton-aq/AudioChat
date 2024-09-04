import gradio as gr
import src.chat as chat
import src.talking as talking
import speech_recognition as sr

# Inicializa o histórico de chat
chat_history = []

def capturaAudio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)

    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
    except sr.UnknownValueError:
        print("Google Web Speech API não conseguiu reconhecer o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço Google Web Speech API; {e}")

    return text

def process_audio():
    try:
        yield [(f"Processando fala...", None)], None, "Aguarde 2 segundo e fale algo."
        question = capturaAudio()
        if not question:
            return [(f"Erro ao capturar áudio.", None)], None, "Erro ao capturar áudio."

        print(f'Texto reconhecido: {question}')
        chat_history.append({"role": "user", "content": f"{question}"})

        yield None, None, "Gerando resposta..."
        answer = chat.generate_answer_llama(chat_history)
        print(f'Resposta Gerada: {answer}')

        chat_history.append({"role": "assistant", "content": f"{answer}"})

        yield None, None, "Processando áudio..."
        audio_file_path = "output.mp3"
        talking.speak(answer, audio_file_path)

        chat_display = [
            (msg['content'], None) if msg['role'] == 'user' else (None, msg['content'])
            for msg in chat_history
        ]

        yield chat_display, audio_file_path, "Processamento completo."

    except Exception as e:
        yield [(f"Erro ao processar áudio: {e}", None)], None, f"Erro ao processar áudio: {e}"

with gr.Blocks() as app:
    gr.Markdown("# Llama Chatbot\n### Chatbot de perguntas e respostas por voz")

    chatbot = gr.Chatbot(
        label="Chat",
        layout="bubble",
        bubble_full_width=True,
        avatar_images=("icon/user.png", "icon/robot.png")
    )

    status_display = gr.Textbox(
        label="Status",
        value="Por favor, clique no botão para começar a falar",
        interactive=False,
        lines=1
    )

    chat_input = gr.Button("Say Something", elem_id="chat_input")

    chat_input.click(
        fn=process_audio,
        inputs=None,
        outputs=[chatbot, gr.Audio(type="filepath", autoplay=True), status_display]
    )

app.launch()