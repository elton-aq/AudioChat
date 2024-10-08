import os
import requests
from groq import Groq
from dotenv import load_dotenv

# Função para gerar resposta usando o Llama
def generate_answer_llama(chat_history):
    load_dotenv()
    client = Groq(api_key=os.getenv("API_KEY"))

    try:
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="llama3-70b-8192",
        )

        answer = chat_completion.choices[0].message.content.strip()
        return answer

    except requests.exceptions.SSLError as e:
        print("Erro SSL: ", e)
        return "Houve um problema com a verificação do certificado SSL."
    except requests.exceptions.RequestException as e:
        print("Erro na requisição: ", e)
        return "Houve um problema com a requisição à API."
