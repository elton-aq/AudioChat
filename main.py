import src.recognizer as recognizer
import src.chat as chat
import src.talking as talking

chat_history = []
while exit != 'q':

    # Captura a pergunta do usuário
    question = recognizer.capturaAudio()
    print(f'Texto reconhecido: {question}')

    # Adiciona a mensagem do usuário ao histórico
    chat_history.append({"role": "user", "content": question})

    # Gera a resposta usando o Llama
    answer = chat.generate_answer_llama(chat_history)
    print(f'Resposta Gerada: {answer}')
    
    # Adiciona a resposta do modelo ao histórico
    chat_history.append({"role": "assistant", "content": answer})

    # Exibe a resposta
    talking.speak(answer)

    exit = input("Tecla 'q' para sair ou qualquer tecla para outra pergunta: ")