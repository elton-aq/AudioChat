import gradio as gr
import src.chat as chat
import src.talking as talking
import speech_recognition as sr

# Inicializa o histórico de chat
chat_history = []

def capturaAudio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        status_display.update(value="Wait a moment...")  # Exibe "Wait a moment..."
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Fale algo...")
        status_display.update(value="Listening...")  # Exibe "Listening..."
        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
        status_display.update(value="Processing...")  # Exibe "Processing..."

    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
    except sr.UnknownValueError:
        print("Google Web Speech API não conseguiu reconhecer o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço Google Web Speech API; {e}")

    return text

def process_audio():
    try:
        question = capturaAudio()
        print(f'Texto reconhecido: {question}')

        chat_history.append({"role": "user", "content": f"👤: {question}"})

        answer = chat.generate_answer_llama(chat_history)
        print(f'Resposta Gerada: {answer}')

        chat_history.append({"role": "assistant", "content": f"🤖: {answer}"})

        audio_file_path = "output.mp3"
        talking.speak(answer, audio_file_path)

        chat_display = [
            (msg['content'], None) if msg['role'] == 'user' else (None, msg['content'])
            for msg in chat_history
        ]

        return chat_display, audio_file_path

    except Exception as e:
        return [(f"Erro ao capturar áudio: {e}", None)], None

with gr.Blocks() as app:
    gr.Markdown("# Llama Chatbot\n### Chatbot de perguntas e respostas")

    chatbot = gr.Chatbot()

    status_display = gr.Textbox(
        label="Status",
        value="Por favor, clique no botão para começar a falar",
        interactive=False,
        lines=1
    )

    chat_input = gr.Button("Say Something", elem_id="chat_input")

    def handle_chat_input():
        status_display.update(value="Ajustando ao ambiente... Aguarde um momento.")

        chat_display, audio_file_path = process_audio()

        status_message = "Você pode começar a falar."
        status_display.update(value=status_message)

        return chat_display, audio_file_path, status_message

    chat_input.click(fn=handle_chat_input, 
                     inputs=None, 
                     outputs=[chatbot, gr.Audio(type="filepath"), status_display])

app.launch(share=False)
