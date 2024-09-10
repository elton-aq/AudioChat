import gradio as gr
import src.chat as chat
import src.talking as talking
import src.speech as speech
import os

# Função para processar o áudio e gerar a resposta
def process_audio(audio, chat_history):
    try:
        question, ret = speech.capturaAudio(audio)
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

        # Após o processamento, resetar o campo de áudio do usuário (sem afetar o áudio da resposta)
        yield chat_display, audio_file_path, "Clique em RECORD para começar a falar", chat_history

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
        value="Clique em RECORD para começar a falar",
        interactive=False,
        lines=1
    )

    # Estado do histórico do chat
    chat_history_state = gr.State([])

    # Definição do botão de entrada do áudio e chamada para processar o áudio
    audio_input = gr.Audio(sources=["microphone"], type="filepath")

    submit_btn = gr.Button("Enviar")

    submit_btn.click(
        fn=process_audio,
        inputs=[audio_input, chat_history_state],
        outputs=[chatbot, gr.Audio(type="filepath", autoplay=True, visible=False), status_display, chat_history_state]
    )

    submit_btn.click(
        fn=lambda: None,
        inputs=[],
        outputs=[audio_input]
    )

app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 5000)))
