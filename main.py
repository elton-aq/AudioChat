import gradio as gr
import src.chat as chat
import src.talking as talking
import speech_recognition as sr


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

def process_audio(chat_history):
    try:
        # Retornando quatro valores, incluindo o estado do histórico de chat
        yield [(f"Processando fala...", None)], None, "Aguarde um segundo e fale algo.", chat_history
        question = capturaAudio()
        if not question:
            return [(f"Erro ao capturar áudio.", None)], None, "Erro ao capturar áudio.", chat_history

        print(f'Texto reconhecido: {question}')
        chat_history.append({"role": "user", "content": f"{question}"})

        yield None, None, "Gerando resposta...", chat_history
        answer = chat.generate_answer_llama(chat_history)
        print(f'Resposta Gerada: {answer}')

        chat_history.append({"role": "assistant", "content": f"{answer}"})

        yield None, None, "Processando áudio...", chat_history
        audio_file_path = "output.mp3"
        talking.speak(answer, audio_file_path)

        chat_display = [
            (msg['content'], None) if msg['role'] == 'user' else (None, msg['content'])
            for msg in chat_history
        ]

        yield chat_display, audio_file_path, "Processamento completo.", chat_history

    except Exception as e:
        yield [(f"Erro ao processar áudio: {e}", None)], None, f"Erro ao processar áudio: {e}", chat_history

with gr.Blocks() as app:
    gr.Markdown("# Llama Chatbot\n### Chatbot de perguntas e respostas por voz")

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

    chat_input = gr.Button("Say Something", elem_id="chat_input")

    # Inicializando o histórico de chat no estado da sessão
    chat_history_state = gr.State([])

    # O botão agora utiliza a função com o estado da sessão
    chat_input.click(
        fn=process_audio,
        inputs=[chat_history_state],
        outputs=[chatbot, gr.Audio(type="filepath", autoplay=True), status_display, chat_history_state]
    )

app.launch()
